# TODO — ansible-role-rustfs

Items from scaffolding the role (2026-11-12) that were not resolved. The role's
logic was exercised against a mock `midclt` in the devcontainer: first run creates
the dataset and app, a second run changes nothing, a changed value triggers one
update, the preflight refuses bad input, and no value is printed. Nothing has run
against a real TrueNAS host.

- [ ] **Read the catalog app's `values` shape from a running instance** and set
  `rustfs_app_values` for the new one. Without it the preflight stops the role, on
  purpose. See the README, "`rustfs_app_values`". Do not paste the output anywhere:
  it contains the root credentials.
- [ ] **Confirm the unknowns in `DESIGN.md`, "Open questions"** on the real host:
  the `midclt` call forms (`app.create`, `app.update` with `-job`), whether
  `app.update` merges or replaces values, that a second instance installs beside the
  first, and the right dataset options.
- [ ] **Confirm the TrueNAS version check on the real host.** `midclt call
  system.version` is assumed to return a string such as `TrueNAS-SCALE-24.10.2.1` or
  `TrueNAS-25.04.2.1`, and 24.10 is assumed to be the first release with the `app.*`
  calls. Check both, and adjust `rustfs_min_truenas_version` if needed. The mock
  returns `TrueNAS-SCALE-25.04.2.1`.
- [ ] **Test on the actual release, and again after a TrueNAS upgrade.** The
  `arensb.truenas` changelog shows the middleware API changing between 25.04 and
  25.10, and the `app.*` calls here could change too.
- [ ] **Watch `arensb.truenas` pull requests #32 (an `app` module) and #63 (a raw
  middleware-call module).** If either is merged, revisit using it; see `DESIGN.md`,
  "Prior art". Optionally test #32 on the real host and report back.
- [ ] **Pin the RustFS version** with `rustfs_app_version` to match the running
  instance, instead of `latest`.
- [ ] **Molecule has not run.** Molecule runs in CI only (disk use), and this role has
  no CI yet, so the scenario has been checked statically (`molecule syntax`,
  `pytest --collect-only`, pre-commit) but never executed. Add
  `.github/workflows/ci.yml` (the logrotate role's is a model: one platform,
  `debian-trixie`), create the GitHub repo, and push; the first CI run is the first
  molecule run. Add `.github/dependabot.yml` too if you want action and hook updates.
- [ ] **The GitHub repo does not exist yet.** `meta/main.yml`'s `issue_tracker_url`
  points at `basictheprogram/ansible-role-rustfs`, the name the repo should have.
- [ ] **Nothing uses the role yet.** A playbook and the site's host variables
  (vault variables for the credentials, the values from the running instance) belong
  in the site repo, not here.
- [ ] **Layer 2 is manual.** Buckets, access keys and IAM policies for the new
  instance are created in the RustFS console. Whether RustFS has a scriptable admin
  API was not checked.
- [ ] **No automated negative test for the preflight.** The refusals were checked by
  hand against the mock, not in molecule.
- [ ] **No `meta/argument_specs.yml`.** The variables are documented in the README
  and checked by the preflight.
- [ ] **Skill/repo conflict on the company name.** `ansible-sync-role` Steps 5 and 5b
  say to set a company in `meta/main.yml` and add it to the LICENSE copyright line.
  Both were left out, as in the logrotate role. Update the skill, or the next sync
  will ask again.
