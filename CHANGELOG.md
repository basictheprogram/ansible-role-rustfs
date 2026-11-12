# Changelog

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
and [human-readable changelog](https://keepachangelog.com/en/1.0.0/).

---

## Unreleased

### Added

- First scaffold of the role, from `roles/_template` and a hand-off spec.
  It creates the datasets and the RustFS catalog app on a TrueNAS SCALE host
  through `midclt`, waits for the app to run, and probes the S3 API for the
  unsigned 403 a healthy instance returns.
- Preflight assertions for the ansible-core version, the OS family, the app
  name (including `rustfs_protected_app_names`), the dataset parent and names,
  the ports, the app values, and the TrueNAS middleware (`core.ping`).
- A preflight check of the TrueNAS release: `midclt call system.version` must not
  report CORE and must be at or above the new `rustfs_min_truenas_version`
  (default `24.10`, an assumption not yet confirmed on a real host).
- A preflight check that `rustfs_app_values` holds no `REPLACE_ME` placeholder,
  at any depth, so an unfilled vault skeleton cannot create an app with a
  placeholder login.
- A GitHub Actions workflow (`.github/workflows/ci.yml`) that lints with pre-commit
  and runs the molecule scenario on `debian-trixie` for every push to
  `ansible-core-2.20`, and a Dependabot config for the workflow's actions and the
  pre-commit hooks.
- A molecule scenario that runs the role against a mock `midclt` and a stub S3
  endpoint, because a TrueNAS host cannot be a molecule target.

### Not yet done

- The shape of `rustfs_app_values` is not defined by this role and has not been
  checked against the catalog app. See `TODO.md`.
