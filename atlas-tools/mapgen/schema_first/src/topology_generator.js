import { rng, sidePosition, manhattanPath, clamp } from "./util.js";

const nodeType = kind => ["plaza", "well", "shrine"].includes(kind) ? kind : ["inn", "shop", "house", "library"].includes(kind) ? "building" : kind;

export function generateTopology(spec) {
  const random = rng(`${spec.seed}:topology`);
  const margin = spec.map_type === "interior" ? 2 : 4;
  const nodes = [];
  for (const port of [...spec.entrances, ...spec.exits]) nodes.push({ id: port.id, kind: spec.entrances.includes(port) ? "entrance" : "exit", position: sidePosition(port.position, spec.width, spec.height), target: port.target });
  const pois = [...spec.required_pois, ...(spec.optional_pois || []).filter(() => random() > 0.35)];
  const focal = pois.find(p => p.focal) || pois[0];
  const center = spec.map_type === "interior"
    ? { x: Math.floor(spec.width / 2), y: Math.floor(spec.height / 2) }
    : { x: Math.floor(spec.width * (0.45 + random() * 0.1)), y: Math.floor(spec.height * (0.42 + random() * 0.12)) };
  const placed = new Map();
  pois.forEach((poi, index) => {
    const size = poi.size || (nodeType(poi.kind) === "building" ? [5, 4] : [3, 3]);
    let position;
    if (poi.id === focal.id) position = center;
    else {
      const angle = (index / Math.max(1, pois.length - 1)) * Math.PI * 2 + random() * 0.4;
      const radiusX = Math.max(5, spec.width * 0.25);
      const radiusY = Math.max(4, spec.height * 0.25);
      position = { x: clamp(Math.round(center.x + Math.cos(angle) * radiusX), margin, spec.width - margin - 1), y: clamp(Math.round(center.y + Math.sin(angle) * radiusY), margin, spec.height - margin - 1) };
    }
    placed.set(poi.id, position);
    nodes.push({ id: poi.id, kind: nodeType(poi.kind), role: poi.kind, position, size, district: poi.district, required: spec.required_pois.includes(poi), focal: poi.id === focal.id });
  });
  const edges = [];
  const focalPosition = placed.get(focal.id);
  for (const port of nodes.filter(n => n.kind === "entrance" || n.kind === "exit")) {
    const p=port.position; const inward={x:p.x===0?2:p.x===spec.width-1?spec.width-3:p.x,y:p.y===0?2:p.y===spec.height-1?spec.height-3:p.y};
    const cells=[...manhattanPath(p,inward,()=>0),...manhattanPath(inward,focalPosition,random).slice(1)];
    edges.push({ from: port.id, to: focal.id, kind: spec.map_type === "interior" ? "corridor" : "main_path", cells });
  }
  for (const poi of nodes.filter(n => !["entrance", "exit"].includes(n.kind) && n.id !== focal.id)) edges.push({ from: focal.id, to: poi.id, kind: poi.kind === "building" ? "access_path" : "side_path", cells: manhattanPath(focalPosition, poi.position, random) });
  if (spec.traversal_style === "loop" && pois.length > 2) edges.push({ from: pois[1].id, to: pois.at(-1).id, kind: "loop_path", cells: manhattanPath(placed.get(pois[1].id), placed.get(pois.at(-1).id), random) });
  const containment = spec.districts.flatMap(d => (d.contains || []).map(child => ({ parent: d.id, child })));
  return { map_id: spec.map_id, seed: spec.seed, traversal_style: spec.traversal_style, focal_node: focal.id, nodes, edges, containment };
}
