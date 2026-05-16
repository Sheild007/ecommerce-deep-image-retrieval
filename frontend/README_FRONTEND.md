# Frontend - React Visual Search UI

Modern React application for searching products using images.

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

Access at http://localhost:5173

## Scripts

```bash
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview build
npm run lint     # Code quality check
```

## Project Structure

```
src/
├── components/
│   ├── Header.jsx         # Navigation & upload
│   ├── ProductCard.jsx    # Product display
│   ├── ProductList.jsx    # Grid layout
│   ├── LazyImage.jsx      # Lazy loading
│   ├── Loader.jsx         # Loading spinner
│   ├── EmptyState.jsx     # Empty message
│   └── Footer.jsx         # Footer
├── styles/                # Component CSS
├── data/
│   └── productsGenerator.js
├── App.jsx                # Main component
└── main.jsx               # Entry point
```

## Components

- **Header**: Navigation, file upload, category filters
- **ProductCard**: Product image, title, price, similarity
- **ProductList**: Responsive grid display
- **LazyImage**: Intersection Observer for lazy loading
- **Loader**: Loading indicator
- **EmptyState**: No results message

## App State

```javascript
- products: Current product list
- loading: Loading state
- selectedFile: Uploaded image
- categories: Available categories
- filters: Applied filters
```

## API Configuration

Edit `src/App.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## Styling

- Global: `src/index.css`
- App: `src/App.css`
- Components: Scoped CSS files

## Technologies

- React 19
- Vite 8
- JavaScript ES6+
- Lucide React (icons)
- CSS (no frameworks)

## Performance

- Lazy image loading
- Code splitting
- Hot Module Replacement

## Responsive

- Desktop: Multi-column
- Tablet: 2-column
- Mobile: Single column

## Build & Deploy

```bash
npm run build              # Production build
# Deploy dist/ folder to Vercel/Netlify/GitHub Pages
```

## Environment Variables

```bash
# .env.production
VITE_API_URL=https://api.example.com
```

## Dependencies

- `react@^19.2.4`
- `react-dom@^19.2.4`
- `lucide-react@^1.7.0`
- `vite@^8.0.1`

## Troubleshooting

**Images not loading**: Check backend CORS, verify API URL

**Slow performance**: Check network tab, enable caching

**Build errors**: Clear node_modules, reinstall

## Resources

- [React Docs](https://react.dev)
- [Vite Guide](https://vitejs.dev)
- [MDN](https://developer.mozilla.org)
