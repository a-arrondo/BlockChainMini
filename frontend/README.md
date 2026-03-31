# BlockChainMini — Frontend
The React explorer for BlockChainMini. For full setup and running instructions see the [main README](../README.md).

## Vite proxy
API calls are proxied to the backend via `vite.config.js`:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/blockchain': 'http://localhost:8000'
    }
  }
})
```
If the backend runs on a different port, update the proxy target accordingly.

## Features
- **History** — full chain log in reverse order, showing index, hash, transaction count, and timestamp per block
- **Transactions** — form to submit a new pending transaction (sender, receiver, amount)
- **Neighbours** — view connected peer nodes, add new ones by IP and port, or clear all

## Project structure
```
├── src/
│   ├── App.jsx       # All components and tab logic
│   ├── App.css       # Styles
│   └── main.jsx      # React entry point
├── index.html
└── vite.config.js
```

---
<img src="https://ai-label.org/image-pack/ai-label_banner-made-with-ai.svg" align="right" width="125">