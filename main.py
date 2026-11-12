"""Remind which SSL certificates need renewal, and who to tell.

Usage: python3 main.py certs.csv [--as-of 2026-11-08]
CSV columns: domain,expiry_date (ISO, e.g. 2027-01-15),contact_email.
EXPIRED: the expiry date already passed.
RENEW NOW: expires within 14 days.
RENEW SOON: expires within 30 days.
OK: more than 30 days left.
Soonest expiry first, so the most urgent reminder is on top.
"""
import argparse, csv, sys
from datetime import date

RENEW_NOW_DAYS = 14
RENEW_SOON_DAYS = 30

def remind(rows, as_of=None):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        expiry = date.fromisoformat(row["expiry_date"].strip())
        days_left = (expiry - as_of).days
        if days_left < 0:
            verdict = "EXPIRED"
        elif days_left <= RENEW_NOW_DAYS:
            verdict = "RENEW NOW"
        elif days_left <= RENEW_SOON_DAYS:
            verdict = "RENEW SOON"
        else:
            verdict = "OK"
        out.append((row["domain"].strip(), expiry.isoformat(), days_left,
                    verdict, row["contact_email"].strip()))
    return sorted(out, key=lambda r: r[2])

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = remind(list(csv.DictReader(f)), as_of)
    for domain, expiry, days_left, verdict, contact in results:
        when = f"{abs(days_left)} days ago" if days_left < 0 else f"in {days_left} days"
        print(f"{domain}: {verdict} (expires {expiry}, {when}; notify {contact})")
    print(f"{sum(1 for *_, v, _ in results if v != 'OK')} certificate(s) need attention.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
