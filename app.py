from flask import Flask, render_template, request, send_file
import os
from xhtml2pdf import pisa
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # Get form data
    client = request.form['client']
    items = request.form.getlist('item')
    prices = request.form.getlist('price')

    total = sum([float(p) for p in prices])

    # Create a timestamped filename
    filename = f'invoice_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    filepath = os.path.join('invoices', filename)

    # Render the invoice HTML
    rendered = render_template('invoice.html', client=client, items=zip(items, prices), total=total, datetime=datetime)


    # Generate PDF using xhtml2pdf
    with open(filepath, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(rendered, dest=result_file)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
