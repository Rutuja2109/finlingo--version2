"""Sends the few emails the app needs (password reset, password-changed notice). Works with any SMTP account (for example
a Gmail app password, Brevo or Zoho) or with Resend. If nothing is configured, send_email() returns False and the app
falls back to its manual-help message.

Environment variables
  SMTP: SMTP_HOST, SMTP_PORT (587), SMTP_USER, SMTP_PASSWORD, MAIL_FROM ("FinLearn <you@example.com>"),
        SMTP_STARTTLS ("0" for a plain test server), SMTP_SSL ("1" for port 465)
  Resend: RESEND_API_KEY, MAIL_FROM
  Web relay (free, for hosts that block SMTP): MAIL_RELAY_URL, MAIL_RELAY_SECRET (a Google Apps Script web app, see docs)
"""
import logging
import os
import smtplib
from email.message import EmailMessage

import httpx
from starlette.concurrency import run_in_threadpool

log = logging.getLogger(__name__)


def configured() -> bool:
    if os.environ.get("MAIL_RELAY_URL") and os.environ.get("MAIL_RELAY_SECRET"):
        return True
    if os.environ.get("RESEND_API_KEY") and os.environ.get("MAIL_FROM"):
        return True
    return bool(os.environ.get("SMTP_HOST") and os.environ.get("MAIL_FROM"))


def _send_smtp(to: str, subject: str, text: str, html: str):
    msg = EmailMessage()
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype="html")
    host, port = os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587"))
    smtp_cls = smtplib.SMTP_SSL if os.environ.get("SMTP_SSL") == "1" else smtplib.SMTP
    with smtp_cls(host, port, timeout=20) as s:
        if smtp_cls is smtplib.SMTP and os.environ.get("SMTP_STARTTLS", "1") != "0":
            s.starttls()
        if os.environ.get("SMTP_USER"):
            s.login(os.environ["SMTP_USER"], os.environ.get("SMTP_PASSWORD", ""))
        s.send_message(msg)


async def send_email(to: str, subject: str, text: str, html: str = "") -> bool:
    if not configured():
        return False
    try:
        if os.environ.get("MAIL_RELAY_URL") and os.environ.get("MAIL_RELAY_SECRET"):
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as c:
                r = await c.post(os.environ["MAIL_RELAY_URL"], json={"secret": os.environ["MAIL_RELAY_SECRET"], "to": to,
                                 "subject": subject, "text": text, "html": html, "name": "FinLearn"})
                r.raise_for_status()
                if not r.json().get("ok"):
                    raise RuntimeError("relay refused")
        elif os.environ.get("RESEND_API_KEY"):
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {os.environ['RESEND_API_KEY']}"},
                                 json={"from": os.environ["MAIL_FROM"], "to": [to], "subject": subject, "text": text, **({"html": html} if html else {})})
                r.raise_for_status()
        else:
            await run_in_threadpool(_send_smtp, to, subject, text, html)
        return True
    except Exception as e:  # never let a mail problem break the request, and never log the message
        log.error("email send failed: %s", type(e).__name__)
        return False


def reset_email(name: str, link: str, minutes: int = 60):
    text = (f"Hi {name},\n\nSomeone asked to reset the password for your FinLearn account. If that was you, open this link "
            f"within {minutes} minutes to choose a new password:\n\n{link}\n\nIf it was not you, ignore this email. Your password stays "
            f"the same.\n\nFinLearn")
    html = (f"<p>Hi {name},</p><p>Someone asked to reset the password for your FinLearn account. If that was you, choose a new password "
            f"within {minutes} minutes:</p><p><a href=\"{link}\" style=\"background:#FF6B35;color:#fff;padding:12px 20px;border-radius:10px;"
            f"text-decoration:none;font-weight:bold\">Reset my password</a></p><p style=\"color:#666\">If it was not you, ignore this email. "
            f"Your password stays the same.</p>")
    return "Reset your FinLearn password", text, html


def google_only_email(name: str):
    text = (f"Hi {name},\n\nSomeone asked to reset the password for your FinLearn account. Your account uses Google sign-in, so it has no "
            f"password. Open the app and tap Continue with Google.\n\nIf it was not you, you can ignore this email.\n\nFinLearn")
    return "Your FinLearn account uses Google sign-in", text, ""


def changed_email(name: str):
    text = (f"Hi {name},\n\nThe password for your FinLearn account was just changed. If you did this, no action is needed. If you did not, "
            f"reply to this email right away so we can secure your account.\n\nFinLearn")
    return "Your FinLearn password was changed", text, ""
