# Microsoft Official References And Code Pattern Anchors

Last verified: 2026-07-12.

Use these official sources before writing final implementation code. Verify live package/API details when the user needs buildable code, because Microsoft Agent Framework and Foundry are moving quickly.

## Agent Framework And Foundry

- Microsoft Agent Framework overview: https://learn.microsoft.com/en-us/agent-framework/overview/
  - Official docs describe Agents, Harness, and Workflows.
  - Use Agents for LLM tool use and conversation.
  - Use Workflows for graph-based multi-step tasks, type-safe routing, checkpointing, and human-in-the-loop support.
- Microsoft Agent Framework GitHub repository: https://github.com/microsoft/agent-framework
  - Official repo describes MAF as a multi-language framework for production-grade AI agents and multi-agent workflows in .NET and Python.
  - It lists Python, .NET, provider, workflow, hosted-agent, observability, declarative-agent, Agent Skills, and DevUI samples.
- Microsoft Foundry Agent Service overview: https://learn.microsoft.com/en-us/azure/foundry/agents/overview
  - Prompt agents are managed configuration.
  - Hosted agents run custom agent code in Foundry.
  - Existing runtimes can call the Responses API directly.

## Agent Skills

- Agent Skills in Microsoft Agent Framework: https://learn.microsoft.com/en-us/agent-framework/agents/skills
  - Skills are portable packages of instructions, scripts, and resources.
  - File-based skill structure is `SKILL.md`, optional `scripts/`, `references/`, and `assets/`.
  - Python uses `SkillsProvider.from_paths(...)`.
  - .NET uses `AgentSkillsProvider(...)` or `AgentSkillsProviderBuilder`.

Minimal Python pattern to adapt after verifying package versions:

```python
from pathlib import Path
from agent_framework import Agent, SkillsProvider
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

skills_provider = SkillsProvider.from_paths(
    skill_paths=Path(__file__).parent / "skills"
)

agent = Agent(
    client=FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
        credential=AzureCliCredential(),
    ),
    name="EnterpriseAgent",
    instructions="Follow the configured task policy and use tools with least privilege.",
    context_providers=[skills_provider],
)
```

Minimal .NET pattern to adapt after verifying package versions:

```csharp
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;

var endpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var model = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME");

AIAgent agent = new AIProjectClient(new Uri(endpoint!), new DefaultAzureCredential())
    .AsAIAgent(
        model: model!,
        instructions: "Follow the configured task policy and use tools with least privilege.",
        name: "EnterpriseAgent");
```

## Implementation Stance

Use official APIs for live Microsoft operations. Use bundled scripts only for local validation, fixtures, or repeatable developer tasks. If a requested implementation would bypass authorization, over-grant permissions, or perform irreversible actions without approval, refuse that design and propose a governed alternative.
