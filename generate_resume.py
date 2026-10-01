from portfolio.utils_pdf import SimplePDF, wrap_text

def build_deepak_resume():
    pdf = SimplePDF(page_width=595, page_height=842) # Standard A4 (595x842 pt)
    
    margin_x = 40
    content_width = 515
    
    # Register Deepak's photo
    pdf.add_image_resource("DeepakPhoto", "static/images/deepak.jpg")
    
    # Photo Box in Top-Right
    box_w = 60
    box_h = 72
    box_x = margin_x + content_width - box_w
    box_y = 736  # top of box will be 736 + 72 = 808
    
    # Scale image to fill box width nicely and show face/shoulders
    img_w = 66
    img_h = img_w * (1024 / 575)  # ~117 pt
    img_x = box_x - (img_w - box_w) / 2
    # Place top of image slightly above top of box so hair and face are centered
    img_y = (box_y + box_h) - img_h + 12
    
    # Draw photo with clipping and glowing violet border
    pdf.draw_image(
        "DeepakPhoto",
        x=img_x,
        y=img_y,
        w=img_w,
        h=img_h,
        clip_box=(box_x, box_y, box_w, box_h),
        border_color=(0.45, 0.25, 0.85),
        border_width=1.2,
    )

    # ------------------ HEADER (Left Column) ------------------
    y = 806
    pdf.add_text(margin_x, y, "DEEPAK SAH KANU", font="F1", size=18, r=0.07, g=0.1, b=0.16)
    y -= 18
    
    pdf.add_text(margin_x, y, "Full-Stack Django Developer", font="F1", size=11, r=0.45, g=0.25, b=0.85)
    y -= 15
    
    pdf.add_text(margin_x, y, "Nepal  |  Phone: +977 9829014425  |  Email: deepakraj90054@email.com", font="F2", size=8.5, r=0.25, g=0.25, b=0.3)
    y -= 12
    pdf.add_text(margin_x, y, "GitHub: github.com/Deepak-sah-25", font="F2", size=8.5, r=0.25, g=0.25, b=0.3)
    
    # Position accent line cleanly beneath both text and photo box
    y = 726
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
    desc_x = margin_x + 128
    for cat, desc in skills:
        pdf.add_text(margin_x, y, "-  " + cat + ":", font="F1", size=8.5, r=0.12, g=0.12, b=0.18)
        pdf.add_text(desc_x, y, desc, font="F2", size=8.5, r=0.22, g=0.22, b=0.25)
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
    
    # 4.1 Star News TV (Live Production)
    pdf.add_text(margin_x, y, "Star News TV - Digital News & Media Portal", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 130, y, "Live: starnewstv.com.np", font="F1", size=8, r=0.45, g=0.25, b=0.85)
    y -= 10.5
    p0_bullets = [
        "Engineered and deployed a live production digital news portal delivering breaking news & multimedia coverage across Nepal.",
        "Implemented high-concurrency content delivery, category filtering, full-text search, and automated publishing workflows."
    ]
    for b in p0_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 10.5
    y -= 2.5

    # 4.2 Kinaun Multi-Vendor E-Commerce (Live Production - Team Project)
    pdf.add_text(margin_x, y, "Kinaun - Multi-Vendor E-Commerce Platform", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 130, y, "Live: kinaun.com", font="F1", size=8, r=0.45, g=0.25, b=0.85)
    y -= 10.5
    p1_bullets = [
        "Collaborated with cross-functional engineering team to build and launch an active multi-vendor shopping marketplace in Nepal.",
        "Engineered merchant seller center, product catalogs, order tracking workflows, and PostgreSQL relational schemas."
    ]
    for b in p1_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 10.5
    y -= 2.5

    # 4.3 Bato Mechanic (Live Production)
    pdf.add_text(margin_x, y, "Bato Mechanic - Roadside Assistance Platform", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 130, y, "Live: batomechanic.com", font="F1", size=8, r=0.45, g=0.25, b=0.85)
    y -= 10.5
    p2_bullets = [
        "Engineered on-demand roadside assistance platform connecting stranded motorists with nearby certified mechanics.",
        "Built REST API endpoints for breakdown service requests, vehicle repair catalogs, and bilingual content workflows."
    ]
    for b in p2_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 10.5
    y -= 2.5

    # 4.4 CDC Cinemas (Live Production)
    pdf.add_text(margin_x, y, "CDC Cinemas - Movie Ticketing & Theater Portal", font="F1", size=9, r=0.08, g=0.1, b=0.15)
    pdf.add_text(margin_x + content_width - 130, y, "Live: cdcnepal.com.np", font="F1", size=8, r=0.45, g=0.25, b=0.85)
    y -= 10.5
    p3_bullets = [
        "Engineered multiplex cinema ticketing web platform with interactive seat selection & showtime scheduling.",
        "Built movie catalog management, dynamic ticket pricing tiers, and secure online transaction workflows."
    ]
    for b in p3_bullets:
        pdf.add_text(margin_x + 4, y, "-", font="F1", size=8.5, r=0.45, g=0.25, b=0.85)
        for line in wrap_text(b, 98):
            pdf.add_text(margin_x + 14, y, line, font="F2", size=8.5, r=0.18, g=0.18, b=0.2)
            y -= 10.5
    y -= 3.5

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
