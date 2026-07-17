import fs from "node:fs";

const required = ["map_id", "seed", "map_type", "biome", "width", "height", "tileset_profile", "theme", "traversal_style", "entrances", "exits", "required_pois", "districts", "boundary_type", "path_style", "constraints", "forbidden_patterns", "event_hooks", "region_painting_rules"];

export function validateIntent(spec) {
  const errors = [];
  for (const field of required) if (!(field in spec)) errors.push(`missing required field: ${field}`);
  if (!Number.isInteger(spec.width) || spec.width < 12) errors.push("width must be an integer >= 12");
  if (!Number.isInteger(spec.height) || spec.height < 10) errors.push("height must be an integer >= 10");
  for (const list of ["entrances", "exits", "required_pois"]) if (!Array.isArray(spec[list]) || !spec[list].length) errors.push(`${list} must be a non-empty array`);
  const ids = [...(spec.entrances || []), ...(spec.exits || []), ...(spec.required_pois || []), ...(spec.optional_pois || [])].map(x => x.id);
  if (new Set(ids).size !== ids.length) errors.push("entrance, exit, and POI ids must be unique");
  return errors;
}

export function parseIntent(path) {
  const spec = JSON.parse(fs.readFileSync(path, "utf8"));
  const errors = validateIntent(spec);
  if (errors.length) throw new Error(`Invalid map intent:\n- ${errors.join("\n- ")}`);
  return spec;
}
