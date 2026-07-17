function pickTile(binding, x, y, seed) {
  const variants=binding.variants||[]; if(!variants.length) return binding.tile_id||0;
  let h=Number(seed)||0; for(const c of `${x},${y}`) h=(Math.imul(h^c.charCodeAt(0),16777619))>>>0; return variants[h%variants.length];
}

export function exportMZ(spec, occupancy, profile) {
  const size=occupancy.width*occupancy.height; const data=Array(size*6).fill(0); const regionAt=new Map(occupancy.regions.map(r=>[`${r.x},${r.y}`,r.region_id]));
  for(let y=0;y<occupancy.height;y++) for(let x=0;x<occupancy.width;x++) { const semantic=occupancy.cells[y][x]; const binding=profile.semantic_tiles[semantic]||profile.semantic_tiles.void; const layer=binding.layer??0; data[layer*size+y*occupancy.width+x]=pickTile(binding,x,y,spec.seed); data[5*size+y*occupancy.width+x]=regionAt.get(`${x},${y}`)||0; }
  const events=[null,...occupancy.event_anchors.map((a,index)=>({id:index+1,name:`ANCHOR:${a.id}`,note:`<atlasAnchor:${a.kind}>`,pages:[],x:a.x,y:a.y,meta:{atlas_anchor_id:a.id,kind:a.kind,target:a.target||null,payload:a.payload||{}}}))];
  return { autoplayBgm:false,autoplayBgs:false,battleback1Name:"",battleback2Name:"",bgm:{name:"",pan:0,pitch:100,volume:90},bgs:{name:"",pan:0,pitch:100,volume:90},disableDashing:false,displayName:spec.theme,encounterList:[],encounterStep:30,height:occupancy.height,note:`<atlasMapId:${spec.map_id}><atlasSeed:${spec.seed}>`,parallaxLoopX:false,parallaxLoopY:false,parallaxName:"",parallaxShow:false,parallaxSx:0,parallaxSy:0,scrollType:0,specifyBattleback:false,tilesetId:profile.tilesetId,width:occupancy.width,data,events,_atlas:{schema_version:"0.1",tileset_profile:profile.profile_id,event_placeholders:true,layer_layout:"data[z * width * height + y * width + x], z=0..3 tiles, z=4 shadow, z=5 region"}};
}
