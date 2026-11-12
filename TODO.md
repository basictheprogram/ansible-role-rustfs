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
  the TrueNAS version and the `midclt` call forms (`app.create`, `app.update` with
  `-job`), whether `app.update` merges or replaces values, that a second instance
  installs beside the first, and the right dataset options.
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
- [ ] **Check whether the `arensb.truenas` collection has an apps module** now. If it
  does, the app tasks could use it instead of `midclt`.
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
