"""Generate Play Store assets (icon, feature graphic, phone screenshots) with headless Edge over CDP.

Needs: the local backend on :8001, the web app dev server on :3000, `pip install websocket-client httpx`.
Run:  python design/store/make_assets.py
"""
import base64
import json
import os
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

import httpx
import websocket

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
APP = "http://localhost:3000"
API = "http://localhost:8001/api"
PORT = 9333


class Cdp:
    def __init__(self):
        self.profile = tempfile.mkdtemp(prefix="fl-edge-")
        self.proc = subprocess.Popen([
            EDGE, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={self.profile}",
            "--no-first-run", "--disable-gpu", "--hide-scrollbars", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
                page = next(t for t in targets if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.5)
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], max_size=None)
        self.n = 0

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def js(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        return r.get("result", {}).get("value")

    def size(self, w, h, scale):
        self.call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=scale, mobile=w < 600)

    def go(self, url, wait=3.5):
        self.call("Page.navigate", url=url)
        time.sleep(wait)

    def shot(self, name):
        data = self.call("Page.captureScreenshot", format="png")["data"]
        (OUT / name).write_bytes(base64.b64decode(data))
        print("saved", name)

    def close(self):
        try:
            self.ws.close()
        finally:
            self.proc.terminate()


def main():
    b = Cdp()
    try:
        # Brand graphics (static pages)
        b.size(512, 512, 1)
        b.go((HERE / "icon.html").as_uri(), 2.5)
        b.shot("icon-512.png")
        b.size(1024, 500, 1)
        b.go((HERE / "feature.html").as_uri(), 3.5)
        b.shot("feature-1024x500.png")

        # Phone screenshots: 390x780 at 2.77x = about 1080x2160 (2:1, allowed by Play)
        b.size(390, 780, 2.7692)
        b.go(APP + "/", 4)
        b.js("localStorage.clear()")
        b.go(APP + "/", 4)
        b.shot("shot-1-landing.png")

        login = httpx.post(f"{API}/auth/login", json={"email": "demo@finlingo.com", "password": "Demo@123"}, timeout=30).json()
        H = {"Authorization": f"Bearer {login['access_token']}"}
        b.js(f"localStorage.setItem('fl_token', {json.dumps(login['access_token'])})")

        courses = httpx.get(f"{API}/courses", timeout=30).json()
        crypto = next(c for c in courses if c["slug"] == "bitcoin-and-crypto")
        full = httpx.get(f"{API}/courses/{crypto['id']}/full", headers=H, timeout=30).json()
        concepts = full["chapters"][0]["modules"][0]["concepts"]
        tip = next(c for c in concepts if "group chat" in c["title"].lower())

        b.go(APP + "/dashboard", 5)
        b.shot("shot-2-dashboard.png")
        b.go(APP + "/courses", 4)
        b.shot("shot-3-courses.png")
        b.go(f"{APP}/learn/{crypto['id']}", 4)
        b.shot("shot-4-course-path.png")

        # Lesson: advance to the first real-life choice
        b.go(f"{APP}/concept/{tip['id']}", 4)
        b.js("""(async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));
          for(let i=0;i<10;i++){ if(document.querySelector('[data-testid=scenario-choice-0]')) break;
            const fc=document.querySelector('[data-testid=flashcard]'); if(fc){fc.click(); await w(300);}
            const n=document.querySelector('[data-testid=btn-next-lesson]'); if(n) n.click(); await w(600);} return true})()""")
        time.sleep(1)
        b.shot("shot-5-choice.png")

        # Pick the wrong answer to show the verdict, the explanation and the wallet bars
        b.js("document.querySelector('[data-testid=scenario-choice-0]').click()")
        time.sleep(1.2)
        b.js("document.querySelector('[data-testid=scenario-feedback]').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
        time.sleep(1)
        b.shot("shot-6-feedback.png")

        b.go(APP + "/account", 4)
        b.shot("shot-7-account.png")
    finally:
        b.close()


if __name__ == "__main__":
    main()
