import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime
import uuid

def generate_certificate(user, attempt, category):
    cert_id = str(uuid.uuid4()).split('-')[0].upper()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_dir = os.path.join(base_dir, 'static', 'certificates')
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
    safe_name = user.name.replace(' ', '_')
    filename = f"{safe_name}_{cert_id}.pdf"
    file_path = os.path.join(cert_dir, filename)
    
    c = canvas.Canvas(file_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # 1. Background
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # 2. Corner Brackets
    margin = 50
    thick_width = 16
    thin_width = 3
    
    teal_color = colors.HexColor('#00B4DB') # Gradient-like bright teal/blue
    dark_blue = colors.HexColor('#211551')
    
    # Top-Left (Thick Teal)
    c.setStrokeColor(teal_color)
    c.setLineWidth(thick_width)
    c.line(margin, height - margin, margin, height - margin - 120) # Vertical
    c.line(margin - (thick_width/2), height - margin, margin + 120, height - margin) # Horizontal
    
    # Bottom-Right (Thick Teal)
    c.setStrokeColor(teal_color)
    c.setLineWidth(thick_width)
    c.line(width - margin, margin, width - margin, margin + 120) # Vertical
    c.line(width - margin + (thick_width/2), margin, width - margin - 120, margin) # Horizontal
    
    # Top-Right (Thin Dark Blue)
    c.setStrokeColor(dark_blue)
    c.setLineWidth(thin_width)
    c.line(width - margin, height - margin, width - margin, height - margin - 100) # Vertical
    c.line(width - margin, height - margin, width - margin - 100, height - margin) # Horizontal
    
    # Bottom-Left (Thin Dark Blue)
    c.setStrokeColor(dark_blue)
    c.setLineWidth(thin_width)
    c.line(margin, margin, margin, margin + 100) # Vertical
    c.line(margin, margin, margin + 100, margin) # Horizontal
    
    # 3. Header / Logo
    logo_y = height - 130
    c.setFillColor(colors.HexColor('#1976D2')) # Blue logo
    c.circle(width/2 - 90, logo_y + 8, 15, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2 - 90, logo_y + 2, "Q")
    
    c.setFillColor(colors.HexColor('#154360')) # Dark blue text
    c.setFont("Helvetica-Bold", 24)
    c.drawString(width/2 - 65, logo_y, "QuizMaster")
    c.setFont("Helvetica", 24)
    c.drawString(width/2 + 65, logo_y, "Academy")
    
    # 4. Title
    title_y = height - 200
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 32)
    c.drawCentredString(width/2, title_y, "CERTIFICATE OF COMPLETION")
    
    # 5. Presented to
    y = title_y - 60
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, y, "Presented to")
    
    # 6. Name
    y -= 45
    name = user.name
    max_name_width = width * 0.7
    font_size = 36
    c.setFont("Helvetica", font_size)
    
    # Auto-resize loop
    while stringWidth(name, "Helvetica", font_size) > max_name_width and font_size >= 20:
        font_size -= 2
        c.setFont("Helvetica", font_size)
    
    c.setFillColor(colors.HexColor('#3498DB')) # Light blue name
    c.drawCentredString(width/2, y, name)
    
    # 7. Achievement Description
    y -= 50
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, y, "For successfully completing the online quiz")
    
    y -= 30
    c.setFont("Helvetica", 20)
    c.drawCentredString(width/2, y, category.name)
    
    # 8. Footer (Provided by)
    y -= 70
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, "Provided by")
    
    y -= 25
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, y, "QuizMaster Academy")
    
    y -= 20
    date_str = attempt.date.strftime('%B %d, %Y') if hasattr(attempt, 'date') and attempt.date else datetime.now().strftime('%B %d, %Y')
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor('#7F8C8D'))
    c.drawCentredString(width/2, y, f"(On {date_str})")
    
    # 9. Verification Note (Bottom Right)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#95A5A6'))
    verification_text = f"To verify this certificate visit https://quizmaster.com/certificate/{cert_id}"
    c.drawRightString(width - margin - 10, margin - 10, verification_text)
    
    c.save()
    
    return cert_id, f"certificates/{filename}"
