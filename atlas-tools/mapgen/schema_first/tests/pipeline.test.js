import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseIntent } from "../src/intent_parser.js";
import { generateTopology } from "../src/topology_generator.js";
import { buildOccupancy } from "../src/occupancy_builder.js";
import { repairMap } from "../src/repair_pass.js";
import { exportMZ } from "../src/mz_exporter.js";
import { compileArtwork } from "../src/artwork_compiler.js";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const profile=JSON.parse(fs.readFileSync(path.join(root,"profiles/sample_tileset_profile.json"),"utf8"));
const examples=["rural_village.json","desert_trade_stop.json","inn_interior.json"];

for(const name of examples)test(`${name} compiles deterministically and validates`,()=>{const spec=parseIntent(path.join(root,"examples",name));const a=generateTopology(spec),b=generateTopology(spec);assert.deepEqual(a,b);const result=repairMap(spec,a,buildOccupancy(spec,a));assert.equal(result.report.valid,true,JSON.stringify(result.report.findings,null,2));const mz=exportMZ(spec,result.occupancy,profile);assert.equal(mz.data.length,spec.width*spec.height*6);assert.equal(mz.events.length,result.occupancy.event_anchors.length+1);assert.equal(mz.data.slice(5*spec.width*spec.height).some(v=>v>0),true);});

test("different seeds change topology",()=>{const spec=parseIntent(path.join(root,"examples/rural_village.json"));const changed={...spec,seed:spec.seed+1};assert.notDeepEqual(generateTopology(spec),generateTopology(changed));});

test("tile IDs come only from profile bindings",()=>{const spec=parseIntent(path.join(root,"examples/rural_village.json"));const topo=generateTopology(spec);const result=repairMap(spec,topo,buildOccupancy(spec,topo));const mz=exportMZ(spec,result.occupancy,profile);const allowed=new Set([0,...Object.values(profile.semantic_tiles).flatMap(b=>[b.tile_id||0,...(b.variants||[])])]);assert.equal(mz.data.slice(0,5*spec.width*spec.height).every(id=>allowed.has(id)),true);});

test("Ashford artwork pass uses real MZ shape and remains a review candidate",()=>{const spec=parseIntent(path.join(root,"examples/rural_village.json"));const topology=generateTopology(spec);const repaired=repairMap(spec,topology,buildOccupancy(spec,topology));const mz=exportMZ(spec,repaired.occupancy,profile);const art=compileArtwork({occupancy:repaired.occupancy,topology,mzBase:mz});assert.equal(art.map.tilesetId,2);assert.equal(art.map.data.length,spec.width*spec.height*6);assert.equal(art.map._atlas.production_promotion,"not_applied");assert.equal(art.report.production_map_modified,false);assert.ok(art.report.placements.some(p=>p.tile_assembly_id==="TASM-ASHFORD-INN-AUTHORED"));assert.deepEqual(art.report.unresolved,[{node_id:"riverside_shrine",reason:"no approved Ashford shrine assembly"}]);});
