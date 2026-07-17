#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseIntent } from "./intent_parser.js";
import { generateTopology } from "./topology_generator.js";
import { buildOccupancy, occupancyToAscii } from "./occupancy_builder.js";
import { repairMap } from "./repair_pass.js";
import { exportMZ } from "./mz_exporter.js";
import { renderSvg } from "./preview_renderer.js";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const profile=JSON.parse(fs.readFileSync(path.join(root,"profiles/sample_tileset_profile.json"),"utf8"));
const writeJson=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,null,2)+"\n");

export function generate(specPath, outputRoot=path.join(root,"output/example_map_outputs")) {
  const spec=parseIntent(specPath); const topology=generateTopology(spec); const occupancy=buildOccupancy(spec,topology); const result=repairMap(spec,topology,occupancy); const mz=exportMZ(spec,result.occupancy,profile);
  const out=path.join(outputRoot,spec.map_id); fs.mkdirSync(out,{recursive:true});
  writeJson(path.join(out,"input_spec.json"),spec); writeJson(path.join(out,"topology.json"),topology); writeJson(path.join(out,"semantic_occupancy.json"),result.occupancy); fs.writeFileSync(path.join(out,"semantic_occupancy.txt"),occupancyToAscii(result.occupancy)); writeJson(path.join(out,"MapMZReady.json"),mz); writeJson(path.join(out,"validation_report.json"),{...result.report,repairs:result.repairs}); fs.writeFileSync(path.join(out,"preview.svg"),renderSvg(result.occupancy));
  return {out,report:result.report};
}

const [command,arg]=process.argv.slice(2);
if(command==="generate-all") { let failed=false; for(const name of ["rural_village.json","desert_trade_stop.json","inn_interior.json"]){const r=generate(path.join(root,"examples",name)); console.log(`${r.report.valid?"PASS":"FAIL"} ${r.out}`); failed ||= !r.report.valid;} if(failed)process.exitCode=1; }
else if(command==="generate"&&arg){const r=generate(path.resolve(arg));console.log(`${r.report.valid?"PASS":"FAIL"} ${r.out}`);if(!r.report.valid)process.exitCode=1;}
else if(import.meta.url===`file://${process.argv[1]}`){console.error("Usage: node src/cli.js generate-all | generate <spec.json>");process.exitCode=2;}
