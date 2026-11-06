"""Phase 1+2 regression smoke (pytest). Password reset and Google sign-in have their own test files."""
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


# Password reset and Google sign-in are tested in test_password_reset.py and test_google_auth.py.


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
