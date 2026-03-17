# billing

Retrieve billing/usage data from provider.

## Synopsis

```
pymissive billing retrieve --provider <name> [--external-id ID]
```

## Required options

| Option | Description |
|--------|-------------|
| `--provider` | Provider name (e.g. maileva) |

## Optional options

| Option | Description |
|--------|-------------|
| `--type` | Missive type (default: postal) |
| `--external-id` | External ID for provider-specific billing |
| `--dir` | Provider config directory |
| `--json` | Path to provider config JSON |

## Examples

```bash
pymissive billing retrieve --provider maileva
pymissive billing retrieve --provider maileva --external-id MY_ID
```
