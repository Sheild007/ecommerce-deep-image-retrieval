import React, { useRef } from 'react'
import { Camera, Heart, Search, ShoppingBag, User } from 'lucide-react'
import '../styles/Header.css'

function Header({ onSearch, searchTerm, onImageSearch }) {
  const fileInputRef = useRef(null)

  const handleSearchChange = (event) => {
    onSearch(event.target.value)
  }

  const handleCameraClick = () => {
    fileInputRef.current?.click()
  }

  const handleImageChange = (event) => {
    const file = event.target.files?.[0]
    if (file && typeof onImageSearch === 'function') {
      onImageSearch(file)
    }
  }

  return (
    <header className="site-header">
      <div className="site-header__inner">
        <a className="brand" href="#catalog" aria-label="METRIC home">
          METRIC.
        </a>

        <div className="header-search">
          <Search size={16} strokeWidth={1.7} className="header-search__icon" aria-hidden="true" />
          <input
            type="search"
            value={searchTerm}
            onChange={handleSearchChange}
            className="header-search__input"
            placeholder="Search products"
            aria-label="Search products"
          />
          <button
            type="button"
            className="header-search__camera"
            onClick={handleCameraClick}
            aria-label="Search by image"
          >
            <Camera size={16} strokeWidth={1.7} />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="header-search__file"
            onChange={handleImageChange}
            aria-hidden="true"
            tabIndex={-1}
          />
        </div>

        <div className="header-actions" aria-label="Account actions">
          <button type="button" className="header-actions__button" aria-label="Wishlist">
            <Heart size={18} strokeWidth={1.7} />
          </button>
          <button type="button" className="header-actions__button" aria-label="Cart">
            <ShoppingBag size={18} strokeWidth={1.7} />
          </button>
          <button type="button" className="header-actions__button" aria-label="Account">
            <User size={18} strokeWidth={1.7} />
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
