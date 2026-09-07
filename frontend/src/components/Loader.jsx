import React from 'react'
import '../styles/Loader.css'

export function Loader({ size = 'md', label = 'Loading' }) {
  return (
    <div className={`loader loader--${size}`} role="status" aria-label={label}>
      <span className="loader__spinner" aria-hidden="true" />
    </div>
  )
}
