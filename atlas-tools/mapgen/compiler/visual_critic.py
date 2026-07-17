"""WO-0075: automated render-based visual critic for generated maps.

Automates the ``AVCP-HOM-ASH-001`` aesthetic constraints that
``quality_gate.py``'s ``NOT_YET_AUTOMATABLE`` list defers to a human --
first-camera salience, path rhythm, decoration density, colour/material
identity -- by scoring a *rendered map image* against the Academy's Dragon
Quest town-grammar checklist (`academy/case-studies/dragon-quest-town-grammar-001.md`)
and the classic-JRPG Review Gate (`academy/knowledge/classic-jrpg-feel.md`),
reference-anchored to the accepted maps (Map017, which scored 8/8, and the
accepted production Map001).

Design contract (mirrors WO-0072's gate discipline):

* **Advisory only.** The critic may return ``flag`` or ``reject``; it can
  never record acceptance. Only Chris via
  ``quality_gate.apply_human_decision(decided_by="Chris")`` accepts.
* **Model-agnostic.** A :class:`VisualCriticBackend` produces the actual
  per-criterion judgement from the image(s). Backends provided:
  :class:`RecordedCritiqueBackend` (plays back a critique authored
  out-of-band -- e.g. by the Claude/Opus frontier VLM during the agent
  session, or a saved JSON -- used for the calibration and for deterministic
  tests), :class:`OllamaVisionBackend` (local, unattended; needs a pulled
  vision model), and :class:`AnthropicVisionBackend` (frontier escalation;
  needs ``ANTHROPIC_API_KEY``). The last two use only the standard library
  (``urllib``) so the module has no third-party dependency.
* **Untrusted until calibrated.** A backend must pass the three-render
  calibration (Map017 = pass, Map001 = pass, the WO-0073 Ashford candidate =
  reject, with the failure citing enclosure / path / material) before it is
  allowed to gate. :func:`run_calibration` is the go/no-go check;
  ``visual_critic.py --calibrate`` exits non-zero if it fails.

This module deliberately imports nothing from ``quality_gate`` -- the gate
imports *this* module (one-way) and adapts a :class:`VisualCritique` into its
own ``AuditResult`` vocabulary, so there is no import cycle and the critic
stays reusable by the overworld/long-tail side as well.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol


# --------------------------------------------------------------------------
# Rubric
# --------------------------------------------------------------------------


VERDICTS = ("pass", "partial", "fail")


@dataclass(frozen=True)
class Criterion:
    """One falsifiable visual criterion.

    ``core`` criteria are load-bearing: a single ``fail`` on any of them
    rejects the map (these are the qualities whose absence produced every
    "mechanical / no soul" rejection). Non-core criteria contribute to a
    softer ``flag``. ``avcp_refs`` records which ``AVCP-HOM-ASH-001``
    constraints -- the ones ``quality_gate.NOT_YET_AUTOMATABLE`` defers -- a
    criterion covers, so the gate can report what this critic now screens.
    """

    id: str
    title: str
    description: str
    core: bool
    avcp_refs: tuple[str, ...] = ()


# The rubric maps the Academy's own two checklists onto one list. Between
# them the core+non-core set covers all ten AVCP ids currently parked in
# quality_gate.NOT_YET_AUTOMATABLE.
RUBRIC: tuple[Criterion, ...] = (
    Criterion(
        "ENCLOSURE-001",
        "Bounded perimeter",
        "The settlement is enclosed by a wall, moat, dense tree-line, or an "
        "equally strong readable boundary (built or natural) -- not sitting in "
        "open, unbounded field.",
        core=True,
        avcp_refs=("ASH-DENSITY-001",),
    ),
    Criterion(
        "PATH-ORGANIC-001",
        "Organic branching paths",
        "Paths branch and curve around buildings with varied width, rather "
        "than forming one uniform straight geometric spine or a rigid cross.",
        core=True,
        avcp_refs=("ASH-PATH-002",),
    ),
    Criterion(
        "PATH-RHYTHM-001",
        "Path rhythm and door alignment",
        "Paths have compression/release and bends, and meet building fronts at "
        "their doors rather than dead-ending against walls.",
        core=True,
        avcp_refs=("ASH-PATH-003", "ASH-RHYTHM-001"),
    ),
    Criterion(
        "BUILDING-VARIETY-001",
        "Varied building massing",
        "Building footprints differ in massing (or are uniform but clearly "
        "icon-differentiated) rather than one repeated shell distinguished only "
        "by a sign.",
        core=True,
        avcp_refs=("ASH-BUILD-002",),
    ),
    Criterion(
        "MATERIAL-IDENTITY-001",
        "Distinct material identity",
        "The place has its own build-material / palette identity with real "
        "contrast, not a single re-tinted material over flat ground.",
        core=True,
        avcp_refs=("ASH-MATERIAL-001", "ASH-MATERIAL-002"),
    ),
    Criterion(
        "DECOR-DENSITY-001",
        "Decoration density",
        "Decoration scatters through the walkable interior and clusters at "
        "walls, path edges, and pockets -- not a thin uniform sprinkle or a "
        "near-empty field.",
        core=True,
        avcp_refs=("ASH-DENSITY-001",),
    ),
    Criterion(
        "DOMINANT-LANDMARK-001",
        "Dominant landmark",
        "One nameable landmark clearly dominates the first read; the eye has "
        "something specific to move toward.",
        core=True,
        avcp_refs=("ASH-FIRST-002",),
    ),
    Criterion(
        "FIRST-VIEW-001",
        "Readable first view",
        "The first view immediately says what kind of place this is and "
        "promises something beyond the current screen.",
        core=False,
        avcp_refs=("ASH-FIRST-001",),
    ),
    Criterion(
        "REWARD-CLUSTER-001",
        "Dressed reward clusters",
        "Reward / curiosity objects read as dressed clusters, not lone "
        "unstyled markers in empty space.",
        core=False,
    ),
    Criterion(
        "WATER-LANDMARK-001",
        "Water or organic plaza",
        "At least one landmark uses water (pond, fountain, river) or the open "
        "square is organically shaped rather than a hard rectangle.",
        core=False,
    ),
    Criterion(
        "VOCAB-LIMITED-001",
        "Limited coherent vocabulary",
        "A limited, consistent material vocabulary is reused throughout rather "
        "than each area introducing unrelated materials.",
        core=False,
        avcp_refs=("ASH-VOCAB-001",),
    ),
    Criterion(
        "MEMORABLE-IDENTITY-001",
        "Memorable identity",
        "The map has a statable, memorable player-facing identity.",
        core=False,
    ),
)

RUBRIC_BY_ID: dict[str, Criterion] = {c.id: c for c in RUBRIC}

# Every AVCP id this critic now screens (the subset of
# quality_gate.NOT_YET_AUTOMATABLE the rubric covers).
COVERED_AVCP_REFS: tuple[str, ...] = tuple(
    sorted({ref for c in RUBRIC for ref in c.avcp_refs})
)

# Overall becomes "flag" (rather than "pass") once this many criteria are
# only partial, even with no outright failure.
PARTIAL_FLAG_THRESHOLD = 3


# --------------------------------------------------------------------------
# Critique data model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CriterionResult:
    criterion_id: str
    verdict: str
    reason: str

    def __post_init__(self) -> None:
        if self.verdict not in VERDICTS:
            raise ValueError(f"unknown verdict {self.verdict!r} (expected one of {VERDICTS})")

    @property
    def criterion(self) -> Criterion | None:
        return RUBRIC_BY_ID.get(self.criterion_id)

    @property
    def core(self) -> bool:
        crit = self.criterion
        return bool(crit and crit.core)

    def to_dict(self) -> dict[str, Any]:
        crit = self.criterion
        return {
            "criterion_id": self.criterion_id,
            "title": crit.title if crit else self.criterion_id,
            "verdict": self.verdict,
            "reason": self.reason,
            "core": self.core,
            "avcp_refs": list(crit.avcp_refs) if crit else [],
        }


@dataclass(frozen=True)
class VisualCritique:
    """A backend's judgement of one rendered map against the rubric."""

    label: str
    image_ref: str
    backend: str
    model: str
    results: tuple[CriterionResult, ...]

    @property
    def failed(self) -> tuple[CriterionResult, ...]:
        return tuple(r for r in self.results if r.verdict == "fail")

    @property
    def core_failures(self) -> tuple[CriterionResult, ...]:
        return tuple(r for r in self.results if r.verdict == "fail" and r.core)

    @property
    def partials(self) -> tuple[CriterionResult, ...]:
        return tuple(r for r in self.results if r.verdict == "partial")

    @property
    def overall(self) -> str:
        """``reject`` on any core failure; ``flag`` on a non-core failure or
        an accumulation of partials; otherwise ``pass``. The critic never
        returns ``accept`` -- a clean map is only ever a candidate for a
        human's decision."""

        if self.core_failures:
            return "reject"
        if self.failed or len(self.partials) >= PARTIAL_FLAG_THRESHOLD:
            return "flag"
        return "pass"

    def cited_core_failure_ids(self) -> set[str]:
        return {r.criterion_id for r in self.core_failures}

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "0.1",
            "label": self.label,
            "image_ref": self.image_ref,
            "backend": self.backend,
            "model": self.model,
            "overall": self.overall,
            "results": [r.to_dict() for r in self.results],
            "covered_avcp_refs": list(COVERED_AVCP_REFS),
        }

    @classmethod
    def from_verdicts(
        cls,
        *,
        label: str,
        image_ref: str,
        backend: str,
        model: str,
        verdicts: Mapping[str, tuple[str, str]],
        fill_missing: str = "partial",
    ) -> "VisualCritique":
        """Build a critique from a ``{criterion_id: (verdict, reason)}`` map.

        Any rubric criterion the backend did not address is filled with
        ``fill_missing`` (defaults to ``partial`` so an omission surfaces as a
        soft concern rather than silently passing). Ids outside the rubric are
        ignored.
        """

        results: list[CriterionResult] = []
        for crit in RUBRIC:
            if crit.id in verdicts:
                verdict, reason = verdicts[crit.id]
                results.append(CriterionResult(crit.id, verdict, reason))
            else:
                results.append(
                    CriterionResult(crit.id, fill_missing, "backend did not address this criterion")
                )
        return cls(label=label, image_ref=image_ref, backend=backend, model=model, results=tuple(results))


def write_critique_evidence(critique: VisualCritique, output_path: Path) -> dict[str, Any]:
    """Persist a critique as JSON evidence, mirroring
    ``quality_gate.record_gate_evidence``'s convention (indent=2, sorted,
    trailing newline). Advisory only: the evidence carries no acceptance."""

    payload = critique.to_dict()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


# --------------------------------------------------------------------------
# Backends
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class CritiqueRequest:
    label: str
    candidate_image: str
    anchor_images: tuple[str, ...] = ()
    map_name: str | None = None


class VisualCriticBackend(Protocol):
    name: str
    model: str

    def critique(self, request: CritiqueRequest) -> VisualCritique: ...


class RecordedCritiqueBackend:
    """Replays critiques authored out-of-band (keyed by request label).

    Used for (a) the frontier-VLM calibration -- the Claude/Opus judgements
    of the three reference renders, formed by viewing the images during the
    agent session, are recorded here and checked against the independently
    specified expected outcomes -- and (b) deterministic unit tests. Raises on
    an unknown label so it can never silently "pass" a map nobody reviewed.
    """

    def __init__(self, critiques: Mapping[str, VisualCritique], *, model: str = "claude-opus-4-8"):
        self.name = "recorded"
        self.model = model
        self._critiques = dict(critiques)

    def critique(self, request: CritiqueRequest) -> VisualCritique:
        if request.label not in self._critiques:
            raise KeyError(
                f"no recorded critique for label {request.label!r}; recorded backend refuses to invent one"
            )
        return self._critiques[request.label]


def build_prompt(request: CritiqueRequest) -> str:
    """The reference-anchored instruction shared by the live backends."""

    lines = [
        "You are a classic-JRPG (Dragon Quest / Final Fantasy era) map-art critic.",
        "You are shown a CANDIDATE rendered map and, for calibration, one or more",
        "ACCEPTED reference maps that are known to read as hand-crafted places.",
        "Judge ONLY the CANDIDATE, using the references as the bar for 'hand-crafted'.",
        "",
        "For EACH criterion below, return a verdict of exactly 'pass', 'partial',",
        "or 'fail', plus ONE short, falsifiable sentence of evidence (name what you",
        "see, never 'does not feel retro enough').",
        "",
        "Criteria:",
    ]
    for crit in RUBRIC:
        tag = "CORE" if crit.core else "soft"
        lines.append(f"- {crit.id} [{tag}] {crit.title}: {crit.description}")
    lines += [
        "",
        "Respond with ONLY a JSON object, no prose, of the form:",
        '{"results": [{"criterion_id": "ENCLOSURE-001", "verdict": "fail",',
        '  "reason": "..."}, ...]}',
    ]
    if request.map_name:
        lines.append(f"\nThe candidate map is named: {request.map_name}.")
    return "\n".join(lines)


def _extract_json(text: str) -> dict[str, Any]:
    """Best-effort JSON extraction from a model reply that may wrap the object
    in prose or code fences."""

    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1] if text.count("```") >= 2 else text.strip("`")
        text = text[4:] if text.lower().startswith("json") else text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


def _critique_from_model_json(
    payload: Mapping[str, Any],
    *,
    request: CritiqueRequest,
    backend: str,
    model: str,
) -> VisualCritique:
    verdicts: dict[str, tuple[str, str]] = {}
    for row in payload.get("results", []):
        cid = str(row.get("criterion_id", "")).strip()
        verdict = str(row.get("verdict", "")).strip().lower()
        reason = str(row.get("reason", "")).strip()
        if cid in RUBRIC_BY_ID and verdict in VERDICTS:
            verdicts[cid] = (verdict, reason or "(no reason given)")
    return VisualCritique.from_verdicts(
        label=request.label,
        image_ref=request.candidate_image,
        backend=backend,
        model=model,
        verdicts=verdicts,
    )


def _b64_image(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


class OllamaVisionBackend:
    """Local, unattended backend. Needs a *vision* model pulled into Ollama
    (e.g. ``ollama pull llama3.2-vision`` or ``llava``); the text-only models
    already present cannot see the render."""

    def __init__(
        self,
        *,
        model: str = "llama3.2-vision",
        host: str = "http://localhost:11434",
        timeout: float = 180.0,
    ):
        self.name = "ollama"
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def critique(self, request: CritiqueRequest) -> VisualCritique:
        raw = self._chat(request)
        payload = _extract_json(raw)
        return _critique_from_model_json(payload, request=request, backend=self.name, model=self.model)

    def _chat(self, request: CritiqueRequest) -> str:
        # Anchors first, candidate last, so "the CANDIDATE" is the final image.
        images = [_b64_image(p) for p in (*request.anchor_images, request.candidate_image)]
        body = json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": build_prompt(request), "images": images}],
                "stream": False,
                "format": "json",
                "options": {"temperature": 0},
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/chat", data=body, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["message"]["content"]


class AnthropicVisionBackend:
    """Frontier escalation backend via the Anthropic Messages API (used when a
    local model fails calibration or for high-stakes checks). Standard-library
    HTTP only, so it needs no ``anthropic`` package -- just an
    ``ANTHROPIC_API_KEY``."""

    def __init__(
        self,
        *,
        model: str = "claude-opus-4-8",
        api_key: str | None = None,
        timeout: float = 180.0,
    ):
        self.name = "anthropic"
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.timeout = timeout

    def critique(self, request: CritiqueRequest) -> VisualCritique:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set; cannot run the Anthropic vision backend")
        raw = self._message(request)
        payload = _extract_json(raw)
        return _critique_from_model_json(payload, request=request, backend=self.name, model=self.model)

    def _image_block(self, path: str) -> dict[str, Any]:
        media = "image/png" if path.lower().endswith(".png") else "image/jpeg"
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media, "data": _b64_image(path)},
        }

    def _message(self, request: CritiqueRequest) -> str:
        content: list[dict[str, Any]] = [{"type": "text", "text": build_prompt(request)}]
        for path in request.anchor_images:
            content.append({"type": "text", "text": "ACCEPTED reference map:"})
            content.append(self._image_block(path))
        content.append({"type": "text", "text": "CANDIDATE map to judge:"})
        content.append(self._image_block(request.candidate_image))
        body = json.dumps(
            {"model": self.model, "max_tokens": 1500, "messages": [{"role": "user", "content": content}]}
        ).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "content-type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return "".join(block.get("text", "") for block in data.get("content", []))


# --------------------------------------------------------------------------
# Calibration (the go/no-go)
# --------------------------------------------------------------------------

# Repo-relative render paths (from the sibling-repo workspace root).
WORKSPACE = Path(__file__).resolve().parents[4]
_R = "rpgmakerLSP/reports/atlas-import"

CALIBRATION_IMAGES: dict[str, str] = {
    "map017": f"{_R}/academy-inspection-002-map017-render.png",
    "map001": f"{_R}/wo-0036-map001-render.png",
    "wo0073_candidate": f"{_R}/ashford-mapvision-v3/ashford-mapvision-candidate-render.png",
}

# Independently specified expected outcomes -- authored from the map history
# (Map017 scored 8/8; Map001 is accepted production; the WO-0073 candidate was
# human-rejected as mechanical, citing missing enclosure, straight paths that
# do not meet doors, and no material variety). A backend must reproduce these
# to be trusted.
CALIBRATION_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "map017": {"overall": {"pass"}},
    "map001": {"overall": {"pass"}},
    "wo0073_candidate": {
        "overall": {"reject"},
        "must_cite_core_failures": {"ENCLOSURE-001", "PATH-ORGANIC-001", "MATERIAL-IDENTITY-001"},
    },
}


@dataclass(frozen=True)
class CalibrationRow:
    label: str
    expected: str
    actual: str
    ok: bool
    note: str


@dataclass(frozen=True)
class CalibrationResult:
    backend: str
    model: str
    rows: tuple[CalibrationRow, ...]

    @property
    def passed(self) -> bool:
        return all(row.ok for row in self.rows)

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "model": self.model,
            "passed": self.passed,
            "rows": [row.__dict__ for row in self.rows],
        }


def run_calibration(
    backend: VisualCriticBackend,
    *,
    anchor_labels: Iterable[str] = ("map017", "map001"),
    collect: dict[str, VisualCritique] | None = None,
) -> CalibrationResult:
    """Confirm ``backend`` reproduces the pass/pass/reject discrimination and
    the required cited failures on the WO-0073 candidate. If ``collect`` is
    provided it is populated with each produced critique (for evidence)."""

    def _abs(label: str) -> str:
        return str(WORKSPACE / CALIBRATION_IMAGES[label])

    anchor_labels = tuple(anchor_labels)
    rows: list[CalibrationRow] = []
    for label, expectation in CALIBRATION_EXPECTATIONS.items():
        request = CritiqueRequest(
            label=label,
            candidate_image=_abs(label),
            anchor_images=tuple(_abs(lbl) for lbl in anchor_labels if lbl != label),
            map_name=label,
        )
        critique = backend.critique(request)
        if collect is not None:
            collect[label] = critique
        actual = critique.overall
        ok = actual in expectation["overall"]
        note = ""
        required = expectation.get("must_cite_core_failures")
        if required:
            cited = critique.cited_core_failure_ids()
            missing = set(required) - cited
            if missing:
                ok = False
                note = f"did not cite required core failures: {sorted(missing)}"
            else:
                note = f"cited required core failures: {sorted(required)}"
        rows.append(
            CalibrationRow(
                label=label,
                expected="|".join(sorted(expectation["overall"])),
                actual=actual,
                ok=ok,
                note=note,
            )
        )
    return CalibrationResult(backend=backend.name, model=backend.model, rows=tuple(rows))


# --------------------------------------------------------------------------
# Frontier-VLM (Claude/Opus, agent session) recorded calibration critiques
# --------------------------------------------------------------------------
#
# These are the genuine per-criterion judgements formed by viewing the three
# renders during the WO-0075 session (2026-07-16). They are recorded verbatim
# so `--calibrate` and the tests are reproducible; provenance is the
# claude-opus-4-8 frontier VLM via the agent session, NOT a live API call.

_MAP017 = {
    "ENCLOSURE-001": ("pass", "A river down the west edge plus a continuous dense tree-line on the north and east bound the village; it is clearly not open field."),
    "PATH-ORGANIC-001": ("pass", "Stone paths wind and branch at irregular angles around the buildings and farm, with varied width and no single straight spine."),
    "PATH-RHYTHM-001": ("pass", "The narrow bridge compresses movement then releases into the statue plaza, and paths meet each building at its door."),
    "BUILDING-VARIETY-001": ("pass", "Six-plus buildings of visibly different massing and roof pitch, several sharing walls into clusters rather than one repeated shell."),
    "MATERIAL-IDENTITY-001": ("pass", "A coherent warm-timber building set reads against grass, stone path, and water as one place, distinct from the ground."),
    "DECOR-DENSITY-001": ("pass", "Barrels, crates, a fenced crop plot, lily pads, stumps and ivy scatter through the interior and cluster at path edges and water."),
    "DOMINANT-LANDMARK-001": ("pass", "The pedestal statue at the central crossroads is the unambiguous first-read focal point."),
    "FIRST-VIEW-001": ("pass", "It instantly reads as a riverside farming village with a clear place to move toward."),
    "REWARD-CLUSTER-001": ("pass", "Barrels and crates are grouped and dressed beside buildings, not lone unstyled markers."),
    "WATER-LANDMARK-001": ("pass", "The river-and-bridge crossing plus a lily-pad pond act as a water landmark and organic plaza."),
    "VOCAB-LIMITED-001": ("pass", "A small reused material set (grass, dirt, stone, water, timber) runs throughout with no unrelated materials."),
    "MEMORABLE-IDENTITY-001": ("pass", "'The farming village with the river, the bridge, and the statue' is immediately statable."),
}

_MAP001 = {
    "ENCLOSURE-001": ("pass", "A continuous dense tree-line rings the whole settlement; it is a clearly bounded place, not open field."),
    "PATH-ORGANIC-001": ("pass", "Stone paths branch organically: a main spine splits into irregular offshoots that wrap around the buildings."),
    "PATH-RHYTHM-001": ("partial", "Paths branch well and reach the building fronts, but the central paved area is a large open expanse so compression/release is softer than Map017."),
    "BUILDING-VARIETY-001": ("pass", "Buildings use genuinely different materials (pink, yellow-stone, brown, tan) with some sharing walls into a cluster."),
    "MATERIAL-IDENTITY-001": ("pass", "Several distinct build materials give a strong varied settlement palette rather than a re-tinted ground."),
    "DECOR-DENSITY-001": ("pass", "A fenced farm plot with crops, wells, lampposts, barrels and NPCs are distributed through the interior and clustered in pockets."),
    "DOMINANT-LANDMARK-001": ("pass", "The central well-and-lamppost plaza anchors the first read."),
    "FIRST-VIEW-001": ("pass", "It reads immediately as an enclosed village with a civic centre."),
    "REWARD-CLUSTER-001": ("pass", "Searchable barrels and crates are grouped beside buildings rather than isolated."),
    "WATER-LANDMARK-001": ("partial", "A well provides a landmark but there is no open water feature, so this reads softer than Map017's river."),
    "VOCAB-LIMITED-001": ("pass", "Grass, stone path, timber and stone-wall vocabulary is reused coherently across the map."),
    "MEMORABLE-IDENTITY-001": ("pass", "The walled village with the central plaza and farm is easy to recall and state."),
}

_WO0073 = {
    "ENCLOSURE-001": ("fail", "There is no perimeter at all; four buildings float in an unbounded flat green field -- the exact open-field failure the grammar forbids."),
    "PATH-ORGANIC-001": ("fail", "Paths form a single rigid plus-shaped cross of uniform width joining building centres, with no branching or curvature."),
    "PATH-RHYTHM-001": ("fail", "There is no compression/release and no bends, and the path arms dead-end near building walls instead of meeting the doors."),
    "BUILDING-VARIETY-001": ("fail", "All four buildings are the same brown shell at near-identical footprint, differentiated only by a sign -- one repeated shell."),
    "MATERIAL-IDENTITY-001": ("fail", "A single brown timber material is used for every structure over flat green; there is no material identity or contrast."),
    "DECOR-DENSITY-001": ("fail", "Decoration is a handful of isolated props (a log, a few flowers, rocks, buckets) in a mostly empty field, with no interior scatter or edge clustering."),
    "DOMINANT-LANDMARK-001": ("fail", "No landmark dominates; the eye finds four equally-weighted identical boxes and nothing specific to move toward."),
    "FIRST-VIEW-001": ("fail", "The first read is 'four boxes and a crossroad in a void,' not a recognisable kind of place."),
    "REWARD-CLUSTER-001": ("fail", "Event/reward positions are bare markers sitting in empty grass, not dressed clusters."),
    "WATER-LANDMARK-001": ("fail", "There is no water feature and the only open space is the hard rectangular path intersection."),
    "VOCAB-LIMITED-001": ("pass", "The material vocabulary is limited -- arguably too limited -- so this lone criterion does not fail, though for the wrong reason."),
    "MEMORABLE-IDENTITY-001": ("fail", "Nothing is statable beyond 'generic four-box village'; there is no memorable identity."),
}


def session_frontier_critiques() -> dict[str, VisualCritique]:
    """The three recorded frontier-VLM calibration critiques."""

    recorded = {
        "map017": _MAP017,
        "map001": _MAP001,
        "wo0073_candidate": _WO0073,
    }
    return {
        label: VisualCritique.from_verdicts(
            label=label,
            image_ref=CALIBRATION_IMAGES[label],
            backend="recorded",
            model="claude-opus-4-8 (agent session)",
            verdicts=verdicts,
        )
        for label, verdicts in recorded.items()
    }


def recorded_calibration_backend() -> RecordedCritiqueBackend:
    return RecordedCritiqueBackend(session_frontier_critiques(), model="claude-opus-4-8 (agent session)")


def _make_backend(name: str, model: str | None) -> VisualCriticBackend:
    if name == "recorded":
        return recorded_calibration_backend()
    if name == "ollama":
        return OllamaVisionBackend(model=model or "llama3.2-vision")
    if name == "anthropic":
        return AnthropicVisionBackend(model=model or "claude-opus-4-8")
    raise SystemExit(f"unknown backend: {name!r} (expected recorded|ollama|anthropic)")


def _cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="WO-0075 automated visual critic")
    parser.add_argument("--calibrate", action="store_true", help="run the three-render calibration go/no-go")
    parser.add_argument("--backend", default="recorded", help="recorded|ollama|anthropic")
    parser.add_argument("--model", default=None, help="override the backend model")
    parser.add_argument("--evidence-dir", default=None, help="write each calibration critique as JSON evidence here")
    args = parser.parse_args(argv)

    if not args.calibrate:
        parser.print_help()
        return 2

    backend = _make_backend(args.backend, args.model)
    collected: dict[str, VisualCritique] = {}
    result = run_calibration(backend, collect=collected)

    print(f"Visual-critic calibration -- backend={result.backend} model={result.model}")
    print(f"{'label':<20} {'expected':<10} {'actual':<8} {'ok':<4} note")
    for row in result.rows:
        print(f"{row.label:<20} {row.expected:<10} {row.actual:<8} {'Y' if row.ok else 'N':<4} {row.note}")
    print(f"\nCALIBRATION: {'PASS' if result.passed else 'FAIL'}  "
          f"(covers AVCP {', '.join(COVERED_AVCP_REFS)})")

    if args.evidence_dir:
        evidence_dir = Path(args.evidence_dir)
        for label, critique in collected.items():
            write_critique_evidence(critique, evidence_dir / f"visual-critic-{label}.json")
        print(f"wrote {len(collected)} critique evidence files to {evidence_dir}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
