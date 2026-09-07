import React from 'react'
import { PackageSearch } from 'lucide-react'
import '../styles/EmptyState.css'

export function EmptyState({ title = 'No products found', description = 'Try a different keyword or category.' }) {
  return (
    <div className="empty-state">
      <PackageSearch size={40} strokeWidth={1.5} className="empty-state__icon" aria-hidden="true" />
      <h2 className="empty-state__title">{title}</h2>
      <p className="empty-state__description">{description}</p>
    </div>
  )
}
