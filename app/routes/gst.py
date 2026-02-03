"""GST Routes - eInvoice, eWay Bill, GSTR filings."""

import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models.company import Company
from app.services.gst_certificate import extract_gstin_from_pdf
from app.services.permissions import role_required
from app.services.gst_service import get_gst_service
import json

bp = Blueprint('gst', __name__, url_prefix='/gst')


@bp.route('/dashboard')
@login_required
def dashboard():
    gst = get_gst_service()
    company = Company.query.first()
    certificate_url = url_for('static', filename='docs/MOHI_GST_CERTIFICATE.pdf')
    return render_template('gst/dashboard.html',
                         provider=gst.provider,
                         sandbox=gst.sandbox,
                         configured=gst.is_configured(),
                         company=company,
                         certificate_url=certificate_url)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def settings():
    """Admin GST settings (Company GSTIN/state code) + certificate extraction."""

    company = Company.query.first()
    if not company:
        default_gstin = os.environ.get('COMPANY_GSTIN', '10GANPS5418H1ZJ')
        default_pan = os.environ.get('COMPANY_PAN', 'UNKNOWN')
        default_state_code = os.environ.get('COMPANY_STATE_CODE')
        default_fssai = os.environ.get('FSSAI_LICENSE', '10423110000282')
        company = Company(
            name='Mohi Industries',
            gstin=default_gstin,
            pan=default_pan,
            fssai_license=default_fssai,
            state_code=default_state_code,
        )
        db.session.add(company)
        db.session.commit()

    certificate_url = url_for('static', filename='docs/MOHI_GST_CERTIFICATE.pdf')
    certificate_fs_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'static',
        'docs',
        'MOHI_GST_CERTIFICATE.pdf',
    )

    extracted_gstin = None

    if request.method == 'POST':
        action = (request.form.get('action') or 'save').strip().lower()
        try:
            if action == 'extract':
                info = extract_gstin_from_pdf(certificate_fs_path)
                if not info:
                    flash('Could not find a GSTIN in the certificate PDF.', 'error')
                else:
                    extracted_gstin = info.gstin
                    company.gstin = info.gstin
                    company.state_code = info.state_code
                    db.session.commit()
                    flash(f'Updated GSTIN from certificate: {info.gstin}', 'success')
            else:
                gstin = (request.form.get('gstin') or '').strip().upper()
                state_code = (request.form.get('state_code') or '').strip()
                if gstin:
                    company.gstin = gstin
                if state_code:
                    company.state_code = state_code
                db.session.commit()
                flash('GST settings saved.', 'success')

            return redirect(url_for('gst.settings'))

        except ImportError:
            db.session.rollback()
            flash('PDF extraction requires pypdf. Install dependencies and try again.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating GST settings: {str(e)}', 'error')

    return render_template(
        'gst/settings.html',
        company=company,
        certificate_url=certificate_url,
        extracted_gstin=extracted_gstin,
    )


@bp.route('/validate-gstin', methods=['GET', 'POST'])
@login_required
def validate_gstin():
    result = None
    if request.method == 'POST':
        gstin = request.form.get('gstin')
        result = get_gst_service().validate_gstin(gstin)
        if result.get('success') is False:
            flash(result.get('error'), 'error')
    return render_template('gst/validate_gstin.html', result=result)


@bp.route('/einvoice', methods=['GET', 'POST'])
@login_required
def einvoice():
    result = None
    if request.method == 'POST':
        payload = request.form.get('invoice_json')
        try:
            invoice_data = json.loads(payload) if payload else {}
            result = get_gst_service().generate_einvoice(invoice_data)
            if result.get('success') is False:
                flash(result.get('error'), 'error')
        except json.JSONDecodeError:
            flash('Invalid JSON payload.', 'error')
    return render_template('gst/einvoice.html', result=result)


@bp.route('/eway-bill', methods=['GET', 'POST'])
@login_required
def eway_bill():
    result = None
    if request.method == 'POST':
        payload = request.form.get('shipment_json')
        try:
            shipment_data = json.loads(payload) if payload else {}
            result = get_gst_service().generate_eway_bill(shipment_data)
            if result.get('success') is False:
                flash(result.get('error'), 'error')
        except json.JSONDecodeError:
            flash('Invalid JSON payload.', 'error')
    return render_template('gst/eway_bill.html', result=result)


@bp.route('/gstr1', methods=['GET', 'POST'])
@login_required
def gstr1():
    result = None
    if request.method == 'POST':
        period = request.form.get('period')
        payload = request.form.get('invoices_json')
        try:
            invoices = json.loads(payload) if payload else []
            result = get_gst_service().file_gstr1(period, invoices)
            if result.get('success') is False:
                flash(result.get('error'), 'error')
        except json.JSONDecodeError:
            flash('Invalid JSON payload.', 'error')
    return render_template('gst/gstr1.html', result=result)


@bp.route('/gstr3b', methods=['GET', 'POST'])
@login_required
def gstr3b():
    result = None
    if request.method == 'POST':
        period = request.form.get('period')
        payload = request.form.get('summary_json')
        try:
            summary = json.loads(payload) if payload else {}
            result = get_gst_service().file_gstr3b(period, summary)
            if result.get('success') is False:
                flash(result.get('error'), 'error')
        except json.JSONDecodeError:
            flash('Invalid JSON payload.', 'error')
    return render_template('gst/gstr3b.html', result=result)


@bp.route('/reconcile-2b', methods=['GET', 'POST'])
@login_required
def reconcile_2b():
    result = None
    if request.method == 'POST':
        period = request.form.get('period')
        result = get_gst_service().reconcile_2b(period)
        if result.get('success') is False:
            flash(result.get('error'), 'error')
    return render_template('gst/reconcile_2b.html', result=result)
