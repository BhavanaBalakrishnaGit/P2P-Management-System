from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Invoice, Vendor, PurchaseOrder
from datetime import date

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    # ── KPI Numbers ──────────────────────────
    total_invoices   = Invoice.query.count()
    total_vendors    = Vendor.query.filter_by(is_active=True).count()
    total_pos        = PurchaseOrder.query.count()
    pending_invoices = Invoice.query.filter_by(status='Submitted').count()

    # ── Approval Rate ────────────────────────
    approved      = Invoice.query.filter_by(status='Approved').count()
    approval_rate = round((approved / total_invoices * 100), 1) \
                    if total_invoices > 0 else 0

    # ── Overdue Invoices ─────────────────────
    overdue = Invoice.query.filter(
                  Invoice.due_date < date.today(),
                  Invoice.status != 'Paid'
              ).count()

    # ── Recent Invoices ──────────────────────
    recent_invoices = Invoice.query.order_by(
                          Invoice.created_at.desc()
                      ).limit(5).all()

    # ── Invoice Status Counts for Chart ──────
    approved_count = Invoice.query.filter_by(status='Approved').count()
    rejected_count = Invoice.query.filter_by(status='Rejected').count()
    pending_count  = Invoice.query.filter_by(status='Submitted').count()
    paid_count     = Invoice.query.filter_by(status='Paid').count()

    return render_template('dashboard.html',
        total_invoices   = total_invoices,
        total_vendors    = total_vendors,
        total_pos        = total_pos,
        pending_invoices = pending_invoices,
        approval_rate    = approval_rate,
        overdue          = overdue,
        recent_invoices  = recent_invoices,
        approved_count   = approved_count,
        rejected_count   = rejected_count,
        pending_count    = pending_count,
        paid_count       = paid_count
    )