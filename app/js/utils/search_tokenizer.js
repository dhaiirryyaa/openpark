export function tokenizeSearchQuery(query) {
  return (query || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .split(/[\s,-]+/).filter(Boolean);
}
