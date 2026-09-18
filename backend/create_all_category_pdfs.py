import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DATA_DIR = Path(__file__).parent / "data"

def make_pdf(filename, category, title, sections):
    cat_dir = BASE_DATA_DIR / category
    os.makedirs(cat_dir, exist_ok=True)
    pdf_path = cat_dir / filename

    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor="#1e3a8a", spaceAfter=12)
    h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=13, leading=16, textColor="#0f172a", spaceBefore=8, spaceAfter=6)
    body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10, leading=14, textColor="#334155", spaceAfter=6)

    story = []
    for idx, (sec_title, sec_body) in enumerate(sections, 1):
        story.append(Paragraph(f"{title}", title_style))
        story.append(Paragraph(f"Category: {category.capitalize()} | Page {idx}", body_style))
        story.append(Spacer(1, 8))
        story.append(Paragraph(sec_title, h2_style))
        for line in sec_body.split('\n'):
            if line.strip():
                story.append(Paragraph(line.strip(), body_style))
        if idx < len(sections):
            story.append(PageBreak())

    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

def generate_all():
    # Pension
    make_pdf("pension_official_guidelines.pdf", "pension", "National Pension Schemes & Senior Citizen Guidelines", [
        ("Indira Gandhi National Old Age Pension Scheme (IGNOAPS)", "The Indira Gandhi National Old Age Pension Scheme provides monthly financial assistance to senior citizens belonging to Below Poverty Line (BPL) households.\nEligibility: Citizen of India, Age 60 years or above, BPL household status.\nBenefit: Rs. 200 to Rs. 500 per month for ages 60-79, and Rs. 500 to Rs. 1000 per month for ages 80 and above."),
        ("Required Documents for Pension Application", "1. Proof of Age: Birth Certificate, PAN Card, Voter ID, or Medical Certificate.\n2. Proof of Address: Aadhaar Card, Ration Card, or Utility Bill.\n3. BPL Income Certificate: BPL Ration Card or Revenue Officer Income Certificate.\n4. Active Bank Account Passbook (Aadhaar-seeded for DBT direct benefit transfer).\n5. Passport Size Photographs: 2 recent photographs."),
        ("Pension Application Procedure", "1. Visit local Gram Panchayat office (rural) or Block Development Office (BDO) / District Social Welfare Office (DSWO) (urban).\n2. Fill out prescribed Pension Application Form.\n3. Attach self-attested copies of Aadhaar, BPL card, Bank Passbook, and Age proof.\n4. Obtain acknowledgment receipt. Verification completes within 30-45 working days.")
    ])

    # Police
    make_pdf("police_procedure_guide.pdf", "police", "Official Guidelines on Filing Police Complaints & FIR", [
        ("Procedure for Filing a Police Complaint", "A formal complaint can be filed by any citizen who has information about a crime.\nSteps:\n1. Write a formal complaint addressed to Station House Officer (SHO) of local police station.\n2. Mention incident date, time, location, detailed facts, accused/witness names, and complainant contact.\n3. Submit two copies and obtain official STAMPED ACKNOWLEDGMENT receipt on duplicate copy."),
        ("First Information Report (FIR) Procedure (Section 154 CrPC / BNSS 173)", "1. Right to Free Copy: Informant is entitled to receive a COPY of the FIR FREE OF COST immediately.\n2. Reading Before Signing: Read carefully to verify statement accuracy before signing.\n3. Zero FIR: Police must register a Zero FIR immediately regardless of territorial jurisdiction and transfer it to concerned station."),
        ("Remedial Measures If Police Refuse to Register FIR", "1. Submit written complaint to Superintendent of Police (SP) or Deputy Commissioner of Police (DCP) under Section 154(3) CrPC / BNSS 173(4).\n2. Judicial Remedy: File application before Judicial Magistrate under Section 156(3) CrPC / BNSS Section 175 directing police to register FIR.")
    ])

    # Vehicle
    make_pdf("vehicle_impound_and_release_guide.pdf", "vehicle", "Motor Vehicle Seizure & Court Release Procedure", [
        ("Grounds for Vehicle Seizure (Section 207 MV Act)", "Traffic Police or RTO officers can impound a vehicle for: driving without valid Driving Licence (DL) or Registration Certificate (RC), driving without third-party insurance, fake number plates, drunk driving (Section 185 MV Act), or carrying commercial load without permit."),
        ("Step-by-Step Vehicle Release Procedure", "1. Obtain Seizure Memo / Impound Receipt (Challan) at the time of seizure.\n2. For compoundable violations, pay penalty at Traffic Police Line / RTO and obtain Release Order.\n3. For non-compoundable offenses or Section 207 seizure, file formal Superdari / Release application under Section 451/457 CrPC before Judicial Magistrate / Traffic Court."),
        ("Checklist of Documents for Vehicle Release", "1. Original Registration Certificate (RC) & copy.\n2. Original Driving Licence (DL).\n3. Valid Motor Insurance Policy & PUCC.\n4. Copy of Seizure Memo / Traffic Challan.\n5. Identity Proof (Aadhaar Card / Voter ID / PAN Card).\n6. Court Release Order & Superdginama (if applicable).")
    ])

    # PAN
    make_pdf("pan_card_services_guide.pdf", "pan", "Income Tax Department Guidelines on PAN Services", [
        ("Procedure for Lost PAN Card / Duplicate PAN Application", "1. Visit official NSDL e-Gov portal or UTIITSL portal.\n2. Select 'Changes or Correction in existing PAN Data / Reprint of PAN Card'.\n3. Fill personal details (Name, DOB, Mobile, existing 10-digit PAN).\n4. Complete e-KYC using Aadhaar OTP.\n5. Pay fee of Rs. 50 (within India). Card delivered in 10-15 business days."),
        ("Steps for Instant e-PAN Download", "1. Visit Income Tax e-Filing portal (incometax.gov.in).\n2. Go to 'Instant e-PAN' -> 'Check Status / Download PAN'.\n3. Enter 12-digit Aadhaar number and OTP.\n4. Download e-PAN PDF instantly free of cost. Password is Date of Birth in DDMMYYYY format.")
    ])

    # Driving License
    make_pdf("driving_licence_services_guide.pdf", "driving_license", "Parivahan Sewa Guidelines on Driving Licence Services", [
        ("Lost Driving Licence - Procedure for Duplicate DL", "1. File online Lost Article Report / FIR on State Police portal and obtain receipt.\n2. Visit Parivahan Sewa portal (parivahan.gov.in) -> Driving Licence Related Services.\n3. Apply for Duplicate DL using DL Number and Date of Birth.\n4. Fill Form 2 (LLD), upload Police Lost Report, Address Proof, and pay fee (approx. Rs. 200-400).\n5. Duplicate Smart Card DL posted to home address via Speed Post."),
        ("Renewal of Driving Licence Rules", "1. Non-transport DL is valid for 20 years or until 40 years of age.\n2. Apply within 1 year before or up to 1 year after expiry without driving re-test penalty.\n3. Form 1-A Medical Certificate is mandatory for applicants above 40 years of age.")
    ])

    # Schemes
    make_pdf("government_welfare_schemes_guide.pdf", "schemes", "Official Handbook on PM-Kisan & Ayushman Bharat Schemes", [
        ("Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", "Benefit: Rs. 6,000 per year transferred in three quarterly installments of Rs. 2,000 into Aadhaar-seeded bank accounts.\nEligibility: Small and marginal landholder farmer families owning cultivable land up to 2 hectares.\nMandatory: e-KYC verification using Aadhaar OTP or biometric authentication.\nRequired: Land ownership record (Khasra/Khatauni), Aadhaar, Bank Passbook."),
        ("Ayushman Bharat - PM-JAY Health Scheme", "Benefit: Free health cover of Rs. 5 Lakh per family per year for secondary and tertiary hospitalization.\nEligibility: SECC 2011 identified families and all Senior Citizens aged 70+ years (Ayushman Vaya Vandana Card).\nHow to Download Card: Visit beneficiary.nha.gov.in -> Search by Aadhaar or Ration Card -> Complete e-KYC -> Download instant Ayushman Card PDF.")
    ])

if __name__ == "__main__":
    generate_all()
