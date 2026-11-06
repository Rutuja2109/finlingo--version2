import React, { useCallback, useEffect, useRef, useState } from "react";
import { BarChart3, Coins, Bitcoin, Rocket, RefreshCw, Flame, ArrowUp, ArrowDown, LineChart, Wallet, History } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

const ICONS = { BarChart3, Coins, Bitcoin, Rocket };
const TFS = ["1MIN", "5MIN", "15MIN", "30MIN", "1H", "1D", "1W"];
const inr = (n, d = 0) =>
  (n < 0 ? "−" : "") + "₹" + Math.abs(Number(n)).toLocaleString("en-IN", { minimumFractionDigits: d, maximumFractionDigits: d });
const pdec = (p) => (p < 1000 ? 2 : 0);
const num = (v) => (v >= 1000 ? Math.round(v).toLocaleString("en-IN") : v.toFixed(1));

function Chart({ series, avg }) {
  const W = 350, H = 210, pl = 6, pr = 62, pt = 14, pb = 12;
  const d = series.map((s) => s.p);
  if (d.length < 2) return <div className="h-[210px]" />;
  let mn = Math.min(...d), mx = Math.max(...d);
  if (mx === mn) { mx += 1; mn -= 1; }
  const minSpan = d[d.length - 1] * 0.005;
  if (mx - mn < minSpan) { const mid = (mx + mn) / 2; mx = mid + minSpan / 2; mn = mid - minSpan / 2; }
  const pad = (mx - mn) * 0.08; mn -= pad; mx += pad;
  const x = (i) => pl + ((W - pl - pr) * i) / (d.length - 1);
  const y = (v) => pt + (H - pt - pb) * (1 - (v - mn) / (mx - mn));
  const line = d.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join("");
  const area = `${line}L${x(d.length - 1).toFixed(1)} ${H - pb}L${x(0).toFixed(1)} ${H - pb}Z`;
  const col = d[d.length - 1] >= d[0] ? "#10B981" : "#EF4444";
  const last = d[d.length - 1], ly = y(last);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" role="img" aria-label="Price chart">
      {[0, 1, 2, 3, 4].map((i) => {
        const v = mn + ((mx - mn) * i) / 4, yy = y(v);
        return (
          <g key={i}>
            <line x1={pl} x2={W - pr + 4} y1={yy} y2={yy} stroke="#f4f4f5" />
            <text x={W - pr + 8} y={yy + 4} fontSize="10.5" fill="#a1a1aa" fontWeight="600">{num(v)}</text>
          </g>
        );
      })}
      <path d={area} fill={col} opacity=".12" />
      <path d={line} fill="none" stroke={col} strokeWidth="2.2" strokeLinejoin="round" strokeLinecap="round" />
      {avg && avg > mn && avg < mx && (
        <g>
          <line x1={pl} x2={W - pr + 4} y1={y(avg)} y2={y(avg)} stroke="#18181b" strokeDasharray="4 4" />
          <text x={pl + 4} y={y(avg) - 4} fontSize="10" fill="#18181b" fontWeight="800">your buy price</text>
        </g>
      )}
      <rect x={W - pr + 2} y={ly - 10} width={pr - 2} height="20" rx="6" fill={col} />
      <text x={W - pr + 7} y={ly + 4} fontSize="11" fill="#fff" fontWeight="800">{num(last)}</text>
    </svg>
  );
}

function Coach({ mood, title, children, tone = "" }) {
  const cls = { warn: "bg-amber-50 border-amber-300", bad: "bg-red-50 border-red-300", good: "bg-emerald-50 border-emerald-300" }[tone] || "bg-white border-zinc-200";
  return (
    <div className={`flex gap-3 items-start border rounded-2xl px-3 py-2.5 mt-3 text-[13px] leading-relaxed ${cls}`}>
      <Lumi size={44} mood={mood} className="shrink-0" />
      <div><b className="font-[Outfit]">{title}</b><br />{children}</div>
    </div>
  );
}

export default function Practice() {
  const { refreshStats } = useAuth();
  const [S, setS] = useState(null);
  const [sel, setSel] = useState("nifty");
  const [tf, setTf] = useState("1MIN");
  const [view, setView] = useState("trade");
  const [sheet, setSheet] = useState(null); // {mode, amt}
  const [msg, setMsg] = useState(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [tour, setTour] = useState(null); // {i, quiz}
  const [f, setF] = useState({});
  const [lastPnl, setLastPnl] = useState(0);
  const [toast, setToast] = useState("");
  const selRef = useRef(sel), tfRef = useRef(tf), inflight = useRef(false), tourChecked = useRef(false), seenResult = useRef(null);
  selRef.current = sel; tfRef.current = tf;

  const load = useCallback(async () => {
    if (inflight.current) return;
    inflight.current = true;
    try {
      const { data } = await api.get("/practice/state", { params: { asset: selRef.current, tf: tfRef.current } });
      setS(data);
      setErr("");
      if (!tourChecked.current) { tourChecked.current = true; if (!data.tour_done) setTour({ i: 0, quiz: null }); }
      const lr = data.last_result;
      if (lr && seenResult.current !== lr.at) {
        if (seenResult.current !== null || Date.now() - Date.parse(lr.at) < 60000) {
          const diff = lr.after - lr.before;
          setMsg({ k: diff < 0 ? "warn" : "good", h: "Crash replay finished", t: `Your portfolio went from ${inr(lr.before)} to ${inr(lr.after)} (${diff >= 0 ? "+" : ""}${inr(diff)}). Prices fell hard, then recovered a little. People who sold at the bottom locked in the loss. People who held, and had some gold, saw less damage.` });
        }
        seenResult.current = lr.at;
      } else if (!lr && seenResult.current === null) seenResult.current = "";
    } catch (e) { setErr(formatApiError(e)); }
    inflight.current = false;
  }, []);

  const crashing = !!S?.scenario?.active;
  useEffect(() => {
    load();
    const iv = setInterval(() => { if (!document.hidden) load(); }, crashing ? 700 : 1500);
    return () => clearInterval(iv);
  }, [load, crashing]);
  useEffect(() => { load(); }, [sel, tf, load]);

  const asset = S?.assets.find((a) => a.id === sel) || S?.assets[0];
  const pos = S?.positions.find((p) => p.asset === sel);
  const total = S?.total || 0;

  const doTrade = async () => {
    if (!sheet || busy) return;
    setBusy(true);
    try {
      const body = sheet.mode === "buy" ? { asset: sel, side: "buy", amount: sheet.amt } : { asset: sel, side: "sell", percent: sheet.amt };
      const { data } = await api.post("/practice/trade", body);
      const st = data.state;
      setSheet(null);
      if (sheet.mode === "buy") {
        setF((x) => ({ ...x, bought: true }));
        const p = st.positions.find((q) => q.asset === sel);
        const share = p ? p.value / st.total : 0;
        setMsg(share > 0.4
          ? { k: "bad", h: "Big bet on one asset", t: `${Math.round(share * 100)}% of your money is now in ${asset.name}. Beginners who spread their money lose less when one asset falls.` }
          : { k: "good", h: `Bought ${inr(data.result.amount)}`, t: `You now own ${data.result.units.toFixed(4)} units. Watch the dashed line: that is your buy price.` });
      } else {
        const pnl = data.result.pnl, amt = data.result.amount;
        setF((x) => ({ ...x, sold: true })); setLastPnl(pnl);
        setMsg(Math.abs(pnl) < amt * 0.003
          ? { k: "good", h: "Roughly break-even", t: "You sold at about the price you paid. Real profit comes from selling clearly above your buy price." }
          : pnl < 0 && data.result.during_scenario
            ? { k: "bad", h: "Panic sell?", t: `You sold during the crash and locked in a loss of ${inr(Math.abs(pnl))}. Prices often recover, but only if you are still holding.` }
            : pnl < 0
              ? { k: "warn", h: "Sold at a loss", t: `You lost ${inr(Math.abs(pnl))} on this trade. Ask: did the reason you bought change, or did you just get scared?` }
              : { k: "good", h: "Sold for a profit", t: `You made ${inr(pnl)}. Notice you only gain if you sell above your buy price.` });
      }
      setS((o) => ({ ...st, selected: o.selected }));
      load();
    } catch (e) { setMsg({ k: "bad", h: "That did not work", t: formatApiError(e) }); setSheet(null); }
    setBusy(false);
  };

  const startCrash = async () => {
    try {
      const { data } = await api.post("/practice/scenario/start", { id: "crash" });
      setS(data); setMsg(null);
    } catch (e) { setMsg({ k: "bad", h: "Could not start", t: formatApiError(e) }); }
  };

  const resetAll = async () => {
    if (S && (S.positions.length || S.trades.length) && !window.confirm("Reset your practice money to ₹1,00,000 and clear your trades?")) return;
    const { data } = await api.post("/practice/reset");
    setS(data); setMsg(null); setSel("nifty");
  };

  // ---------------- Lumi's tour
  const TOUR = [
    { m: "cheer", h: "Welcome!", t: "Hi, I am Lumi! I will show you how practice trading works in about two minutes. You get ₹1,00,000 of practice money. It is not real, so you cannot lose a single rupee here.", b: "Show me" },
    { m: "happy", h: "Your cash", t: "This is your cash: money you have not invested yet. It goes down when you buy something and up when you sell.", hl: "#pt-bal", b: "Got it" },
    { m: "happy", h: "Pick an asset", t: "An asset is something you can buy, like gold or a share. Tap NIFTY. It is a basket of 50 big companies, so it moves gently.", hl: "[data-a=nifty]", wait: () => sel === "nifty", hint: "Tap NIFTY above" },
    { m: "happy", h: "The price chart", t: "The line shows the price. Green means it is higher than at the start of this view, red means lower. The tag on the right is the price right now.", hl: "#pt-chart", b: "Next" },
    { m: "happy", h: "Zoom in and out", t: "Tap 5MIN to see a longer stretch of time. Short views show quick wiggles, longer views show the bigger trend.", hl: "[data-t='5MIN']", wait: () => tf === "5MIN", hint: "Tap 5MIN" },
    { m: "cheer", h: "Buy", t: "Buying means swapping cash for a share of the asset. Tap Buy.", hl: "#pt-buy", wait: () => f.sheetBuy || f.bought, hint: "Tap Buy" },
    { m: "cheer", h: "Choose an amount", t: "Pick how much to invest, for example ₹5,000 or ₹10,000, then tap Confirm buy.", hl: "#pt-go", wait: () => f.bought, hint: "Tap Confirm buy" },
    { m: "happy", h: "Your profit or loss", t: "Watch the dashed line on the chart: it is your buy price. Price above it means profit. Below it means a loss. The line right under the chart shows it live.", hl: "#pt-mypos", b: "Next" },
    { m: "nervous", h: "Quick check", quiz: { q: "The price drops below your dashed line. What does that mean?", opts: ["You are making a profit", "You are in a loss, but only on paper until you sell", "Your money is safe from loss"], ok: 1, fb: ["Not quite. Below your buy price means a loss.", "Right. It is a loss on paper. It only becomes real if you sell.", "Not quite. Prices can fall, so nothing is guaranteed."] } },
    { m: "cheer", h: "Sell", t: "Selling swaps your holding back into cash. Tap Sell.", hl: "#pt-sell", wait: () => f.sheetSell || f.sold, hint: "Tap Sell" },
    { m: "cheer", h: "Sell it all", t: "Choose 100% and tap Confirm sell.", hl: "#pt-go", wait: () => f.sold, hint: "Tap Confirm sell" },
    { m: "cheer", h: "Your result", t: lastPnl >= 0 ? `You made ${inr(lastPnl)}. This time the price went up. In real life it can go either way, and that is the risk.` : `You lost ${inr(Math.abs(lastPnl))}. That can happen. Risk means prices can fall as well as rise.`, b: "Next" },
    { m: "happy", h: "Spread your money", t: "Tap Portfolio to see how your money is split. Spreading it across different assets means one bad day cannot sink you.", hl: "[data-v=port]", wait: () => f.port, hint: "Tap Portfolio" },
    { m: "nervous", h: "Practice a crash", t: "On the Trade tab there is a button to replay a market crash. Try it when you are ready: it teaches you to stay calm.", b: "Next", goTrade: true },
    { m: "cheer", h: "Ready!", t: "You know the basics. I will reset your practice money to ₹1,00,000 so you can start fresh. Practice here, and think carefully before you ever invest real money.", b: "Start practicing", finish: true },
  ];
  const step = tour ? TOUR[tour.i] : null;

  const tourEnd = async (finished) => {
    setTour(null); setSheet(null); setF({});
    try {
      if (finished) { await api.post("/practice/reset"); setView("trade"); setMsg(null); }
      const { data } = await api.post("/practice/tour-complete", { skipped: !finished });
      if (data.xp) { setToast(`Tour complete! +${data.xp} XP and +${data.coins} coins`); setTimeout(() => setToast(""), 4000); refreshStats?.(); }
      load();
    } catch (e) { setErr(formatApiError(e)); }
  };
  const tourNext = () => {
    if (step.finish) return tourEnd(true);
    const ni = tour.i + 1;
    if (TOUR[ni]?.goTrade) setView("trade");
    setTour({ i: ni, quiz: null });
  };

  // highlight the element the tour points at
  useEffect(() => {
    document.querySelectorAll(".pt-hl").forEach((e) => e.classList.remove("pt-hl"));
    if (step?.hl) { const t = document.querySelector(step.hl); if (t) t.classList.add("pt-hl"); }
  });
  useEffect(() => {
    if (step?.hl && !step.hl.includes("pt-go")) document.querySelector(step.hl)?.scrollIntoView({ block: "center", behavior: "smooth" });
  }, [tour?.i]); // eslint-disable-line

  if (!S) return <div className="py-20 text-center text-zinc-500">{err || "Opening your practice account…"}</div>;
  const series = S.selected.asset === sel ? S.selected.series : [];
  const first = series[0]?.p, lastP = series[series.length - 1]?.p;
  const chg = first ? ((lastP - first) / first) * 100 : 0;
  const held = pos?.value || 0;
  const canNext = step?.quiz ? tour.quiz !== null : !step?.wait || step.wait();

  return (
    <div className="max-w-md mx-auto pb-24" data-testid="practice-page">
      {/* header */}
      <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#FF6B35] via-[#FF8A4C] to-[#EC4899]">
        <div className="flex items-center justify-between gap-2">
          <button onClick={resetAll} className="flex items-center gap-1 rounded-full bg-white/25 px-3 py-1.5 text-[13px] font-bold font-[Outfit]" data-testid="pt-reset"><RefreshCw className="w-3.5 h-3.5" />Reset</button>
          <div className="text-center">
            <div id="pt-bal" className="inline-block px-3 mb-1.5 font-[Outfit] font-black text-2xl tracking-tight" data-testid="pt-cash">{inr(S.cash)}</div>
            <div className="text-[11.5px] font-semibold opacity-90">Practice money, not real money</div>
          </div>
          <span className="w-[68px]" />
        </div>
      </div>

      {crashing && (
        <div className="mt-2 bg-zinc-900 text-white rounded-2xl px-3 py-2 text-[13px] font-bold flex items-center gap-2" data-testid="pt-crash-banner">
          <Flame className="w-4 h-4 text-[#FF6B35]" /> Market crash replay: day {Math.min(10, Math.ceil((S.scenario.tick + 1) / 5))} of 10. Hold your nerve.
        </div>
      )}

      {/* Lumi's tour card */}
      {step && (
        <div className="sticky top-[68px] z-30 mt-2 bg-white border-2 border-[#FF6B35] rounded-2xl p-2.5 shadow-lg" data-testid="pt-tour">
          <div className="text-[11px] font-extrabold tracking-[.14em] uppercase text-[#FF6B35]">Lumi’s tour · {tour.i + 1} of {TOUR.length}</div>
          <div className="flex gap-2.5 items-start mt-1">
            <Lumi size={44} mood={step.m} className="shrink-0" />
            <div className="text-[13px] leading-snug"><b className="font-[Outfit]">{step.h}</b><br />{step.quiz ? step.quiz.q : step.t}</div>
          </div>
          {step.quiz && step.quiz.opts.map((o, i) => (
            <button key={i} onClick={() => tour.quiz === null && setTour({ ...tour, quiz: i })}
              className={`block w-full text-left border-2 rounded-xl px-2.5 py-2 mt-1.5 text-[13px] font-semibold ${tour.quiz === null ? "border-zinc-200 bg-white" : i === step.quiz.ok ? "border-emerald-500 bg-emerald-50" : i === tour.quiz ? "border-red-500 bg-red-50" : "border-zinc-200"}`}>{o}</button>
          ))}
          {step.quiz && tour.quiz !== null && <div className="text-[13px] mt-1.5">{step.quiz.fb[tour.quiz]}</div>}
          <div className="flex items-center gap-2 mt-2.5">
            <button onClick={tourNext} disabled={!canNext} data-testid="pt-tour-next"
              className={`rounded-xl px-4 py-2 font-[Outfit] font-extrabold text-sm text-white ${canNext ? "bg-[#FF6B35]" : "bg-[#fdba9b]"}`}>
              {canNext ? step.b || "Next" : step.hint || "Do the step above"}
            </button>
            <button onClick={() => tourEnd(false)} className="ml-auto text-[12.5px] font-bold text-zinc-500" data-testid="pt-tour-skip">Skip tour</button>
          </div>
        </div>
      )}

      {/* tabs */}
      <div className="grid grid-cols-3 gap-1 bg-zinc-100 rounded-2xl p-1 mt-3">
        {[["trade", "Trade", LineChart], ["port", "Portfolio", Wallet], ["log", "History", History]].map(([v, label, I]) => (
          <button key={v} data-v={v} onClick={() => { setView(v); if (v === "port") setF((x) => ({ ...x, port: true })); }}
            className={`flex items-center justify-center gap-1.5 py-2 rounded-xl text-[13px] font-bold ${view === v ? "bg-white shadow text-[#FF6B35]" : "text-zinc-500"}`}><I className="w-4 h-4" />{label}</button>
        ))}
      </div>

      {err && <div className="mt-2 text-[12.5px] text-red-700 bg-red-50 rounded-xl px-3 py-2">{err}</div>}

      {view === "trade" && asset && (
        <div className="mt-3">
          <div className="flex gap-3 overflow-x-auto px-2 pt-2 pb-3 -mx-2 [scrollbar-width:none]">
            {S.assets.map((a) => {
              const I = ICONS[a.icon] || BarChart3;
              return (
                <button key={a.id} data-a={a.id} data-testid={`pt-asset-${a.id}`} onClick={() => { setSel(a.id); setMsg(null); }} className="shrink-0 w-16 text-center">
                  <div className={`w-[52px] h-[52px] rounded-full grid place-items-center text-white mx-auto mb-1 border-[3px] ${a.id === sel ? "border-zinc-900" : "border-transparent"}`} style={{ background: a.color }}><I className="w-6 h-6" /></div>
                  <span className={`text-[11px] font-bold ${a.id === sel ? "text-zinc-900" : "text-zinc-500"}`}>{a.short}</span>
                </button>
              );
            })}
          </div>
          <div className="flex items-end justify-between mt-1 mb-1">
            <div>
              <div className="text-[12.5px] font-bold text-zinc-500">{asset.name}</div>
              <div className="font-[Outfit] font-black text-[28px] tracking-tight leading-tight" data-testid="pt-price">{inr(asset.price, pdec(asset.price))}</div>
            </div>
            <span className={`font-[Outfit] font-extrabold text-[13px] px-2.5 py-1 rounded-full ${chg >= 0 ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>{chg >= 0 ? "+" : ""}{chg.toFixed(2)}%</span>
          </div>
          <div id="pt-chart" className="bg-white border border-zinc-200 rounded-[20px] px-1 pt-1.5"><Chart series={series} avg={pos ? pos.cost / pos.units : null} /></div>
          <div className="flex justify-between my-2">
            {TFS.map((k) => <button key={k} data-t={k} onClick={() => setTf(k)} className={`font-[Outfit] font-extrabold text-xs px-2 py-1.5 rounded-[10px] ${k === tf ? "bg-zinc-900 text-white" : "text-zinc-400"}`}>{k}</button>)}
          </div>
          <div id="pt-mypos" className="text-[12.5px] text-zinc-500 mx-1 mb-2">
            {pos ? <>You hold <b>{inr(pos.value)}</b> of {asset.short} · profit/loss <b className={pos.pnl >= 0 ? "text-emerald-700" : "text-red-700"}>{pos.pnl >= 0 ? "+" : ""}{inr(pos.pnl)}</b></> : `You do not own any ${asset.short} yet.`}
          </div>
          <div className="grid grid-cols-2 gap-2.5">
            <button id="pt-sell" data-testid="pt-sell" disabled={!pos} onClick={() => { setSheet({ mode: "sell", amt: 100 }); setF((x) => ({ ...x, sheetSell: true })); }}
              className={`rounded-2xl py-3 text-white font-[Outfit] font-black text-base flex items-center justify-center gap-1.5 ${pos ? "bg-red-500 active:scale-[.97]" : "bg-red-300"}`}><ArrowDown className="w-4 h-4" />Sell</button>
            <button id="pt-buy" data-testid="pt-buy" onClick={() => { setSheet({ mode: "buy", amt: Math.min(10000, Math.floor(S.cash)) }); setF((x) => ({ ...x, sheetBuy: true })); }}
              className="rounded-2xl py-3 text-white font-[Outfit] font-black text-base flex items-center justify-center gap-1.5 bg-emerald-500 active:scale-[.97]"><ArrowUp className="w-4 h-4" />Buy</button>
          </div>
          {msg
            ? <Coach mood={msg.k === "bad" ? "angry" : msg.k === "warn" ? "nervous" : "cheer"} title={msg.h} tone={msg.k}>{msg.t}</Coach>
            : <Coach mood="happy" title="Lumi says">{asset.why}</Coach>}
          {!crashing && (
            <button onClick={startCrash} data-testid="pt-crash" className="mx-auto mt-3 flex items-center gap-1.5 border-2 border-red-500 text-red-700 bg-white rounded-2xl px-3 py-2 font-[Outfit] font-extrabold text-[13px]"><Flame className="w-4 h-4" />Replay a market crash</button>
          )}
          {!tour && <button onClick={() => { setTour({ i: 0, quiz: null }); setF({}); }} className="block mx-auto mt-2 text-[12.5px] font-extrabold text-[#FF6B35]" data-testid="pt-replay-tour">Replay Lumi’s tour</button>}
        </div>
      )}

      {view === "port" && <Portfolio S={S} total={total} />}

      {view === "log" && (
        <div className="mt-3 bg-white border border-zinc-200 rounded-[20px] p-3.5">
          <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-1.5">Trade history</p>
          {S.trades.length ? S.trades.map((l, i) => (
            <div key={i} className="flex items-center justify-between gap-2 py-2 border-t first:border-t-0 border-zinc-100 text-sm">
              <div><b>{l.side === "buy" ? "Bought" : "Sold"} {l.name}</b><div className="text-[12.5px] text-zinc-500">{inr(l.amount)} at {inr(l.price, pdec(l.price))}</div></div>
              {l.side === "sell" && <span className={`font-[Outfit] font-extrabold text-[13px] px-2.5 py-1 rounded-full ${l.pnl >= 0 ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>{l.pnl >= 0 ? "+" : ""}{inr(l.pnl)}</span>}
            </div>
          )) : <p className="text-[12.5px] text-zinc-500">No trades yet.</p>}
        </div>
      )}

      {/* buy / sell sheet */}
      {sheet && asset && (
        <div className="fixed inset-0 z-50 bg-black/45 flex items-end justify-center" onClick={() => setSheet(null)}>
          <div className="bg-white rounded-t-[26px] w-full max-w-md px-4 pt-4 pb-6" onClick={(e) => e.stopPropagation()} data-testid="pt-sheet">
            {(() => {
              const buy = sheet.mode === "buy";
              const opts = buy ? [5000, 10000, 25000, 50000] : [25, 50, 100];
              const amount = buy ? sheet.amt : (held * sheet.amt) / 100;
              const tooMuch = buy && sheet.amt > S.cash;
              const tooSmall = buy && sheet.amt < S.min_buy;
              return (
                <>
                  <h3 className="font-[Outfit] font-black text-xl">{buy ? "Buy " : "Sell "}{asset.name}</h3>
                  <div className="text-[12.5px] text-zinc-500">Price now {inr(asset.price, pdec(asset.price))} · {buy ? `Cash ${inr(S.cash)}` : `You hold ${inr(held)}`}</div>
                  <div className="flex gap-2 flex-wrap my-3">
                    {opts.map((o) => <button key={o} onClick={() => setSheet({ ...sheet, amt: o })} className={`border-2 rounded-[14px] px-3 py-2 font-[Outfit] font-extrabold text-sm ${o === sheet.amt ? "border-[#FF6B35] bg-[#FF6B35]/10" : "border-zinc-200"}`}>{buy ? inr(o) : `${o}%`}</button>)}
                  </div>
                  <div className="bg-white border border-zinc-200 rounded-2xl px-3 py-1 mb-2.5">
                    <div className="flex justify-between py-2 text-sm"><span>{buy ? "You spend" : "You receive"}</span><b>{inr(amount)}</b></div>
                    <div className="flex justify-between py-2 text-sm border-t border-zinc-100"><span>Units</span><b>{(amount / asset.price).toFixed(4)}</b></div>
                  </div>
                  {tooMuch && <p className="text-red-700 text-[13px] mb-2">You only have {inr(S.cash)} of practice money.</p>}
                  {tooSmall && !tooMuch && <p className="text-red-700 text-[13px] mb-2">The smallest purchase is {inr(S.min_buy)}.</p>}
                  <button id="pt-go" data-testid="pt-go" onClick={doTrade} disabled={busy || tooMuch || tooSmall}
                    className={`w-full rounded-2xl py-3.5 font-[Outfit] font-black text-base text-white ${buy ? "bg-emerald-500" : "bg-red-500"} disabled:opacity-50`}>Confirm {buy ? "buy" : "sell"}</button>
                  <button onClick={() => setSheet(null)} className="w-full rounded-2xl py-3 mt-2 bg-zinc-100 font-[Outfit] font-extrabold">Cancel</button>
                </>
              );
            })()}
          </div>
        </div>
      )}

      {toast && <div className="fixed bottom-24 inset-x-4 z-50 mx-auto max-w-sm bg-zinc-900 text-white text-center rounded-2xl py-3 font-bold text-sm" data-testid="pt-toast">{toast}</div>}
    </div>
  );
}

function Portfolio({ S, total }) {
  const pnl = total - S.start_cash;
  const segs = [["Cash", S.cash, "#d4d4d8"], ...S.positions.map((p) => { const a = S.assets.find((x) => x.id === p.asset); return [a.short, p.value, a.color]; })];
  const top = [...S.positions].sort((a, b) => b.value - a.value)[0];
  const share = top ? top.value / total : 0;
  const topName = top ? S.assets.find((a) => a.id === top.asset).name : "";
  return (
    <div className="mt-3 space-y-2.5">
      <div className="bg-white border border-zinc-200 rounded-[20px] p-3.5">
        <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500">Total value</p>
        <div className="font-[Outfit] font-black text-[22px]" data-testid="pt-total">{inr(total)}</div>
        <span className={`inline-block mt-1 font-[Outfit] font-extrabold text-[13px] px-2.5 py-1 rounded-full ${pnl >= 0 ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>{pnl >= 0 ? "+" : ""}{inr(pnl)} ({((pnl / S.start_cash) * 100).toFixed(2)}%)</span>
        <div className="flex h-3.5 rounded-full overflow-hidden bg-zinc-100 my-2">{segs.map((s, i) => <div key={i} style={{ width: `${(s[1] / total) * 100}%`, background: s[2] }} />)}</div>
        <div className="text-[12.5px] text-zinc-500">{segs.map((s) => `${s[0]} ${Math.round((s[1] / total) * 100)}%`).join(" · ")}</div>
      </div>
      <div className="bg-white border border-zinc-200 rounded-[20px] p-3.5">
        <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-1.5">Your holdings</p>
        {S.positions.length ? S.positions.map((p) => {
          const a = S.assets.find((x) => x.id === p.asset);
          return (
            <div key={p.asset} className="flex items-center justify-between py-2 border-t first:border-t-0 border-zinc-100 text-sm">
              <div><b>{a.name}</b><div className="text-[12.5px] text-zinc-500">{p.units.toFixed(4)} units</div></div>
              <div className="text-right"><b>{inr(p.value)}</b><div className={`text-xs font-extrabold ${p.pnl >= 0 ? "text-emerald-700" : "text-red-700"}`}>{p.pnl >= 0 ? "+" : ""}{inr(p.pnl)}</div></div>
            </div>
          );
        }) : <p className="text-[12.5px] text-zinc-500">Nothing yet. Buy something on the Trade tab.</p>}
      </div>
      {top && (share > 0.4
        ? <Coach mood="angry" tone="bad" title="Too much in one basket">{Math.round(share * 100)}% of your money is in {topName}. If it falls 30%, you lose about {Math.round(share * 30)}% of everything.</Coach>
        : S.positions.length >= 3
          ? <Coach mood="cheer" tone="good" title="Nicely spread out">You hold {S.positions.length} different assets. One bad day will not sink you.</Coach>
          : <Coach mood="nervous" tone="warn" title="Try spreading out">Holding a mix of assets, like an index fund and gold, softens the bad days.</Coach>)}
    </div>
  );
}
