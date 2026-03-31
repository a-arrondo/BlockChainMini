# BlockChainMini
A minimal blockchain implementation built from scratch in Python, with a React explorer frontend. Designed for learning purposes.

## Objective
This project illustrates the core mechanics of a blockchain: transaction handling, proof-of-work mining, and multi-node consensus. It is not intended for production use.

## Requirements
- Python 3.13+ and [uv](https://github.com/astral-sh/uv)
- Node.js 18+ and npm

## Setup
```bash
git clone <repo-url>
cd BlockChainMini
uv sync
cd frontend && npm install
```

## Running
Start the backend (defaults to port 8000):
```bash
uv run uvicorn main:app
```
Start the frontend:
```bash
cd frontend && npm run dev
```
Open `http://localhost:5173`. The frontend proxies all `/blockchain` calls to the backend automatically.

To run multiple nodes:
```bash
uv run uvicorn main:app --port 8001
uv run uvicorn main:app --port 8002
```
Then use the Neighbours tab in the explorer to connect nodes to each other.

## API overview
Interactive API docs are available at `http://localhost:<port>/docs`.

| Endpoint | Method | Description |
|---|---|---|
| `/blockchain/status` | GET | Chain length and validity |
| `/blockchain/history` | GET | Full chain, length and validity |
| `/blockchain/append` | POST | Submit a new transaction |
| `/blockchain/neighbours` | GET / POST / DELETE | Manage peer nodes |
| `/blockchain/block` | POST | Receive a block from a peer (not intended to trigger manually) |

## Project structure
```
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── service.py        # Business logic and async loops
│   ├── domain.py         # Domain classes (Blockchain, Block, Transaction...)
│   ├── schemas.py        # Pydantic models
│   └── config.py         # Configuration parameters
└── frontend/
    ├── src/
    │   ├── App.jsx       # All components and tab logic
    │   └── App.css       # Styles
    ├── index.html
    └── vite.config.js
```

## Screenshots
### History
![Explorer: history](screenshots/history.png)
### Transactions
![Explorer: transactions](screenshots/transactions.png)
### Neighbours
![Explorer: neighbours](screenshots/neighbours.png)

---
<table>
  <tr>
    <td>The <strong>backend</strong> was built with the assistance of generative AI.</td>
    <td><img src="https://ai-label.org/image-pack/ai-label_banner-assisted-by-ai.svg" width="125"></td>
  </tr>
  <tr>
    <td>The <strong>frontend</strong> is completely coded by AI .</td>
    <td><img src="https://ai-label.org/image-pack/ai-label_banner-made-with-ai.svg" width="125"></td>
  </tr>
</table>