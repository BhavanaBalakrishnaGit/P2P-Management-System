from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Vendor
from app import db

vendors = Blueprint('vendors', __name__)

@vendors.route('/vendors')
@login_required
def list():
    all_vendors = Vendor.query.order_by(Vendor.vendor_name).all()
    return render_template('vendors/list.html', vendors=all_vendors)

@vendors.route('/vendors/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        # Check duplicate vendor code
        existing = Vendor.query.filter_by(
            vendor_code=request.form.get('vendor_code')
        ).first()
        if existing:
            flash('Vendor code already exists!', 'danger')
            return redirect(url_for('vendors.add'))

        vendor = Vendor(
            vendor_code   = request.form.get('vendor_code'),
            vendor_name   = request.form.get('vendor_name'),
            email         = request.form.get('email'),
            phone         = request.form.get('phone'),
            country       = request.form.get('country'),
            payment_terms = int(request.form.get('payment_terms', 30))
        )
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor added successfully!', 'success')
        return redirect(url_for('vendors.list'))
    return render_template('vendors/add.html')

@vendors.route('/vendors/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    vendor = Vendor.query.get_or_404(id)
    if request.method == 'POST':
        vendor.vendor_name   = request.form.get('vendor_name')
        vendor.email         = request.form.get('email')
        vendor.phone         = request.form.get('phone')
        vendor.country       = request.form.get('country')
        vendor.payment_terms = int(request.form.get('payment_terms', 30))
        db.session.commit()
        flash('Vendor updated successfully!', 'success')
        return redirect(url_for('vendors.list'))
    return render_template('vendors/edit.html', vendor=vendor)

@vendors.route('/vendors/<int:id>/deactivate')
@login_required
def deactivate(id):
    vendor           = Vendor.query.get_or_404(id)
    vendor.is_active = False
    db.session.commit()
    flash('Vendor deactivated!', 'warning')
    return redirect(url_for('vendors.list'))

@vendors.route('/vendors/<int:id>/activate')
@login_required
def activate(id):
    vendor           = Vendor.query.get_or_404(id)
    vendor.is_active = True
    db.session.commit()
    flash('Vendor activated!', 'success')
    return redirect(url_for('vendors.list'))

@vendors.route('/vendors/<int:id>/detail')
@login_required
def detail(id):
    vendor   = Vendor.query.get_or_404(id)
    invoices = vendor.invoices
    return render_template('vendors/detail.html',
                           vendor=vendor, invoices=invoices)