// Haptic feedback via Web Vibration API (works on Android without any plugin).
// Silently no-ops on iOS / desktop.

const vib = (pattern) => {
  try { navigator.vibrate?.(pattern); } catch (_) {}
};

export const haptics = {
  light:     () => vib(25),
  medium:    () => vib(50),
  success:   () => vib([30, 20, 50]),    // double-tap feel
  error:     () => vib([70, 30, 70]),    // two heavy pulses
  celebrate: () => vib([30, 15, 30, 15, 80]), // staccato burst
};
