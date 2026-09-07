import React, { useState } from 'react'
import { Heart } from 'lucide-react'
import '../styles/ProductCard.css'

function ProductCard({ product }) {
  const [isFavorite, setIsFavorite] = useState(false)
  const [isAdded, setIsAdded] = useState(false)

  const handleAddToCart = () => {
    setIsAdded(true)
    window.setTimeout(() => setIsAdded(false), 1400)
  }

  return (
    <article className="product-card">
      <div className="product-card__image-wrap">
        <img
          src={product.image_link || 'https://via.placeholder.com/600x600?text=Image'}
          alt={product.productDisplayName}
          className="product-card__image"
          loading="lazy"
          onError={(event) => {
            event.currentTarget.src =
              'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 600 600%22%3E%3Crect width=%22600%22 height=%22600%22 fill=%22%23f8f8f8%22/%3E%3Cpath d=%22M120 420l120-120 90 90 80-80 110 110%22 fill=%22none%22 stroke=%22%23cfcfcf%22 stroke-width=%2240%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22/%3E%3Ccircle cx=%22280%22 cy=%22210%22 r=%2245%22 fill=%22%23dedede%22/%3E%3C/svg%3E'
          }}
        />

        <button
          type="button"
          className={`product-card__favorite ${isFavorite ? 'is-active' : ''}`}
          onClick={() => setIsFavorite((value) => !value)}
          aria-label={isFavorite ? 'Remove from wishlist' : 'Add to wishlist'}
        >
          <Heart size={16} strokeWidth={1.8} fill={isFavorite ? 'currentColor' : 'none'} />
        </button>
      </div>

      <div className="product-card__body">
        <p className="product-card__eyebrow">
          {product.masterCategory || product.gender || 'Product'}
        </p>

        <h3 className="product-card__title">{product.productDisplayName}</h3>

        <p className="product-card__meta">
          {product.articleType}
          {product.baseColour ? ` · ${product.baseColour}` : ''}
        </p>

        <div className="product-card__footer">
          <div className="product-card__price">
            Rs {Number(product.price_pkr || 0).toLocaleString()}
          </div>

          <button
            type="button"
            className={`product-card__button ${isAdded ? 'is-added' : ''}`}
            onClick={handleAddToCart}
          >
            {isAdded ? 'Added' : 'Add to Cart'}
          </button>
        </div>
      </div>
    </article>
  )
}

export default ProductCard
