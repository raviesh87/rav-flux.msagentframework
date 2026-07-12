---
name: microsoft-agent-framework-builder
description: Design, review, scaffold, and validate Microsoft Agent Framework agents and agentic applications for Microsoft Foundry / Azure AI Foundry. Use when asked to build MAF agents, choose prompt vs hosted agents, use Foundry Agent Service, add Agent Skills, define MCP tools, create governance checklists, migrate from Semantic Kernel or AutoGen, or assess production readiness for enterprise agent deployments.
---

# Microsoft Agent Framework Builder

## Overview

Use this skill to help teams design production-ready Microsoft Agent Framework (MAF) agents and workflows that can run locally, call Microsoft Foundry models and tools, or deploy through Microsoft Foundry Agent Service.

For Microsoft API names, package names, preview status, SDK behavior, and Foundry deployment details, verify against official Microsoft sources before writing final implementation code.

## Workflow

1. Clarify the agent scenario:
   - User task, triggering channel, expected autonomy, human approval points, and production SLA.
   - Data sources, tools, external systems, identity boundaries, compliance constraints, and deployment environment.
   - Whether the agent needs custom code, multi-agent orchestration, stateful workflows, deterministic tools, MCP servers, or only managed configuration.
2. Choose the Foundry pattern:
   - Prompt agent: use when instructions, model, and managed tools are enough.
   - Hosted agent: use when custom code, custom orchestration, multi-agent workflows, custom protocols, custom tools, or framework control is needed.
   - Existing app plus Responses API: use when an application already owns runtime, UX, and deployment, but needs Foundry models and platform tools.
3. Choose the MAF construct:
   - Agent for open-ended conversational/tool-use behavior.
   - Workflow for well-defined multi-step processes, routing, fan-out/fan-in, checkpointing, retries, or human-in-the-loop.
   - Function/MCP tool for deterministic business logic or external system integration.
4. Design the capability package:
   - Instructions and behavioral contract.
   - Tools and MCP servers with least privilege.
   - Agent Skills for reusable domain procedures, policies, templates, and deterministic scripts.
   - Identity, state, persistence, evaluations, telemetry, governance, and escalation paths.
5. Produce implementation artifacts:
   - Architecture decision record.
   - Agent blueprint JSON.
   - Minimal Python or .NET skeleton when requested.
   - Foundry deployment checklist.
   - Production readiness assessment.

## Reference Routing

- Read `references/microsoft-official-references.md` when producing Microsoft Agent Framework, Foundry, Agent Skills, hosted agent, workflow, or SDK implementation guidance.
- Read `references/architecture-guide.md` when designing an agent architecture, selecting prompt vs hosted agents, defining skills/tools, or creating deployment guidance.
- Run `scripts/assess_agent_blueprint.py` when given or creating a blueprint JSON and the user wants a readiness check.

## Blueprint Shape

Use this compact JSON shape for reviews and implementation planning:

```json
{
  "name": "agent-name",
  "business_goal": "Describe the measurable business outcome.",
  "agent_type": "hosted",
  "maf_constructs": ["agent", "workflow", "tools"],
  "custom_code_required": true,
  "human_approval_required": true,
  "data_sources": ["system or knowledge source"],
  "tools": ["tool or MCP integration"],
  "identity": {
    "auth": "Microsoft Entra managed identity or delegated user identity",
    "rbac": ["least-privileged permission"]
  },
  "safety_controls": ["content filters", "least privilege", "approval gates"],
  "evaluation": ["golden task set", "tool-call accuracy", "regression checks"],
  "observability": ["Foundry tracing", "Application Insights", "OpenTelemetry"],
  "deployment": {
    "target": "Microsoft Foundry Agent Service hosted agent",
    "release": "versioned publish with rollback"
  }
}
```

## Script Usage

Run the blueprint assessor:

```bash
python scripts/assess_agent_blueprint.py path/to/blueprint.json
```

Use local scripts only for deterministic review or validation. For live Microsoft services, use official SDKs, least-privileged identity, and the organization's approved deployment controls.
