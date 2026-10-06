from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Invoice, Vendor
from app import db
from datetime import datetime
import pandas as pd

invoices = Blueprint('invoices', __name__)

@invoices.route('/invoices')
@login_required
def list():
    all_invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return render_template('invoices/list.html', invoices=all_invoices)

@invoices.route('/invoices/add', methods=['GET', 'POST'])
@login_required
def add():
    vendors = Vendor.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        # Check duplicate invoice
        existing = Invoice.query.filter_by(
            invoice_number=request.form.get('invoice_number')
        ).first()
        if existing:
            flash('Invoice number already exists!', 'danger')
            return redirect(url_for('invoices.add'))

        invoice = Invoice(
            invoice_number = request.form.get('invoice_number'),
            vendor_id      = request.form.get('vendor_id'),
            po_number      = request.form.get('po_number'),
            invoice_date   = datetime.strptime(
                                 request.form.get('invoice_date'), '%Y-%m-%d'),
            due_date       = datetime.strptime(
                                 request.form.get('due_date'), '%Y-%m-%d'),
            amount         = float(request.form.get('amount')),
            status         = 'Submitted'
        )
        db.session.add(invoice)
        db.session.commit()
        flash('Invoice added successfully!', 'success')
        return redirect(url_for('invoices.list'))
    return render_template('invoices/add.html', vendors=vendors)

@invoices.route('/invoices/<int:id>/approve')
@login_required
def approve(id):
    invoice        = Invoice.query.get_or_404(id)
    invoice.status = 'Approved'
    db.session.commit()
    flash('Invoice Approved!', 'success')
    return redirect(url_for('invoices.list'))

@invoices.route('/invoices/<int:id>/reject')
@login_required
def reject(id):
    invoice        = Invoice.query.get_or_404(id)
    invoice.status = 'Rejected'
    db.session.commit()
    flash('Invoice Rejected!', 'warning')
    return redirect(url_for('invoices.list'))

@invoices.route('/invoices/<int:id>/paid')
@login_required
def mark_paid(id):
    invoice        = Invoice.query.get_or_404(id)
    invoice.status = 'Paid'
    db.session.commit()
    flash('Invoice Marked as Paid!', 'success')
    return redirect(url_for('invoices.list'))

@invoices.route('/invoices/<int:id>/delete')
@login_required
def delete(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    db.session.commit()
    flash('Invoice Deleted!', 'warning')
    return redirect(url_for('invoices.list'))

@invoices.route('/invoices/export')
@login_required
def export():
    all_invoices = Invoice.query.all()
    data = [{
        'Invoice No'   : i.invoice_number,
        'Vendor'       : i.vendor.vendor_name,
        'PO Number'    : i.po_number,
        'Amount'       : i.amount,
        'Status'       : i.status,
        'Match Status' : i.match_status,
        'Invoice Date' : i.invoice_date,
        'Due Date'     : i.due_date
    } for i in all_invoices]

    pd.DataFrame(data).to_excel('output/invoices_export.xlsx', index=False)
    flash('Exported to Excel successfully!', 'success')
    return redirect(url_for('invoices.list'))