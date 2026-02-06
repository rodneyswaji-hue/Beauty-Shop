from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
import os

def generate_invoice_pdf(invoice_number: str, amount: float, email: str, items: list):
    # Ensure the 'invoices' folder exists
    os.makedirs("invoices", exist_ok=True)
    
    file_name = f"invoice_{invoice_number}.pdf"
    file_path = os.path.join("invoices", file_name)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    brand_color = colors.HexColor("#d63384") 

    # 1. Header Bar
    c.setFillColor(brand_color)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "BEAUTY SHOP LTD")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 40, "Official Invoice")
    c.drawRightString(width - 50, height - 55, f"#{invoice_number}")

    # 2. Customer & Date Details
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 120, "BILL TO:")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 135, f"{email}")
    c.drawRightString(width - 50, height - 120, datetime.now().strftime('%Y-%m-%d'))
    c.drawRightString(width - 50, height - 135, "PENDING")

    # 3. Table Header
    c.setStrokeColor(brand_color)
    c.line(50, height - 160, width - 50, height - 160)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, height - 180, "Item Description")
    c.drawCentredString(width - 180, height - 180, "Qty")
    c.drawRightString(width - 60, height - 180, "Subtotal (KES)")
    c.line(50, height - 190, width - 50, height - 190)

    # 4. DYNAMIC ITEMS LOOP
    c.setFont("Helvetica", 11)
    y_position = height - 215
    
    for item in items:
        # Drawing the name, quantity, and price for each item
        c.drawString(60, y_position, f"{item['name']}")
        c.drawCentredString(width - 180, y_position, f"{item['quantity']}")
        c.drawRightString(width - 60, y_position, f"{item['price'] * item['quantity']:,.2f}")
        y_position -= 20  # Move down for the next item

    # 5. Grand Total Box (Adjusted Y position based on items)
    # We move the total box further down if there are many items
    total_y = y_position - 30
    c.setFillColor(colors.HexColor("#fdf2f8"))
    c.rect(width - 250, total_y - 15, 200, 40, fill=True, stroke=False)
    
    c.setFillColor(brand_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 240, total_y, "GRAND TOTAL")
    c.drawRightString(width - 60, total_y, f"KES {amount:,.2f}")

    # 6. Footer
    c.setFillColor(colors.grey)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width/2.0, 50, "Thank you for shopping with Beauty Shop Ltd!")

    c.save()
    return file_path