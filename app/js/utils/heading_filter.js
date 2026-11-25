export class CompassHeadingSmoother {
  constructor(alpha = 0.25) {
    this.alpha = alpha;
    this.prev = null;
  }
  smooth(current) {
    if (this.prev === null) { this.prev = current; return current; }
    let diff = (current - this.prev + 180) % 360 - 180;
    this.prev = (this.prev + this.alpha * diff + 360) % 360;
    return this.prev;
  }
}
