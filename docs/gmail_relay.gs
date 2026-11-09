// Free email relay: Google Apps Script web app. Sends from the Google account that owns the script.
// Setup: see docs/LAUNCH_CHECKLIST.md section 2.4. Put your own long random text in SECRET below.
const SECRET = "PASTE-A-LONG-RANDOM-TEXT-HERE";

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    if (d.secret !== SECRET) return out({ ok: false });
    MailApp.sendEmail({ to: d.to, subject: d.subject, body: d.text, htmlBody: d.html || undefined, name: d.name || "FinLearn" });
    return out({ ok: true });
  } catch (err) {
    return out({ ok: false });
  }
}
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
