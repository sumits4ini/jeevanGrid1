# Contributing to JeevanGrid

Thank you for contributing to **JeevanGrid** — an open-source, next-generation disaster intelligence and emergency response platform.

## Code of Conduct
We adhere to strict standards of professional collaboration, respect, and technical integrity.

---

## Branching Strategy

We follow a structured Git branching workflow:

- `master` / `main`: Production-ready, validated code. Direct pushes are forbidden.
- `develop`: Integration branch for active phase development.
- `feature/<phase-number>-<feature-name>`: Feature branches (e.g. `feature/phase2-fastapi-core`, `feature/phase5-maplibre-gis`).
- `fix/<issue-name>`: Bug fixes.

---

## Commit Message Convention

All commits must strictly follow the **Conventional Commits** specification:

```text
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Allowed Types:
- `feat`: A new feature or capability
- `fix`: A bug fix
- `docs`: Documentation updates only
- `style`: Code style/formatting changes (no logic changes)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance optimizations
- `test`: Adding or correcting tests
- `chore`: Build process, dependency updates, tooling

### Examples:
- `feat(gis): add dynamic postgis buffer query for hospital vulnerability radius`
- `fix(risk-engine): normalize MCDA population exposure weights to sum to 1.0`
- `docs(arch): update ai inference pipeline sequence diagrams`

---

## Development Workflow & Rules

1. **Modular Architecture**: Never write monolithic spaghetti code. Keep API schemas, business logic, GIS spatial routines, and ML inference strictly separated.
2. **Environment Variables**: Never hardcode credentials, connection strings, or API tokens. Always use `.env` and reference `.env.example`.
3. **Data Authenticity**: Never fabricate real disaster data and present it as genuine. Mock datasets must be clearly isolated under `data/mock/` with clear schema definitions and provenance notes.
4. **Type Safety & Linting**:
   - Backend: Python code must pass `ruff`, `mypy`, and `pytest`.
   - Frontend: TypeScript code must be strictly typed (avoid `any`) and pass ESLint checks.
5. **GIS Integrity**: Always specify Coordinate Reference Systems (EPSG:4326 for storage, EPSG:3857 for web visualization).
6. **AI/ML Reproducibility**: All models must have documented inputs, outputs, baseline metrics, and reproducible training notebooks/scripts.

---

## Pull Request Checklist

Before submitting a Pull Request:
- [ ] Code builds cleanly with no linter warnings.
- [ ] Unit & integration tests added and passing.
- [ ] Relevant documentation updated under `docs/`.
- [ ] No secrets or huge raw binary datasets committed.
- [ ] Tested against local Docker or local virtual environment.
