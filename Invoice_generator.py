from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import os
app = Flask(__name__)
pdf_directory = os.path.join(app.root_path, 'static', 'invoices')
os.makedirs(pdf_directory, exist_ok=True)
def generate_invoice_pdf(customer_name, product_name, quantity, price_per_unit, total):
    pdf_path = os.path.join(pdf_directory, f"invoice_{customer_name.replace(' ', '_')}.pdf")
    generate_pdf(pdf_path, customer_name, product_name, quantity, price_per_unit, total)
    return pdf_path
def generate_pdf(pdf_path, customer_name, product_name, quantity, price_per_unit, total):
    c = canvas.Canvas(pdf_path)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Invoice")
    c.drawString(100, 730, f"Customer: {customer_name}")
    c.drawString(100, 710, f"Product: {product_name}")
    c.drawString(100, 690, f"Quantity: {quantity}")
    c.drawString(100, 670, f"Price per unit: {price_per_unit}.Rs")
    c.drawString(100, 650, f"Total: {total}.Rs")
    c.save()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    customer_name = request.form['customer_name']
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    price_per_unit = float(request.form['price_per_unit'])
    total = quantity * price_per_unit
    pdf_path = generate_invoice_pdf(customer_name, product_name, quantity, price_per_unit, total)
    return send_file(pdf_path, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)

