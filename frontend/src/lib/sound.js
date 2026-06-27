// Synthetic sound effects via Web Audio API — no audio files needed.
// All sounds generated programmatically; works on Android WebView Chrome 69+.

let _ctx = null;

function ctx() {
  if (!_ctx) _ctx = new (window.AudioContext || window.webkitAudioContext)();
  // Resume if suspended (browser autoplay policy)
  if (_ctx.state === "suspended") _ctx.resume();
  return _ctx;
}

function tone(freq, startSec, durSec, type = "sine", vol = 0.28) {
  try {
    const c = ctx();
    const osc  = c.createOscillator();
    const gain = c.createGain();
    osc.connect(gain);
    gain.connect(c.destination);
    osc.type = type;
    osc.frequency.setValueAtTime(freq, c.currentTime + startSec);
    gain.gain.setValueAtTime(0, c.currentTime + startSec);
    gain.gain.linearRampToValueAtTime(vol, c.currentTime + startSec + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + startSec + durSec);
    osc.start(c.currentTime + startSec);
    osc.stop(c.currentTime + startSec + durSec + 0.02);
  } catch (_) {}
}

export const sound = {
  // Two rising notes — correct answer
  correct() {
    tone(523.25, 0,    0.13);   // C5
    tone(659.25, 0.11, 0.20);   // E5
  },

  // Two falling gritty notes — wrong answer
  wrong() {
    tone(311.13, 0,    0.11, "sawtooth", 0.22);  // Eb4
    tone(233.08, 0.09, 0.20, "sawtooth", 0.16);  // Bb3
  },

  // Three-note fanfare — lesson complete
  complete() {
    tone(523.25, 0,    0.13);   // C5
    tone(659.25, 0.13, 0.13);   // E5
    tone(783.99, 0.26, 0.40);   // G5
  },

  // Card whoosh — flashcard flip
  flip() {
    try {
      const c = ctx();
      const osc  = c.createOscillator();
      const gain = c.createGain();
      osc.connect(gain);
      gain.connect(c.destination);
      osc.type = "sine";
      osc.frequency.setValueAtTime(700, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(320, c.currentTime + 0.09);
      gain.gain.setValueAtTime(0.18, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.09);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + 0.1);
    } catch (_) {}
  },

  // Rising arpeggio — streak / milestone
  streak() {
    [523.25, 587.33, 659.25, 783.99, 1046.5].forEach((f, i) =>
      tone(f, i * 0.09, 0.14)
    );
  },

  // Subtle tap — button press
  tap() { tone(800, 0, 0.04, "sine", 0.10); },
};
