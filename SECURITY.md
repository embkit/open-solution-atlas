# Security Policy

## What this repository is

Open Solution Atlas is a **documentation/knowledge repository** — Markdown
specifications, YAML metadata, and diagram sources. It contains no running
service, no credentials, and no production code deployments. A "security
issue" here usually means:

1. Content that teaches an unsafe design pattern or contradicts a cited
   security standard.
2. Malicious content smuggled into a pack (e.g. a code snippet containing
   intentional vulnerabilities, credential-harvesting links).
3. Tooling/scripts in the repository with a real vulnerability.

## Reporting a vulnerability

**Do not open a public issue.** Use GitHub's **private vulnerability
reporting** on this repository (Security tab → "Report a vulnerability"),
which routes only to the repository maintainers.

No dedicated security email alias exists yet — this project is honest that it
has no named maintainers ([`MAINTAINERS.md`](MAINTAINERS.md)); an address will
be published here once one is established. Until then the GitHub private
channel is the only supported route.

Please include:

- file path / pack slug and commit hash
- description of the issue and why it is unsafe
- public reference (CVE, CWE, standard) if applicable

We aim to acknowledge within 72 hours and to give a remediation or rationale
within 14 days.

## What is explicitly out of scope

- "Vulnerabilities" in systems merely *described* by packs — the packs are
  design documents, not deployments.
- Hypothetical issues without a concrete unsafe artifact in this repository.
- Requests to disclose private employer or client information — we never
  accept such content in the first place (see CONTRIBUTING.md).

## Content safety note for users

Solution Packs are generalized educational material. Anyone implementing a
system from a pack remains responsible for their own threat modeling,
dependency management, and compliance validation.
