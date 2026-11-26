export function animateNumber(fromVal, toVal, durationMs, onUpdate) {
  const start = performance.now();
  function frame(now) {
    const progress = Math.min(1, (now - start) / durationMs);
    const cur = fromVal + (toVal - fromVal) * progress;
    onUpdate(cur);
    if (progress < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
