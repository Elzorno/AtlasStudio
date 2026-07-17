export function hashSeed(value) {
  let h = 2166136261;
  for (const c of String(value)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

export function rng(seed) {
  let state = hashSeed(seed) || 1;
  return () => { state = (state + 0x6d2b79f5) | 0; let t = state; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

export const key = (x, y) => `${x},${y}`;
export const clone = value => JSON.parse(JSON.stringify(value));
export const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));

export function sidePosition(position, width, height) {
  const { side, offset } = position;
  if (side === "north") return { x: clamp(offset, 1, width - 2), y: 0 };
  if (side === "south") return { x: clamp(offset, 1, width - 2), y: height - 1 };
  if (side === "west") return { x: 0, y: clamp(offset, 1, height - 2) };
  return { x: width - 1, y: clamp(offset, 1, height - 2) };
}

export function manhattanPath(a, b, random) {
  const cells = [{ ...a }]; let x = a.x; let y = a.y;
  const horizontalFirst = random() < 0.5;
  const walkX = () => { while (x !== b.x) { x += Math.sign(b.x - x); cells.push({ x, y }); } };
  const walkY = () => { while (y !== b.y) { y += Math.sign(b.y - y); cells.push({ x, y }); } };
  horizontalFirst ? (walkX(), walkY()) : (walkY(), walkX());
  return cells;
}
