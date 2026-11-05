import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { LogOut, Trash2, Shield } from "lucide-react";
import { PRIVACY_URL } from "@/lib/api";

export default function Account() {
  const { user, logout, deleteAccount } = useAuth();
  const [confirming, setConfirming] = useState(false);
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  const onDelete = async (e) => {
    e.preventDefault();
    setErr(""); setBusy(true);
    const res = await deleteAccount(password);
    setBusy(false);
    if (res.ok) window.location.replace("/login");
    else setErr(res.error);
  };

  return (
    <div className="max-w-xl mx-auto pb-24">
      <h1 className="font-[Outfit] font-black text-3xl tracking-tight mb-6">Account</h1>

      <div className="bg-white border border-zinc-200 rounded-3xl p-6 mb-4">
        <p className="uppercase tracking-[0.2em] text-xs font-bold text-zinc-500 mb-1">Signed in as</p>
        <p className="font-[Outfit] font-bold text-xl">{user?.name}</p>
        <p className="text-sm text-zinc-500">{user?.email}</p>
        <button
          onClick={() => { logout(); window.location.replace("/login"); }}
          data-testid="account-logout"
          className="mt-5 inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-zinc-900 text-white font-[Outfit] font-bold"
        >
          <LogOut className="w-4 h-4" /> Log out
        </button>
      </div>

      <div className="bg-white border border-zinc-200 rounded-3xl p-6 mb-4">
        <p className="uppercase tracking-[0.2em] text-xs font-bold text-zinc-500 mb-2">About</p>
        <a href={PRIVACY_URL} target="_blank" rel="noopener noreferrer" data-testid="account-privacy"
          className="inline-flex items-center gap-2 font-[Outfit] font-bold text-[#FF6B35] hover:underline">
          <Shield className="w-4 h-4" /> Privacy policy
        </a>
        <p className="text-xs text-zinc-500 mt-3">
          FinLearn is for education only and is not financial advice.
        </p>
      </div>

      {user?.role !== "admin" && (
        <div className="bg-white border border-red-200 rounded-3xl p-6">
          <p className="uppercase tracking-[0.2em] text-xs font-bold text-red-600 mb-1">Danger zone</p>
          <h2 className="font-[Outfit] font-bold text-xl mb-1">Delete account</h2>
          <p className="text-sm text-zinc-500 mb-4">
            Permanently deletes your account, progress, XP and streaks. This cannot be undone.
          </p>
          {!confirming ? (
            <button
              onClick={() => setConfirming(true)}
              data-testid="account-delete-start"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl border border-red-300 text-red-600 font-[Outfit] font-bold hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" /> Delete my account
            </button>
          ) : (
            <form onSubmit={onDelete}>
              <label className="block text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5">
                Confirm your password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Leave blank if you signed in with Google"
                className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-red-400 focus:ring-2 focus:ring-red-200 mb-3"
                data-testid="account-delete-password"
              />
              {err && (
                <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-3 py-2 mb-3">{err}</div>
              )}
              <div className="flex gap-3">
                <button
                  type="submit" disabled={busy}
                  data-testid="account-delete-confirm"
                  className="px-5 py-3 rounded-xl bg-red-600 text-white font-[Outfit] font-bold disabled:opacity-60"
                >
                  {busy ? "Deleting…" : "Yes, delete everything"}
                </button>
                <button
                  type="button"
                  onClick={() => { setConfirming(false); setPassword(""); setErr(""); }}
                  className="px-5 py-3 rounded-xl bg-zinc-100 font-[Outfit] font-bold"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      )}
    </div>
  );
}
