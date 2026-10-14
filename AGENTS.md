# Contributor instructions for coding agents

- Scope: Phase 2 local Bridge MVP. Do not build a full Obsidian plugin or add AI/network calls unless the user explicitly requests them.
- Read README.md and docs/ROADMAP.md before editing.
- Run `python -m unittest discover -s tests -v` from this repository root.
- Tests must use temporary vaults, never personal vaults. Do not mutate examples/demo-vault during tests.
- Preserve generated-area conflict detection, manual content, Canvas positions, stable IDs, import receipts, backups, and rollback behavior.
- Runtime is Python 3.10+ standard library; Windows UI uses PowerShell/Windows Forms. Do not add dependencies without a concrete need.
- Protocol versioning and migration are explicit. Do not silently reverse edges or equate import success with factual verification.
- Do not publish, push, or message collaborators without user authorization.
