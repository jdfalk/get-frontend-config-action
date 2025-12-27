<!-- file: .github/copilot-instructions.md -->
<!-- version: 1.0.0 -->
<!-- guid: 7d8e9f01-2345-6789-abcd-ef5678901234 -->

# AI Agent Instructions (Standard)

- Use VS Code tasks for non-git operations; prefer MCP GitHub tools for git operations.
- Commits must use conventional commits (type(scope): description).
- Include versioned headers in docs/configs and bump versions on changes.
- For workflows: favor reusable workflows in ghcommon; use repository-config.yml as the source of truth.
- For PRs: enforce rebase-only merges via label-triggered auto-merge; delete branches after merge.
- Provide concise plans and progress updates; use the manage_todo_list tool to track multi-step tasks.
