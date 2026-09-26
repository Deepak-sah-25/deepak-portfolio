import os

class SimplePDF:
    def __init__(self, page_width=595, page_height=842):
        self.width = page_width
        self.height = page_height
        self.pages = []
        self.current_page_commands = []
        self.current_page_num = 0
        self.images = {}
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

    def add_rect(self, x, y, w, h, fill_rgb=None, stroke_rgb=None, width=0.6):
        cmds = ["q"]
        if fill_rgb:
            r, g, b = fill_rgb
            cmds.append(f"{r:.2f} {g:.2f} {b:.2f} rg")
        if stroke_rgb:
            r, g, b = stroke_rgb
            cmds.append(f"{r:.2f} {g:.2f} {b:.2f} RG {width:.2f} w")
        op = "B" if (fill_rgb and stroke_rgb) else ("f" if fill_rgb else "S")
        cmds.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op} Q")
        self.current_page_commands.append(" ".join(cmds))

    def add_image_resource(self, name, jpeg_path):
        import struct
        with open(jpeg_path, "rb") as f:
            data = f.read()
        i = 0
        size = len(data)
        width, height = 0, 0
        while i < size - 8:
            if data[i] == 0xFF:
                marker = data[i+1]
                if marker in (0xC0, 0xC1, 0xC2):
                    height, width = struct.unpack(">HH", data[i+5:i+9])
                    break
                elif marker in (0xD8, 0xD9):
                    i += 2
                else:
                    length = struct.unpack(">H", data[i+2:i+4])[0]
                    i += 2 + length
            else:
                i += 1
        self.images[name] = {"data": data, "width": width, "height": height}

    def draw_image(self, name, x, y, w, h, clip_box=None, border_color=(0.45, 0.25, 0.85), border_width=1.0):
        if clip_box:
            cx, cy, cw, ch = clip_box
            self.current_page_commands.append(
                f"q {cx:.2f} {cy:.2f} {cw:.2f} {ch:.2f} re W n {w:.2f} 0 0 {h:.2f} {x:.2f} {y:.2f} cm /{name} Do Q"
            )
            if border_color and border_width > 0:
                r, g, b = border_color
                self.current_page_commands.append(
                    f"q {r:.2f} {g:.2f} {b:.2f} RG {border_width:.2f} w {cx:.2f} {cy:.2f} {cw:.2f} {ch:.2f} re S Q"
                )
        else:
            self.current_page_commands.append(
                f"q {w:.2f} 0 0 {h:.2f} {x:.2f} {y:.2f} cm /{name} Do Q"
            )

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
        # fonts: F1, F2, F3
        # images: Im1..
        # page content streams
        
        f1_idx = 3 + num_pages
        f2_idx = f1_idx + 1
        f3_idx = f2_idx + 1
        
        img_indices = {}
        curr_idx = f3_idx + 1
        for img_name in self.images:
            img_indices[img_name] = curr_idx
            curr_idx += 1
            
        first_content_idx = curr_idx
        
        # 1. Catalog
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        
        # 2. Pages
        kids = " ".join([f"{3 + i} 0 R" for i in range(num_pages)])
        objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {num_pages} >>".encode("ascii"))
        
        # XObject dictionary string for resources
        if self.images:
            xobj_entries = " ".join([f"/{name} {img_indices[name]} 0 R" for name in self.images])
            xobj_str = f"/XObject << {xobj_entries} >>"
        else:
            xobj_str = ""

        # 3.. Page objects
        for i in range(num_pages):
            content_ref = f"{first_content_idx + i} 0 R"
            page_obj = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width} {self.height}] "
                f"/Resources << /Font << /F1 {f1_idx} 0 R /F2 {f2_idx} 0 R /F3 {f3_idx} 0 R >> {xobj_str} >> "
                f"/Contents {content_ref} >>"
            ).encode("ascii")
            objects.append(page_obj)
            
        # Fonts
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>")
        
        # Image XObjects
        for img_name, img_info in self.images.items():
            img_stream = img_info["data"]
            img_header = (
                f"<< /Type /XObject /Subtype /Image /Width {img_info['width']} /Height {img_info['height']} "
                f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(img_stream)} >>\nstream\n"
            ).encode("ascii")
            objects.append(img_header + img_stream + b"\nendstream")
        
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
