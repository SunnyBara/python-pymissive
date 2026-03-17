# attachment

Manage attachments via provider.

## Synopsis

```
pymissive attachment <subcommand> --provider <name> [options]
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `retrieve` | List attachments (use --external-id for postal) |
| `add` | Add attachment (not yet implemented) |
| `delete` | Delete attachment (requires --external-id and --document-id) |

## Required options

| Option | Description |
|--------|-------------|
| `--provider` | Provider name (e.g. maileva) |

## Optional options

| Option | Description |
|--------|-------------|
| `--external-id` | External ID (required for postal retrieve/delete) |
| `--document-id` | Document ID (required for delete) |

## Examples

```bash
pymissive attachment retrieve --provider maileva --external-id MY_ID
pymissive attachment delete --provider maileva --external-id MY_ID --document-id DOC_ID
```
