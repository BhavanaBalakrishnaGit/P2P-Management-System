from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import PurchaseOrder, POLineItem, Invoice, GoodsReceipt, Vendor
from app import db
from datetime import datetime

purchase_orders = Blueprint('purchase_orders', __name__)

@purchase_orders.route('/po')
@login_required
def list():
    all_pos = PurchaseOrder.query.order_by(
                  PurchaseOrder.created_at.desc()).all()
    return render_template('po/list.html', pos=all_pos)

@purchase_orders.route('/po/add', methods=['GET', 'POST'])
@login_required
def add():
    vendors = Vendor.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        # Check duplicate PO number
        existing = PurchaseOrder.query.filter_by(
            po_number=request.form.get('po_number')
        ).first()
        if existing:
            flash('PO number already exists!', 'danger')
            return redirect(url_for('purchase_orders.add'))

        po = PurchaseOrder(
            po_number    = request.form.get('po_number'),
            vendor_id    = request.form.get('vendor_id'),
            po_date      = datetime.strptime(
                               request.form.get('po_date'), '%Y-%m-%d'),
            total_amount = float(request.form.get('total_amount')),
            status       = 'Open'
        )
        db.session.add(po)
        db.session.commit()

        # Save line items
        descriptions = request.form.getlist('description')
        quantities   = request.form.getlist('quantity')
        unit_prices  = request.form.getlist('unit_price')

        for i in range(len(descriptions)):
            if descriptions[i]:
                line = POLineItem(
                    po_id       = po.id,
                    description = descriptions[i],
                    quantity    = float(quantities[i]),
                    unit_price  = float(unit_prices[i]),
                    total_price = float(quantities[i]) * float(unit_prices[i])
                )
                db.session.add(line)

        db.session.commit()
        flash('Purchase Order created successfully!', 'success')
        return redirect(url_for('purchase_orders.list'))
    return render_template('po/add.html', vendors=vendors)

@purchase_orders.route('/po/<int:id>/detail')
@login_required
def detail(id):
    po       = PurchaseOrder.query.get_or_404(id)
    invoice  = Invoice.query.filter_by(po_number=po.po_number).first()
    grn      = GoodsReceipt.query.filter_by(po_number=po.po_number).first()
    return render_template('po/detail.html', po=po,
                           invoice=invoice, grn=grn)

@purchase_orders.route('/po/<int:id>/close')
@login_required
def close(id):
    po        = PurchaseOrder.query.get_or_404(id)
    po.status = 'Closed'
    db.session.commit()
    flash('PO Closed!', 'success')
    return redirect(url_for('purchase_orders.list'))

@purchase_orders.route('/po/matching')
@login_required
def matching():
    results = []
    all_pos = PurchaseOrder.query.all()

    for po in all_pos:
        invoice = Invoice.query.filter_by(
                      po_number=po.po_number).first()
        grn     = GoodsReceipt.query.filter_by(
                      po_number=po.po_number).first()

        # ── Matching Logic ────────────────────────
        if not invoice:
            match_result  = 'No Invoice Found'
            match_class   = 'secondary'

        elif abs(po.total_amount - invoice.amount) > 10:
            match_result  = '2-Way Mismatch'
            match_class   = 'danger'

        elif not grn:
            match_result  = '2-Way Match (No GRN yet)'
            match_class   = 'warning'

        elif grn.received_qty != sum(
                 li.quantity for li in po.line_items):
            match_result  = '3-Way Qty Mismatch'
            match_class   = 'danger'

        else:
            match_result  = '3-Way Match Passed'
            match_class   = 'success'

        # ── Update Invoice Match Status ───────────
        if invoice:
            invoice.match_status = match_result
            db.session.commit()

        results.append({
            'po_number'   : po.po_number,
            'vendor'      : po.vendor.vendor_name,
            'po_amount'   : po.total_amount,
            'inv_number'  : invoice.invoice_number if invoice else 'N/A',
            'inv_amount'  : invoice.amount if invoice else 'N/A',
            'grn_qty'     : grn.received_qty if grn else 'N/A',
            'match_result': match_result,
            'match_class' : match_class
        })

    return render_template('po/matching.html', results=results)

@purchase_orders.route('/grn/add', methods=['GET', 'POST'])
@login_required
def add_grn():
    pos = PurchaseOrder.query.filter_by(status='Open').all()
    if request.method == 'POST':
        grn = GoodsReceipt(
            po_number     = request.form.get('po_number'),
            received_date = datetime.strptime(
                                request.form.get('received_date'), '%Y-%m-%d'),
            received_qty  = float(request.form.get('received_qty')),
            received_by   = request.form.get('received_by')
        )
        db.session.add(grn)
        db.session.commit()
        flash('Goods Receipt added successfully!', 'success')
        return redirect(url_for('purchase_orders.matching'))
    return render_template('po/add_grn.html', pos=pos)