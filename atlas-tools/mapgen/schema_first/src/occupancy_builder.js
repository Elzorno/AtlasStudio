import { key, clamp } from "./util.js";

const WALKABLE = new Set(["grass", "dirt", "road", "plaza", "sand", "interior_floor", "doorway", "event_anchor", "region_marker"]);

function grid(width, height, fill) { return Array.from({ length: height }, () => Array(width).fill(fill)); }
function paintRect(cells, x0, y0, w, h, value) { for (let y = y0; y < y0 + h; y++) for (let x = x0; x < x0 + w; x++) if (cells[y]?.[x] !== undefined) cells[y][x] = value; }

export function buildOccupancy(spec, topology) {
  const base = spec.map_type === "interior" ? "wall" : spec.biome.includes("desert") ? "sand" : "grass";
  const cells = grid(spec.width, spec.height, base);
  const boundary = spec.map_type === "interior" ? "wall" : ({ forest: "obstacle", cliff: "cliff", water: "water", wall: "wall", interior_wall: "wall", open: base }[spec.boundary_type]);
  for (let x = 0; x < spec.width; x++) { cells[0][x] = boundary; cells[spec.height - 1][x] = boundary; }
  for (let y = 0; y < spec.height; y++) { cells[y][0] = boundary; cells[y][spec.width - 1] = boundary; }
  const pathSemantic = spec.path_style.semantic;
  for (const edge of topology.edges) for (const p of edge.cells) {
    const half = Math.floor(spec.path_style.width / 2);
    paintRect(cells, p.x - half, p.y - half, spec.path_style.width, spec.path_style.width, pathSemantic);
  }
  const anchors = [];
  const footprints = [];
  for (const node of topology.nodes) {
    const { x, y } = node.position;
    if (["entrance", "exit"].includes(node.kind)) { cells[y][x] = "doorway"; anchors.push({ id: node.id, kind: node.kind === "exit" ? "transfer" : "transfer", x, y, target: node.target }); continue; }
    if (node.kind === "building") {
      const [w, h] = node.size; const x0 = clamp(x - Math.floor(w / 2), 1, spec.width - w - 1); const y0 = clamp(y - Math.floor(h / 2), 1, spec.height - h - 1);
      paintRect(cells, x0, y0, w, h, spec.map_type === "interior" ? "interior_floor" : "building_footprint");
      if (spec.map_type !== "interior") { const door = { x: clamp(x, x0, x0 + w - 1), y: y0 + h - 1 }; cells[door.y][door.x] = "doorway"; anchors.push({ id: `${node.id}_door`, kind: "doorway", ...door, poi_id: node.id }); }
      footprints.push({ poi_id: node.id, x: x0, y: y0, width: w, height: h });
    } else {
      paintRect(cells, x - 1, y - 1, 3, 3, node.kind === "plaza" ? "plaza" : pathSemantic);
      cells[y][x] = node.kind === "well" ? "obstacle" : "special_marker";
    }
  }
  for (const hook of spec.event_hooks) {
    const node = topology.nodes.find(n => n.id === hook.at); if (!node) continue;
    let { x, y } = node.position;
    if (!WALKABLE.has(cells[y][x])) { for (const [dx, dy] of [[0,1],[1,0],[-1,0],[0,-1]]) if (WALKABLE.has(cells[y+dy]?.[x+dx])) { x += dx; y += dy; break; } }
    anchors.push({ id: hook.id, kind: hook.kind, x, y, payload: hook.payload || {}, poi_id: hook.at });
  }
  const regions = [];
  for (const rule of spec.region_painting_rules) for (let y = 0; y < spec.height; y++) for (let x = 0; x < spec.width; x++) if (cells[y][x] === rule.semantic) regions.push({ x, y, region_id: rule.region_id, purpose: rule.purpose });
  return { map_id: spec.map_id, width: spec.width, height: spec.height, cells, footprints, event_anchors: anchors, regions, walkable_semantics: [...WALKABLE] };
}

export function occupancyToAscii(occupancy) {
  const glyph = { void:" ", grass:".", dirt:",", road:"=", plaza:"+", water:"~", sand:":", cliff:"^", mountain:"M", building_footprint:"B", doorway:"D", wall:"#", interior_floor:"_", furniture_zone:"f", obstacle:"O", decorative:"*", special_marker:"!", event_anchor:"@", region_marker:"r" };
  return occupancy.cells.map(row => row.map(c => glyph[c] ?? "?").join("")).join("\n") + "\n";
}
