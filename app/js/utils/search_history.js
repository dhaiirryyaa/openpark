export class SearchHistoryLRU {
  constructor(limit = 8) { this.limit = limit; this.key = 'openpark_search_history'; }
  push(query) {
    try {
      let list = JSON.parse(localStorage.getItem(this.key) || '[]');
      list = [query, ...list.filter(q => q !== query)].slice(0, this.limit);
      localStorage.setItem(this.key, JSON.stringify(list));
    } catch (e) {}
  }
}
