"""CLI entry point. Run from the repo root: python analyze.py"""

import argparse
import os

from src.gap_detector import Document, detect_gaps

SAMPLES = {
    "business": ["sample_data/pdd_kyc_document_verification.md"],
    "design": ["sample_data/sdd_kyc_document_verification.md"],
    "meeting": ["sample_data/meeting_summary_clarification_call.md"],
}


def load(paths, role):
    docs = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            docs.append(Document(os.path.basename(path), role, f.read()))
    return docs


def main():
    parser = argparse.ArgumentParser(
        description="Surface unresolved requirement gaps before development."
    )
    parser.add_argument("--business", nargs="*", default=SAMPLES["business"])
    parser.add_argument("--design", nargs="*", default=SAMPLES["design"])
    parser.add_argument("--meeting", nargs="*", default=SAMPLES["meeting"])
    parser.add_argument("--supporting", nargs="*", default=[])
    args = parser.parse_args()

    documents = (
        load(args.business, "business")
        + load(args.design, "design")
        + load(args.meeting, "meeting")
        + load(args.supporting, "supporting")
    )

    result = detect_gaps(documents)

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