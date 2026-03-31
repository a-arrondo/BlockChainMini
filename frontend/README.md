# BlockChainMini — Frontend

A minimal blockchain explorer built with React and Vite, designed to interact with the [BlockChainMini](../backend/README.md/README.md) backend.

## Requirements

- Node.js 18+
- npm

## Setup

From the frontend directory, install dependencies:

```bash
npm install
```

## Running

Start the backend first (defaults to port 8000):

```bash
cd backend/
uv run uvicorn main:app
```

Then start the frontend dev server:

```bash
cd frontend/
npm run dev
```

Open `http://localhost:5173` in your browser.

## Vite proxy

API calls are proxied to the backend via `vite.config.js`. Make sure it contains:

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

- **Status** — block count and chain integrity, shown persistently in the sidebar with auto-refresh every 5 seconds
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