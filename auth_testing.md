# FinLingo Auth Testing Playbook

## Test Credentials
- Admin: admin@finlingo.com / Admin@123
- Demo user: demo@finlingo.com / Demo@123

## Endpoints (all under /api/auth)
- POST /api/auth/register {email, password, name}
- POST /api/auth/login {email, password}
- POST /api/auth/logout
- GET  /api/auth/me  (auth required, returns current user)
- POST /api/auth/refresh

## Cookie behavior
Login/register set httpOnly cookies `access_token` (15m) + `refresh_token` (7d).
Frontend axios uses `withCredentials: true`. `/api/auth/me` should return user when cookies present.

## Quick curl
```
curl -c c.txt -X POST $URL/api/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"admin@finlingo.com","password":"Admin@123"}'
curl -b c.txt $URL/api/auth/me
```
