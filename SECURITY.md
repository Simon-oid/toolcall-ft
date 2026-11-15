# Security policy

## Supported versions

toolcall-ft is pre-1.0. Fixes land on `main` and ship in the next release; older
tags are not back-patched.

## Reporting a vulnerability

Please report vulnerabilities privately via
[GitHub's private vulnerability reporting](https://github.com/Simon-oid/toolcall-ft/security/advisories/new)
(Security tab → "Report a vulnerability"). Do not open a public issue for
an exploitable bug. You should get an acknowledgement within a few days; a
minimal reproducer is the fastest to act on.

## Scope

toolcall-ft is a training and evaluation project: the model it produces emits tool calls, and the host that runs them must validate them (the judge uses cMCP's schema validator for exactly that).
