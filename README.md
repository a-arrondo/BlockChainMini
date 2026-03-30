# BlockChainMini
A minimal blockchain implementation built from scratch in Python, designed for learning purposes.

## Objective
This project aims to illustrate the core mechanics of a blockchain: transaction handling, proof-of-work mining, and multi-node consensus. It is not intended for production use.

## Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv)

## Setup
Clone the repository and install dependencies:
```bash
git clone <repo-url>
cd BlockChainMini
uv sync
```

## Running the nodes
Start the first node (defaults to port 8000):
```bash
uv run uvicorn main:app
```
Add more nodes on different ports:
```bash
uv run uvicorn main:app --port 8001
uv run uvicorn main:app --port 8002
```
Then use the `/blockchain/neighbours` endpoint to connect nodes to each other.

## API overview
Once running, interactive API docs are available at `http://localhost:<port>/docs`.

| Endpoint | Method | Description |
|---|---|---|
| `/blockchain/status` | GET | Chain length and validity |
| `/blockchain/history` | GET | Full chain, length and validity |
| `/blockchain/append` | POST | Submit a new transaction |
| `/blockchain/neighbours` | GET / POST / DELETE | Manage peer nodes |
| `/blockchain/block` | POST | Receive a block from a peer (not intended to trigger manually) |

## Project structure
```
├── main.py       # FastAPI routes
├── service.py    # Business logic and async loops
├── domain.py     # Domain classes (Blockchain, Block, Transaction...)
├── schemas.py    # Pydantic models
└── config.py     # Configuration parameters
```

## Roadmap
- Fix edge cases in decentralized consensus
- Improve code cleanliness
- Explore a visual interface
- Update pending transactions correct

---

<img src="https://ai-label.org/image-pack/ai-label_banner-assisted-by-ai.svg" align="right" width="125">
