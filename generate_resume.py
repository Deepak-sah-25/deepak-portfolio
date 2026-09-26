from portfolio.utils_pdf import SimplePDF, wrap_text

def build_deepak_resume():
    pdf = SimplePDF(page_width=595, page_height=842) # Standard A4 (595x842 pt)
    
    margin_x = 40
    content_width = 515
    y = 804
    
    # ------------------ HEADER ------------------
    pdf.add_text(margin_x, y, "DEEPAK SAH KANU", font="F1", size=18, r=0.07, g=0.1, b=0.16)
    y -= 17
    
    pdf.add_text(margin_x, y, "Full-Stack Django Developer", font="F1", size=11, r=0.45, g=0.25, b=0.85)
    y -= 15
    
    contact_str = "Nepal  |  Phone: +977 9829014425  |  Email: deepakraj90054@email.com  |  GitHub: github.com/Deepak-sah-25"
    pdf.add_text(margin_x, y, contact_str, font="F2", size=8.5, r=0.25, g=0.25, b=0.3)
    y -= 10
    
    # Top Accent Line
    pdf.add_line(margin_x, y, margin_x + content_width, y, r=0.45, g=0.25, b=0.85, width=1.2)
    y -= 15
    
    def section_header(title):
        nonlocal y
        pdf.add_text(margin_x, y, title.upper(), font="F1", size=9.5, r=0.1, g=0.12, b=0.18)
        y -= 3
        pdf.add_line(margin_x, y, margin_x + content_width, y, r=0.8, g=0.8, b=0.85, width=0.5)
        y -= 12

    # ------------------ 1. PROFESSIONAL SUMMARY ------------------
    section_header("Professional Summary")
    summary_text = (
        "Results-driven Full-Stack Django Developer with over 2 years of experience in designing, building, and deploying "
        "scalable web applications and RESTful APIs. Specializes in Python, Django REST Framework (DRF), PostgreSQL, and "
        "multi-tenant SaaS architectures. Proven track record of developing robust backend systems, optimizing database "
        "performance, and delivering secure, user-friendly solutions for the healthcare and e-commerce sectors."
    )
    for line in wrap_text(summary_text, 102):
        pdf.add_text(margin_x, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
        y -= 11.5
    y -= 4

    # ------------------ 2. TECHNICAL SKILLS ------------------
    section_header("Technical Skills")
    skills = [
        ("Backend Development", "Python, Django, Django REST Framework (DRF)"),
        ("Frontend Development", "HTML5, CSS3, JavaScript, Bootstrap"),
        ("Databases & Architecture", "PostgreSQL, Multi-Tenant Architecture (django-tenants), Schema Isolation"),
        ("Tools & Technologies", "Git/GitHub, Docker, Redis, Celery, Linux, VS Code, AI Coding Tools"),
        ("Core Competencies", "REST API Design, Background Task Processing, Database Modeling, Third-Party Integrations")
    ]
    for cat, desc in skills:
        pdf.add_text(margin_x, y, "-  " + cat + ":", font="F1", size=8.5, r=0.12, g=0.12, b=0.18)
        offset = len(cat) * 4.7 + 16
        pdf.add_text(margin_x + offset, y, desc, font="F2", size=8.5, r=0.22, g=0.22, b=0.25)
        y -= 11.5
    y -= 4

    # ------------------ 3. PROFESSIONAL EXPERIENCE ------------------
    section_header("Professional Experience")
    
    # 3.1 Anjan Lab Company
    pdf.add_text(margin_x, y, "Anjan Lab Company", font="F1", size=9.5, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + 112, y, "|  Nepal", font="F2", size=9, r=0.35, g=0.35, b=0.4)
    pdf.add_text(margin_x + content_width - 105, y, "August 2024 - Present", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
    y -= 12
    pdf.add_text(margin_x, y, "Django Developer", font="F3", size=9, r=0.2, g=0.2, b=0.25)
    y -= 11.5
    
    exp1_bullets = [
        "Lead the backend development of secure, database-driven healthcare web applications using Django and Django REST Framework.",
        "Architect and implement multi-tenant SaaS structures using PostgreSQL and django-tenants, ensuring strict schema isolation and data security across multiple hospital networks.",
        "Build and maintain complex REST APIs for appointment management, patient workflows, and centralized clinical modules.",
        "Optimize database queries and implement asynchronous task processing using Redis and Celery to improve application response times and performance.",
        "Collaborate with cross-functional teams to refactor legacy codebases and streamline deployment workflows using Docker containerization."
    ]
    for b in exp1_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 11
    y -= 3
    
    # 3.2 Independent Web Developer
    pdf.add_text(margin_x, y, "Independent Web Developer", font="F1", size=9.5, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + 145, y, "|  Nepal", font="F2", size=9, r=0.35, g=0.35, b=0.4)
    pdf.add_text(margin_x + content_width - 110, y, "May 2024 - August 2024", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
    y -= 12
    pdf.add_text(margin_x, y, "Full-Stack Python Developer", font="F3", size=9, r=0.2, g=0.2, b=0.25)
    y -= 11.5
    
    exp2_bullets = [
        "Designed and developed end-to-end web solutions for local businesses, focusing on backend logic, database management, and responsive frontend UI.",
        "Created custom dashboards and data analytics tools, improving client operational efficiency."
    ]
    for b in exp2_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 11
    y -= 4

    # ------------------ 4. KEY PROJECTS ------------------
    section_header("Key Projects")
    
    # 4.1 Anjan HMIS
    pdf.add_text(margin_x, y, "Anjan Hospital Management Information System (HMIS)", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 110, y, "Healthcare SaaS", font="F3", size=8, r=0.4, g=0.4, b=0.45)
    y -= 11
    p1_bullets = [
        "Architected a comprehensive clinical workflow platform tailored for the healthcare sector.",
        "Developed secure multi-tenant hospital configurations, allowing separate medical facilities to operate independently on a unified backend.",
        "Built dynamic REST API endpoints for patient registers, real-time appointment scheduling, and automated billing generation."
    ]
    for b in p1_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 11
    y -= 3

    # 4.2 Sadi Sewa
    pdf.add_text(margin_x, y, "Sadi Sewa - Event & Wedding Booking Marketplace", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 110, y, "Full-Stack Marketplace", font="F3", size=8, r=0.4, g=0.4, b=0.45)
    y -= 11
    p2_bullets = [
        "Developed a scalable multi-vendor booking platform connecting users with wedding and event service providers.",
        "Implemented comprehensive vendor profiles, dynamic service packaging, booking management systems, and secure payment architecture.",
        "Designed an intuitive user interface utilizing Bootstrap and responsive HTML/CSS layouts."
    ]
    for b in p2_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 11
    y -= 3

    # 4.3 E-Commerce
    pdf.add_text(margin_x, y, "E-Commerce Seller Center Dashboard", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 110, y, "Analytics & Orders", font="F3", size=8, r=0.4, g=0.4, b=0.45)
    y -= 11
    p3_bullets = [
        "Engineered a comprehensive seller dashboard featuring functionalities for seller registration, robust analytics, and earnings reports.",
        "Integrated real-time order tracking and status management using optimized PostgreSQL database relationships."
    ]
    for b in p3_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 11
    y -= 4

    # ------------------ 5. EDUCATION ------------------
    section_header("Education")
    pdf.add_text(margin_x, y, "Bachelor in Computer Application (BCA)", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 110, y, "Running (3rd Year)", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
    y -= 11.5
    pdf.add_text(margin_x, y, "Prime College  |  Kathmandu, Nepal", font="F2", size=8.5, r=0.25, g=0.25, b=0.3)
    y -= 12
    
    print(f"Final y coordinate on single page: {y:.1f}")
    return pdf.get_bytes()

if __name__ == "__main__":
    pdf_data = build_deepak_resume()
    output_path = "static/files/Deepak_Sah_Kanu_Resume.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_data)
    print(f"Resume written to {output_path}, total bytes: {len(pdf_data)}")
