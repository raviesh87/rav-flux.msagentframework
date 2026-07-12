# How To Use The Microsoft Agent Framework Builder Skill In GitHub Copilot For VS Code

This guide explains how developers can use the reusable `microsoft-agent-framework-builder` Agent Skill with GitHub Copilot in VS Code for any Microsoft Agent Framework (MAF) and Microsoft Foundry / Azure AI Foundry use case.

The project skill lives here:

```text
.github/skills/microsoft-agent-framework-builder
```

The leadership brokerage demo lives separately here:

```text
demo
```

Keep that separation: the skill is reusable enablement; the demo is only one example.

## Skill Package Contents

GitHub Copilot in VS Code discovers Agent Skills from the skill folder and `SKILL.md`.

The skill package contains:

```text
.github/skills/microsoft-agent-framework-builder/SKILL.md
.github/skills/microsoft-agent-framework-builder/references/
.github/skills/microsoft-agent-framework-builder/scripts/
```

## What The Skill Does

Use the skill to help developers:

- Decide whether to build a prompt agent, hosted agent, or existing app plus Responses API integration.
- Choose MAF agents, workflows, tools, MCP servers, or Agent Skills.
- Create an architecture decision record.
- Create an agent blueprint JSON.
- Review production readiness.
- Identify security, identity, observability, evaluation, and deployment gaps.
- Anchor implementation guidance to official Microsoft Agent Framework and Foundry references.

The skill does not automatically deploy to Foundry, create Azure resources, or call live enterprise systems by itself. It helps Copilot produce the design, code skeletons, checklists, and review artifacts developers need.

## Use It In VS Code

GitHub Copilot in VS Code supports Agent Skills as folders containing `SKILL.md`. Project skills are discovered from standard repository locations such as:

```text
.github/skills/
.claude/skills/
.agents/skills/
```

Official references:

- VS Code Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills
- VS Code agent customization overview: https://code.visualstudio.com/docs/agent-customization/overview
- GitHub repository custom instructions: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions

This workspace already includes the Copilot-ready location:

```text
.github/skills/microsoft-agent-framework-builder
```

To use it:

1. Open this repository/folder in VS Code.
2. Open GitHub Copilot Chat or Agent mode.
3. Type `/` and look for the `microsoft-agent-framework-builder` skill.
4. Invoke it with your use case.

Example:

```text
/microsoft-agent-framework-builder Design a Microsoft Agent Framework hosted agent for onboarding new vendors, including workflow nodes, tools, approvals, evaluation, observability, and Foundry deployment guidance.
```

If the slash command does not appear:

- Run `/skills` in Copilot Chat to open the Configure Skills menu.
- Confirm the folder is trusted in VS Code.
- Confirm the skill folder name matches the `name` field in `SKILL.md`.
- If you store skills outside `.github/skills`, configure VS Code's `chat.agentSkillsLocations` setting.

To use this skill in another repository, copy this folder into that repository:

```text
.github/skills/microsoft-agent-framework-builder
```

## Developer Workflow

1. Describe the use case.

   Include the business goal, users, data sources, tools, approval needs, security constraints, and expected deployment target.

2. Ask the skill for an architecture recommendation.

   ```text
   /microsoft-agent-framework-builder Recommend the best Microsoft Foundry pattern and MAF constructs for this agentic application:

   <use case>
   ```

3. Ask for a blueprint JSON.

   ```text
   /microsoft-agent-framework-builder Create an agent blueprint JSON for this use case. Include business goal, agent type, MAF constructs, data sources, tools, identity, safety controls, evaluation, observability, and deployment.
   ```

4. Assess the blueprint.

   Save the blueprint as JSON, then run:

   ```powershell
   python .\.github\skills\microsoft-agent-framework-builder\scripts\assess_agent_blueprint.py .\path\to\blueprint.json
   ```

5. Ask Copilot to fix gaps.

   ```text
   /microsoft-agent-framework-builder Improve this blueprint based on the assessment warnings and failures:

   <assessment output>
   ```

6. Ask for implementation guidance.

   ```text
   /microsoft-agent-framework-builder Create a developer build plan, minimal code skeleton, Foundry deployment checklist, and evaluation plan for this blueprint.
   ```

## Reusable Prompt Templates

Architecture:

```text
/microsoft-agent-framework-builder Design a MAF and Foundry architecture for:

Business goal:
Users:
Data sources:
Tools/systems:
Security constraints:
Human approvals:
Deployment target:
```

Hosted agent decision:

```text
/microsoft-agent-framework-builder Decide whether this should be a Foundry prompt agent, Foundry hosted agent, or existing app using Responses API. Explain the tradeoffs and recommendation.
```

Workflow design:

```text
/microsoft-agent-framework-builder Model this use case as a MAF workflow. Include workflow nodes, tool calls, approval gates, retry behavior, and failure handling.
```

Agent Skills:

```text
/microsoft-agent-framework-builder Identify what should be packaged as Agent Skills for this use case, and what should remain deterministic tools or MCP servers.
```

Production readiness review:

```text
/microsoft-agent-framework-builder Review this proposed agent for production readiness. Prioritize risks, missing controls, missing tests, identity/RBAC concerns, observability, and deployment gaps.
```

Code skeleton:

```text
/microsoft-agent-framework-builder Generate a minimal Python and .NET implementation skeleton for this MAF hosted agent. Use official Microsoft references and call out anything that must be verified against current docs.
```

## Blueprint Template

Use this shape for any use case:

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

## Expected Outputs

A good skill-assisted result should include:

- Recommended Foundry pattern.
- Recommended MAF construct: agent, workflow, tools, MCP, or Agent Skills.
- Architecture sketch in text or Mermaid.
- Blueprint JSON.
- Risks and controls.
- Implementation plan.
- Evaluation plan.
- Observability plan.
- Deployment checklist.
- Official Microsoft docs to verify before coding.

## Using The Brokerage Demo

The demo is only an example of how the reusable skill can support a specific leadership story.

Run guide:

```text
demo/run-sensitive-brokerage-demo.md
```

Demo use case:

```text
demo/sensitive-brokerage-demo-use-case.md
```

Reusable Copilot skill:

```text
.github/skills/microsoft-agent-framework-builder
```

## Guidance For Teams

Use the skill early, before writing code. It is most valuable when teams are still deciding:

- Whether they need a prompt agent or hosted agent.
- Whether a process should be a MAF workflow.
- Which actions should be deterministic tools.
- Which procedures belong in Agent Skills.
- What identity, approval, evaluation, and observability controls are required.

For live implementation, verify all SDK names, package versions, hosted agent deployment steps, permissions, and preview limitations against current official Microsoft documentation.
