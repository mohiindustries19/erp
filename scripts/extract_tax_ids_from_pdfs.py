from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

GSTIN_RE = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}\b")
# FSSAI is typically 14 digits in India
FSSAI_RE = re.compile(r"\b\d{14}\b")


def extract_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            parts.append("")
    return "\n".join(parts)


def find_ids(text: str) -> tuple[list[str], list[str]]:
    gstins = sorted(set(GSTIN_RE.findall(text)))
    fssai = sorted(set(FSSAI_RE.findall(text)))

    # Reduce false positives for FSSAI by requiring nearby keyword if there are many numbers.
    if len(fssai) > 5:
        narrowed: set[str] = set()
        for m in FSSAI_RE.finditer(text):
            start = max(0, m.start() - 50)
            end = min(len(text), m.end() + 50)
            window = text[start:end].lower()
            if "fssai" in window or "licence" in window or "license" in window:
                narrowed.add(m.group(0))
        if narrowed:
            fssai = sorted(narrowed)

    return gstins, fssai


def main() -> int:
    pdfs = [
        Path(r"d:/OtherRepos/mohierp/mohi-erp/data/Fassai Mihi.pdf"),
        Path(r"d:/OtherRepos/mohierp/mohi-erp/data/MOHI GST CERTIFICATE.pdf"),
    ]

    for pdf in pdfs:
        print(f"\n=== {pdf.name} ===")
        if not pdf.exists():
            print("MISSING")
            continue
        text = extract_text(pdf)
        gstins, fssai = find_ids(text)
        print("GSTIN:", ", ".join(gstins) if gstins else "(none found)")
        print("FSSAI:", ", ".join(fssai) if fssai else "(none found)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
