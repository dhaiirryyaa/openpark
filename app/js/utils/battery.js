export async function initBatteryWatcher(onPowerChange) {
  if ('getBattery' in navigator) {
    try {
      const battery = await navigator.getBattery();
      battery.addEventListener('levelchange', () => onPowerChange(battery.level, battery.charging));
      onPowerChange(battery.level, battery.charging);
      return battery;
    } catch (e) {}
  }
  return null;
}
