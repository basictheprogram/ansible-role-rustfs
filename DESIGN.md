# Design: realtime.rustfs

The spec for the role, written from the hand-off that started it. If the code
disagrees with this file, this file is right: flag the discrepancy and ask.

## Why

A RustFS instance that was a non-production store passed QA and was promoted to
production. The non-production environment is left pointing at production's store.
Until it has an instance of its own, both share one bucket set and one key set, and
an object key that contains a database id can collide if non-production data came
from a production copy. The role stands up a separate instance, next to the running
one, without touching it.

## Two layers

**Layer 1, TrueNAS (this role).**

1. Create the dataset or datasets for the instance under the same pool and parent as
   the running instance, with a clear name. Never touch the running instance's.
2. Create the catalog app (`app.create`, `catalog_app: rustfs`, `train: community`)
   with its S3 and console ports, its datasets and new root credentials.
3. Be idempotent: look the app up by name first, create when missing, update only
   when values differ, change nothing on a re-run, never restart a healthy app.
4. Wait for the app to report running, then probe the S3 port: an unsigned request
   must return 403.
5. `no_log: true` on every task that carries credentials.

**Layer 2, RustFS contents (not this role).** Buckets, access keys and IAM policies
live inside RustFS and are created in its console. The shapes are the same as the
running instance's, with keys of its own. Whether RustFS has a scriptable admin API
for this has not been checked. Do not pull `mc` or other admin tools from a public
registry for it: they would handle admin credentials.

## Settled decisions

* **Catalog app driven through `midclt`**, not a custom Docker Compose app. The catalog
  app matches what the running instance uses and what the TrueNAS UI manages.
* **`midclt`, not the REST API.** The REST API is deprecated and being removed.
* **A new role, `realtime.rustfs`**, not a task file of a wider `truenas` role. Nothing
  for TrueNAS existed in the playbooks repo when it was created.
* **Credentials come from vault variables** the consumer references inside
  `rustfs_app_values`; the role has no credential variables of its own and uses
  `no_log` wherever the config passes through.
* **Protected app names.** The role refuses to manage an app named in
  `rustfs_protected_app_names` (default `rustfs`, the running instance's name), so a
  mistaken `rustfs_app_name` cannot touch production.
* **Required variables have no defaults.** App name, dataset parent, the two ports and
  the app values are unset by default and enforced by the preflight.
* **Existing datasets are never modified** and an existing app is never moved to
  another catalog version or train.
* **Molecule against a mock.** A TrueNAS host cannot be a molecule target, so the
  scenario uses a mock `midclt` and a stub 403 endpoint. A manual check list covers
  the real host.

## Open questions

If a task touches one of these, leave a `# TODO(open-q):` comment.

1. **The shape of `rustfs_app_values`** has not been read from the catalog app. It
   must be taken from a running instance (see the README) before the first real run.
2. **TrueNAS version.** Which releases support the `app.*` calls as the role uses
   them, and the exact `-job` and argument forms, are unconfirmed.
3. **`app.update` semantics:** whether it merges the supplied values into the stored
   ones or replaces them. The role assumes merge and enforces only the keys it is
   given.
4. **Whether a second instance of the catalog app can be installed beside the first**
   without a port or dataset collision.
5. **Version matching.** The new instance should run the same RustFS version as the
   running one, so non-production tests what production runs. Set
   `rustfs_app_version` explicitly; `latest` does not guarantee a match.
6. **An apps module.** The `arensb.truenas` collection had no apps module when this
   was written; confirm against its current release. If there is one, the app tasks
   could use it.
7. **Dataset create options** (such as an apps share type) are passed through
   `rustfs_dataset_options`; the right defaults are unknown.

## Must not

* Change the running instance's app, datasets, keys or policies.
* Use the running instance's keys, or any root login, in the new instance.
* Put credentials in a playbook, a commit, a log or a pasted command.
* Route the console port through a proxy or publish either port on a VIP.
* Push to any remote: the maintainer pushes.

## Done when

* `midclt call app.query '[["name","=","<instance>"]]'` shows the app running, and
  the running instance is untouched: same state, same ports, same data.
* An unsigned request to the new S3 port returns 403.
* A second run of the playbook reports no changes.
* No credential appears in the playbook output, the repo or the role's logs.
