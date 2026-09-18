import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_aadhaar_pdf():
    output_dir = Path(__file__).parent / "data" / "aadhaar"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = output_dir / "aadhaar_official_guide.pdf"

    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor="#1e3a8a", spaceAfter=12)
    h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=14, leading=18, textColor="#0f172a", spaceBefore=10, spaceAfter=8)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10, leading=15, textColor="#334155", spaceAfter=8)

    story = []

    # Page 1: Lost Aadhaar Procedure
    story.append(Paragraph("UIDAI Official Handbook: Aadhaar Services & Lost Card Retrieval", title_style))
    story.append(Paragraph("Category: Aadhaar Services | Page 1", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("1. What to Do If Your Aadhaar Card Is Lost", h2_style))
    story.append(Paragraph("If a citizen loses their physical Aadhaar card or forgets their Aadhaar number (UID) or Enrolment ID (EID), they can retrieve it online through the official UIDAI myAadhaar portal (myaadhaar.uidai.gov.in).", body_style))
    story.append(Paragraph("Steps to Retrieve Lost Aadhaar Number (UID) or Enrolment ID (EID):", h2_style))
    story.append(Paragraph("Step 1: Visit the official UIDAI web portal at myaadhaar.uidai.gov.in and click on 'Retrieve EID / Aadhaar number'.", body_style))
    story.append(Paragraph("Step 2: Select whether you want to retrieve your 12-digit Aadhaar Number (UID) or 28-digit Enrolment ID (EID).", body_style))
    story.append(Paragraph("Step 3: Enter your full name exactly as registered on your Aadhaar card.", body_style))
    story.append(Paragraph("Step 4: Enter your registered mobile number or registered email address.", body_style))
    story.append(Paragraph("Step 5: Enter the captcha code and click 'Send OTP'.", body_style))
    story.append(Paragraph("Step 6: Enter the 6-digit One Time Password (OTP) received on your registered mobile number.", body_style))
    story.append(Paragraph("Step 7: Upon successful verification, your 12-digit Aadhaar number (or EID) will be sent via SMS directly to your registered mobile phone.", body_style))
    story.append(PageBreak())

    # Page 2: How to Download E-Aadhaar
    story.append(Paragraph("UIDAI Official Handbook: E-Aadhaar Download & Password Rules", title_style))
    story.append(Paragraph("Category: Aadhaar Services | Page 2", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. How to Download E-Aadhaar Online", h2_style))
    story.append(Paragraph("An e-Aadhaar is a digitally signed electronic document issued by UIDAI. As per Section 4(3) of the Aadhaar Act 2016, an e-Aadhaar is legally valid for all official government and financial purposes across India.", body_style))
    story.append(Paragraph("Steps to Download E-Aadhaar PDF:", h2_style))
    story.append(Paragraph("Step 1: Go to myaadhaar.uidai.gov.in and select 'Download Aadhaar'.", body_style))
    story.append(Paragraph("Step 2: Enter your 12-digit Aadhaar Number, 28-digit Enrolment ID (EID), or 16-digit Virtual ID (VID).", body_style))
    story.append(Paragraph("Step 3: If you prefer to conceal your Aadhaar digits for privacy, select 'Do you want a masked Aadhaar?'. Masked Aadhaar hides the first 8 digits and displays only the last 4 digits (XXXX-XXXX-1234).", body_style))
    story.append(Paragraph("Step 4: Click 'Send OTP' and enter the 6-digit code received on your mobile.", body_style))
    story.append(Paragraph("Step 5: Click 'Verify & Download' to download the PDF document.", body_style))
    story.append(Paragraph("Password Format for E-Aadhaar PDF:", h2_style))
    story.append(Paragraph("The downloaded e-Aadhaar PDF is password protected. The password consists of the FIRST 4 LETTERS of your name in CAPITAL letters followed by your YEAR OF BIRTH (YYYY). For example, if your name is RAMESH KUMAR and your birth year is 1990, your password is RAME1990.", body_style))
    story.append(PageBreak())

    # Page 3: Aadhaar PVC Card
    story.append(Paragraph("UIDAI Official Handbook: Ordering Physical PVC Aadhaar Card", title_style))
    story.append(Paragraph("Category: Aadhaar Services | Page 3", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Ordering Physical Aadhaar PVC Card", h2_style))
    story.append(Paragraph("Citizens who require a physical, durable Aadhaar card can order an official Aadhaar PVC Card online.", body_style))
    story.append(Paragraph("Aadhaar PVC Card Features:", h2_style))
    story.append(Paragraph("The Aadhaar PVC card comes with security features including a digitally signed QR code, micro-text, ghost image, issue date, print date, and embossed Aadhaar emblem.", body_style))
    story.append(Paragraph("How to Order Aadhaar PVC Card Online:", h2_style))
    story.append(Paragraph("Step 1: Visit myaadhaar.uidai.gov.in and select 'Order Aadhaar PVC Card'.", body_style))
    story.append(Paragraph("Step 2: Enter your 12-digit Aadhaar number or 28-digit Enrolment ID.", body_style))
    story.append(Paragraph("Step 3: If your mobile number is NOT registered with Aadhaar, check the box 'My mobile number is not registered' and enter any active mobile number to receive OTP.", body_style))
    story.append(Paragraph("Step 4: Pay a nominal fee of Rs. 50 (inclusive of GST and Speed Post delivery charges) using UPI, net banking, or debit card.", body_style))
    story.append(Paragraph("Step 5: Note down your Service Request Number (SRN) to track dispatch status.", body_style))
    story.append(Paragraph("The PVC card will be dispatched via India Post Speed Post directly to your registered address within 5 to 7 working days.", body_style))
    story.append(PageBreak())

    # Page 4: Aadhaar Update & Document Requirements
    story.append(Paragraph("UIDAI Official Handbook: Aadhaar Update & Document Requirements", title_style))
    story.append(Paragraph("Category: Aadhaar Services | Page 4", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Documents Required for Aadhaar Update & Correction", h2_style))
    story.append(Paragraph("To update demographic details (Name, Address, Date of Birth, Gender), valid supporting documents must be submitted.", body_style))
    story.append(Paragraph("Accepted Proof of Identity (PoI) Documents:", h2_style))
    story.append(Paragraph("Passport, PAN Card, Voter ID, Driving Licence, Ration Card, Government Photo ID Card, Service Photo ID Card.", body_style))
    story.append(Paragraph("Accepted Proof of Address (PoA) Documents:", h2_style))
    story.append(Paragraph("Electricity Bill (last 3 months), Water Bill, Bank Statement / Passbook, Passport, Property Tax Receipt, Ration Card, Rent Agreement.", body_style))
    story.append(Paragraph("Accepted Proof of Date of Birth (DoB) Documents:", h2_style))
    story.append(Paragraph("Birth Certificate issued by Registrar of Births, SSLC Certificate / Marksheet, Passport, PAN Card.", body_style))
    story.append(Paragraph("Online Address Update Procedure:", h2_style))
    story.append(Paragraph("Citizens can update their address online at myaadhaar.uidai.gov.in by uploading a self-attested color copy of valid Proof of Address document and paying Rs. 50 processing fee.", body_style))
    story.append(Paragraph("Offline Biometric & Demographic Updates:", h2_style))
    story.append(Paragraph("For updates to Name, Date of Birth, Gender, Biometrics (Iris, Fingerprints, Photo), or Mobile Number, citizens MUST visit an authorized Aadhaar Seva Kendra (ASK). No document proof is required for mobile number or biometric updates.", body_style))
    story.append(PageBreak())

    # Page 5: Troubleshooting Lost Aadhaar Number & Non-Registered Mobile
    story.append(Paragraph("UIDAI Official Handbook: Troubleshooting Lost Aadhaar & Mobile Updates", title_style))
    story.append(Paragraph("Category: Aadhaar Services | Page 5", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. What to Do If You Cannot Find Your Aadhaar Number or Mobile Is Not Registered", h2_style))
    story.append(Paragraph("If you do not remember your Aadhaar number AND your mobile number is not registered or no longer active:", body_style))
    story.append(Paragraph("Method 1: Call Toll-Free Helpline 1947", h2_style))
    story.append(Paragraph("Dial UIDAI toll-free helpline number 1947. Provide your full name, demographic details, address, and pin code to the customer service representative to retrieve your Enrolment ID (EID).", body_style))
    story.append(Paragraph("Method 2: Visit Nearest Aadhaar Seva Kendra", h2_style))
    story.append(Paragraph("Visit the nearest Aadhaar enrolment center or Aadhaar Seva Kendra. Request printout of your Aadhaar card using biometric search (fingerprint / iris scan).", body_style))
    story.append(Paragraph("Method 3: Register / Update Mobile Number", h2_style))
    story.append(Paragraph("To link a new mobile number with your Aadhaar, visit an Aadhaar Seva Kendra or post office counter. Fill out the Aadhaar Update Form, provide fingerprint biometric authentication, and pay Rs. 50. The mobile number gets updated within 24 to 48 hours.", body_style))

    doc.build(story)
    print(f"Sample Aadhaar PDF created successfully at: {pdf_path}")

if __name__ == "__main__":
    generate_aadhaar_pdf()
