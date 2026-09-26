import os

class SimplePDF:
    def __init__(self, page_width=595, page_height=842):
        self.width = page_width
        self.height = page_height
        self.pages = []
        self.current_page_commands = []
        self.current_page_num = 0
        self.new_page()

    def new_page(self):
        if self.current_page_commands:
            self.pages.append("\n".join(self.current_page_commands))
            self.current_page_commands = []
        self.current_page_num += 1

    def _escape(self, text):
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def add_line(self, x1, y1, x2, y2, r=0.2, g=0.2, b=0.2, width=0.6):
        self.current_page_commands.append(f"q {r:.2f} {g:.2f} {b:.2f} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q")

    def add_text(self, x, y, text, font="F2", size=10, r=0.1, g=0.1, b=0.1):
        escaped = self._escape(text)
        self.current_page_commands.append(
            f"BT /{font} {size:.1f} Tf {r:.2f} {g:.2f} {b:.2f} rg 1 0 0 1 {x:.2f} {y:.2f} Tm ({escaped}) Tj ET"
        )

    def finish(self):
        if self.current_page_commands:
            self.pages.append("\n".join(self.current_page_commands))
            self.current_page_commands = []

    def get_bytes(self):
        self.finish()
        num_pages = len(self.pages)
        
        objects = []
        # obj 1: Catalog
        # obj 2: Pages
        # obj 3..2+num_pages: Page objects
        # font objects: F1 (Helvetica-Bold), F2 (Helvetica), F3 (Helvetica-Oblique)
        # then content stream objects for each page
        
        f1_idx = 3 + num_pages
        f2_idx = f1_idx + 1
        f3_idx = f2_idx + 1
        
        first_content_idx = f3_idx + 1
        
        # 1. Catalog
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        
        # 2. Pages
        kids = " ".join([f"{3 + i} 0 R" for i in range(num_pages)])
        objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {num_pages} >>".encode("ascii"))
        
        # 3.. Page objects
        for i in range(num_pages):
            content_ref = f"{first_content_idx + i} 0 R"
            page_obj = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width} {self.height}] "
                f"/Resources << /Font << /F1 {f1_idx} 0 R /F2 {f2_idx} 0 R /F3 {f3_idx} 0 R >> >> "
                f"/Contents {content_ref} >>"
            ).encode("ascii")
            objects.append(page_obj)
            
        # Fonts
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>")
        
        # Content streams
        for page_cmd in self.pages:
            cmd_bytes = page_cmd.encode("latin-1", errors="replace")
            stream_obj = b"<< /Length " + str(len(cmd_bytes)).encode("ascii") + b" >>\nstream\n" + cmd_bytes + b"\nendstream"
            objects.append(stream_obj)
            
        # Build PDF with xref
        output = [b"%PDF-1.4\n"]
        xref_offsets = [0]
        
        current_offset = len(output[0])
        
        for idx, obj in enumerate(objects, 1):
            xref_offsets.append(current_offset)
            header = f"{idx} 0 obj\n".encode("ascii")
            footer = b"\nendobj\n"
            current_offset += len(header) + len(obj) + len(footer)
            output.append(header + obj + footer)
            
        startxref = current_offset
        xref_section = [f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii")]
        for offset in xref_offsets[1:]:
            xref_section.append(f"{offset:010d} 00000 n \n".encode("ascii"))
            
        trailer = (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{startxref}\n%%EOF\n"
        ).encode("ascii")
        
        return b"".join(output + xref_section + [trailer])


def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + (1 if curr else 0) <= max_chars:
            curr.append(w)
            curr_len += len(w) + (1 if curr else 0)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
    if curr:
        lines.append(" ".join(curr))
    return lines
