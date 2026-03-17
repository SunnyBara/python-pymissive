# recipient

Validate and format recipient data.

## Synopsis

```
pymissive recipient <subcommand> --recipients '<json>' [options]
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `validate` | Validate recipients (keeps only valid email/phone/address objects) |
| `format` | Format recipients as pretty JSON |

## Required options

| Option | Description |
|--------|-------------|
| `--recipients` | JSON array of recipients |

## Recipient format

- **Email**: `{"email": "x@y.com", "name": "John"}`
- **Phone**: `{"phone": "+33612345678", "name": "Jane"}`
- **Address**: `{"address": {"address_line1": "...", "city": "...", "postal_code": "...", "country": "France"}}`

## Examples

```bash
pymissive recipient validate --recipients '[{"email":"user@example.com"}]'
pymissive recipient format --recipients '[{"email":"a@b.com"},{"phone":"+33612345678"}]'
```
