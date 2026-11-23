/** Mobile Haptic Feedback */
export function triggerHaptic(type = 'light') {
  if (!('vibrate' in navigator)) return;
  try {
    switch (type) {
      case 'light': navigator.vibrate(10); break;
      case 'medium': navigator.vibrate(25); break;
      case 'success': navigator.vibrate([15, 40, 20]); break;
      case 'warning': navigator.vibrate([30, 60, 30]); break;
      case 'error': navigator.vibrate([50, 80, 50, 80, 50]); break;
    }
  } catch (e) {}
}
