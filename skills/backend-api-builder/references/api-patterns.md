# API patterns

## One error shape everywhere

```json
{ "error": { "code": "rate_limited", "message": "Daily limit reached, resets at 00:00 UTC", "details": {} } }
```

## Status codes

| Code | Use for |
|---|---|
| 200 / 201 / 204 | OK / created / done with no body |
| 400 | Request is malformed |
| 401 | No or bad credentials |
| 403 | Logged in but not allowed |
| 404 | Resource does not exist (also for resources the caller may not see) |
| 409 | Conflict, such as a duplicate unique field |
| 422 | Valid JSON but fails validation |
| 429 | Rate limited, send `Retry-After` |
| 500 | Our bug. Log it with a request id, never leak a stack trace |
| 502 / 504 | An upstream service failed or timed out |

## FastAPI skeleton

```python
import os, time, uuid, logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

log = logging.getLogger("api")
app = FastAPI(title="my-api")

@app.middleware("http")
async def request_id(request: Request, call_next):
    rid = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["x-request-id"] = rid
    log.info("%s %s %s %.0fms", rid, request.method, request.url.path, (time.perf_counter() - start) * 1000)
    return response

@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code,
                        content={"error": {"code": str(exc.status_code), "message": exc.detail}})

@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
```

## Auth

- API keys: store only a hash (SHA-256 of a long random key is fine), show the key once, compare with `hmac.compare_digest`.
- Passwords: `argon2` or `bcrypt`, never plain SHA.
- Sessions or JWT: short expiry, refresh flow, secret from the environment.

## Rate limits and quotas

- Per key, per window. Store counters in Redis or the database, not process memory, if more than one instance runs or the host restarts.
- Daily quotas: store the reset time in UTC and return it in the 429 message.

## Lists

Paginate with `limit` (default 20, max 100) and a cursor. Return `next_cursor`. Never return an unbounded list.

## Retries

Retry only safe calls (GET, or POST with an idempotency key). Use a timeout on every outside call (5 to 15 s) and back off between retries.

## .env.example

```
PORT=8000
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=change-me
ALLOWED_ORIGINS=https://example.com
```

## Deploying on Railway, Render or Koyeb

- Bind to `0.0.0.0` and read `PORT` from the environment.
- Set the start command explicitly, for example `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Point the platform health check at `/health`.
- Free tiers may sleep or restart: do not keep state in memory or on the local disk.
- Pin dependency versions in `requirements.txt` or the lockfile.

## Bugs that come up again and again

| Symptom | Usual cause |
|---|---|
| Works locally, 502 on host | Listening on `127.0.0.1` or a hard-coded port |
| CORS error in browser | Origin not in the allowed list, or credentials with `*` |
| Random 500s under load | Shared DB connection without a pool, or sync code blocking the event loop |
| Limits reset unexpectedly | Counters kept in memory and the host restarted |
| Secrets in the repo | `.env` committed. Rotate the key; deleting the file is not enough |
