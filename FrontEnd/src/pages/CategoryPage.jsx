import React from 'react';
import { useParams } from 'react-router-dom';
import { products } from '../services/fakeData';
import ProductCard from '../features/products/ProductCard';

const CategoryPage = () => {
  const { category } = useParams(); // Gets 'skincare', 'makeup', etc. from URL

  // Helper to normalize text (e.g., "skincare" matches "Skincare")
  const categoryName = category ? category.charAt(0).toUpperCase() + category.slice(1) : 'Shop All';

  // Filter products: If "shop" (Shop All), show everything. Otherwise, filter by category.
  const displayProducts = category === 'shop' 
    ? products 
    : products.filter(p => p.category.toLowerCase() === category.toLowerCase());

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">{categoryName}</h1>
        <p className="text-gray-500 max-w-2xl mx-auto">
          Explore our curated collection of premium {categoryName} products. Designed to bring out your natural beauty.
        </p>
      </div>

      {displayProducts.length > 0 ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {displayProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ) : (
        <div className="text-center py-20 bg-gray-50 rounded-xl border border-dashed border-gray-300">
          <h3 className="text-xl font-serif text-gray-400">No products found in this category yet.</h3>
          <p className="text-gray-400 text-sm mt-2">Check back soon for new arrivals!</p>
        </div>
      )}
    </div>
  );
};

export default CategoryPage;