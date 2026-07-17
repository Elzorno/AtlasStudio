import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const FLOOR_TABLE = [
[[2,4],[1,4],[2,3],[1,3]],[[2,0],[1,4],[2,3],[1,3]],[[2,4],[3,0],[2,3],[1,3]],[[2,0],[3,0],[2,3],[1,3]],
[[2,4],[1,4],[2,3],[3,1]],[[2,0],[1,4],[2,3],[3,1]],[[2,4],[3,0],[2,3],[3,1]],[[2,0],[3,0],[2,3],[3,1]],
[[2,4],[1,4],[2,1],[1,3]],[[2,0],[1,4],[2,1],[1,3]],[[2,4],[3,0],[2,1],[1,3]],[[2,0],[3,0],[2,1],[1,3]],
[[2,4],[1,4],[2,1],[3,1]],[[2,0],[1,4],[2,1],[3,1]],[[2,4],[3,0],[2,1],[3,1]],[[2,0],[3,0],[2,1],[3,1]],
[[0,4],[1,4],[0,3],[1,3]],[[0,4],[3,0],[0,3],[1,3]],[[0,4],[1,4],[0,3],[3,1]],[[0,4],[3,0],[0,3],[3,1]],
[[2,2],[1,2],[2,3],[1,3]],[[2,2],[1,2],[2,3],[3,1]],[[2,2],[1,2],[2,1],[1,3]],[[2,2],[1,2],[2,1],[3,1]],
[[2,4],[3,4],[2,3],[3,3]],[[2,4],[3,4],[2,1],[3,3]],[[2,0],[3,4],[2,3],[3,3]],[[2,0],[3,4],[2,1],[3,3]],
[[2,4],[1,4],[2,5],[1,5]],[[2,0],[1,4],[2,5],[1,5]],[[2,4],[3,0],[2,5],[1,5]],[[2,0],[3,0],[2,5],[1,5]],
[[0,4],[3,4],[0,3],[3,3]],[[2,2],[1,2],[2,5],[1,5]],[[0,2],[1,2],[0,3],[1,3]],[[0,2],[1,2],[0,3],[3,1]],
[[2,2],[3,2],[2,3],[3,3]],[[2,2],[3,2],[2,1],[3,3]],[[2,4],[3,4],[2,5],[3,5]],[[2,0],[3,4],[2,5],[3,5]],
[[0,4],[1,4],[0,5],[1,5]],[[0,4],[3,0],[0,5],[1,5]],[[0,2],[3,2],[0,3],[3,1]],[[0,2],[1,2],[0,5],[1,5]],
[[0,4],[3,4],[0,5],[3,5]],[[2,2],[3,2],[2,5],[3,5]],[[0,2],[3,2],[0,5],[3,5]],[[0,0],[1,0],[0,1],[1,1]]
];

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const load=p=>JSON.parse(fs.readFileSync(p,"utf8"));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const makeAutotile=(kind,shape)=>2048+kind*48+shape;
const isPath=s=>["road","plaza","doorway","special_marker"].includes(s);

function autotileShape(cells,x,y,member){
  const same=(dx,dy)=>member(cells[y+dy]?.[x+dx]); const n=same(0,-1),s=same(0,1),w=same(-1,0),e=same(1,0);
  const desired=[
    n&&w?(same(-1,-1)?[2,4]:[2,2]):n?[0,4]:w?[2,0]:[0,0],
    n&&e?(same(1,-1)?[1,4]:[1,2]):n?[3,4]:e?[1,0]:[3,0],
    s&&w?(same(-1,1)?[2,3]:[2,1]):s?[0,3]:w?[2,5]:[0,5],
    s&&e?(same(1,1)?[1,3]:[3,1]):s?[3,3]:e?[1,5]:[3,5]
  ];
  const shape=FLOOR_TABLE.findIndex(entry=>equal(entry,desired));
  if(shape>=0)return shape;
  return FLOOR_TABLE.map((entry,index)=>({index,score:entry.reduce((sum,q,i)=>sum+(equal(q,desired[i])?0:1),0)})).sort((a,b)=>a.score-b.score||a.index-b.index)[0].index;
}

function stampAssembly(data,width,height,assembly,x0,y0){
  for(const cell of assembly.layered_cells) for(const layer of cell.layers){const x=x0+cell.x,y=y0+cell.y,z=layer.layer;if(x>=0&&y>=0&&x<width&&y<height&&z>=0&&z<4)data[z*width*height+y*width+x]=layer.tile_id;}
}

function assemblyKey(node){if(node.role==="inn")return "inn";if(node.role==="shop")return "shop";if(node.id==="elder_house")return "elder_house";if(node.role==="house")return "house";return null;}

export function compileArtwork({occupancy,topology,mzBase,profilePath=path.join(root,"profiles/ashford_artwork_profile.json")}){
  const profile=load(profilePath),width=occupancy.width,height=occupancy.height,size=width*height,data=Array(size*6).fill(0),placements=[],unresolved=[];
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){
    const semantic=occupancy.cells[y][x],binding=profile.terrain[semantic]||profile.terrain.grass;
    const membership=binding===profile.terrain.road?c=>isPath(c):c=>!isPath(c);
    data[y*width+x]=makeAutotile(binding.autotile_kind,autotileShape(occupancy.cells,x,y,membership));
    const region=occupancy.regions.find(r=>r.x===x&&r.y===y); if(region)data[5*size+y*width+x]=region.region_id;
  }
  for(const node of topology.nodes.filter(n=>n.kind==="building")){
    const key=assemblyKey(node); if(!key||!profile.assemblies[key]){unresolved.push({node_id:node.id,reason:"no approved assembly binding"});continue;}
    const assemblyPath=path.resolve(path.dirname(profilePath),profile.assemblies[key]),assembly=load(assemblyPath),anchor=assembly.anchors.find(a=>a.role==="entry")||assembly.anchors[0],door=occupancy.event_anchors.find(a=>a.poi_id===node.id&&a.kind==="doorway");
    const x0=door?door.x-anchor.x:node.position.x-Math.floor(assembly.dimensions.width/2),y0=door?door.y-anchor.y:node.position.y-Math.floor(assembly.dimensions.height/2);
    if(x0<0||y0<0||x0+assembly.dimensions.width>width||y0+assembly.dimensions.height>height){unresolved.push({node_id:node.id,reason:"approved assembly exceeds map bounds"});continue;}
    stampAssembly(data,width,height,assembly,x0,y0);placements.push({node_id:node.id,tile_assembly_id:assembly.tile_assembly_id,x:x0,y:y0,width:assembly.dimensions.width,height:assembly.dimensions.height,approval:"human_approved"});
  }
  const tree=load(path.resolve(path.dirname(profilePath),profile.assemblies.tree)); let treeCount=0;
  const occupied=(x,y,w,h)=>placements.some(p=>p.x<x+w&&p.x+p.width>x&&p.y<y+h&&p.y+p.height>y);
  for(let y=2;y<height-2&&treeCount<16;y+=3)for(let x=2;x<width-2&&treeCount<16;x+=4){const safe=[occupancy.cells[y][x],occupancy.cells[y][x+1],occupancy.cells[y+1][x],occupancy.cells[y+1][x+1]].every(c=>["grass","decorative","obstacle"].includes(c));if(safe&&!occupied(x,y,2,2)&&((x*31+y*17+Number(topology.seed||0))%5<2)){stampAssembly(data,width,height,tree,x,y);placements.push({node_id:`decorative_tree_${treeCount+1}`,tile_assembly_id:tree.tile_assembly_id,x,y,width:2,height:2,approval:"verified_reusable"});treeCount++;}}
  for(const node of topology.nodes.filter(n=>["well","shrine"].includes(n.kind))) if(node.kind==="well")placements.push({node_id:node.id,preview_overlay:"well",x:node.position.x-1,y:node.position.y-1,width:2,height:2,approval:"human_approved",map_serialization:"pending combined tileset slot"});else unresolved.push({node_id:node.id,reason:"no approved Ashford shrine assembly"});
  const result={...mzBase,tilesetId:profile.tilesetId,data,_atlas:{...mzBase._atlas,artwork_profile:profile.profile_id,artwork_state:"review_candidate",approved_assembly_placements:placements,unresolved_artwork:unresolved,production_promotion:"not_applied"}};
  return {map:result,report:{map_id:occupancy.map_id,state:"review_candidate",tileset_id:profile.tilesetId,placements,unresolved,production_map_modified:false}};
}

export function compileArtworkFiles(exampleDir){const occupancy=load(path.join(exampleDir,"semantic_occupancy.json")),topology=load(path.join(exampleDir,"topology.json")),mzBase=load(path.join(exampleDir,"MapMZReady.json")),result=compileArtwork({occupancy,topology,mzBase});fs.writeFileSync(path.join(exampleDir,"MapArtworkCandidate.json"),JSON.stringify(result.map,null,2)+"\n");fs.writeFileSync(path.join(exampleDir,"artwork_report.json"),JSON.stringify(result.report,null,2)+"\n");return result;}

if(import.meta.url===`file://${process.argv[1]}`){const exampleDir=path.resolve(process.argv[2]||path.join(root,"output/example_map_outputs/EX-RURAL-VILLAGE-001"));const result=compileArtworkFiles(exampleDir);console.log(`Artwork candidate: ${exampleDir} (${result.report.placements.length} placements, ${result.report.unresolved.length} unresolved)`);}
