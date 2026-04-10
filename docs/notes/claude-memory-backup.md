# Claude Code Memory Backup

Snapshot of `~/.claude/projects/-home-sgibson-dev-gl-goldlapel/memory/`.
This is what makes Claude Code sessions in this directory feel "tuned in" —
project context, workflow preferences, and org knowledge accumulated over time.

Restore by copying these files back into the memory directory on a new machine.

---

## MEMORY.md (index)

### Project Overview
- **Product**: Gold Lapel — a self-optimizing Postgres proxy (Rust)
- **GitHub org**: github.com/goldlapel (was stephengibson12)
- **Binary**: `goldlapel`
- **Crate name**: `goldlapel`

### Key Naming Conventions
- Default port: 7932 (79 = atomic number for gold, 32 = second half of 5432/Postgres)
- Env var prefix: `GOLDLAPEL_` (e.g. `GOLDLAPEL_PORT`, `GOLDLAPEL_UPSTREAM`)
- DB schema: `_goldlapel`
- Matview names: `_goldlapel.mv_<hash>` (schema mode) or `_goldlapel_mv_<hash>` (public fallback)
- Index names: `_goldlapel.idx_<hash>` or `_goldlapel_idx_<hash>`
- Skip annotation: `/* goldlapel:skip */`

### Pricing
- Two paid plans: Per Instance ($149/mo) and Site License ($24,000/yr, unlimited instances)
- 14-day free trial, no free tier
- Bellhop/Butler are operating modes, not pricing tiers (Bellhop = kill switch, Butler = full optimization)

### GitHub Repos
- `goldlapel/goldlapel` — Rust proxy (private)
- `goldlapel/goldlapel-python` — PyPI wrapper (Python, 18 tests)
- `goldlapel/goldlapel-js` — npm wrapper (ESM, 15 tests, node:test runner)
- `goldlapel/goldlapel-ruby` — RubyGems wrapper (Ruby, 24 tests, minitest)
- `goldlapel/goldlapel-java` — Maven Central wrapper (Java, 22 tests, JUnit 5)
- `goldlapel/goldlapel-php` — Composer/Packagist wrapper (PHP, 19 tests)
- `goldlapel/goldlapel-go` — Go module wrapper
- `goldlapel/goldlapel-dotnet` — NuGet wrapper (C#, 23 tests, xUnit, netstandard2.0)
- Plugins (Django, Rails, Laravel, Spring Boot, Prisma, SQLAlchemy, Drizzle) are now consolidated into their respective language wrapper packages
- `goldlapel/goldlapel-hq — website + API + comms hub
- `goldlapel/homebrew-tap` — Homebrew tap (public, auto-generated formula)

### Docs Structure
- `docs/ROADMAP.md` — living roadmap (incomplete work)
- `docs/SHIPPED.md` — completed work archive (includes SQL Optimization Strategies detail tables)
- `docs/INTEGRATIONS.md` — wrapper/plugin status
- `docs/ARCHITECTURE.md` — target architecture reference (two-tier: origin proxy + edge cache)
- `docs/todos/RELEASE-TODOS.md` — release workflow, secrets, plugin publishing
- `docs/notes/PRICING.md` — pricing working doc
- `docs/notes/goldlapel-market-research.md` — market research
- `docs/notes/goldlapel-technical-research.md` — technical research

### Release Workflow
- 12 workflow files in `.github/workflows/`: `release.yml`, `release-python.yml`, `release-js.yml`, `release-ruby.yml`, `release-java.yml`, `release-php.yml`, `release-go.yml`, `release-dotnet.yml`, `release-docker.yml`, `release-public.yml`, `release-plugins.yml`, `release-homebrew.yml`
- Chain: tag push → build + GitHub Release → all publish workflows triggered by release:published
- `release-plugins.yml` publishes all 7 plugins inline (Django, SQLAlchemy, Prisma, Drizzle, Rails, Spring Boot, Laravel) — single-pane visibility from main repo Actions
- GitHub Release uses a PAT (`RELEASE_TOKEN`), not GITHUB_TOKEN, so downstream workflows trigger
- `RELEASE_TOKEN` PAT also used for cross-repo checkout and asset download
- Packagist (PHP) is git-based — workflow commits binaries + tags to goldlapel-php, Packagist auto-discovers via webhook (no secret needed)
- Go module proxy is git-based — workflow commits binaries + tags to goldlapel-go, proxy.golang.org auto-discovers (no secret needed)
- 11 secrets (org-level, `visibility=all`): `RELEASE_TOKEN`, `PYPI_API_TOKEN`, `NPM_TOKEN`, `RUBYGEMS_API_KEY`, `MAVEN_CENTRAL_USERNAME`, `MAVEN_CENTRAL_PASSWORD`, `MAVEN_GPG_PRIVATE_KEY`, `MAVEN_GPG_PASSPHRASE`, `NUGET_API_KEY`, `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- Target platforms: linux-x86_64, linux-aarch64, darwin-aarch64, windows-x86_64 (4 platforms)
- Publish workflows have `workflow_dispatch` trigger for manual re-runs
- Linux builds use `cross` (glibc 2.31 containers, manylinux_2_31 tags)
- npm: @goldlapel/linux-x64, @goldlapel/linux-arm64, @goldlapel/darwin-arm64 (scoped platform packages with os/cpu fields)
- PyPI version auto-set from tag (strips v prefix, updates pyproject.toml in CI)
- RubyGems: platform gems (x86_64-linux, aarch64-linux, arm64-darwin), version/platform via env vars in gemspec

### License Strategy
- Signed license files (offline, cryptographically verified against baked-in public key)
- Phone-home validation piggybacks on telemetry ping, falls back to local check

### Key Architecture Decisions
- Wrappers spawn Rust binary as subprocess (not FFI/PyO3/maturin)
- Both wrappers use regex for port replacement (not URL parsers — avoids decoding percent-encoded chars)
- PyPI: platform-tagged wheels via `wheel tags --remove`
- npm: ES modules (`"type": "module"`), zero dependencies, `"files"` field controls publish contents
- Driver-agnostic: wrappers return a connection string URL, work with any Postgres driver

### Framework Plugins (built)
- Django, Laravel, Rails, Spring Boot — glue on top of language wrappers
- Planned: additional frameworks TBD

### Java Wrapper Details
- Maven coordinates: `com.goldlapel:goldlapel`
- Single JAR bundles all 3 platform binaries (detected at runtime via `extractBinary()`)
- Resources path: `bin/goldlapel-<os>-<arch>` in classpath
- Maven Central publishing requires GPG signing + Sonatype Central Portal account
- pom.xml still needs Maven Central metadata (`<licenses>`, `<developers>`, `<scm>`, `<distributionManagement>`, `maven-gpg-plugin`)

### Strategic Direction
- Host-agnostic CLI/library is the core product
- Every Postgres provider is a distribution partner, not a competitor
- **Docker image** (planned) — self-hosted Docker/Helm: GL proxy + pre-configured Postgres with all extensions. User deploys, GL provides the image. Revenue without ops burden.
- Docker image is additive (enhances existing providers, doesn't replace them) — no channel conflict
- "GL Valet" name dropped — Docker images don't need brand names

---

## feedback_audit_workflow.md

Don't merge audit/fix branches to main until the user has reviewed the changes. Keep the branch open so it's easy to revert or cherry-pick.

Broad "audit everything and fix what you find" prompts produce a mix of real fixes, unnecessary hardening, new features, and self-inflicted bugs. Each pass creates roughly as many problems as it solves (the "audit treadmill"). Instead: identify the issues, write them up with implementation details, then fix them one at a time as separate focused tasks.

**Why:** Three audit passes (March 2026) produced 700 lines of changes. ~50% was genuinely valuable. The rest was defense-in-depth on internal values, hardening for theoretical concerns, a new feature smuggled in as a "security fix", and fixes for bugs the audit itself introduced.

**How to apply:** When asked to audit or do broad fixes, produce a findings document first. Let the user decide what to fix. Implement each fix as a separate commit on a branch. Don't merge until reviewed.

---

## feedback_shipped_scope.md

Don't add minor bug fixes to SHIPPED.md — only features and milestones belong there. Bug fixes live in git history.

**Why:** User considers SHIPPED.md a product achievement log, not a changelog. Minor fixes dilute the signal.

**How to apply:** When completing work, only update SHIPPED.md for new features, major capabilities, or significant milestones. Skip it for bug fixes, small corrections, and internal improvements.

---

## project_plugin_ci_consolidation.md

SHIPPED (March 2026). All plugin publishing (Django, SQLAlchemy, Prisma, Drizzle, Rails, Spring Boot, Laravel) now happens inline in `release-plugins.yml` in the main repo. Plugin repo workflows changed to `workflow_dispatch` only — tags still created post-publish for version history but no longer trigger publishing.

**Why:** Single-pane release visibility from main repo Actions page. Also fixed Spring Boot race condition (now polls Maven Central for Java wrapper before building).

**How to apply:** If adding new plugins, add a new job to `release-plugins.yml` following the same pattern. Plugin repo workflows are manual-only now.

---

## reference_secrets_setup.md

All 11 publish secrets live at **org level only** with `visibility=all`. No repo-level secrets anywhere. Repo-level duplicates on `goldlapel/goldlapel` were removed (2026-03-16) after plugin CI consolidation moved all publishing to the main repo.

Secrets (11): `RELEASE_TOKEN`, `PYPI_API_TOKEN`, `NPM_TOKEN`, `RUBYGEMS_API_KEY`, `MAVEN_CENTRAL_USERNAME`, `MAVEN_CENTRAL_PASSWORD`, `MAVEN_GPG_PRIVATE_KEY`, `MAVEN_GPG_PASSPHRASE`, `NUGET_API_KEY`, `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

Maven has 5 values total but only 4 need to be GitHub secrets — the GPG key ID (`rsa4096/FFEE23C145AB01A6`) is extracted automatically by `actions/setup-java` from the private key.

Token values are backed up in local `.env` file (gitignored). `.env` also has `packagist_api` (not needed in CI — Packagist is git-based) and Stripe keys (API server, not CI).

The GPG private key export command: `echo "<passphrase>" | gpg --batch --pinentry-mode loopback --passphrase-fd 0 --armor --export-secret-keys FFEE23C145AB01A6`

**How to apply:** When rotating a secret, set it once at org level: `gh secret set <NAME> --org goldlapel --visibility all --body "<value>"`. No repo-level secrets to update.
