"""Documents module (upload/download).

DB-backed to work reliably on Railway where container filesystem is ephemeral.
"""

from __future__ import annotations

from io import BytesIO
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from app import db
from app.models.document import Document
from app.services.permissions import role_required


bp = Blueprint('documents', __name__, url_prefix='/documents')


@bp.route('/')
@login_required
@role_required(['admin'])
def index():
    category = (request.args.get('category') or '').strip()
    q = (request.args.get('q') or '').strip()

    query = Document.query
    if category:
        query = query.filter(Document.category == category)
    if q:
        like = f"%{q}%"
        query = query.filter(Document.title.ilike(like))

    documents = query.order_by(Document.created_at.desc()).all()
    categories = [r[0] for r in db.session.query(Document.category).distinct().order_by(Document.category).all() if r[0]]

    return render_template(
        'documents/index.html',
        documents=documents,
        categories=categories,
        selected_category=category,
        q=q,
    )


@bp.route('/upload', methods=['POST'])
@login_required
@role_required(['admin'])
def upload():
    title = (request.form.get('title') or '').strip()
    category = (request.form.get('category') or '').strip() or None

    file = request.files.get('file')
    if not title:
        flash('Title is required.', 'error')
        return redirect(url_for('documents.index'))
    if not file or not file.filename:
        flash('Please choose a file to upload.', 'error')
        return redirect(url_for('documents.index'))

    data = file.read()
    if not data:
        flash('Uploaded file is empty.', 'error')
        return redirect(url_for('documents.index'))

    doc = Document(
        title=title,
        category=category,
        original_filename=file.filename,
        content_type=file.mimetype,
        data=data,
        uploaded_by=getattr(current_user, 'id', None),
        created_at=datetime.utcnow(),
    )

    db.session.add(doc)
    db.session.commit()

    flash('Document uploaded successfully.', 'success')
    return redirect(url_for('documents.index'))


@bp.route('/<int:doc_id>/download')
@login_required
@role_required(['admin'])
def download(doc_id: int):
    doc = Document.query.get_or_404(doc_id)

    return send_file(
        BytesIO(doc.data),
        mimetype=doc.content_type or 'application/octet-stream',
        as_attachment=True,
        download_name=doc.original_filename or f"document-{doc.id}",
    )


@bp.route('/<int:doc_id>/delete', methods=['POST'])
@login_required
@role_required(['admin'])
def delete(doc_id: int):
    doc = Document.query.get_or_404(doc_id)
    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted.', 'success')
    return redirect(url_for('documents.index'))
