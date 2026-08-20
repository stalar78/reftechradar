from __future__ import annotations

import argparse

from reftechradar.application.service import run_fixture_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the RefTechRadar fixture pipeline.")
    parser.add_argument("--db", default="data/reftechradar.sqlite3", help="SQLite database path.")
    parser.add_argument("--out", default="reports", help="Report output directory.")
    parser.add_argument("--cycle", type=int, default=1, help="Fixture cycle number.")
    args = parser.parse_args()

    result = run_fixture_pipeline(db_path=args.db, output_dir=args.out, cycle=args.cycle)
    summary = result.report["summary"]
    print("RefTechRadar fixture run complete")
    print(f"Found: {summary['found']}")
    print(f"Rejected automatically: {summary['rejected_automatically']}")
    print(f"Low match: {summary['low_match']}")
    print(f"Maybe: {summary['maybe']}")
    print(f"Strong Match: {summary['strong_match']}")
    print(f"New Strong Match: {summary['new_strong_match']}")
    print(f"Markdown: {result.markdown_path}")
    print(f"JSON: {result.json_path}")


if __name__ == "__main__":
    main()
