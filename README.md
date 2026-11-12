# ssl-cert-renewal-reminder

Remind which SSL certificates need renewal from a CSV: EXPIRED when past the date, RENEW NOW within 14 days, RENEW SOON within 30 days, otherwise OK — soonest expiry first, with the contact to notify.

## How to run

```sh
python3 main.py certs.csv --as-of 2026-11-08
```

## Example output

```
old.example: EXPIRED (expires 2026-11-01, 7 days ago; notify admin@example.com)
shop.example: RENEW NOW (expires 2026-11-18, in 10 days; notify admin@example.com)
2 certificate(s) need attention.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
