# FinLingo Auth Testing Playbook

## Test Credentials
Set via backend environment variables (`ADMIN_EMAIL`, `ADMIN_PASSWORD`, `DEMO_EMAIL`, `DEMO_PASSWORD`).
Never commit real values. Use a strong, unique admin password in production.

## Endpoints (all under /api/auth)
- POST /api/auth/register {email, password, name}
- POST /api/auth/login {email, password}
- POST /api/auth/logout
- GET  /api/auth/me  (auth required, returns current user)
- POST /api/auth/refresh
- DELETE /api/auth/account {password}  (auth required, deletes the user and their data)

## Cookie behavior
Login/register set httpOnly cookies `access_token` (15m) + `refresh_token` (7d).
The app also stores the returned `access_token` and sends it as a Bearer header.

## Quick curl
```
curl -X POST $URL/api/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"$DEMO_EMAIL","password":"$DEMO_PASSWORD"}'
```
