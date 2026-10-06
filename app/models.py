from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50), unique=True)
    password   = db.Column(db.String(200))
    role       = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.now)

class Vendor(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    vendor_code   = db.Column(db.String(20), unique=True)
    vendor_name   = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(100))
    phone         = db.Column(db.String(20))
    country       = db.Column(db.String(50))
    payment_terms = db.Column(db.Integer, default=30)
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.now)
    invoices        = db.relationship('Invoice', backref='vendor', lazy=True)
    purchase_orders = db.relationship('PurchaseOrder', backref='vendor', lazy=True)

class PurchaseOrder(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    po_number    = db.Column(db.String(50), unique=True)
    vendor_id    = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    po_date      = db.Column(db.Date)
    total_amount = db.Column(db.Float)
    status       = db.Column(db.String(20), default='Open')
    created_at   = db.Column(db.DateTime, default=datetime.now)
    line_items   = db.relationship('POLineItem', backref='po', lazy=True)

class POLineItem(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    po_id       = db.Column(db.Integer, db.ForeignKey('purchase_order.id'))
    description = db.Column(db.String(200))
    quantity    = db.Column(db.Float)
    unit_price  = db.Column(db.Float)
    total_price = db.Column(db.Float)

class Invoice(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True)
    vendor_id      = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    po_number      = db.Column(db.String(50))
    invoice_date   = db.Column(db.Date)
    due_date       = db.Column(db.Date)
    amount         = db.Column(db.Float)
    status         = db.Column(db.String(20), default='Submitted')
    match_status   = db.Column(db.String(30), default='Pending')
    created_at     = db.Column(db.DateTime, default=datetime.now)

class GoodsReceipt(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    po_number     = db.Column(db.String(50))
    received_date = db.Column(db.Date)
    received_qty  = db.Column(db.Float)
    received_by   = db.Column(db.String(50))
    created_at    = db.Column(db.DateTime, default=datetime.now)