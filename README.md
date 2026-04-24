# bl0ck_v0: A Pseudo Blockchain API

## About
bl0ck_v0 is a local, educational pseudo-blockchain project built to simulate core blockchain-like workflows without implementing a real decentralized network.

The application includes:
- A FastAPI backend for mining and blockchain controls
- A browser UI for interacting with the chain
- Persistent local storage in blockchain_data.json
- Dynamic difficulty controls and mining timeout controls
- Live mining telemetry and in-app logs

## Contents
- [Project Intent](#project-intent)
- [Core Features](#core-features)
- [API Contracts and Versioning](#api-contracts-and-versioning)
- [Pseudo-Blockchain Anatomy vs Actual Blockchain](#pseudo-blockchain-anatomy-vs-actual-blockchain)
- [Quick Setup](#quick-setup)

## Project Intent
This project mimics selected blockchain mechanics such as block chaining, hashing, and proof-like mining loops. It is intentionally not a public, private, consortium, or hybrid production blockchain.

Primary goals:
- Learn blockchain-adjacent architecture and control flows
- Experiment with mining difficulty and timeout behavior
- Observe live mining state in a web dashboard

## Core Features
### Basic Operations
- Add a new block
- View the latest block
- View full blockchain state
- Persist and reload blockchain from local JSON storage

### Dynamic Operations
- Toggle between automatic and manual difficulty behavior
- Set manual difficulty in the range 1 to 10
- Switch back to automatic mode
- Set mining timeout in the range 10 to 300 seconds

### Runtime Observability
- Live mining telemetry over WebSocket
- In-memory backend log stream exposed to UI

## API Contracts and Versioning
The API now uses a versioned namespace and a normalized response contract.

### Versioned Prefix
All REST endpoints are served under:
- /api/v1

Examples:
- /api/v1/status
- /api/v1/blockchain/display
- /api/v1/blockchain/add
- /api/v1/blockchain/last-block
- /api/v1/difficulty/current
- /api/v1/difficulty/set-manual/{difficulty}
- /api/v1/difficulty/switch-to-auto
- /api/v1/mining/set-timeout/{timeout}
- /api/v1/logs

### Success Envelope
All successful REST responses follow:

```json
{
    "success": true,
    "message": "Human-readable status",
    "data": {}
}
```

### Error Envelope
All handled REST errors follow:

```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Descriptive message",
        "details": {}
    }
}
```

### Contract Modeling
Response shapes are defined with Pydantic models in backend/contracts.py, and route handlers declare response models to keep endpoint contracts explicit and stable.

## Pseudo-Blockchain Anatomy vs Actual Blockchain
This section outlines how the project behaves internally and how that differs from a real blockchain network.

### 1. Network Topology
Pseudo-blockchain in this project:
- Single-node runtime
- No peer discovery or gossip protocol
- No distributed state agreement

Actual blockchain:
- Multi-node peer-to-peer network
- Node discovery, message propagation, and synchronization
- Shared state across independent participants

### 2. Consensus and Finality
Pseudo-blockchain in this project:
- No consensus protocol
- Block acceptance is local process logic
- Finality is immediate in local memory and file write

Actual blockchain:
- Consensus protocols coordinate block validity across nodes
- Finality depends on protocol rules and confirmations
- Fork choice and reorg handling are protocol-level concerns

### 3. Mining Model
Pseudo-blockchain in this project:
- CPU nonce iteration with timeout guard
- Difficulty controls are local and session-aware
- Mining failure handling uses retries and thresholds

Actual blockchain:
- Network-wide economic and cryptographic security model
- Difficulty retargeting depends on protocol economics and global behavior
- Block production incentives and penalties are integral to security

### 4. Data and Storage
Pseudo-blockchain in this project:
- Chain persisted in one local JSON file
- Storage owned and controlled by one operator
- No shared canonical ledger outside local machine

Actual blockchain:
- Canonical ledger reproduced by many nodes
- Storage includes full state/history models with protocol validation
- Tamper resistance emerges from distributed replication and consensus

### 5. Trust and Threat Model
Pseudo-blockchain in this project:
- Trusted local environment
- Educational and experimental use case
- Not designed for adversarial production environments

Actual blockchain:
- Designed for partial trust or trust-minimized operation
- Security assumptions include adversarial behavior
- Economic and cryptographic incentives are foundational

### 6. Smart Contract and Execution Layer
Pseudo-blockchain in this project:
- No on-chain VM or smart contract execution
- Focused on block creation and chain observation

Actual blockchain:
- Often includes programmable execution environment
- Contract determinism, gas, state transitions, and verification are core concerns

## Quick Setup
For setup and local run instructions, use:
- [backend/README.md](backend/README.md)

Note:
- Hashing currently uses Python hashlib with SHA-256.


