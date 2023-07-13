from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
from time import ctime

def create_pdf(order_items, customer_name, customer_address):
    folder = '\\static'
    absolute_path = os.path.dirname(__file__)
    print(absolute_path)
    file_name = str(f'shopping_order_{customer_name}.pdf')
    file_path = os.path.join(absolute_path + folder, file_name)
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(f"Printing Place", styles['Heading1']))
    elements.append(Paragraph(f"---------------------", styles['Heading1']))
    elements.append(Paragraph(f"Order to: {customer_name}", styles['Heading1']))
    elements.append(Paragraph(f"Send to: {customer_address}", styles['Normal']))
    elements.append(Paragraph(f"Ordered at {ctime()}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    data = [['Product', 'Product Description', 'Price', 'Quantity', 'Total']]
    total_amount = 0

    for item in order_items:
        product = item['product']
        description = item['description']
        price = item['price']
        quantity = item['quantity']
        total = price * quantity
        total_amount += total

        data.append([product, description, price, quantity, total])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (-1, -1), (-2, -2), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (-1, -1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (-1, -1), (-1, -1), colors.black),
        ('ALIGN', (-1, -1), (-1, -1), 'CENTER'),
        ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (-1, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    elements.append(Paragraph(f"Total Amount: ${total_amount}", styles['Heading2']))

    doc.build(elements)
    return file_name