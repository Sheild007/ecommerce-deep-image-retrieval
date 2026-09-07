import React from 'react'
import '../styles/Footer.css'

function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <div className="site-footer__brand">
          <h2>METRIC.</h2>
          <p>Selected apparel, footwear, and accessories.</p>
        </div>

        <div className="site-footer__grid">
          <div>
            <h3>Shop</h3>
            <ul>
              <li><a href="#catalog">All products</a></li>
              <li><a href="#catalog">Men</a></li>
              <li><a href="#catalog">Women</a></li>
              <li><a href="#catalog">Accessories</a></li>
            </ul>
          </div>

          <div>
            <h3>Support</h3>
            <ul>
              <li><a href="#contact">Contact</a></li>
              <li><a href="#shipping">Shipping</a></li>
              <li><a href="#returns">Returns</a></li>
              <li><a href="#faq">FAQ</a></li>
            </ul>
          </div>

          <div>
            <h3>Company</h3>
            <ul>
              <li><a href="#about">About</a></li>
              <li><a href="#careers">Careers</a></li>
              <li><a href="#privacy">Privacy</a></li>
              <li><a href="#terms">Terms</a></li>
            </ul>
          </div>

          <div>
            <h3>Follow</h3>
            <ul>
              <li><a href="#instagram">Instagram</a></li>
              <li><a href="#pinterest">Pinterest</a></li>
              <li><a href="#facebook">Facebook</a></li>
            </ul>
          </div>
        </div>

        <div className="site-footer__bottom">
          <p>© {currentYear} METRIC.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
