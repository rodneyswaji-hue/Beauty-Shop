import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { clearCart } from '../cart/cartSlice';
import { createOrder } from '../../services/fakeData'; // Import the service
import { Loader2 } from 'lucide-react'; // Spinner icon

const Checkout = () => {
  const { items, totalAmount } = useSelector((state) => state.cart);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);

  const [formData, setFormData] = useState({
    firstName: '', lastName: '', email: '', address: '', city: '', zip: '', card: ''
  });

  // Redirect if cart is empty
  if (items.length === 0) {
    React.useEffect(() => { navigate('/cart'); }, [navigate]);
    return null;
  }

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsProcessing(true); // Start loading

    const orderPayload = {
      customer: formData,
      items: items,
      total: totalAmount,
    };

    try {
      // 1. Call the Fake DB Service
      const newOrder = await createOrder(orderPayload);
      
      // 2. Clear Redux Cart
      dispatch(clearCart());
      
      // 3. Navigate to Invoice using the NEW generated ID
      navigate(`/invoice/${newOrder.id}`);
      
    } catch (error) {
      console.error("Checkout failed", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-serif text-gray-900 mb-8 text-center">Checkout</h1>
      
      <div className="grid md:grid-cols-2 gap-12">
        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <h3 className="font-bold text-lg">Shipping Details</h3>
          <div className="grid grid-cols-2 gap-4">
            <input required name="firstName" placeholder="First Name" onChange={handleChange} className="border p-3 rounded-lg w-full" />
            <input required name="lastName" placeholder="Last Name" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          </div>
          <input required name="email" type="email" placeholder="Email Address" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          <input required name="address" placeholder="Shipping Address" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          <div className="grid grid-cols-2 gap-4">
            <input required name="city" placeholder="City" onChange={handleChange} className="border p-3 rounded-lg w-full" />
            <input required name="zip" placeholder="Zip Code" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          </div>

          <h3 className="font-bold text-lg pt-4">Payment</h3>
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
             <p className="text-sm text-gray-500 mb-2">Simulated Payment Gateway</p>
             <input required name="card" type="text" maxLength="19" placeholder="Card Number (XXXX XXXX XXXX XXXX)" className="border p-3 rounded-lg w-full bg-white" />
          </div>

          <button 
            type="submit" 
            disabled={isProcessing}
            className="w-full bg-pink-600 text-white py-4 rounded-full font-bold hover:bg-pink-700 transition shadow-lg mt-4 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center"
          >
            {isProcessing ? (
              <><Loader2 className="animate-spin mr-2" /> Processing...</>
            ) : (
              `Pay $${totalAmount.toFixed(2)}`
            )}
          </button>
        </form>

        {/* Order Preview */}
        <div className="bg-gray-50 p-8 rounded-2xl h-fit">
          <h3 className="font-serif text-lg mb-4">Your Order</h3>
          <div className="space-y-3 mb-4 max-h-64 overflow-y-auto">
            {items.map(item => (
              <div key={item.id} className="flex justify-between text-sm">
                <span>{item.name} <span className="text-gray-400">x{item.quantity}</span></span>
                <span className="font-bold">${item.totalPrice.toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="border-t border-gray-200 pt-4 flex justify-between font-bold text-lg">
            <span>Total</span>
            <span>${totalAmount.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;