# 🔄 P2P Management System

A full-stack **Procure-to-Pay (P2P) Web Application** built with Python Flask and SQLite — designed to manage the complete invoice lifecycle from purchase order creation to payment.

---

## 🎯 About This Project

This project was built to demonstrate real-world P2P domain knowledge combined with Python web development skills. It replicates core features found in enterprise P2P systems like SAP, Oracle, and Accenture's internal tools.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 🔐 Login System | Secure authentication with password hashing |
| 📊 KPI Dashboard | Real-time charts showing invoice status |
| 🧾 Invoice Management | Add, Approve, Reject, Pay, Export to Excel |
| 🏢 Vendor Management | Add, Edit, Activate/Deactivate vendors |
| 📦 Purchase Orders | Create POs with multiple line items |
| ✅ PO Matching Engine | Automated 2-way & 3-way matching |
| 📬 Goods Receipt (GRN) | Record and verify goods received |
| 📈 Excel Export | One-click export using Pandas |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Web Framework | Flask |
| Database | SQLite |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Frontend | HTML5, Bootstrap 5 |
| Charts | Chart.js |
| Icons | Font Awesome |
| Excel Export | Pandas, Openpyxl |

---

## 📊 P2P Flow Covered
Purchase Order Created

↓

Goods Receipt Recorded (GRN)

↓

Invoice Submitted by Vendor

↓

2-Way Match → PO ↔ Invoice

↓

3-Way Match → PO ↔ Invoice ↔ GRN

↓

Invoice Approved & Payment Released

---

## ⚙️ How to Run Locally

### Step 1 — Clone the repository
git clone https://github.com/BhavanaBalakrishnaGit/P2P-Management-System.git

cd P2P-Management-System

### Step 2 — Create virtual environment
python -m venv venv

venv\Scripts\activate

### Step 3 — Install dependencies
pip install -r requirements.txt

### Step 4 — Run the app
python run.py

### Step 5 — Open in browser
http://localhost:5000
---

## 🔑 Default Login

Username : admin

Password : admin123


---

## 📁 Project Structure

P2P-Management-System/

│

├── app/

│ ├── init.py ← App factory

│ ├── models.py ← Database tables

│ │

│ ├── routes/

│ │ ├── auth.py ← Login & Logout

│ │ ├── dashboard.py ← KPI Dashboard

│ │ ├── invoices.py ← Invoice management

│ │ ├── vendors.py ← Vendor management

│ │ └── purchase_orders.py ← PO & Matching

│ │

│ ├── templates/

│ │ ├── base.html ← Master layout

│ │ ├── login.html ← Login page

│ │ ├── dashboard.html ← Dashboard page

│ │ ├── invoices/ ← Invoice pages

│ │ ├── vendors/ ← Vendor pages

│ │ └── po/ ← PO pages

│ │

│ └── static/

│ └── css/

│ └── style.css ← Custom styles

│

├── config.py ← App configuration

├── run.py ← Start the app

├── requirements.txt ← All dependencies

└── README.md ← This file


---

## 💡 What I Learned

✅ Python Flask web development

✅ Database design with SQLAlchemy

✅ P2P domain — invoices, POs, GRN, matching

✅ User authentication & security

✅ Bootstrap responsive UI design

✅ Chart.js data visualization

✅ Pandas Excel automation

✅ GitHub version control


---

## 👩‍💻 Author

**Bhavana Balakrishna**
SQL Developer | P2P Domain Expert

3-5 Years Experience in P2P & Invoice Processing

> 🤖 Built with guidance from Claude AI (Anthropic) as a hands-on learning project.

🔗 GitHub: github.com/BhavanaBalakrishnaGit

---

## 📝 License

This project is open source and available under the MIT License.
