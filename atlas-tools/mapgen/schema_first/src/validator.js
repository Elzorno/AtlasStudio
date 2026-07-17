import { key } from "./util.js";

const neighbors = (x, y) => [[x+1,y],[x-1,y],[x,y+1],[x,y-1]];

function flood(occ, starts) {
  const walkable = new Set(occ.walkable_semantics); const seen = new Set(); const queue = [...starts];
  while (queue.length) { const p = queue.shift(); if (!p || seen.has(key(p.x,p.y)) || !walkable.has(occ.cells[p.y]?.[p.x])) continue; seen.add(key(p.x,p.y)); for (const [x,y] of neighbors(p.x,p.y)) queue.push({x,y}); }
  return seen;
}

export function validateMap(spec, topology, occupancy) {
  const findings = []; const error = (code, message, evidence={}) => findings.push({ severity:"error", code, message, evidence }); const warning = (code,message,evidence={}) => findings.push({severity:"warning",code,message,evidence});
  const entrances = occupancy.event_anchors.filter(a => spec.entrances.some(e => e.id === a.id));
  const reachable = flood(occupancy, entrances);
  for (const door of occupancy.event_anchors.filter(a => a.kind === "doorway")) if (!neighbors(door.x,door.y).some(([x,y]) => reachable.has(key(x,y)))) error("doorway_disconnected", `Doorway ${door.id} lacks reachable exterior access.`, door);
  for (const poi of spec.required_pois) { const node = topology.nodes.find(n => n.id === poi.id); const footprint = occupancy.footprints.find(f => f.poi_id === poi.id); const points = footprint ? [{x:footprint.x+Math.floor(footprint.width/2),y:footprint.y+footprint.height-1}, ...neighbors(footprint.x+Math.floor(footprint.width/2),footprint.y+footprint.height-1).map(([x,y])=>({x,y}))] : node ? [node.position,...neighbors(node.position.x,node.position.y).map(([x,y])=>({x,y}))] : []; if (!points.some(p => reachable.has(key(p.x,p.y)))) error("required_poi_unreachable", `Required POI ${poi.id} is unreachable.`, {poi_id:poi.id}); }
  const walkableCells = []; for (let y=0;y<occupancy.height;y++) for(let x=0;x<occupancy.width;x++) if (occupancy.walkable_semantics.includes(occupancy.cells[y][x])) walkableCells.push({x,y});
  const islands = walkableCells.filter(p => !reachable.has(key(p.x,p.y)));
  if (islands.length && !spec.constraints.allow_walkable_islands) error("walkable_islands", `${islands.length} walkable cells are disconnected.`, {count:islands.length});
  const pathSet = new Set(["road","dirt","sand","interior_floor"]); const deadEnds = [];
  for (const p of walkableCells.filter(p=>pathSet.has(occupancy.cells[p.y][p.x]))) { const degree=neighbors(p.x,p.y).filter(([x,y])=>pathSet.has(occupancy.cells[y]?.[x])).length; if(degree<=1 && !occupancy.event_anchors.some(a=>Math.abs(a.x-p.x)+Math.abs(a.y-p.y)<=1)) deadEnds.push(p); }
  if (deadEnds.length > Math.max(4, Math.floor(walkableCells.length*0.03))) warning("excess_dead_ends", "Path network contains unexplained dead ends.", {count:deadEnds.length});
  const allowed = spec.constraints.allowed_building_dimensions || [];
  for (const f of occupancy.footprints) if (allowed.length && !allowed.some(([w,h])=>w===f.width&&h===f.height)) error("invalid_building_dimensions", `Building ${f.poi_id} uses disallowed ${f.width}x${f.height} footprint.`, f);
  const ports=occupancy.event_anchors.filter(a=>[...spec.entrances,...spec.exits].some(p=>p.id===a.id)); const boundaryLeaks=[];
  for(let y=0;y<occupancy.height;y++)for(let x=0;x<occupancy.width;x++)if((x===0||y===0||x===occupancy.width-1||y===occupancy.height-1)&&occupancy.walkable_semantics.includes(occupancy.cells[y][x])&&!ports.some(p=>Math.abs(p.x-x)+Math.abs(p.y-y)<=Math.ceil(spec.path_style.width/2)))boundaryLeaks.push({x,y});
  if (spec.boundary_type !== "open" && boundaryLeaks.length) error("boundary_leak", "Walkable boundary cells exist outside declared ports.",{cells:boundaryLeaks});
  const emptySemantics = new Set(["grass","sand","void"]); const empty = occupancy.cells.flat().filter(c=>emptySemantics.has(c)).length/occupancy.width/occupancy.height;
  if (empty > (spec.constraints.max_empty_ratio ?? 0.65)) error("excess_empty_terrain", `Unstructured terrain ratio ${empty.toFixed(3)} exceeds threshold.`, {ratio:empty});
  for(let y=0;y<occupancy.height;y++) for(let x=0;x<occupancy.width;x++) { const c=occupancy.cells[y][x]; if(c==="water" && neighbors(x,y).some(([nx,ny])=>occupancy.cells[ny]?.[nx]==="interior_floor")) error("invalid_semantic_adjacency","Water directly adjoins interior floor.",{x,y}); if(c==="decorative" && reachable.has(key(x,y))) error("blocking_decoration","Decoration occupies a traversal tile.",{x,y}); }
  for(const r of occupancy.regions) if(!Number.isInteger(r.region_id)||r.region_id<1||r.region_id>255) error("invalid_region","Region ID must be 1..255.",r);
  for(const a of occupancy.event_anchors) if(!occupancy.cells[a.y]?.[a.x] || !occupancy.walkable_semantics.includes(occupancy.cells[a.y][a.x])) error("invalid_event_anchor",`Event anchor ${a.id} is not on a walkable tile.`,a);
  if(spec.map_type==="town") { if(!topology.nodes.some(n=>n.focal&&["plaza","well","shrine","building"].includes(n.kind))) error("town_missing_focal_node","Town lacks a focal node."); if(topology.edges.length<spec.required_pois.length) error("town_weak_hierarchy","Town circulation hierarchy is incomplete."); if(spec.forbidden_patterns.includes("generic_crossroad_three_houses")&&spec.required_pois.filter(p=>p.kind==="house").length===3&&spec.required_pois.length===3) error("forbidden_generic_layout","Town matches forbidden crossroad plus three houses pattern."); }
  if(spec.map_type==="interior" && !spec.event_hooks.length) warning("interior_missing_functional_anchors","Interior has no functional event anchors.");
  return { map_id: spec.map_id, valid: !findings.some(f=>f.severity==="error"), summary: { errors:findings.filter(f=>f.severity==="error").length, warnings:findings.filter(f=>f.severity==="warning").length, reachable_cells:reachable.size, walkable_cells:walkableCells.length }, findings };
}
