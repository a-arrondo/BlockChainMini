
import time
import httpx
import asyncio
from dataclasses import dataclass, field

from config import Config
from domain import Blockchain, Transaction, Neighbour
from schemas import StatusModel, HistoryModel, TransactionModel, PeersModel, NeighbourModel, BlockModel

@dataclass
class BlockChainHandler:
    cfg: Config = field(default_factory=Config)
    blockchain: Blockchain = field(init=False)
    last_mine: float = field(default_factory=time.time, init=False)

    def __post_init__(self):
        self.blockchain = Blockchain(difficulty=self.cfg.difficulty)

    def get_status(self) -> StatusModel:
        return StatusModel(
            length=len(self.blockchain.chain),
            is_valid=self.blockchain.validate_chain()
        )
    
    def get_history(self) -> HistoryModel:
        hist = [
            block._to_block_model()
                for block in self.blockchain.chain
        ]

        return HistoryModel(
            length=len(self.blockchain.chain),
            is_valid=self.blockchain.validate_chain(),
            history=hist
        )

    def add_transaction(
            self,
            transaction: TransactionModel
            ) -> None:
        self.blockchain.add_transaction(
            Transaction(
                sender=transaction.sender,
                receiver=transaction.receiver,
                amount=transaction.amount
            )
        )

    def get_neighbours(self) -> PeersModel:
        peers = [
            peer._to_neighbour_model()
                for peer in self.blockchain.peers
        ]
        return PeersModel(
            n_peers=len(self.blockchain.peers),
            peers=peers
        )

    def add_neighbours(
            self,
            neighbours: list[NeighbourModel]
            ) -> None:
        neighs = [
            Neighbour(
                ip=neigh.ip,
                port=neigh.port
            )
            for neigh in neighbours
        ]
        self.blockchain.add_neighbours(
            neighs
        )

    def reset_neighbours(self) -> None:
        self.blockchain.reset_neighbours()

    def _should_mine(self):
        enough_transactions = len(self.pending_transactions) >= self.cfg.min_transactions
        timeout_reached = (time.time() - self.last_mine) >= self.cfg.mining_interval
        return enough_transactions or (timeout_reached and bool(self.pending_transactions))

    async def _send_block_to(
            self,
            client: httpx.AsyncClient,
            peer: NeighbourModel,
            block: BlockModel
            ) -> None:
        try:
            await client.post(f"{peer.url}/blockchain/block", json=block)
        except Exception:
            # TODO: apply some policy?
            pass

    async def mining_loop(self) -> None:
        while True:
            await asyncio.sleep(1)
            if self._should_mine():
                mined_block = self.create_new_block()
                self.last_time = time.time()
                async with httpx.AsyncClient as client:
                    tasks = [
                        self._send_block_to(
                            client,
                            peer._to_neighbour_model(),
                            mined_block._to_block_model()
                        ) for peer in self.blockchain.peers
                    ]
                    await asyncio.gather(*tasks, return_exceptions=True)

    def add_block(
            self,
            incoming_block: BlockModel
            ) -> None:
        try:
            block = Block(
                index=incoming_block.index,
                previous_hash=incoming_block.previous_hash,
                timestamp=incoming_block.timestamp,
                transactions = [
                    Transaction(
                        sender=trans.sender,
                        receiver=trans.receiver,
                        amount=trans.amount
                    ) for trans in incoming_block.transactions
                ],
                nonce=incoming_block.nonce,
                hash=incoming_block.hash
            )
            
            is_next = block.previous_hash == self.blockchain.chain.last_block.hash
            if (block.hash == block.calculate_hash() and is_next):
                self.blockchain.chain.append(block)
            elif not is_next:
                # TODO apply consensus policy
                # check sender's chain:
                ## if longer and valid: copy
                ## otherwise: ignore
            else:
                raise ValueError("Invalid block hash")

        except ValueError as ve:
            # invalid transaction or invalid block
            raise

