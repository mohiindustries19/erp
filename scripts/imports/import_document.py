"""One-off helper to import a file into the ERP Documents table.

Usage:
  python import_document.py --path data/Some.docx --title "Some" --category "Legal"

Safe to run multiple times: it will skip if a document with same title+filename exists.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.document import Document


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--category', default='Legal')
    parser.add_argument('--content-type', default=None)
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    data = path.read_bytes()
    content_type = args.content_type

    app = create_app()
    with app.app_context():
        existing = Document.query.filter_by(title=args.title, original_filename=path.name).first()
        if existing:
            print(f"Already exists: id={existing.id} title={existing.title!r} filename={existing.original_filename!r}")
            return 0

        doc = Document(
            title=args.title,
            category=args.category or None,
            original_filename=path.name,
            content_type=content_type,
            data=data,
        )
        db.session.add(doc)
        db.session.commit()

        print(f"Imported: id={doc.id} title={doc.title!r} filename={doc.original_filename!r}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
