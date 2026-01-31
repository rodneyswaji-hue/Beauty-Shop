import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import Home from '../pages/Home';
import ProductDetails from '../features/products/ProductDetails';
import Cart from '../features/cart/Cart';
import Checkout from '../features/orders/Checkout';
import Invoice from '../features/orders/Invoice';
import CategoryPage from '../pages/CategoryPage'; // <--- Import the new page

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout><Home /></MainLayout>} />
      
      {/* Dynamic Category Route */}
      {/* This one line handles /skincare, /makeup, /haircare, and /shop */}
      <Route path="/:category" element={<MainLayout><CategoryPage /></MainLayout>} />
      
      <Route path="/product/:id" element={<MainLayout><ProductDetails /></MainLayout>} />
      <Route path="/cart" element={<MainLayout><Cart /></MainLayout>} />
      <Route path="/checkout" element={<MainLayout><Checkout /></MainLayout>} />
      <Route path="/invoice/:orderId" element={<MainLayout><Invoice /></MainLayout>} />
      
      {/* Note: Remove the specific 404 route if it conflicts, or put it last */}
    </Routes>
  );
};

export default AppRoutes;