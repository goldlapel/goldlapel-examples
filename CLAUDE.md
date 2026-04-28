# Coding Guidelines for Claude

## Communication

- Proactively offer constructive criticism, flag bad ideas, suggest better alternatives, and surface trade-offs — don't wait to be asked, kindly push back when it's helpful.
- Don't use interactive question prompts.
- When pushing back on an idea, the reason should be product-level (wrong for the user, dilutes the story, creates operational burden, conflicts with something else) — never effort-level.

## Project Philosophy

- Simple, Lovable, Complete over MVP. We're building artisanal software — polished, thorough, no rough edges or known-broken edge cases left behind. Take the time to get things right.
- This is AI-assisted coding. Implementation cost is near-zero — don't use effort or time as reasons to defer, scope down, or discourage features. Evaluate ideas on product merit: "does this make GL better?" not "is this too much work?"
- Engage with ambitious ideas before narrowing. Explore the full vision first, then find the right shape together. The user's exploratory style is how the product finds its direction — rabbit holes are productive, not wasteful.
- When in doubt, more cowbell.

## Workflow

1. Create a branch for the feature/fix
2. Discuss until all questions are resolved
3. Enter Plan mode, explore codebase, write plan, implement after approval
4. Build → test → review → fix → repeat until clean
5. Merge to main

**Extended thinking in plan mode**: Use extended or ultra thinking liberally both *while writing the plan* and *during implementation*. If a task is simple enough to not need deep thinking, it doesn't need plan mode — just do it. Plans should always include the directive: "Use extended or ultra thinking liberally throughout implementation."

The build/test/review loop (step 4):
1. Build/fix the change
2. Create and run unit tests where applicable — if any fail, return to step 1
3. Full code review of changed code and any code it may have affected — if issues found, return to step 1
4. Iterate until tests and code review all return clean
5. Commit the clean change

- For visual changes, use Playwright to take screenshots and review them to ensure the design looks great.

## Subagent Workflow

- When a task is clearly defined, launch it in a subagent
- Keep subagents topped off at a rolling pipeline of up to 5 concurrent agents
- Scope each agent to non-overlapping files or repos to avoid merge conflicts
- Give each agent clear exit criteria: fix → test → code review → repeat until review is clean → commit → add unit/integration tests → run relevant tests to ensure no regressions
- Backfill new agents as each completes to maintain throughput

This enables parallel execution while keeping the main conversation free for discussion and decisions.

## Code Review

After every fix, do a full code review of the changed code. Check for:
- Bugs, logic errors, off-by-ones, edge cases
- Naming inconsistencies
- Dead code or unused imports introduced by the changes
- Missing error handling at system boundaries
- Anything that doesn't match existing patterns in the codebase

If issues found: fix them, then do another full code review of the fixes. Repeat until clean.

- Don't overengineer — multiple passes until elegant, bug-free, maintainable
- For tough/tricky/high-risk bugs, use extended thinking
- If a code review keeps finding new errors, use your best judgement on when to stop trying to fix it. Report back the nature of the issue.

## Gold Lapel Product Context

This repo holds runnable example apps + demos. The product source of truth lives in the main proxy repo:

- `/home/sgibson/dev/gl/goldlapel/docs/ROADMAP.md` — living roadmap
- `/home/sgibson/dev/gl/goldlapel/docs/ARCHITECTURE.md` — architecture reference
- `/home/sgibson/dev/gl/goldlapel/docs/SHIPPED.md` — completed work
- `/home/sgibson/dev/gl/goldlapel/docs/PRICING.md` — pricing + licensing canonical doc

## Git Management

- Commit after every code change (enables easy reverts)
- Use concise but detailed commit messages
- Push at natural breakpoints without asking (feature complete, bug fixed, etc.)
- Branch workflow: new branch for changes → merge to main when done → delete branch locally and remote

## Code Style

- Don't overengineer — simple, direct solutions over clever abstractions
- Keep API minimal — no service layers or helper abstractions
- No type checking or type hinting
- No Pydantic models
- No TypeScript type annotations
- No Pydoc or JSDoc

## UX

- Never use `cursor: not-allowed` anywhere in the site. Ever.
- Instead use `cursor: pointer` or `cursor: default` with visual effects (opacity, muted colors, spinners) to communicate disabled/loading states. Concierge, not bouncer.

## Examples-Specific

This repo holds runnable example apps + demos in multiple languages. Each example has its own conventions for running and testing — refer to the local `README.md` in each example directory for setup and run instructions. The cross-repo guidelines above (communication, workflow, code review, git management) apply throughout.
