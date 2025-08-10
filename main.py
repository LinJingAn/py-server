"""
main.py

CLI entrypoint for the safe Hubstaff simulator.
"""

import argparse
import logging
from simulator import Simulator

LOG_FMT = "%(asctime)s %(levelname)s %(message)s"

def parse_args():
    p = argparse.ArgumentParser(description="Hubstaff Simulator (DRY-RUN safe mode)")
    p.add_argument("--duration", type=int, default=1, help="Run duration in minutes")
    p.add_argument("--tech_stack", type=str, default="html", help="Snippet stack folder to use")
    p.add_argument("--min_events", type=int, default=None, help="Override min events per minute (optional)")
    p.add_argument("--verbose", action="store_true", help="Enable DEBUG logging")
    return p.parse_args()


def main():
    args = parse_args()
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format=LOG_FMT)

    sim = Simulator(tech_stack=args.tech_stack, dry_run=True)
    if args.min_events:
        sim.min_events_per_minute = args.min_events

    try:
        sim.run(duration_minutes=args.duration)
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
