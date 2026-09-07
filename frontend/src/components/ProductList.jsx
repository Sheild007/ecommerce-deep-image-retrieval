import React from 'react'
import ProductCard from './ProductCard'
import '../styles/ProductList.css'

function ProductList({ products }) {
  if (!products || products.length === 0) return null

  return (
    <div className="product-grid">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

export default ProductList
