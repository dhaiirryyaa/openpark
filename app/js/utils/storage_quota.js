export async function estimateStorageQuota() {
  if (navigator.storage && navigator.storage.estimate) {
    const est = await navigator.storage.estimate();
    return {
      usageMb: Math.round((est.usage || 0) / (1024 * 1024)),
      quotaMb: Math.round((est.quota || 0) / (1024 * 1024))
    };
  }
  return { usageMb: 0, quotaMb: 0 };
}
