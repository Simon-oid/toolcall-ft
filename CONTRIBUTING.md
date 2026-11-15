# Contributing to toolcall-ft

Thanks for taking the time. Issues and pull requests are welcome.

## Before a pull request

1. Open an issue first for anything larger than a small fix, so the scope
   can be agreed before the work.
2. Keep one change per pull request, with a test that fails without it.
3. Run the same checks CI runs:

   ```sh
   .venv/bin/ruff check src tests scripts
   .venv/bin/mypy src/toolcall
   .venv/bin/pytest -q --cov=toolcall --cov-fail-under=80
   ```

4. Add a line to `CHANGELOG.md` under *Unreleased*.

## Style

ruff and mypy clean; a change to the data generator or the scorer comes with the affected results regenerated.

Commit messages follow `type: description` (`feat`, `fix`, `docs`, `test`,
`refactor`, `perf`, `chore`, `ci`), in English.

## Measurements

Numbers in the README and in `KNOWN_LIMITATIONS.md` are measured, with the
command that reproduces them. A change that moves one updates it, with the
new measurement.

## Security

Do not open a public issue for a vulnerability: see [`SECURITY.md`](SECURITY.md).
