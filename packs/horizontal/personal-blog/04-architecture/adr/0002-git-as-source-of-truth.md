# ADR-0002 — Git repository as the source of truth for content

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Ownership and portability are core promises (FR-017/018, NFR-011, journey
J-05). Content must remain readable without the publishing software, support
natural revision history, and offer a manual channel if the authoring service
is gone. Options:

1. Git tree: Markdown + YAML frontmatter + media, repository as SSOT
2. Operational database as SSOT, export as derived dump
3. Object-store blobs + separate metadata DB

## Options considered

1. **Git SSOT** — forkable, diffable, durable, tool-agnostic, doubles as
   backup and emergency channel; binary media handled via LFS/storage refs.
2. **DB SSOT** — flexible queries, easy autosave; but content becomes hostage
   to schema/software, export is lossy-by-neglect, and lock-in creeps back.
3. **Blobs + DB** — splits the truth; consistency between stores becomes a
   permanent source of bugs.

## Decision

The Git repository is the source of truth for everything publishable. The
operational DB holds only derived/transient data: sessions, mentions,
scheduling state, audit records. A Git push is a valid authoring event.

## Consequences

- Positive: exit guarantee is structural (J-05); revisions come free; backup
  story = git remote + storage mirror.
- Negative: autosave needs a staging area (unsaved draft workspace outside
  the committed tree until debounced commit); concurrent editing is not
  supported (acceptable: single author).
- Conflict rule: API path commits on author's behalf; direct Git commits are
  merged by "last writer" with conflict surfaced in admin rather than
  silently overwritten.
