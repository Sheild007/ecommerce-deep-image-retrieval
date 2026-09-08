import { useEffect, useState } from 'react'
import Header from './components/Header'
import ProductList from './components/ProductList'
import Loader from './components/Loader'
import EmptyState from './components/EmptyState'
import Footer from './components/Footer'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:7860/api'
const ITEMS_PER_PAGE = 50

function App() {
  const [products, setProducts] = useState([])
  const [totalProducts, setTotalProducts] = useState(0)
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [currentPage, setCurrentPage] = useState(1)

  // Visual Search States
  const [visualSearchLoading, setVisualSearchLoading] = useState(false)
  const [visualSearchError, setVisualSearchError] = useState('')
  const [visualSearchResults, setVisualSearchResults] = useState(null)
  const [uploadedImagePreview, setUploadedImagePreview] = useState(null)
  const [visibleCount, setVisibleCount] = useState(12)  // Initially show 12 items

  // Fetch products from backend (Server-side pagination and filtering)
  useEffect(() => {
    if (visualSearchResults) return // Don't fetch normal catalog if viewing visual search

    const fetchProducts = async () => {
      try {
        setLoading(true)
        setError('')

        const offset = (currentPage - 1) * ITEMS_PER_PAGE
        const queryParams = new URLSearchParams({
          limit: ITEMS_PER_PAGE,
          offset: offset,
          category: selectedCategory,
          search: searchTerm
        })

        const response = await fetch(`${API_URL}/products?${queryParams}`)
        const data = await response.json()

        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Unable to load products')
        }

        setProducts(data.products || [])
        setTotalProducts(data.total || 0)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    const timer = setTimeout(fetchProducts, 300) // Debounce search
    return () => clearTimeout(timer)
  }, [currentPage, searchTerm, selectedCategory, visualSearchResults])

  const handleImageSearch = async (file) => {
    try {
      setVisualSearchLoading(true)
      setVisualSearchError('')
      
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImagePreview(e.target.result)
      }
      reader.readAsDataURL(file)
      
      const formData = new FormData()
      formData.append('image', file)
      formData.append('k', 12)
      
      const response = await fetch(`${API_URL}/visual-search`, {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      
      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to process visual search')
      }
      
      setVisualSearchResults({
        products: data.products || [],
        total: data.total_results || 0
      })
      setVisibleCount(12)
      setCurrentPage(1)
      window.scrollTo({ top: document.getElementById('catalog').offsetTop - 20, behavior: 'smooth' })
    } catch (err) {
      setVisualSearchError(err.message)
      setUploadedImagePreview(null)
    } finally {
      setVisualSearchLoading(false)
    }
  }

  const clearVisualSearch = () => {
    setVisualSearchResults(null)
    setUploadedImagePreview(null)
    setVisualSearchError('')
    setVisibleCount(12)
  }

  const loadMoreSimilarItems = () => {
    setVisibleCount(prev => Math.min(prev + 12, visualSearchResults.total))
  }

  // Reset page to 1 when filters change
  useEffect(() => {
    setCurrentPage(1)
  }, [searchTerm, selectedCategory])

  // Determine what to render
  const displayProducts = visualSearchResults ? visualSearchResults.products : products
  const productsToDisplay = visualSearchResults 
    ? displayProducts.slice(0, visibleCount)
    : displayProducts

  const totalPages = Math.max(1, Math.ceil(totalProducts / ITEMS_PER_PAGE))
  
  const handlePreviousPage = () => {
    setCurrentPage((page) => Math.max(1, page - 1))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleNextPage = () => {
    setCurrentPage((page) => Math.min(totalPages, page + 1))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const categories = ['All', 'Apparel', 'Accessories', 'Footwear', 'Personal Care', 'Men', 'Women', 'Boys', 'Girls']

  const resultsStart = displayProducts.length === 0 ? 0 : ((currentPage - 1) * ITEMS_PER_PAGE) + 1
  const resultsEnd = Math.min(currentPage * ITEMS_PER_PAGE, totalProducts)

  return (
    <div className="App">
      <Header
        onSearch={setSearchTerm}
        searchTerm={searchTerm}
        onImageSearch={handleImageSearch}
      />

      <main className="main-content" id="catalog">
        <div className="container">
          {/* Visual Search Results View */}
          {visualSearchResults && (
            <section className="visual-search-section" style={{ marginBottom: '32px' }}>
              <div className="visual-search-header" style={{
                display: 'flex',
                gap: '24px',
                alignItems: 'flex-start',
                paddingBottom: '24px',
                borderBottom: '1px solid var(--color-border)'
              }}>
                <div style={{ flex: '0 0 auto' }}>
                  {uploadedImagePreview && (
                    <>
                      <p style={{ fontSize: '12px', color: 'var(--color-muted)', marginBottom: '8px' }}>
                        Your uploaded image:
                      </p>
                      <img
                        src={uploadedImagePreview}
                        alt="Uploaded for search"
                        style={{
                          width: '150px',
                          height: '150px',
                          objectFit: 'cover',
                          borderRadius: '8px',
                          border: '1px solid var(--color-border)'
                        }}
                      />
                    </>
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <div>
                      <h2 style={{ fontSize: '20px', marginBottom: '4px' }}>Similar Products</h2>
                      <p style={{ color: 'var(--color-muted)', fontSize: '14px' }}>
                        Found {visualSearchResults.total} similar items from our catalog
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={clearVisualSearch}
                      style={{
                        padding: '8px 16px',
                        borderRadius: '6px',
                        border: '1px solid var(--color-border)',
                        background: 'transparent',
                        cursor: 'pointer',
                        fontSize: '14px'
                      }}
                    >
                      ← Back to Catalog
                    </button>
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* Category Filter - Hide during visual search */}
          {!visualSearchResults && (
            <section className="filter-section" aria-label="Categories">
              <div className="section-heading">
                <h2>Browse</h2>
                <p>{totalProducts.toLocaleString()} products available</p>
              </div>

              <div className="category-filter">
                {categories.map((category) => (
                  <button
                    key={category}
                    type="button"
                    className={`category-btn ${selectedCategory === category ? 'active' : ''}`}
                    onClick={() => setSelectedCategory(category)}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </section>
          )}

          <section className="products-section" aria-label="Products">
            <div className="results-header">
              <div>
                <h1>
                  {visualSearchResults ? 'Similar Products' : 'Selected products'}
                </h1>
                <p className="results-summary">
                  {visualSearchResults 
                    ? `${productsToDisplay.length.toLocaleString()} items`
                    : `${totalProducts.toLocaleString()} items total`
                  }
                  {!visualSearchResults && totalProducts > 0 && ` · Showing ${resultsStart}-${resultsEnd}`}
                </p>
              </div>
            </div>

            {visualSearchLoading ? (
              <div className="loading-state">
                <Loader size="lg" label="Searching for similar products..." />
                <p>Generating embeddings and searching catalog...</p>
              </div>
            ) : visualSearchError ? (
              <EmptyState
                title="Visual search failed"
                description={visualSearchError}
              />
            ) : loading && !visualSearchResults ? (
              <div className="loading-state">
                <Loader size="lg" label="Loading products" />
                <p>Loading catalog...</p>
              </div>
            ) : error && !visualSearchResults ? (
              <EmptyState title="Products unavailable" description={error} />
            ) : productsToDisplay.length === 0 ? (
              <EmptyState
                title={visualSearchResults ? "No similar products found" : "No products match your filters"}
                description={visualSearchResults ? "Try uploading a different image" : "Try a different search term or clear one of the category filters."}
              />
            ) : (
              <>
                <ProductList products={productsToDisplay} />

                {visualSearchResults && visibleCount < visualSearchResults.total && (
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    padding: '24px',
                    gap: '12px',
                    flexDirection: 'column',
                    alignItems: 'center'
                  }}>
                    <button
                      type="button"
                      onClick={loadMoreSimilarItems}
                      style={{
                        padding: '12px 24px',
                        borderRadius: '6px',
                        border: '1px solid var(--color-border)',
                        background: 'var(--color-primary)',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '16px',
                        fontWeight: '500'
                      }}
                    >
                      Load More Similar Items
                    </button>
                    <p style={{ 
                      margin: 0, 
                      padding: '12px 0',
                      color: 'var(--color-muted)',
                      fontSize: '14px'
                    }}>
                      Showing {visibleCount} of {visualSearchResults.total} items
                    </p>
                  </div>
                )}

                {!visualSearchResults && totalPages > 1 && (
                  <div className="pagination-controls">
                    <button
                      type="button"
                      className="pagination-btn"
                      onClick={handlePreviousPage}
                      disabled={currentPage === 1}
                    >
                      Previous
                    </button>

                    <span className="pagination-status">
                      Page {currentPage} of {totalPages}
                    </span>

                    <button
                      type="button"
                      className="pagination-btn"
                      onClick={handleNextPage}
                      disabled={currentPage === totalPages}
                    >
                      Next
                    </button>
                  </div>
                )}
              </>
            )}
          </section>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default App
