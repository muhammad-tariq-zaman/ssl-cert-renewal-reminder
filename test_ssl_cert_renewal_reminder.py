import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import remind

import datetime
AS_OF = datetime.date(2026, 11, 8)

def row(d, expiry, contact="admin@example.com"):
    return {"domain": d, "expiry_date": expiry, "contact_email": contact}

class TestCertRenewalReminder(unittest.TestCase):
    def test_expired(self):
        self.assertEqual(remind([row("a.example", "2026-11-01")], AS_OF)[0][3], "EXPIRED")
    def test_renew_now(self):
        self.assertEqual(remind([row("a.example", "2026-11-18")], AS_OF)[0][3], "RENEW NOW")
    def test_renew_now_boundary_14_days(self):
        self.assertEqual(remind([row("a.example", "2026-11-22")], AS_OF)[0][3], "RENEW NOW")
    def test_renew_soon(self):
        self.assertEqual(remind([row("a.example", "2026-12-01")], AS_OF)[0][3], "RENEW SOON")
    def test_renew_soon_boundary_30_days(self):
        self.assertEqual(remind([row("a.example", "2026-12-08")], AS_OF)[0][3], "RENEW SOON")
    def test_ok(self):
        self.assertEqual(remind([row("a.example", "2027-06-01")], AS_OF)[0][3], "OK")
    def test_days_left_computed(self):
        self.assertEqual(remind([row("a.example", "2026-11-18")], AS_OF)[0][2], 10)
    def test_soonest_first(self):
        r = remind([row("late.example", "2027-06-01"), row("soon.example", "2026-11-18")], AS_OF)
        self.assertEqual(r[0][0], "soon.example")
