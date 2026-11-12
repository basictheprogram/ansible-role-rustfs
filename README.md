# ansible-role-rustfs

Ansible role that creates and maintains a [RustFS](https://rustfs.com) (S3-compatible
object store) catalog app on a TrueNAS SCALE host, through `midclt`: the datasets it
stores data in, the app with its ports and values, and a check that the S3 API answers.

It is built for standing up a second instance next to a running one, so it is
conservative: it refuses to manage protected app names, never touches a dataset or
app that already matches, and never prints credentials.

## What it does

Layer 1, the TrueNAS side:

1. Creates the datasets under `rustfs_dataset_parent` that do not exist yet.
2. Creates the catalog app, or updates it only when a value the role enforces
   differs. A healthy app that already matches is not touched or restarted.
3. Waits until the app reports `RUNNING`.
4. Sends an unsigned request to the S3 API and expects a `403`, which is what a
   healthy RustFS answers.

## What it does not do

Layer 2, the contents of RustFS (buckets, access keys, IAM policies), lives inside
RustFS and is not managed here. Create it by hand in the RustFS console, with
credentials of its own for each instance; never reuse another instance's.

Also out of scope, so they are your follow-up checklist after a first run:

* DNS for the instance's hostname.
* The reverse proxy route to the S3 API port. Route the S3 API only, never the
  console.
* Firewall rules. Do not publish the S3 or console port on a VIP.
* The settings of the applications that use the store.
* Copying test data in.

## Requirements

- ansible-core >= 2.20
- Run against the TrueNAS host itself, with a user that can `become` root: `midclt`
  needs root.
- No collections.

## Supported platforms

| Platform | Versions |
|----------|----------|
| TrueNAS SCALE / Community Edition (Debian-based, Docker-based apps) | 24.10 or newer, an assumption not yet confirmed on a real host (`rustfs_min_truenas_version`); CORE is refused |

## Role variables

All of the variables below are in `defaults/main.yml`. Those marked required fail
the preflight until you set them.

| Variable | Default | Description |
|----------|---------|-------------|
| `rustfs_app_name` | `""` (required) | App instance name: lowercase letters, digits, hyphens. |
| `rustfs_dataset_parent` | `""` (required) | Parent dataset, for example `tank/apps`. No leading or trailing slash. |
| `rustfs_dataset_names` | `["{{ rustfs_app_name }}"]` | Datasets created under the parent. |
| `rustfs_dataset_options` | `{}` | Extra `pool.dataset.create` parameters. |
| `rustfs_s3_port` | `0` (required) | S3 API port the app publishes. |
| `rustfs_console_port` | `0` (required) | Console port. Must differ from the S3 port. |
| `rustfs_app_values` | `{}` (required) | The `values` the catalog app is created with and kept at. |
| `rustfs_catalog_app` | `rustfs` | Catalog app to install. |
| `rustfs_train` | `community` | Catalog train. |
| `rustfs_app_version` | `latest` | Applied when the app is created; an existing app is never moved. |
| `rustfs_protected_app_names` | `[rustfs]` | Names the role refuses to manage. `[]` allows an app named `rustfs`. |
| `rustfs_min_truenas_version` | `24.10` | Oldest TrueNAS release the role runs on. CORE is always refused. |
| `rustfs_probe_host` | the host's address | Where the unsigned probe connects. |
| `rustfs_probe_expected_status` | `403` | The status a healthy S3 API answers. |
| `rustfs_wait_retries`, `rustfs_wait_delay` | `30`, `10` | How long to wait for `RUNNING` and for the probe. |

### `rustfs_app_values`

The shape of the values belongs to the catalog app, so this role does not define it.
Take it from an existing instance, on the TrueNAS shell:

```bash
midclt call app.query '[["name","=","<existing app>"]]' '{"extra":{"retrieve_config":true}}'
```

The output includes the root credentials: do not paste it into chat, a ticket or a
commit. Copy the structure only, replace the credentials with vault variables, and
set the ports and paths for the new instance. Every key you list is enforced on every
run; a key you leave out is left as TrueNAS has it.

## Task flow

1. **Preflight** (`tasks/preflight.yml`, tag `always`): ansible-core >= 2.20, a
   Debian-family host, a well-formed app name that is not protected, a usable dataset
   parent and names, two distinct ports in 1024 to 65535, non-empty app values with
   no `REPLACE_ME` placeholder left in them, `midclt call core.ping` answering
   `pong`, and `midclt call system.version` reporting a non-CORE release at or above
   `rustfs_min_truenas_version`.
2. **Datasets** (`tasks/dataset.yml`): look each one up, create the missing ones.
3. **App** (`tasks/app.yml`): look it up, create it, update it when values differ,
   wait for `RUNNING`. Every task that carries the config uses `no_log`.
4. **Verify** (`tasks/verify.yml`): the unsigned S3 probe.

In check mode the lookups run and the changes, the wait and the probe do not.

## Example playbook

```yaml
- hosts: truenas.example.com
  become: true
  roles:
    - role: realtime.rustfs
      vars:
        rustfs_app_name: rustfs-stage
        rustfs_dataset_parent: tank/apps
        rustfs_s3_port: 40292
        rustfs_console_port: 40293
        rustfs_app_values:
          # Copied from an existing instance; credentials come from the vault.
          # <the catalog app's structure>
```

## Testing

A TrueNAS host cannot be a molecule target. The molecule scenario runs the role in a
Debian container against a mock `midclt` that keeps its state in a JSON file, and a
stub endpoint that answers every request with `403`. Molecule runs in CI only;
locally, use `pre-commit`, `molecule syntax` and `pytest --collect-only`.

## License

[MIT](LICENSE)

## Author information

- Bob Tanner
