export class TelemetryEventQueue {
  constructor(batchSize = 10, flushIntervalMs = 5000) {
    this.batchSize = batchSize;
    this.queue = [];
  }
  push(event, onFlush) {
    this.queue.push({ ...event, timestamp: Date.now() });
    if (this.queue.length >= this.batchSize) {
      this.flush(onFlush);
    }
  }
  flush(onFlush) {
    if (this.queue.length === 0) return;
    const batch = [...this.queue];
    this.queue = [];
    if (onFlush) onFlush(batch);
  }
}
