#!/usr/bin/env python3
"""Assess a Microsoft Agent Framework / Foundry agent blueprint."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "name": "Agent name",
    "business_goal": "Business outcome",
    "agent_type": "prompt, hosted, or responses-api",
    "maf_constructs": "agent, workflow, skills, or function",
    "data_sources": "Grounding and operational data",
    "tools": "Tool or MCP integrations",
    "identity": "Authentication and authorization",
    "safety_controls": "Safety and approval controls",
    "evaluation": "Quality and regression checks",
    "observability": "Tracing, metrics, and logs",
    "deployment": "Target hosting and release model",
}

VALID_AGENT_TYPES = {"prompt", "hosted", "responses-api"}
GOVERNANCE_TERMS = ("approval", "human", "rbac", "managed identity", "entra", "content", "filter")
OBSERVABILITY_TERMS = ("trace", "tracing", "opentelemetry", "application insights", "metrics", "logs")
EVALUATION_TERMS = ("golden", "eval", "accuracy", "regression", "quality", "latency")


def _as_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(f"{k} {_as_text(v)}" for k, v in value.items())
    if isinstance(value, list):
        return " ".join(_as_text(item) for item in value)
    return str(value)


def _has_any(value: Any, terms: tuple[str, ...]) -> bool:
    text = _as_text(value).lower()
    return any(term in text for term in terms)


def _recommend_agent_type(data: dict[str, Any]) -> str:
    constructs = {str(item).lower() for item in data.get("maf_constructs", [])}
    custom_code = bool(data.get("custom_code_required"))
    has_workflow = "workflow" in constructs
    has_custom_protocol = bool(data.get("custom_protocol_required"))
    tools = data.get("tools", [])

    if custom_code or has_workflow or has_custom_protocol:
        return "hosted"
    if data.get("existing_runtime"):
        return "responses-api"
    if tools and len(tools) > 4:
        return "hosted"
    return "prompt"


def assess(data: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    passes: list[str] = []
    warnings: list[str] = []
    failures: list[str] = []

    for key, label in REQUIRED_TOP_LEVEL.items():
        value = data.get(key)
        if value:
            passes.append(f"{label} is present.")
        else:
            failures.append(f"Missing {key}: {label}.")

    agent_type = str(data.get("agent_type", "")).lower()
    if agent_type in VALID_AGENT_TYPES:
        passes.append(f"Agent type '{agent_type}' is recognized.")
    elif agent_type:
        failures.append("agent_type must be one of: prompt, hosted, responses-api.")

    recommended = _recommend_agent_type(data)
    if agent_type and agent_type != recommended:
        warnings.append(
            f"Blueprint says '{agent_type}', but the inputs suggest '{recommended}' because of custom code, workflows, tools, or existing runtime."
        )
    elif agent_type:
        passes.append(f"Agent type matches recommendation: {recommended}.")

    if data.get("human_approval_required") or _has_any(data.get("safety_controls"), ("approval", "human")):
        passes.append("Human approval or equivalent control is represented.")
    else:
        warnings.append("Add human approval for irreversible writes, production changes, or customer-impacting actions.")

    if _has_any(data.get("identity"), ("managed identity", "entra", "rbac")):
        passes.append("Identity design mentions managed identity, Entra, or RBAC.")
    else:
        warnings.append("Identity should specify Microsoft Entra managed identity and scoped RBAC.")

    if _has_any(data.get("safety_controls"), GOVERNANCE_TERMS):
        passes.append("Safety controls include governance-oriented terms.")
    else:
        warnings.append("Safety controls should include content filters, prompt-injection handling, RBAC, and approvals.")

    if _has_any(data.get("evaluation"), EVALUATION_TERMS):
        passes.append("Evaluation plan has measurable quality or regression checks.")
    else:
        warnings.append("Evaluation should include a golden set, quality metrics, tool-call accuracy, and regression gates.")

    if _has_any(data.get("observability"), OBSERVABILITY_TERMS):
        passes.append("Observability includes tracing, metrics, logs, or OpenTelemetry.")
    else:
        warnings.append("Observability should include Foundry tracing, Application Insights, metrics, and logs.")

    deployment_text = _as_text(data.get("deployment")).lower()
    if "version" in deployment_text or "rollback" in deployment_text:
        passes.append("Deployment plan includes versioning or rollback.")
    else:
        warnings.append("Deployment should include versioned publishing and rollback.")

    return passes, warnings, failures


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: assess_agent_blueprint.py <blueprint.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Blueprint not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {path}: {exc}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("Blueprint root must be a JSON object.", file=sys.stderr)
        return 2

    passes, warnings, failures = assess(data)
    denominator = max(1, len(passes) + len(warnings) + len(failures))
    score = max(0, round(100 * (len(passes) - len(failures)) / denominator))
    status = "READY WITH REVIEW" if not failures and score >= 75 else "NEEDS WORK"

    print(f"# Agent Blueprint Assessment: {data.get('name', path.stem)}")
    print()
    print(f"Status: {status}")
    print(f"Readiness score: {score}/100")
    print()
    print("## Passes")
    for item in passes:
        print(f"- PASS: {item}")
    print()
    print("## Warnings")
    if warnings:
        for item in warnings:
            print(f"- WARN: {item}")
    else:
        print("- None")
    print()
    print("## Failures")
    if failures:
        for item in failures:
            print(f"- FAIL: {item}")
    else:
        print("- None")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
