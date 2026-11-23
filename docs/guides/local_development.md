# Local Development Guide

## Prerequisites
- Python 3.9+
- Node.js 18+ (for testing client assets)
- Modern browser with Service Worker support

## Quickstart
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
python3 -m uvicorn backend.main:app --port 8000 --reload
```
