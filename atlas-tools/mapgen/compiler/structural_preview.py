"""ASCII and SVG previews for engine-neutral generated MapPlans."""

from __future__ import annotations

import html

from map_plan import MapPlan


def _zones(plan: MapPlan) -> list[dict]:
    return [item for item in plan.to_dict().get("terrain", []) if item.get("area", {}).get("shape") == "rect"]


def render_ascii(plan: MapPlan) -> str:
    payload = plan.to_dict()
    width, height = payload["dimensions"]["width"], payload["dimensions"]["height"]
    grid = [["." for _ in range(width)] for _ in range(height)]
    legend = []
    symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for index, zone in enumerate(_zones(plan)):
        symbol = symbols[index % len(symbols)]
        area = zone["area"]
        for y in range(area["y"], area["y"] + area["h"]):
            for x in range(area["x"], area["x"] + area["w"]):
                grid[y][x] = symbol
        legend.append(f"{symbol}={zone['terrain_type']}")
    return "\n".join("".join(row) for row in grid) + "\n\n" + "\n".join(legend) + "\n"


def render_svg(plan: MapPlan, scale: int = 32) -> str:
    payload = plan.to_dict()
    width, height = payload["dimensions"]["width"], payload["dimensions"]["height"]
    colors = ["#d9a441", "#568f5b", "#6086c4", "#a56ca5", "#c96c4b", "#65a6a6", "#9b8755"]
    elements = [f'<rect width="{width * scale}" height="{height * scale}" fill="#151922"/>']
    for index, zone in enumerate(_zones(plan)):
        area = zone["area"]
        x, y, w, h = area["x"] * scale, area["y"] * scale, area["w"] * scale, area["h"] * scale
        label = html.escape(zone["terrain_type"])
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{colors[index % len(colors)]}" stroke="#f5ead7" stroke-width="2"/>')
        elements.append(f'<text x="{x + 4}" y="{y + 16}" fill="#111" font-family="monospace" font-size="11">{label}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * scale}" height="{height * scale}" viewBox="0 0 {width * scale} {height * scale}">' + "".join(elements) + "</svg>\n"
