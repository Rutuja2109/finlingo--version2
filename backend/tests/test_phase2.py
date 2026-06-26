"""Phase 2 backend tests: admin endpoints, revisions (SM-2 lite), boss battles."""
import os
import pytest
import requests
import uuid

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://adaptive-academy-16.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

ADMIN_EMAIL = "admin@finlingo.com"
ADMIN_PASSWORD = "Admin@123"
DEMO_EMAIL = "demo@finlingo.com"
DEMO_PASSWORD = "Demo@123"

AI_COURSE_ID = "36fa5852-7597-46e1-8f55-5054486721b3"


def _login(email, password):
    r = requests.post(f"{API}/auth/login", json={"email": email, "password": password}, timeout=20)
    assert r.status_code == 200, f"Login failed for {email}: {r.status_code} {r.text}"
    return r.json()["access_token"]


@pytest.fixture(scope="session")
def admin_token():
    return _login(ADMIN_EMAIL, ADMIN_PASSWORD)


@pytest.fixture(scope="session")
def demo_token():
    return _login(DEMO_EMAIL, DEMO_PASSWORD)


def H(tok):
    return {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}


# ----------------- ADMIN: jobs & PDFs -----------------
class TestAdmin:
    def test_admin_jobs_lists_completed(self, admin_token):
        r = requests.get(f"{API}/admin/jobs", headers=H(admin_token), timeout=20)
        assert r.status_code == 200
        rows = r.json()
        assert isinstance(rows, list)
        assert len(rows) >= 1, "expected at least one previously completed generation job"
        completed = [j for j in rows if j.get("status") == "completed"]
        assert completed, f"no completed jobs; statuses seen: {[j.get('status') for j in rows]}"
        # one of them must reference the AI course id
        assert any(j.get("course_id") == AI_COURSE_ID for j in completed), \
            "expected completed job tied to AI_COURSE_ID"

    def test_admin_pdf_list(self, admin_token):
        r = requests.get(f"{API}/admin/pdf/list", headers=H(admin_token), timeout=20)
        assert r.status_code == 200
        rows = r.json()
        assert isinstance(rows, list)
        assert len(rows) >= 1, "expected at least one uploaded PDF"
        assert "id" in rows[0] and "original_name" in rows[0]

    def test_non_admin_forbidden_jobs(self, demo_token):
        r = requests.get(f"{API}/admin/jobs", headers=H(demo_token), timeout=20)
        assert r.status_code == 403

    def test_non_admin_forbidden_pdfs(self, demo_token):
        r = requests.get(f"{API}/admin/pdf/list", headers=H(demo_token), timeout=20)
        assert r.status_code == 403

    def test_unauth_admin_blocked(self):
        r = requests.get(f"{API}/admin/jobs", timeout=20)
        assert r.status_code == 401


# ----------------- COURSES -----------------
class TestCourses:
    def test_list_courses_includes_ai(self):
        r = requests.get(f"{API}/courses", timeout=20)
        assert r.status_code == 200
        rows = r.json()
        assert isinstance(rows, list)
        ids = [c.get("id") for c in rows]
        assert AI_COURSE_ID in ids, f"AI course missing from /courses; got ids={ids}"
        ai = next(c for c in rows if c["id"] == AI_COURSE_ID)
        # The spec says course name should be 'LOMA 281 v2'
        assert "loma" in (ai.get("name", "") + ai.get("title", "")).lower()
        assert ai.get("ai_generated") is True

    def test_course_full_requires_auth(self):
        r = requests.get(f"{API}/courses/{AI_COURSE_ID}/full", timeout=20)
        assert r.status_code == 401

    def test_course_full_returns_nested(self, demo_token):
        r = requests.get(f"{API}/courses/{AI_COURSE_ID}/full", headers=H(demo_token), timeout=30)
        assert r.status_code == 200
        c = r.json()
        assert c["id"] == AI_COURSE_ID
        chapters = c.get("chapters", [])
        assert len(chapters) >= 2, f"expected >=2 chapters, got {len(chapters)}"
        # At least one module with concepts
        total_concepts = 0
        for ch in chapters:
            for m in ch.get("modules", []):
                for con in m.get("concepts", []):
                    assert "progress" in con, "concept missing progress field"
                    assert "status" in con["progress"]
                    total_concepts += 1
        assert total_concepts >= 5, f"expected several concepts, got {total_concepts}"


# ----------------- REVISIONS -----------------
class TestRevisions:
    def test_due_returns_list_shape(self, demo_token):
        r = requests.get(f"{API}/revisions/due", headers=H(demo_token), timeout=20)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        for item in data:
            assert "progress" in item
            assert "concept" in item

    def _pick_concept_for_demo(self, demo_token):
        # Get any completed concept for the demo user, else complete one quickly.
        r = requests.get(f"{API}/progress/me", headers=H(demo_token), timeout=20)
        assert r.status_code == 200
        progs = r.json()
        for p in progs:
            if p.get("status") in ("completed", "mastered"):
                return p["concept_id"]
        # Complete one. Use AI course's first concept
        r2 = requests.get(f"{API}/courses/{AI_COURSE_ID}/full", headers=H(demo_token), timeout=30)
        assert r2.status_code == 200
        for ch in r2.json().get("chapters", []):
            for m in ch.get("modules", []):
                for con in m.get("concepts", []):
                    cid = con["id"]
                    rc = requests.post(f"{API}/progress/complete-concept",
                                       headers=H(demo_token),
                                       json={"concept_id": cid, "score": 80, "duration_sec": 1},
                                       timeout=20)
                    if rc.status_code == 200:
                        return cid
        pytest.skip("Could not find/complete a concept for demo user")

    def test_grade_good_increases_interval_and_xp(self, demo_token):
        cid = self._pick_concept_for_demo(demo_token)
        # First, baseline xp
        s0 = requests.get(f"{API}/stats/me", headers=H(demo_token), timeout=10).json()
        r = requests.post(f"{API}/revisions/grade", headers=H(demo_token),
                          json={"concept_id": cid, "quality": 2}, timeout=20)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["xp_bonus"] == 5
        assert data["next_review_in_days"] >= 2
        s1 = requests.get(f"{API}/stats/me", headers=H(demo_token), timeout=10).json()
        assert s1["total_xp"] >= s0["total_xp"] + 5

    def test_grade_again_resets_to_1_day(self, demo_token):
        cid = self._pick_concept_for_demo(demo_token)
        r = requests.post(f"{API}/revisions/grade", headers=H(demo_token),
                          json={"concept_id": cid, "quality": 0}, timeout=20)
        assert r.status_code == 200
        data = r.json()
        assert data["next_review_in_days"] == 1
        assert data["xp_bonus"] == 0

    def test_grade_unknown_concept_404(self, demo_token):
        r = requests.post(f"{API}/revisions/grade", headers=H(demo_token),
                          json={"concept_id": str(uuid.uuid4()), "quality": 2}, timeout=20)
        assert r.status_code == 404


# ----------------- BOSS BATTLE -----------------
class TestBossBattle:
    def _pick_chapter(self, token):
        r = requests.get(f"{API}/courses/{AI_COURSE_ID}/full", headers=H(token), timeout=30)
        assert r.status_code == 200
        chs = r.json().get("chapters", [])
        assert chs, "no chapters"
        return chs[0]["id"], chs[0]

    def test_boss_returns_shape(self, demo_token):
        chid, _ = self._pick_chapter(demo_token)
        r = requests.get(f"{API}/boss-battles/{chid}", headers=H(demo_token), timeout=20)
        assert r.status_code == 200
        data = r.json()
        for k in ["chapter", "unlocked", "concepts_total", "concepts_done", "questions"]:
            assert k in data, f"missing key {k}"
        assert isinstance(data["unlocked"], bool)
        assert isinstance(data["questions"], list)

    def test_boss_locked_when_incomplete(self, demo_token):
        chid, _ = self._pick_chapter(demo_token)
        r = requests.get(f"{API}/boss-battles/{chid}", headers=H(demo_token), timeout=20)
        data = r.json()
        if data["concepts_done"] < data["concepts_total"]:
            assert data["unlocked"] is False
        else:
            assert data["unlocked"] is True

    def test_boss_submit_passing_awards_xp(self, demo_token):
        chid, _ = self._pick_chapter(demo_token)
        s0 = requests.get(f"{API}/stats/me", headers=H(demo_token), timeout=10).json()
        r = requests.post(f"{API}/boss-battles/submit", headers=H(demo_token),
                          json={"chapter_id": chid, "correct_count": 8, "total": 10}, timeout=20)
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["passed"] is True
        assert data["xp_earned"] == 50
        assert data["score"] == 80
        s1 = requests.get(f"{API}/stats/me", headers=H(demo_token), timeout=10).json()
        assert s1["total_xp"] >= s0["total_xp"] + 50
        # achievement boss_slayer should be unlocked (idempotent across runs)
        assert "boss_slayer" in s1.get("achievements", [])

    def test_boss_submit_failing_low_xp(self, demo_token):
        chid, _ = self._pick_chapter(demo_token)
        r = requests.post(f"{API}/boss-battles/submit", headers=H(demo_token),
                          json={"chapter_id": chid, "correct_count": 2, "total": 10}, timeout=20)
        assert r.status_code == 200
        data = r.json()
        assert data["passed"] is False
        assert data["xp_earned"] == 10

    def test_boss_invalid_chapter_404(self, demo_token):
        r = requests.get(f"{API}/boss-battles/{uuid.uuid4()}", headers=H(demo_token), timeout=20)
        assert r.status_code == 404


# ----------------- PHASE 1 REGRESSION -----------------
class TestPhase1Regression:
    def test_health(self):
        r = requests.get(f"{API}/", timeout=10)
        assert r.status_code == 200

    def test_login_and_me(self, demo_token):
        r = requests.get(f"{API}/auth/me", headers=H(demo_token), timeout=10)
        assert r.status_code == 200
        assert r.json()["email"] == DEMO_EMAIL

    def test_leaderboard(self, demo_token):
        r = requests.get(f"{API}/leaderboard", headers=H(demo_token), timeout=20)
        assert r.status_code == 200
        rows = r.json()
        assert isinstance(rows, list)
        if rows:
            assert "rank" in rows[0] and "total_xp" in rows[0]

    def test_my_stats(self, demo_token):
        r = requests.get(f"{API}/stats/me", headers=H(demo_token), timeout=10)
        assert r.status_code == 200
        s = r.json()
        for k in ["total_xp", "level", "coins", "streak_days", "achievements"]:
            assert k in s
