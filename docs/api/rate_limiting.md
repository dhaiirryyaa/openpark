# Rate Limiting & Quota Policy

- Public IP Rate Limit: 120 requests / minute.
- Authenticated Driver: 600 requests / minute.
- Implementation: Token bucket algorithm with Redis / in-memory fallback.
