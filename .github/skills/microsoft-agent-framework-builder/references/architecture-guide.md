# Microsoft Agent Framework And Foundry Architecture Guide

Last verified against official Microsoft sources: 2026-07-12.

## Decision Matrix

Use a prompt agent when the agent can be expressed as instructions, model choice, managed tools, and configuration. This is the fastest path for internal assistants and production use cases that do not need custom orchestration code.

Use a hosted agent when the team needs custom code, Microsoft Agent Framework workflows, multi-agent collaboration, custom protocols, advanced state handling, custom tools, enterprise integrations, or framework-level control while still using Foundry-managed endpoint, scaling, identity, and observability.

Use an existing app plus the Responses API when the application already owns UX, runtime, deployment, and release controls, but should call Foundry models and platform tools.

Use a MAF workflow when the process has explicit steps, routing, parallel branches, checkpoints, retries, or human approval gates. Use a single agent when the task is open-ended or conversational. Use deterministic functions or MCP tools when an LLM is unnecessary for the operation.

## Reusable Architecture Pattern

Separate reasoning from deterministic operations:

1. The MAF agent interprets the user request, clarifies missing details, chooses tools, and explains outcomes.
2. MAF workflows coordinate multi-step processes, branching, retries, and human approvals.
3. Deterministic tools handle external systems, file processing, data transformations, or irreversible actions.
4. Agent Skills package reusable instructions, policies, templates, examples, and scripts for a domain.
5. Foundry deployment, tracing, evaluations, and monitoring provide production controls.

## Production Architecture Checklist

1. Architecture:
   - State the business goal, user journey, autonomy level, failure modes, and measurable success criteria.
   - Choose prompt agent, hosted agent, or external app plus Responses API with a short rationale.
   - Choose agent, workflow, deterministic tool, MCP server, or skill package with a short rationale.
2. Identity and access:
   - Prefer Microsoft Entra managed identity for deployed agents where supported.
   - Use delegated identity when user-specific permissions must be honored.
   - Use RBAC and tool-level scopes for least privilege.
   - Separate read, write, approval, and external-sharing permissions.
3. Tools and MCP:
   - Prefer MCP or narrow service tools for reusable enterprise integrations.
   - Document each tool's auth mode, permissions, allowed operations, rate limits, and fallback behavior.
   - Keep tool outputs compact and structured.
4. Agent Skills:
   - Package domain policies, procedures, templates, and repeatable scripts as file-based skills.
   - Put long policies in `references/`, executable repeatable checks in `scripts/`, and output templates in `assets/`.
   - Keep `SKILL.md` concise and route to references only when needed.
5. Safety and governance:
   - Add prompt injection handling for external content and retrieved documents.
   - Use content filters and block unsafe tool actions.
   - Require approvals for irreversible writes, customer-impacting actions, financial actions, data movement, external sharing, or policy-sensitive operations.
   - Document third-party model, server, and data-flow risks.
6. Evaluation:
   - Build a golden task set with expected reasoning boundaries and tool calls.
   - Evaluate answer quality, retrieval grounding, tool-call accuracy, refusal/escalation behavior, and latency.
   - Add regression tests before publishing new versions.
7. Observability:
   - Capture Foundry tracing, OpenTelemetry spans, tool calls, model inputs/outputs subject to policy, latency, errors, costs, and approval decisions.
   - Define dashboards for success rate, escalation rate, unsafe request rate, tool failure rate, latency, and cost.
8. Deployment:
   - Use versioned publishing with rollback.
   - Validate networking, data residency, environment isolation, and secret management.
   - Prefer CI/CD for repeatable environment promotion.
   - Monitor after release and set an owner for triage.

## Code Skeleton Guidance

For pure MAF agent orchestration, Python or .NET can work. Choose the language that best fits the team's runtime, libraries, enterprise SDKs, and deployment target.

For a hosted agent, scaffold:

1. Agent or workflow entry point.
2. Foundry project endpoint and model configuration from environment variables.
3. Managed identity or delegated user credential path.
4. Tool registration for external systems and deterministic operations.
5. Skill provider registration if using file-based skills.
6. Telemetry initialization.
7. Health endpoint or startup validation.
8. Container or zip packaging for Foundry Agent Service.

## Review Output Format

When reviewing or designing an agent, return:

1. Recommendation: prompt agent, hosted agent, or existing app plus Responses API.
2. MAF construct: agent, workflow, skill package, deterministic tool, or MCP server.
3. Architecture sketch: components, data flow, identities, tools, and approval points.
4. Risks: security, data residency, prompt injection, tool misuse, cost, reliability, and operational ownership.
5. Build plan: smallest useful prototype, production hardening, deployment path.
6. Validation: task fixtures, evals, traces, and monitoring needed before launch.
