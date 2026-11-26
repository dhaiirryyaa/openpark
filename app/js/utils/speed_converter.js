export function convertSpeed(val, fromUnit = 'kmh', toUnit = 'mps') {
  const inMps = fromUnit === 'kmh' ? val / 3.6 : (fromUnit === 'mph' ? val * 0.44704 : val);
  if (toUnit === 'kmh') return inMps * 3.6;
  if (toUnit === 'mph') return inMps / 0.44704;
  return inMps;
}
