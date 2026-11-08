---
name: backend-api-builder
description: Designs and builds backend APIs and services in Python or Node: routes, auth, databases, background jobs, rate limits and deployment. Use when the user asks for an API, server, bot backend, database layer, webhook handler, or help deploying a backend.
---

# Backend API builder

## Before you start

Confirm four things, guessing sensibly if the user is vague: language and framework, database, where it will be deployed, and who will call the API. Default to FastAPI for Python and Express or Fastify for Node.

## Workflow

1. **Write the contract first.** List endpoints with method, path, request body, response body and error cases. Show it before writing code.
2. **Model the data.** Tables or collections, keys, indexes, and what must be unique.
3. **Build in layers.** Routes call services, services call the data layer. Keep business rules out of route handlers.
4. **Secure it.** Validate all input. Hash passwords with a proper algorithm. Keep secrets in environment variables and ship an `.env.example`. Add rate limits on auth and expensive routes.
5. **Handle failure.** Consistent error shape, timeouts on outside calls, retries only where the call is safe to repeat.
6. **Test.** Write tests for the contract: one success and the main failures per endpoint. Run them. When a test fails, fix the code, never loosen the test to make it pass.
7. **Deploy notes.** Start command, required environment variables, health check route, and the logs to watch.

## Quality bar

- Every endpoint documented and every error returns a clear message and status code.
- No secrets, tokens or keys in code or logs.
- Database queries are parameterized.
- The app starts from a clean clone with the README steps alone.
- A `/health` route exists.

## Output

Contract, then folder structure, then code file by file, then run and deploy steps. Keep each file complete so the user can paste it without guessing.

## Avoid

- Building auth from scratch when a vetted library fits.
- Storing anything sensitive in plain text.
- Hidden global state that breaks when the host restarts or scales.
- Claiming a deploy works without a way to check it.
