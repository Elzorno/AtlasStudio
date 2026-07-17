import { validateMap } from "./validator.js";

const isWalkable = (occ,x,y) => occ.walkable_semantics.includes(occ.cells[y]?.[x]);

export function repairMap(spec, topology, occupancy, maxPasses=4) {
  const repairs=[];
  for(let pass=0;pass<maxPasses;pass++) {
    const report=validateMap(spec,topology,occupancy); if(report.valid) return {occupancy,repairs,report};
    let changed=false;
    for(const f of report.findings.filter(x=>x.severity==="error")) {
      if(f.code==="doorway_disconnected") { const d=f.evidence; for(const [dx,dy] of [[0,1],[1,0],[-1,0],[0,-1]]) { const x=d.x+dx,y=d.y+dy; if(x>0&&y>0&&x<occupancy.width-1&&y<occupancy.height-1) { occupancy.cells[y][x]=spec.path_style.semantic; repairs.push({pass,code:f.code,action:"carved doorway approach",x,y}); changed=true; break; } } }
      if(f.code==="invalid_event_anchor") { const a=occupancy.event_anchors.find(x=>x.id===f.evidence.id); if(a) { let destination=null; search: for(let radius=1;radius<8;radius++) for(let y=Math.max(1,a.y-radius);y<Math.min(occupancy.height-1,a.y+radius+1);y++) for(let x=Math.max(1,a.x-radius);x<Math.min(occupancy.width-1,a.x+radius+1);x++) if(isWalkable(occupancy,x,y)){destination={x,y};break search;} if(destination){a.x=destination.x;a.y=destination.y;repairs.push({pass,code:f.code,action:"moved anchor",id:a.id,...destination});changed=true;} } }
      if(f.code==="walkable_islands"||f.code==="required_poi_unreachable") { const entrance=occupancy.event_anchors.find(a=>spec.entrances.some(e=>e.id===a.id)); const target=f.code==="required_poi_unreachable"?topology.nodes.find(n=>n.id===f.evidence.poi_id)?.position:topology.nodes.find(n=>n.focal)?.position; if(entrance&&target){let x=entrance.x,y=entrance.y;while(x!==target.x){x+=Math.sign(target.x-x);if(y>0&&y<occupancy.height-1)occupancy.cells[y][x]=spec.path_style.semantic;}while(y!==target.y){y+=Math.sign(target.y-y);if(x>0&&x<occupancy.width-1)occupancy.cells[y][x]=spec.path_style.semantic;}repairs.push({pass,code:f.code,action:"connected component to entrance"});changed=true;} }
      if(f.code==="excess_empty_terrain") { for(let y=2;y<occupancy.height-2;y+=4) for(let x=2;x<occupancy.width-2;x+=5) if(["grass","sand"].includes(occupancy.cells[y][x])) occupancy.cells[y][x]="decorative"; repairs.push({pass,code:f.code,action:"added non-blocking terrain texture markers"}); changed=true; }
    }
    if(!changed) return {occupancy,repairs,report};
  }
  return {occupancy,repairs,report:validateMap(spec,topology,occupancy)};
}
