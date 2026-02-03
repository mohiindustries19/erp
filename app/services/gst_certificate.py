"""GST certificate helpers.

Extracts GSTIN/state code from a GST certificate PDF.

This is best-effort and depends on PDF text being extractable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


GSTIN_RE = re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b")


@dataclass(frozen=True)
class GstCertificateInfo:
    gstin: str

    @property
    def state_code(self) -> str:
        return self.gstin[:2]


def extract_gstin_from_pdf(pdf_path: str) -> Optional[GstCertificateInfo]:
    """Try to extract GSTIN from a PDF using `pypdf`.

    Returns None if not found.
    Raises ImportError if pypdf isn't installed.
    """

    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(pdf_path)
    text_parts: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            text_parts.append(page_text)

    text = "\n".join(text_parts)
    match = GSTIN_RE.search(text)
    if not match:
        return None

    return GstCertificateInfo(gstin=match.group(0))
