"""CLI entry point. Run from the repo root: python analyze.py"""

import argparse

from src.gap_detector import detect_gaps

DEFAULTS = {
    "pdd": "sample_data/pdd_kyc_document_verification.md",
    "sdd": "sample_data/sdd_kyc_document_verification.md",
    "summary": "sample_data/meeting_summary_clarification_call.md",
}


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="Surface unresolved requirement gaps before development."
    )
    parser.add_argument("--pdd", default=DEFAULTS["pdd"])
    parser.add_argument("--sdd", default=DEFAULTS["sdd"])
    parser.add_argument("--summary", default=DEFAULTS["summary"])
    args = parser.parse_args()

    result = detect_gaps(read(args.pdd), read(args.sdd), read(args.summary))

    print(f"\n{len(result.gaps)} gaps found\n" + "=" * 70 + "\n")

    # Hedge-anchored gaps first: they carry the strongest signal
    for i, gap in enumerate(
        sorted(result.gaps, key=lambda g: not g.is_hedge_anchored), 1
    ):
        flag = "  [hedge]" if gap.is_hedge_anchored else ""
        print(f"{i}. {gap.question}{flag}")
        print(f"   {gap.rationale}")
        print(f"   Sources: {', '.join(gap.source_documents)}")
        print(f'   "{gap.supporting_quote}"\n')


if __name__ == "__main__":
    main()
