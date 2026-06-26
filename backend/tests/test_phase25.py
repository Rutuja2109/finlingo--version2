"""Phase 2.5 backend tests: forgot-password, reset-password, google/session,
and Phase 1+2 regression smoke."""
import os
import pytest
import requests

BASE_URL = os.environ["REACT_APP_BACKEND_URL"].rstrip("/")
API = f"{BASE_URL}/api"

DEMO_EMAIL = "demo@finlingo.com"
DEMO_PASSWORD = "Demo@123"
TMP_PASSWORD = "TmpPass@999"

ADMIN_EMAIL = "admin@finlingo.com"
ADMIN_PASSWORD = "Admin@123"

AI_COURSE_ID = "36fa5852-7597-46e1-8f55-5054486721b3"


def _login(email, password):
    r = requests.post(f"{API}/auth/login", json={"email": email, "password": password}, timeout=20)
    return r


def H(tok):
    return {"Authorization": f"Bearer {tok}"}


# -------------- forgot-password / reset-password --------------
class TestPasswordReset:
    """Full forgot-password → reset-password lifecycle. We mutate the demo
    password during the test class and restore Demo@123 at the end."""

    def test_forgot_existing_user_returns_dev_reset_url(self):
        r = requests.post(f"{API}/auth/forgot-password",
                          json={"email": DEMO_EMAIL}, timeout=15)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("ok") is True
        assert data.get("dev_reset_url"), f"expected dev_reset_url, got {data}"
        assert "/reset-password?token=" in data["dev_reset_url"]

    def test_forgot_unknown_email_returns_200_no_url(self):
        r = requests.post(f"{API}/auth/forgot-password",
                          json={"email": "nope_does_not_exist@finlingo.com"}, timeout=15)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("ok") is True
        assert data.get("dev_reset_url") is None, data

    def test_reset_with_invalid_token_returns_400(self):
        r = requests.post(f"{API}/auth/reset-password",
                          json={"token": "this-token-does-not-exist-123",
                                "new_password": "Whatever@123"}, timeout=15)
        assert r.status_code == 400, r.text
        body = r.json()
        # detail string per server.py
        assert "Invalid" in body.get("detail", ""), body

    def test_full_cycle_reset_then_login_then_restore(self):
        # Step 1: forgot-password
        r1 = requests.post(f"{API}/auth/forgot-password",
                           json={"email": DEMO_EMAIL}, timeout=15)
        assert r1.status_code == 200
        url1 = r1.json()["dev_reset_url"]
        token1 = url1.split("token=")[1]
        assert len(token1) > 10

        # Step 2: reset-password to TMP_PASSWORD
        r2 = requests.post(f"{API}/auth/reset-password",
                           json={"token": token1, "new_password": TMP_PASSWORD}, timeout=15)
        assert r2.status_code == 200, r2.text
        body2 = r2.json()
        assert body2["email"] == DEMO_EMAIL
        assert body2.get("access_token"), "expected access_token in reset response"

        # Step 3: token reuse should fail
        r2b = requests.post(f"{API}/auth/reset-password",
                            json={"token": token1, "new_password": "AnotherPwd@1"}, timeout=15)
        assert r2b.status_code == 400, r2b.text

        # Step 4: login with new password
        r3 = _login(DEMO_EMAIL, TMP_PASSWORD)
        assert r3.status_code == 200, f"login with new pwd failed: {r3.text}"
        tok = r3.json()["access_token"]

        # /auth/me should also work
        rme = requests.get(f"{API}/auth/me", headers=H(tok), timeout=15)
        assert rme.status_code == 200
        assert rme.json()["email"] == DEMO_EMAIL

        # Step 5: login with OLD password should fail
        r_old = _login(DEMO_EMAIL, DEMO_PASSWORD)
        assert r_old.status_code == 401, f"old password should not work: {r_old.status_code}"

        # Step 6: restore -> forgot again, reset back to Demo@123
        r4 = requests.post(f"{API}/auth/forgot-password",
                           json={"email": DEMO_EMAIL}, timeout=15)
        assert r4.status_code == 200
        token2 = r4.json()["dev_reset_url"].split("token=")[1]
        r5 = requests.post(f"{API}/auth/reset-password",
                           json={"token": token2, "new_password": DEMO_PASSWORD}, timeout=15)
        assert r5.status_code == 200, r5.text

        # Step 7: confirm demo creds work again
        r6 = _login(DEMO_EMAIL, DEMO_PASSWORD)
        assert r6.status_code == 200, f"restore failed; demo creds broken: {r6.text}"


# -------------- google/session (negative path only) --------------
class TestGoogleSession:
    def test_invalid_session_id_returns_401(self):
        r = requests.post(f"{API}/auth/google/session",
                          json={"session_id": "totally-bogus-session-id-xyz"}, timeout=20)
        assert r.status_code == 401, f"expected 401, got {r.status_code} body={r.text}"
        body = r.json()
        assert "Invalid Google session" in body.get("detail", ""), body


# -------------- Phase 1 + 2 regression smoke --------------
class TestRegression:
    @pytest.fixture(scope="class")
    def demo_token(self):
        r = _login(DEMO_EMAIL, DEMO_PASSWORD)
        assert r.status_code == 200, r.text
        return r.json()["access_token"]

    @pytest.fixture(scope="class")
    def admin_token(self):
        r = _login(ADMIN_EMAIL, ADMIN_PASSWORD)
        assert r.status_code == 200, r.text
        return r.json()["access_token"]

    def test_login_demo_works(self, demo_token):
        assert demo_token and isinstance(demo_token, str)

    def test_auth_me(self, demo_token):
        r = requests.get(f"{API}/auth/me", headers=H(demo_token), timeout=15)
        assert r.status_code == 200
        assert r.json()["email"] == DEMO_EMAIL

    def test_courses_list(self, demo_token):
        r = requests.get(f"{API}/courses", headers=H(demo_token), timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list) and len(data) > 0

    def test_stats_me(self, demo_token):
        r = requests.get(f"{API}/stats/me", headers=H(demo_token), timeout=15)
        assert r.status_code == 200
        d = r.json()
        for k in ("total_xp", "level", "coins"):
            assert k in d

    def test_admin_jobs(self, admin_token):
        r = requests.get(f"{API}/admin/jobs", headers=H(admin_token), timeout=15)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_revisions_due(self, demo_token):
        r = requests.get(f"{API}/revisions/due", headers=H(demo_token), timeout=15)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_boss_battle_endpoint(self, demo_token):
        # Need a chapter id. Fetch course full to get one.
        r = requests.get(f"{API}/courses/{AI_COURSE_ID}/full",
                         headers=H(demo_token), timeout=20)
        if r.status_code != 200:
            pytest.skip("AI course not available in this env")
        course = r.json()
        chapters = course.get("chapters") or []
        if not chapters:
            pytest.skip("no chapters")
        ch_id = chapters[0]["id"]
        rb = requests.get(f"{API}/boss-battles/{ch_id}",
                          headers=H(demo_token), timeout=20)
        assert rb.status_code == 200, rb.text
        body = rb.json()
        # Boss endpoint returns 'unlocked' flag plus chapter info
        assert "unlocked" in body
        assert "chapter" in body
