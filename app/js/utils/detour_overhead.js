export function calculateDetourOverhead(directDistM, detourDistM) {
  if (directDistM <= 0) return 0;
  const extra = Math.max(0, detourDistM - directDistM);
  return Math.round((extra / directDistM) * 100);
}
