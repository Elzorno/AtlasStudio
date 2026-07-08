from __future__ import annotations

import re
from collections.abc import Callable

from .models import ClassificationResult, WorkOrderRequest


CANON_NOUNS = (
    "story",
    "character",
    "protagonist",
    "quest",
    "sidequest",
    "dialogue",
    "lore",
    "world",
    "region",
    "location",
    "faction",
    "backstory",
    "npc",
    "blacksmith",
    "shopkeeper",
    "ashford village",
    "rowan",
    "elara",
    "covenant",
    "relay",
)
CANON_CAPABILITIES = {"canon-design", "creative-writing", "final-canon"}
STRONG_CANON_TERMS = (
    "dialogue",
    "lore",
    "quest",
    "sidequest",
    "backstory",
    "story",
    "canon",
)
CANON_AUTHORING_VERBS = ("write", "design", "decide", "resolve", "finalize", "canonize")
ORCHESTRATION_CAPABILITIES = {
    "architecture-review",
    "schema-design",
    "graph-analysis",
    "implementation",
}
ATLASSTUDIO_TERMS = (
    "tools/",
    "studio/",
    "schemas/",
    "atlas graph",
    "planning engine",
    "canon linter",
    "graph diff",
    "studio doctor",
    "agent scheduler",
    "work order router",
    "router",
)
BRIDGE_TERMS = (
    "synchronization",
    "sync",
    "import",
    "imported",
    "handoff",
    "traceability",
    "comparing",
    "comparison",
    "proposal",
    "propose",
    "adoptable tool",
)
GAME_IMPLEMENTATION_FILE_PATTERNS = (
    r"\bMap\d{3}\b",
    r"\bMap\d{3}\.json\b",
    r"\bSystem\.json\b",
    r"\bTilesets\.json\b",
    r"\bmap_ownership\.json\b",
    r"\btileset\b",
    r"\btransfer event\b",
    r"\bmap trigger event\b",
    r"\bpassability\b",
    r"\bevent list\b",
    r"\bIMP-[A-Z]+-\d{3}\b",
)
IMPLEMENTATION_PACKET_PATTERN = r"\bIMP-[A-Z]+-\d{3}\b"
IMPLEMENTATION_VERBS = ("build", "implement", "create", "apply", "wire", "update", "add", "modify")
IMPLEMENTATION_NOUN_PATTERNS = (
    r"\bshop\b",
    r"\bmap\b",
    r"\bevent\b",
    r"\bnpc placement\b",
    r"\btransfer\b",
    r"\btransfers\b",
    r"\btileset\b",
    r"\broute\b",
)


def classify(request: WorkOrderRequest) -> ClassificationResult:
    matches: list[tuple[str, str]] = []
    for check in SIGNAL_CHECKS:
        result = check(request)
        if result is not None:
            matches.append(result)
    if not matches:
        return ClassificationResult(
            classification="ambiguous",
            signals_matched=[],
            conflicting_classifications=[],
            ambiguous_reason="no_signal_matched",
        )
    classifications = sorted({classification for classification, _signal in matches})
    signals = [signal for _classification, signal in matches]
    if len(classifications) == 1:
        return ClassificationResult(
            classification=classifications[0],
            signals_matched=signals,
        )
    return ClassificationResult(
        classification="ambiguous",
        signals_matched=signals,
        conflicting_classifications=classifications,
        ambiguous_reason="conflicting_repository_signals",
    )


def request_text(request: WorkOrderRequest) -> str:
    parts = [request.title, request.purpose, *request.scope_in, *request.scope_out]
    return " ".join(part for part in parts if part)


def _check_canon_capability(request: WorkOrderRequest) -> tuple[str, str] | None:
    capabilities = {capability.lower() for capability in request.required_capabilities}
    matched = sorted(capabilities & CANON_CAPABILITIES)
    if matched:
        return ("canon", f"required_capabilities contains {', '.join(matched)}")
    return None


def _check_canon_noun(request: WorkOrderRequest) -> tuple[str, str] | None:
    text = request_text(request).lower()
    if "canon linter" in text and "dialogue" not in text and "sidequest" not in text:
        return None
    if _has_implementation_packet(text) and _has_packet_implementation_context(text):
        if not _has_stronger_canon_context(text):
            return None
    matched = [
        noun
        for noun in CANON_NOUNS
        if re.search(rf"(?<![a-z0-9]){re.escape(noun)}(?![a-z0-9])", text)
    ]
    if matched:
        return ("canon", "canon noun: " + ", ".join(matched[:3]))
    return None


def _check_game_implementation_capability(request: WorkOrderRequest) -> tuple[str, str] | None:
    text = request_text(request)
    lowered = text.lower()
    if _has_stronger_tooling_context(lowered) or _has_stronger_canon_context(lowered):
        return None
    capabilities = {capability.lower() for capability in request.required_capabilities}
    has_capability = "rpg-maker-json" in capabilities or request.engine_specific
    has_file = any(re.search(pattern, text, re.IGNORECASE) for pattern in GAME_IMPLEMENTATION_FILE_PATTERNS)
    implement_packet = re.search(r"\bimplement\s+IMP-[A-Z]+-\d{3}\b", text, re.IGNORECASE)
    packet_implementation = _has_implementation_packet(lowered) and _has_packet_implementation_context(lowered)
    map_event = re.search(r"\b(map trigger event|trigger event)\b", text, re.IGNORECASE)
    if (has_capability and has_file) or implement_packet or packet_implementation or map_event:
        reasons: list[str] = []
        if "rpg-maker-json" in capabilities:
            reasons.append("required_capabilities contains rpg-maker-json")
        if request.engine_specific:
            reasons.append("engine_specific is true")
        if implement_packet:
            reasons.append("request names an Atlas implementation packet")
        if packet_implementation and not implement_packet:
            reasons.append("implementation packet plus implementation verb or noun")
        if map_event:
            reasons.append("scope names a map trigger event")
        if has_file:
            reasons.append("scope names a Game repository file, map, or event")
        return ("game_implementation", " + ".join(reasons))
    return None


def _has_implementation_packet(text: str) -> bool:
    return bool(re.search(IMPLEMENTATION_PACKET_PATTERN, text, re.IGNORECASE))


def _has_packet_implementation_context(text: str) -> bool:
    has_verb = any(re.search(rf"\b{re.escape(verb)}\b", text, re.IGNORECASE) for verb in IMPLEMENTATION_VERBS)
    has_noun = any(re.search(pattern, text, re.IGNORECASE) for pattern in IMPLEMENTATION_NOUN_PATTERNS)
    return has_verb or has_noun


def _has_stronger_canon_context(text: str) -> bool:
    has_authoring_verb = any(re.search(rf"\b{re.escape(verb)}\b", text) for verb in CANON_AUTHORING_VERBS)
    has_canon_term = any(re.search(rf"\b{re.escape(term)}\b", text) for term in STRONG_CANON_TERMS)
    return has_authoring_verb and has_canon_term


def _has_stronger_tooling_context(text: str) -> bool:
    return any(term in text for term in ATLASSTUDIO_TERMS)


def _check_orchestration_capability(request: WorkOrderRequest) -> tuple[str, str] | None:
    text = request_text(request).lower()
    if "propose" in text and "thelastswordprotocol-atlas" in text:
        return None
    capabilities = {capability.lower() for capability in request.required_capabilities}
    has_capability = bool(capabilities & ORCHESTRATION_CAPABILITIES)
    has_term = any(term in text for term in ATLASSTUDIO_TERMS)
    if has_capability and has_term:
        matched_caps = sorted(capabilities & ORCHESTRATION_CAPABILITIES)
        return (
            "production_orchestration",
            f"required_capabilities contains {', '.join(matched_caps)} and scope names AtlasStudio tooling",
        )
    if has_term and re.search(r"\b(create|build|add|extend|design|document|implement|rename|write|fix)\b", text):
        return ("production_orchestration", "scope names AtlasStudio tooling")
    return None


def _check_bridge_signal(request: WorkOrderRequest) -> tuple[str, str] | None:
    text = request_text(request).lower()
    has_bridge_term = any(term in text for term in BRIDGE_TERMS)
    sibling_reference = (
        "atlas" in text
        or "imported" in text
        or re.search(r"\bimp-[a-z]+-\d{3}\b", text)
    )
    if has_bridge_term and sibling_reference:
        return (
            "cross_repository_bridge",
            "scope describes importing, diffing, comparing, proposing, or handing off sibling-repo content",
        )
    return None


SIGNAL_CHECKS: list[Callable[[WorkOrderRequest], tuple[str, str] | None]] = [
    _check_canon_capability,
    _check_canon_noun,
    _check_game_implementation_capability,
    _check_orchestration_capability,
    _check_bridge_signal,
]
