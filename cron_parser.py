#!/usr/bin/env python3
"""cron_parser - Cron expression parser with next-run calculation."""
import sys, re
from datetime import datetime, timedelta

class CronExpr:
    def __init__(self, expr):
        parts = expr.split()
        assert len(parts) == 5
        self.minute = self._parse(parts[0],0,59)
        self.hour = self._parse(parts[1],0,23)
        self.dom = self._parse(parts[2],1,31)
        self.month = self._parse(parts[3],1,12)
        self.dow = self._parse(parts[4],0,6)
    def _parse(self, field, lo, hi):
        vals = set()
        for part in field.split(","):
            if part == "*": return set(range(lo, hi+1))
            m = re.match(r'\*/(\d+)', part)
            if m: vals.update(range(lo, hi+1, int(m.group(1)))); continue
            m = re.match(r'(\d+)-(\d+)', part)
            if m: vals.update(range(int(m.group(1)), int(m.group(2))+1)); continue
            vals.add(int(part))
        return vals
    def matches(self, dt):
        return dt.minute in self.minute and dt.hour in self.hour and dt.day in self.dom and dt.month in self.month
    def next_run(self, after=None):
        dt = (after or datetime.now()).replace(second=0, microsecond=0) + timedelta(minutes=1)
        for _ in range(525600):
            if self.matches(dt): return dt
            dt += timedelta(minutes=1)
        return None

def main():
    now = datetime(2026, 3, 29, 8, 0)
    print("Cron parser demo\n")
    for expr, desc in [("*/15 * * * *","every 15m"),("0 9 * * *","daily 9am"),("30 */2 * * *","2h at :30"),("0 0 1 * *","monthly")]:
        c = CronExpr(expr)
        nxt = c.next_run(now)
        print(f"  {expr:20s} ({desc}): next={nxt.strftime('%m/%d %H:%M')}")

if __name__ == "__main__":
    main()
