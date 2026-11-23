# Railway Deployment Runbook

Deployments trigger automatically upon push to `main`:
- Build System: Railway Nixpacks
- Entry Point: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
