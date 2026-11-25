export function formatINR(amount, includeSymbol = true) {
  const num = Number(amount) || 0;
  const formatted = num.toLocaleString('en-IN', { maximumFractionDigits: 2 });
  return includeSymbol ? `₹${formatted}` : formatted;
}
export function calculateGST(baseRate, gstPercent = 18) {
  const tax = (baseRate * gstPercent) / 100;
  return { base: baseRate, tax, total: baseRate + tax };
}
