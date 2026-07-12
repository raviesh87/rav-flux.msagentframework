# Microsoft Agent Framework Builder Skill

This repository contains a reusable GitHub Copilot Agent Skill for teams building agents and agentic applications with Microsoft Agent Framework and Microsoft Foundry / Azure AI Foundry.

The skill helps developers plan, review, and scaffold production-ready agent solutions before they start writing code.

## What It Does

Use this skill in GitHub Copilot for VS Code to:

- Choose the right Foundry pattern: prompt agent, hosted agent, or existing app with Responses API.
- Decide when to use Microsoft Agent Framework agents, workflows, tools, MCP servers, or Agent Skills.
- Create an agent blueprint JSON for a use case.
- Review production readiness for identity, security, evaluation, observability, and deployment.
- Generate implementation guidance anchored to official Microsoft Agent Framework and Foundry references.

## Where The Skill Lives

```text
.github/skills/microsoft-agent-framework-builder
```

GitHub Copilot in VS Code discovers project skills from `.github/skills/`.

## How To Use It

Open this repository in VS Code, then open GitHub Copilot Chat or Agent mode.

Type `/` and choose:

```text
/microsoft-agent-framework-builder
```

Example prompt:

```text
/microsoft-agent-framework-builder Design a Microsoft Agent Framework hosted agent for vendor onboarding. Include workflow nodes, tools, approval gates, evaluation, observability, and Foundry deployment guidance.
```

## What You Get Back

A good skill-assisted response should include:

- Recommended Foundry pattern.
- Recommended MAF construct: agent, workflow, tools, MCP, or Agent Skills.
- Architecture sketch.
- Agent blueprint JSON.
- Risks and controls.
- Build plan.
- Evaluation plan.
- Observability plan.
- Deployment checklist.
- Microsoft docs to verify before implementation.

## Blueprint Assessment

The skill includes a small readiness assessor:

```powershell
python .\.github\skills\microsoft-agent-framework-builder\scripts\assess_agent_blueprint.py .\path\to\blueprint.json
```

## More Guidance

See the full developer guide:

```text
docs/how-to-use-microsoft-agent-framework-builder-skill.md
```

## Notes

This repository provides a Copilot Agent Skill, not a deployed agent application. It does not create Azure resources or deploy to Foundry by itself. Developers should verify SDK names, package versions, permissions, and deployment steps against current official Microsoft documentation before implementation.
