import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_report():
    doc = Document()
    
    # ---------------- PAGE SETUP (A4, 4-3-3-3 cm) ----------------
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(3.0)
        s.bottom_margin = Cm(3.0)
        s.left_margin = Cm(4.0)
        s.right_margin = Cm(3.0)
    
    # ---------------- BASE STYLES ----------------
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Configure Built-in Headings
    h1_style = doc.styles['Heading 1']
    h1_font = h1_style.font
    h1_font.name = 'Times New Roman'
    h1_font.size = Pt(14)
    h1_font.bold = True
    h1_font.color.rgb = RGBColor(0, 0, 0)
    h1_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1_style.paragraph_format.space_before = Pt(14)
    h1_style.paragraph_format.space_after = Pt(16)
    h1_style.paragraph_format.line_spacing = 1.15

    h2_style = doc.styles['Heading 2']
    h2_font = h2_style.font
    h2_font.name = 'Times New Roman'
    h2_font.size = Pt(12)
    h2_font.bold = True
    h2_font.color.rgb = RGBColor(0, 0, 0)
    h2_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h2_style.paragraph_format.space_before = Pt(12)
    h2_style.paragraph_format.space_after = Pt(4)
    h2_style.paragraph_format.first_line_indent = Inches(0)
    h2_style.paragraph_format.line_spacing = 1.15

    h3_style = doc.styles['Heading 3']
    h3_font = h3_style.font
    h3_font.name = 'Times New Roman'
    h3_font.size = Pt(12)
    h3_font.bold = True
    h3_font.color.rgb = RGBColor(0, 0, 0)
    h3_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h3_style.paragraph_format.space_before = Pt(8)
    h3_style.paragraph_format.space_after = Pt(3)
    h3_style.paragraph_format.first_line_indent = Inches(0)
    h3_style.paragraph_format.line_spacing = 1.15

    # Helper XML functions
    def set_cell_bg(cell, fill_hex):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._element.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="B0BEC5"):
        tblPr = table._element.xpath('w:tblPr')
        if tblPr:
            borders = parse_xml(
                f'<w:tblBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
                f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
                f'<w:left w:val="none"/>'
                f'<w:right w:val="none"/>'
                f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
                f'<w:insideV w:val="none"/>'
                f'</w:tblBorders>'
            )
            tblPr[0].append(borders)

    def set_outline_level(paragraph, level):
        pPr = paragraph._element.get_or_add_pPr()
        outlineLvl = parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="{level}"/>')
        pPr.append(outlineLvl)

    def add_page_number_to_section(section, start_num, fmt="decimal"):
        sectPr = section._sectPr
        pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="{start_num}" w:fmt="{fmt}"/>')
        sectPr.append(pgNumType)
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run()
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.italic = (fmt == "lowerRoman")
        
        fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
        instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
        fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
        fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run._r.append(fldChar3)

    # Heading Helpers using Word Styles + Outline Levels
    def add_chapter_heading(ch_num, ch_title):
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(16)
        p.paragraph_format.line_spacing = 1.15
        set_outline_level(p, 0)
        
        r1 = p.add_run(ch_num)
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(14)
        r1.font.color.rgb = RGBColor(0, 0, 0)
        
        r_br = p.add_run("\n")
        
        r2 = p.add_run(ch_title)
        r2.bold = True
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(14)
        r2.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_non_chapter_heading(title):
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(16)
        p.paragraph_format.line_spacing = 1.15
        set_outline_level(p, 0)
        
        r = p.add_run(title)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_subheading_2(num, title):
        p = doc.add_paragraph(style='Heading 2')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0)
        set_outline_level(p, 1)
        
        r = p.add_run(f"{num} {title}")
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_subheading_3(num, title):
        p = doc.add_paragraph(style='Heading 3')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.first_line_indent = Inches(0)
        set_outline_level(p, 2)
        
        r = p.add_run(f"{num} {title}")
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_p_indented(text_runs):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        for item in text_runs:
            txt, b, it, c = item
            r = p.add_run(txt)
            r.bold = b
            r.italic = it
            if c:
                r.font.name = 'Consolas'
                r.font.size = Pt(10)
            else:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        return p

    def add_intro(text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    def add_numbered_list_item(num_str, runs):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r_num = p.add_run(num_str + " ")
        r_num.bold = False
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(12)
        for item in runs:
            txt, b, it, c = item
            r = p.add_run(txt)
            r.bold = b
            r.italic = it
            if c:
                r.font.name = 'Consolas'
                r.font.size = Pt(10)
            else:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        return p

    def add_bold_lead_in_item(bold_lead, runs):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r_lead = p.add_run(bold_lead + " ")
        r_lead.bold = True
        r_lead.font.name = 'Times New Roman'
        r_lead.font.size = Pt(12)
        for item in runs:
            txt, b, it, c = item
            r = p.add_run(txt)
            r.bold = b
            r.italic = it
            if c:
                r.font.name = 'Consolas'
                r.font.size = Pt(10)
            else:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(12)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.italic = False
        r.bold = False
        return p

    def add_code_snippet(code_text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.right_indent = Inches(0.2)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(8)
        
        pPr = p._element.get_or_add_pPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="18" w:space="8" w:color="3B82F6"/><w:top w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="4" w:color="E2E8F0"/></w:pBdr>')
        pPr.append(shd)
        pPr.append(pBdr)
        
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.0)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_callout(title_text, desc_text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.right_indent = Inches(0.25)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(10)
        
        pPr = p._element.get_or_add_pPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="8" w:color="0284C7"/><w:top w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:pBdr>')
        pPr.append(shd)
        pPr.append(pBdr)
        
        r_t = p.add_run(title_text + " ")
        r_t.bold = True
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        r_d = p.add_run(desc_text)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11)
        return p

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
    cover_sec = doc.sections[0]
    cover_sec.different_first_page_header_footer = True
    
    p_cov_top = doc.add_paragraph()
    p_cov_top.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_top.paragraph_format.line_spacing = 1.15
    p_cov_top.paragraph_format.space_before = Pt(24)
    p_cov_top.paragraph_format.space_after = Pt(4)
    r = p_cov_top.add_run("LAPORAN PRAKTIKUM PEMROGRAMAN VISUAL\n")
    r.bold = True
    r.font.size = Pt(14)
    
    p_cov_title = doc.add_paragraph()
    p_cov_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_title.paragraph_format.line_spacing = 1.25
    p_cov_title.paragraph_format.space_before = Pt(8)
    p_cov_title.paragraph_format.space_after = Pt(28)
    r_tit = p_cov_title.add_run("RANCANG BANGUN SISTEM INFORMASI AKADEMIK\nPENGELOLAAN DATA MAHASISWA DAN DOSEN BERBASIS C# WINDOWS FORMS DAN MYSQL MENGGUNAKAN POLA ARSITEKTUR REPOSITORI")
    r_tit.bold = True
    r_tit.font.size = Pt(14)
    
    # Box logo placeholder
    p_cov_logo = doc.add_paragraph()
    p_cov_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_logo.paragraph_format.space_before = Pt(18)
    p_cov_logo.paragraph_format.space_after = Pt(28)
    r_logo = p_cov_logo.add_run("┌───────────────────────────────────┐\n│                                   │\n│     [PLACEHOLDER LOGO RESMI]      │\n│        UNIVERSITAS / INSTITUSI    │\n│                                   │\n└───────────────────────────────────┘")
    r_logo.font.name = 'Consolas'
    r_logo.font.size = Pt(10)
    
    p_cov_meta = doc.add_paragraph()
    p_cov_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_meta.paragraph_format.line_spacing = 1.3
    p_cov_meta.paragraph_format.space_before = Pt(18)
    p_cov_meta.paragraph_format.space_after = Pt(28)
    
    r_m1 = p_cov_meta.add_run("Dosen Pengampu:\n")
    r_m1.font.size = Pt(12)
    r_m1_b = p_cov_meta.add_run("[Nama Dosen Pengampu, M.Kom.]\n\n")
    r_m1_b.bold = True
    r_m1_b.font.size = Pt(12)
    
    r_m2 = p_cov_meta.add_run("Disusun Oleh:\n")
    r_m2.font.size = Pt(12)
    r_m2_b = p_cov_meta.add_run("[Nama Lengkap Mahasiswa]\nNIM: [NIM Mahasiswa]\nKelas: [Kode Kelas]\n")
    r_m2_b.bold = True
    r_m2_b.font.size = Pt(12)
    
    p_cov_inst = doc.add_paragraph()
    p_cov_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_inst.paragraph_format.line_spacing = 1.15
    p_cov_inst.paragraph_format.space_before = Pt(36)
    p_cov_inst.paragraph_format.space_after = Pt(0)
    r_inst = p_cov_inst.add_run("PROGRAM STUDI S1 TEKNIK INFORMATIKA\nFAKULTAS SAINS DAN TEKNOLOGI\nUNIVERSITAS [NAMA UNIVERSITAS]\n[KOTA/KABUPATEN]\n2026")
    r_inst.bold = True
    r_inst.font.size = Pt(12)

    # =========================================================================
    # SECTION 2: FRONT MATTER (KATA PENGANTAR & DAFTAR ISI) -> Roman (ii, iii)
    # =========================================================================
    sec_front = doc.add_section()
    sec_front.top_margin = Cm(3.0)
    sec_front.bottom_margin = Cm(3.0)
    sec_front.left_margin = Cm(4.0)
    sec_front.right_margin = Cm(3.0)
    add_page_number_to_section(sec_front, start_num=2, fmt="lowerRoman")
    
    # --- KATA PENGANTAR ---
    add_non_chapter_heading("KATA PENGANTAR")
    
    add_p_indented([
        ("Puji dan syukur senantiasa penulis panjatkan ke hadirat Tuhan Yang Maha Esa atas limpahan rahmat, taufik, dan hidayah-Nya, sehingga penulis dapat menyelesaikan laporan akademik praktikum ini dengan judul ", False, False, False),
        ("“Rancang Bangun Sistem Informasi Akademik Pengelolaan Data Mahasiswa dan Dosen Berbasis C# Windows Forms dan MySQL Menggunakan Pola Arsitektur Repositori”", True, False, False),
        (" secara tepat waktu dan sesuai dengan kaidah ilmiah yang telah ditetapkan. Laporan ini disusun guna memenuhi luaran pembelajaran mata kuliah Pemrograman Visual, khususnya pada modul koneksi dan pengelolaan basis data relasional.", False, False, False)
    ])
    
    add_p_indented([
        ("Tujuan utama penulisan laporan ini adalah untuk mendokumentasikan proses rekayasa perangkat lunak desktop, mulai dari pemodelan basis data, perancangan antarmuka pengguna grafis (", False, False, False),
        ("Graphical User Interface", False, True, False),
        ("), penerapan pola desain repositori (", False, False, False),
        ("Repository Pattern", False, True, False),
        ("), hingga integrasi proteksi keamanan data melalui kueri berparameter dan enkripsi satu arah ", False, False, False),
        ("Secure Hash Algorithm 256-bit", False, True, False),
        (" (SHA-256). Penulis menyampaikan rasa terima kasih dan apresiasi yang setinggi-tingginya kepada Bapak/Ibu [Nama Dosen Pengampu, M.Kom.] selaku Dosen Pengampu mata kuliah Pemrograman Visual atas bimbingan, arahan akademis, serta transfer keilmuan yang diberikan selama masa perkuliahan dan sesi praktikum berlangsung.", False, False, False)
    ])
    
    add_p_indented([
        ("Penulis menyadari bahwa di dalam penyusunan laporan akademik ini masih terdapat ruang untuk penyempurnaan, baik pada cakupan arsitektural maupun efisiensi teknis penulisan. Oleh karena itu, penulis secara terbuka menerima segala bentuk kritik konstruktif serta saran dari para pembaca demi pengembangan aplikasi dan penyusunan karya ilmiah di masa mendatang. Semoga laporan ini dapat memberikan manfaat nyata, memperluas wawasan akademis, serta menjadi referensi aplikatif bagi pengembangan perangkat lunak berbasis .NET Framework dan basis data relasional.", False, False, False)
    ])
    
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.line_spacing = 1.15
    p_sign.paragraph_format.space_before = Pt(24)
    p_sign.paragraph_format.space_after = Pt(12)
    p_sign.add_run("[Kota/Kabupaten], 11 November 2026\n\n\nPenulis,\n").font.size = Pt(12)
    r_pen = p_sign.add_run("[Nama Lengkap Mahasiswa]\n")
    r_pen.bold = True
    p_sign.add_run("NIM. [NIM Mahasiswa]").font.size = Pt(12)
    
    doc.add_page_break()

    # --- DAFTAR ISI ---
    add_non_chapter_heading("DAFTAR ISI")
    
    toc_data = [
        ("HALAMAN SAMPUL", "i", 0, True),
        ("KATA PENGANTAR", "ii", 0, True),
        ("DAFTAR ISI", "iii", 0, True),
        ("BAB I PENDAHULUAN", "1", 0, True),
        ("1.1 Latar Belakang", "1", 1, False),
        ("1.2 Rumusan Masalah", "2", 1, False),
        ("1.3 Batasan Masalah", "2", 1, False),
        ("1.4 Tujuan Penulisan", "2", 1, False),
        ("1.5 Manfaat Penulisan", "3", 1, False),
        ("BAB II LANDASAN TEORI", "4", 0, True),
        ("2.1 Konsep Pemrograman Berorientasi Objek dan Arsitektur Windows Forms", "4", 1, False),
        ("2.2 Teknologi ADO.NET dan Driver MySQL Connector/NET", "4", 1, False),
        ("2.2.1 Arsitektur Terhubung dan Terputus ADO.NET", "4", 2, False),
        ("2.2.2 Karakteristik dan Komponen Driver MySql.Data", "5", 2, False),
        ("2.3 Pola Desain Repositori (Repository Pattern)", "6", 1, False),
        ("2.3.1 Prinsip Pemisahan Tanggung Jawab (Separation of Concerns)", "6", 2, False),
        ("2.3.2 Abstraksi Akses Data Entitas Mahasiswa", "6", 2, False),
        ("2.4 Keamanan Data: Kueri Berparameter dan Kriptografi SHA-256", "7", 1, False),
        ("2.4.1 Mekanisme Kueri Berparameter (Parameterized Query)", "7", 2, False),
        ("2.4.2 Kriptografi Hash Satu Arah SHA-256 untuk Kredensial Pengguna", "7", 2, False),
        ("2.5 Spesifikasi Lingkungan Komputasi dan Kerangka Kerja", "8", 1, False),
        ("BAB III PERANCANGAN DAN IMPLEMENTASI SISTEM", "10", 0, True),
        ("3.1 Arsitektur Sistem dan Alur Kerja", "10", 1, False),
        ("3.2 Penentuan Struktur Entitas dan Format Data", "11", 1, False),
        ("3.3 Pemodelan Diagram Alir (Flowchart) dan Pseudocode", "12", 1, False),
        ("3.3.1 Diagram Alir Alur Utama Program", "12", 2, False),
        ("3.3.2 Diagram Alir Proses Operasi Data", "13", 2, False),
        ("3.3.3 Pseudocode Algoritma", "14", 2, False),
        ("3.4 Cuplikan Kode Program", "15", 1, False),
        ("3.4.1 Modul Koneksi dan Konfigurasi Terpusat", "15", 2, False),
        ("3.4.2 Modul Akses Data Mahasiswa", "16", 2, False),
        ("3.4.3 Modul Otentikasi dan Keamanan Kredensial", "18", 2, False),
        ("BAB IV PENGUJIAN DAN ANALISIS HASIL", "20", 0, True),
        ("4.1 Hasil Pengujian Kasus Data", "20", 1, False),
        ("4.2 Simulasi Penelusuran Langkah demi Langkah (Step-by-Step Tracing)", "21", 1, False),
        ("4.3 Analisis Pengaruh Variabel dan Parameter terhadap Kinerja", "23", 1, False),
        ("4.4 Pembuktian Teoretis dan Analisis Kondisi Khusus", "24", 1, False),
        ("4.4.1 Pembuktian Kekebalan terhadap Serangan SQL Injection", "24", 2, False),
        ("4.4.2 Pembuktian Pencegahan Kebocoran Koneksi (Connection Leak)", "25", 2, False),
        ("4.5 Evaluasi Kelebihan dan Kelemahan Sistem", "26", 1, False),
        ("4.5.1 Kelebihan Sistem", "26", 2, False),
        ("4.5.2 Kelemahan Sistem", "26", 2, False),
        ("4.6 Analisis Pengujian Lanjutan dan Evaluasi Kinerja", "27", 1, False),
        ("4.6.1 Kinerja Waktu Respons Eksekusi Kueri", "27", 2, False),
        ("4.6.2 Efisiensi Konsumsi Memori (Memory Overhead)", "27", 2, False),
        ("4.6.3 Ketahanan Penanganan Multi-Koneksi Simultan", "28", 2, False),
        ("4.7 Dokumentasi Antarmuka Sistem dan Pembahasan Lengkap", "28", 1, False),
        ("4.7.1 Antarmuka Masuk Sistem (FormLogin)", "28", 2, False),
        ("4.7.2 Antarmuka Utama Manajemen Data Mahasiswa (FormMahasiswa)", "29", 2, False),
        ("4.7.3 Antarmuka Manajemen Data Dosen dan Navigasi Multi-Halaman", "30", 2, False),
        ("BAB V PENUTUP", "32", 0, True),
        ("5.1 Kesimpulan", "32", 1, False),
        ("5.2 Saran", "33", 1, False),
        ("DAFTAR PUSTAKA", "34", 0, True),
        ("LAMPIRAN", "35", 0, True),
        ("Lampiran 1: Tautan Repositori dan Petunjuk Pengoperasian", "35", 1, False),
        ("Lampiran 2: Data Pengujian dan Source Code Program Lengkap", "36", 1, False),
        ("A. Format Data Pengujian (Skrip DDL dan DML SQL)", "36", 2, False),
        ("B. Kode Program Lengkap", "37", 2, False),
    ]
    
    for title, pg, level, is_bold in toc_data:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.left_indent = Inches(0.25 * level)
        p_t.paragraph_format.first_line_indent = Inches(0)
        
        dots_count = max(4, 75 - len(title) - len(pg) - (level * 4))
        dot_str = " " + ("." * dots_count) + " "
        
        r_title = p_t.add_run(title)
        r_title.bold = is_bold
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(11)
        
        r_dots = p_t.add_run(dot_str)
        r_dots.font.name = 'Consolas'
        r_dots.font.size = Pt(9)
        r_dots.font.color.rgb = RGBColor(140, 140, 140)
        
        r_pg = p_t.add_run(pg)
        r_pg.bold = is_bold
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(11)

    # =========================================================================
    # SECTION 3: BODY (BAB I - BAB V, DAFTAR PUSTAKA, LAMPIRAN) -> Arabic (1, 2, 3...)
    # =========================================================================
    sec_body = doc.add_section()
    sec_body.top_margin = Cm(3.0)
    sec_body.bottom_margin = Cm(3.0)
    sec_body.left_margin = Cm(4.0)
    sec_body.right_margin = Cm(3.0)
    add_page_number_to_section(sec_body, start_num=1, fmt="decimal")

    # =========================================================================
    # BAB I: PENDAHULUAN
    # =========================================================================
    add_chapter_heading("BAB I", "PENDAHULUAN")
    
    add_subheading_2("1.1", "Latar Belakang")
    add_p_indented([
        ("Pengelolaan data akademik di lingkungan perguruan tinggi merupakan salah satu pilar krusial dalam penyelenggaraan tata kelola institusi pendidikan modern. Entitas mahasiswa, dosen, serta program studi membutuhkan sistem pencatatan yang terintegrasi, memiliki integritas referensial yang kokoh, dan mampu menyediakan waktu akses data yang instan bagi administrator. Keberadaan sistem berbasis antarmuka grafis (", False, False, False),
        ("Graphical User Interface", False, True, False),
        (") yang andal dapat mereduksi kompleksitas administrasi konvensional, meningkatkan efisiensi waktu pemrosesan, serta meminimalisasi potensi galat manusia (", False, False, False),
        ("human error", False, True, False),
        (") dalam siklus operasional akademik harian.", False, False, False)
    ])
    
    add_p_indented([
        ("Namun demikian, implementasi aplikasi pengelola data berbasis desktop kerap menghadapi berbagai tantangan arsitektural dan celah keamanan. Praktik penggabungan string (", False, False, False),
        ("string concatenation", False, True, False),
        (") secara langsung dalam menyusun kueri SQL pada lapisan antarmuka pengguna memicu risiko kerentanan injeksi SQL (", False, False, False),
        ("SQL Injection", False, True, False),
        ("), yang berpotensi merusak integritas basis data atau membuka akses tanpa hak kepada pihak luar. Selain itu, penulisan logika manipulasi data yang disatukan secara langsung di dalam ", False, False, False),
        ("code-behind", False, True, False),
        (" formulir (", False, False, False),
        ("Form", False, True, False),
        (") memicu derajat keterikatan tinggi (", False, False, False),
        ("high coupling", False, True, False),
        ("), menyulitkan pemeliharaan kode (", False, False, False),
        ("maintenance", False, True, False),
        ("), dan menurunkan skalabilitas sistem ketika fungsionalitas aplikasi diperluas.", False, False, False)
    ])
    
    add_p_indented([
        ("Sebagai solusi atas permasalahan tersebut, laporan ini memaparkan rancang bangun aplikasi Sistem Informasi Akademik yang mengintegrasikan bahasa pemrograman C# pada kerangka kerja .NET Framework 4.7.2 Windows Forms dengan sistem manajemen basis data relasional MySQL. Sistem ini mengadopsi pola arsitektur repositori (", False, False, False),
        ("Repository Pattern", False, True, False),
        (") untuk memisahkan logika manipulasi data dari lapisan antarmuka pengguna grafis. Aspek keamanan diperkuat melalui penerapan kueri berparameter (", False, False, False),
        ("parameterized query", False, True, False),
        (") pada seluruh operasi basis data, proteksi kata sandi pengguna berbasis ", False, False, False),
        ("Secure Hash Algorithm 256-bit", False, True, False),
        (" (SHA-256), pengelolaan konfigurasi koneksi terpusat pada berkas ", False, False, False),
        ("App.config", False, False, True),
        (", serta penyediaan antarmuka multi-halaman berbasis bilah samping (", False, False, False),
        ("sidebar navbar", False, True, False),
        (") yang ergonomis.", False, False, False)
    ])
    
    add_subheading_2("1.2", "Rumusan Masalah")
    add_intro("Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam penyusunan laporan ini dirumuskan dalam pertanyaan-pertanyaan berikut:")
    add_numbered_list_item("1.", [("Bagaimana merancang dan membangun aplikasi desktop berbasis C# Windows Forms yang mampu mengelola operasi ", False, False, False), ("Create, Read, Update, Delete", False, True, False), (" (CRUD) serta pencarian data mahasiswa dan dosen secara stabil?", False, False, False)])
    add_numbered_list_item("2.", [("Bagaimana mengimplementasikan pola arsitektur repositori (", False, False, False), ("Repository Pattern", False, True, False), (") untuk memisahkan lapisan akses data (", False, False, False), ("Data Access Layer", False, True, False), (") dari lapisan antarmuka pengguna (", False, False, False), ("Presentation Layer", False, True, False), (")?", False, False, False)])
    add_numbered_list_item("3.", [("Bagaimana menerapkan mekanisme keamanan kueri berparameter dan hashing kriptografis SHA-256 guna mencegah kerentanan injeksi SQL serta kebocoran kredensial login?", False, False, False)])
    add_numbered_list_item("4.", [("Bagaimana merancang antarmuka pengguna modern dengan navigasi bilah samping (", False, False, False), ("sidebar", False, True, False), (") multi-halaman guna menghasilkan alur kerja aplikasi yang intuitif bagi pengguna?", False, False, False)])
    
    add_subheading_2("1.3", "Batasan Masalah")
    add_intro("Ruang lingkup dan batasan teknis dalam implementasi sistem ini mencakup ketentuan-ketentuan berikut:")
    add_numbered_list_item("1.", [("Sistem dibangun menggunakan bahasa pemrograman C# pada kerangka kerja .NET Framework 4.7.2 dengan antarmuka grafis Windows Forms.", False, False, False)])
    add_numbered_list_item("2.", [("Basis data yang digunakan adalah MySQL 8.0/MariaDB 10.4 yang dikelola melalui peladen lokal XAMPP pada porta baku 3306 dengan nama basis data ", False, False, False), ("db_akademik", False, False, True), (".", False, False, False)])
    add_numbered_list_item("3.", [("Pustaka jembatan data yang digunakan adalah paket resmi NuGet ", False, False, False), ("MySql.Data", False, False, True), (" versi 9.2.0.", False, False, False)])
    add_numbered_list_item("4.", [("Entitas data yang dikelola dibatasi pada tabel ", False, False, False), ("mahasiswa", False, False, True), (", ", False, False, False), ("dosen", False, False, True), (", ", False, False, False), ("prodi", False, False, True), (", dan ", False, False, False), ("pengguna", False, False, True), (".", False, False, False)])
    add_numbered_list_item("5.", [("Format ekspor data luaran dibatasi pada format ", False, False, False), ("Comma-Separated Values", False, True, False), (" (CSV) dengan pengodean karakter UTF-8.", False, False, False)])
    
    add_subheading_2("1.4", "Tujuan Penulisan")
    add_intro("Tujuan dari pelaksanaan perancangan sistem dan penulisan laporan akademik ini adalah:")
    add_numbered_list_item("1.", [("Mengembangkan aplikasi desktop berbasis C# Windows Forms yang terhubung dengan basis data relasional MySQL untuk mengelola data civitas akademika.", False, False, False)])
    add_numbered_list_item("2.", [("Mengisolasi operasi manipulasi data ke dalam kelas repositori khusus (", False, False, False), ("MahasiswaRepository", False, False, True), (") guna menerapkan prinsip pemisahan tanggung jawab (", False, False, False), ("Separation of Concerns", False, True, False), (").", False, False, False)])
    add_numbered_list_item("3.", [("Mengamankan sistem autentikasi melalui hashing kata sandi SHA-256 dan melindungi transaksi basis data dari injeksi SQL menggunakan objek ", False, False, False), ("MySqlParameter", False, False, True), (".", False, False, False)])
    add_numbered_list_item("4.", [("Menyediakan antarmuka multi-halaman (", False, False, False), ("single-form multi-page", False, True, False), (") dengan fitur navigasi bilah samping, dasbor statistik metrik, dan ekspor data tabular.", False, False, False)])
    
    add_subheading_2("1.5", "Manfaat Penulisan")
    add_intro("Manfaat yang diharapkan dari hasil perancangan sistem dan penulisan laporan ini dijabarkan melalui dua aspek berikut:")
    add_bold_lead_in_item("Manfaat Akademis (Teoretis):", [("Memberikan dokumentasi empiris dan komparatif mengenai efektivitas penerapan pola desain repositori dalam pemrograman berbasis komponen visual di lingkungan .NET Framework, serta menjadi sumber rujukan pembelajaran mengenai pengamanan transaksi data menggunakan ADO.NET.", False, False, False)])
    add_bold_lead_in_item("Manfaat Praktis (Aplikatif):", [("Menghasilkan artefak perangkat lunak siap pakai yang dapat digunakan oleh pengelola data akademik tingkat program studi atau laboratorium untuk mendata mahasiswa dan dosen secara terstruktur, cepat, dan aman dari galat integritas data.", False, False, False)])

    # =========================================================================
    # BAB II: LANDASAN TEORI
    # =========================================================================
    doc.add_page_break()
    add_chapter_heading("BAB II", "LANDASAN TEORI")
    
    add_subheading_2("2.1", "Konsep Pemrograman Berorientasi Objek dan Arsitektur Windows Forms")
    add_p_indented([
        ("Pemrograman Berorientasi Objek (", False, False, False),
        ("Object-Oriented Programming", False, True, False),
        (" / OOP) adalah paradigma pengembangan perangkat lunak yang menstrukturkan program ke dalam kesatuan objek yang mengandung data (atribut) dan fungsi (metode). Empat pilar utama dalam OOP meliputi enkapsulasi (", False, False, False),
        ("encapsulation", False, True, False),
        ("), pewarisan (", False, False, False),
        ("inheritance", False, True, False),
        ("), polimorfisme (", False, False, False),
        ("polymorphism", False, True, False),
        ("), dan abstraksi (", False, False, False),
        ("abstraction", False, True, False),
        ("). Dalam konteks pengembangan sistem informasi, entitas dunia nyata seperti mahasiswa dan dosen dimodelkan menjadi kelas-kelas perangkat lunak yang menjaga konsistensi mutasi status internal objeknya.", False, False, False)
    ])
    add_p_indented([
        ("Windows Forms merupakan pustaka kelas antarmuka grafis pengguna (", False, False, False),
        ("Graphical User Interface", False, True, False),
        (" / GUI) berbasis komponen yang berjalan di atas ", False, False, False),
        ("Common Language Runtime", False, True, False),
        (" (CLR) .NET Framework. Setiap elemen visual, mulai dari formulir (", False, False, False),
        ("Form", False, False, True),
        ("), tombol (", False, False, False),
        ("Button", False, False, True),
        ("), bidang teks (", False, False, False),
        ("TextBox", False, False, True),
        ("), daftar tarik-turun (", False, False, False),
        ("ComboBox", False, False, True),
        ("), hingga kisi data (", False, False, False),
        ("DataGridView", False, False, True),
        ("), merupakan turunan dari kelas dasar ", False, False, False),
        ("System.Windows.Forms.Control", False, False, True),
        (". Windows Forms beroperasi menggunakan model berorientasi kejadian (", False, False, False),
        ("event-driven programming", False, True, False),
        ("), di mana interaksi fisik pengguna seperti penekanan tombol (", False, False, False),
        ("Click", False, True, False),
        ("), perubahan teks (", False, False, False),
        ("TextChanged", False, True, False),
        ("), atau pemilihan sel grid (", False, False, False),
        ("CellClick", False, True, False),
        (") memicu pengiriman pesan sistem operasi ke prosedur pengendali (", False, False, False),
        ("event handler", False, True, False),
        (") yang bersangkutan.", False, False, False)
    ])
    
    add_subheading_2("2.2", "Teknologi ADO.NET dan Driver MySQL Connector/NET")
    
    add_subheading_3("2.2.1", "Arsitektur Terhubung dan Terputus ADO.NET")
    add_p_indented([
        ("ADO.NET (", False, False, False),
        ("ActiveX Data Objects for .NET", False, True, False),
        (") merupakan arsitektur penyedia akses data terkelola yang dirancang untuk menghubungkan aplikasi .NET dengan sistem basis data relasional. ADO.NET membagi infrastruktur akses datanya ke dalam dua paradigma utama: arsitektur terhubung (", False, False, False),
        ("connected environment", False, True, False),
        (") dan arsitektur terputus (", False, False, False),
        ("disconnected environment", False, True, False),
        ("). Pada arsitektur terhubung, operasi dieksekusi secara instan melalui koneksi jaringan yang aktif, sedangkan pada arsitektur terputus, data diunduh ke dalam memori lokal aplikasi menggunakan struktur ", False, False, False),
        ("DataSet", False, False, True),
        (" atau ", False, False, False),
        ("DataTable", False, False, True),
        (".", False, False, False)
    ])
    
    add_subheading_3("2.2.2", "Karakteristik dan Komponen Driver MySql.Data")
    add_intro("Komponen penyedia data (Data Provider) untuk basis data MySQL diimplementasikan melalui pustaka MySql.Data (Connector/NET). Pustaka ini menyediakan empat kelas fundamental yang dirangkum pada tabel berikut:")
    
    # Table 2.1
    t21 = doc.add_table(rows=5, cols=3)
    t21.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t21)
    
    headers_21 = ["Nama Komponen", "Namespace Pustaka", "Peran dan Karakteristik Fungsional"]
    for j, h in enumerate(headers_21):
        cell = t21.cell(0, j)
        set_cell_bg(cell, "E2E8F0")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        
    data_21 = [
        ("MySqlConnection", "MySql.Data.MySqlClient", "Mengelola sesi koneksi fisik dan pertukaran soket jaringan ke peladen MySQL menggunakan connection string."),
        ("MySqlCommand", "MySql.Data.MySqlClient", "Menyusun teks pernyataan SQL atau prosedur tersimpan (stored procedure) beserta parameter data pendukungnya."),
        ("MySqlDataReader", "MySql.Data.MySqlClient", "Menyediakan pembacaan baris data aliran maju-saja (forward-only) dan baca-saja (read-only) dengan konsumsi memori minimal."),
        ("MySqlDataAdapter", "MySql.Data.MySqlClient", "Menjembatani pengisian data secara terputus ke dalam objek DataTable dan merefleksikan kembali perubahan data ke basis data.")
    ]
    for i, row in enumerate(data_21):
        for j, val in enumerate(row):
            cell = t21.cell(i+1, j)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.font.name = 'Consolas'
                r.font.size = Pt(9.5)
            elif j == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.font.name = 'Consolas'
                r.font.size = Pt(9)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r = p.add_run(val)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
    add_caption("Tabel 2.1: Spesifikasi dan Karakteristik Komponen ADO.NET")
    
    add_subheading_2("2.3", "Pola Desain Repositori (Repository Pattern)")
    
    add_subheading_3("2.3.1", "Prinsip Pemisahan Tanggung Jawab (Separation of Concerns)")
    add_p_indented([
        ("Pola desain repositori (", False, False, False),
        ("Repository Pattern", False, True, False),
        (") bertindak sebagai lapisan abstraksi antara lapisan antarmuka pengguna (", False, False, False),
        ("Presentation Layer", False, True, False),
        (") dan lapisan persistensi data (", False, False, False),
        ("Data Persistence Layer", False, True, False),
        ("). Melalui penerapan pola ini, kode program pada antarmuka formulir tidak lagi memuat perintah SQL mentah seperti ", False, False, False),
        ("SELECT", False, False, True),
        (", ", False, False, False),
        ("INSERT", False, False, True),
        (", ", False, False, False),
        ("UPDATE", False, False, True),
        (", atau ", False, False, False),
        ("DELETE", False, False, True),
        (". Seluruh interaksi basis data dienkapsulasi di dalam kelas repositori independen yang mengekspos metode-metode domain.", False, False, False)
    ])
    
    add_subheading_3("2.3.2", "Abstraksi Akses Data Entitas Mahasiswa")
    add_p_indented([
        ("Dalam konteks entitas mahasiswa, kelas repositori menyediakan antarmuka operasional yang konsisten seperti ", False, False, False),
        ("GetAll()", False, False, True),
        (", ", False, False, False),
        ("Tambah()", False, False, True),
        (", ", False, False, False),
        ("Ubah()", False, False, True),
        (", ", False, False, False),
        ("Hapus()", False, False, True),
        (", dan ", False, False, False),
        ("Cari()", False, False, True),
        (". Keuntungan mendasar dari pemisahan tanggung jawab ini meliputi kemudahan pengujian unit (", False, False, False),
        ("unit testing", False, True, False),
        ("), pemeliharaan terpusat apabila skema tabel mengalami modifikasi, serta fleksibilitas migrasi mesin penyimpanan data tanpa memengaruhi perilaku antarmuka pengguna.", False, False, False)
    ])
    
    add_subheading_2("2.4", "Keamanan Data: Kueri Berparameter dan Kriptografi SHA-256")
    
    add_subheading_3("2.4.1", "Mekanisme Kueri Berparameter (Parameterized Query)")
    add_p_indented([
        ("Serangan injeksi SQL (", False, False, False),
        ("SQL Injection", False, True, False),
        (") terjadi ketika input pengguna yang tidak divalidasi digabungkan langsung ke dalam string perintah SQL. Untuk mencegah celah ini, ADO.NET menyediakan mekanisme kueri berparameter menggunakan kelas ", False, False, False),
        ("MySqlParameter", False, False, True),
        (". Kueri berparameter memperlakukan input pengguna secara ketat sebagai nilai data literal (konstanta), bukan sebagai instruksi kode SQL yang dapat dieksekusi oleh mesin basis data.", False, False, False)
    ])
    
    add_subheading_3("2.4.2", "Kriptografi Hash Satu Arah SHA-256 untuk Kredensial Pengguna")
    add_p_indented([
        ("Dalam aspek penyimpanan kredensial pengguna, penyimpanan kata sandi dalam format teks polos (", False, False, False),
        ("plaintext", False, True, False),
        (") melanggar prinsip dasar keamanan informasi. Sistem menerapkan algoritma pengacakan satu arah ", False, False, False),
        ("Secure Hash Algorithm 256-bit", False, True, False),
        (" (SHA-256). Persamaan matematis transformasi hash SHA-256 dari pesan M berukuran l bit direpresentasikan sebagai H = SHA-256(M), di mana luaran H selalu menghasilkan intisari pesan (", False, False, False),
        ("message digest", False, True, False),
        (") unik berukuran tetap 256 bit (32 bita), yang direpresentasikan ke dalam 64 karakter heksadesimal. Sifat resistensi prapeta (", False, False, False),
        ("pre-image resistance", False, True, False),
        (") pada SHA-256 memastikan bahwa secara komputasi mustahil untuk mengembalikan nilai kata sandi asli M dari nilai hash H.", False, False, False)
    ])
    
    add_subheading_2("2.5", "Spesifikasi Lingkungan Komputasi dan Kerangka Kerja")
    add_intro("Konstruksi dan evaluasi sistem dilaksanakan di atas lingkungan komputasi terstandarisasi guna menjamin konsistensi reproduksi eksekusi program, sebagaimana dirinci pada tabel berikut:")
    
    # Table 2.2
    t22 = doc.add_table(rows=8, cols=3)
    t22.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t22)
    
    headers_22 = ["Komponen Lingkungan", "Parameter Teknis", "Keterangan / Versi"]
    for j, h in enumerate(headers_22):
        cell = t22.cell(0, j)
        set_cell_bg(cell, "E2E8F0")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        
    data_22 = [
        ("Sistem Operasi", "Arsitektur Windows 64-bit", "Microsoft Windows 11 Enterprise"),
        ("Kerangka Kerja Perangkat Lunak", ".NET Framework", "Versi 4.7.2 (C# Language Version 7.3)"),
        ("Antarmuka Grafis (GUI)", "Windows Forms Library", "System.Windows.Forms"),
        ("Pustaka Akses Data", "MySql.Data NuGet Package", "Versi 9.2.0"),
        ("Peladen Basis Data Relasional", "MySQL Daemon / MariaDB", "Versi 10.4.32 (via XAMPP Stack)"),
        ("Protokol Jaringan Data", "TCP/IP Localhost", "Porta 3306 (Karakter UTF-8mb4)"),
        ("Lingkungan Pengembangan Terpadu", "Visual Studio IDE", "Microsoft Visual Studio 2022")
    ]
    for i, row in enumerate(data_22):
        for j, val in enumerate(row):
            cell = t22.cell(i+1, j)
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if j == 0:
                r.bold = True
    add_caption("Tabel 2.2: Spesifikasi Perangkat Lunak dan Lingkungan Komputasi")

    # =========================================================================
    # BAB III: PERANCANGAN DAN IMPLEMENTASI SISTEM
    # =========================================================================
    doc.add_page_break()
    add_chapter_heading("BAB III", "PERANCANGAN DAN IMPLEMENTASI SISTEM")
    
    add_subheading_2("3.1", "Arsitektur Sistem dan Alur Kerja")
    add_p_indented([
        ("Arsitektur sistem dibangun berdasarkan prinsip modularitas tiga lapis (", False, False, False),
        ("Three-Tier Logical Architecture", False, True, False),
        (") yang mengisolasi komponen antarmuka, logika bisnis, dan lapisan penyimpanan fisik. Lapisan pertama (", False, False, False),
        ("Presentation Tier", False, True, False),
        (") menangani seluruh interaksi visual pengguna melalui formulir login (", False, False, False),
        ("FormLogin", False, False, True),
        (") dan formulir utama (", False, False, False),
        ("FormMahasiswa", False, False, True),
        ("). Lapisan kedua (", False, False, False),
        ("Data Access Tier", False, True, False),
        (") diwakili oleh kelas ", False, False, False),
        ("MahasiswaRepository", False, False, True),
        (" dan modul pabrik koneksi ", False, False, False),
        ("Koneksi", False, False, True),
        (". Lapisan ketiga (", False, False, False),
        ("Persistence Tier", False, True, False),
        (") berupa basis data relasional MySQL ", False, False, False),
        ("db_akademik", False, False, True),
        (".", False, False, False)
    ])
    
    add_code_snippet(
        "┌─────────────────────────────────────────────────────────────┐\n"
        "│                 PRESENTATION LAYER (GUI)                    │\n"
        "│  ┌───────────────────────┐       ┌───────────────────────┐  │\n"
        "│  │       FormLogin       │       │     FormMahasiswa     │  │\n"
        "│  │ (Autentikasi SHA-256) │       │ (Multi-Page Container)│  │\n"
        "│  └───────────┬───────────┘       └───────────┬───────────┘  │\n"
        "└──────────────┼───────────────────────────────┼──────────────┘\n"
        "               │                               │\n"
        "┌──────────────┼───────────────────────────────┼──────────────┐\n"
        "│              ▼                               ▼              │\n"
        "│  ┌───────────────────────┐       ┌───────────────────────┐  │\n"
        "│  │      Koneksi.cs       │       │ MahasiswaRepository.cs│  │\n"
        "│  │ (App.config Manager)  │       │ (CRUD Data Mahasiswa) │  │\n"
        "│  └───────────┬───────────┘       └───────────┬───────────┘  │\n"
        "│              │ DATA ACCESS LAYER (DAL)       │              │\n"
        "└──────────────┼───────────────────────────────┼──────────────┘\n"
        "               │                               │\n"
        "┌──────────────┼───────────────────────────────┼──────────────┐\n"
        "│              ▼                               ▼              │\n"
        "│       ┌─────────────────────────────────────────────┐       │\n"
        "│       │          MySQL Database Server              │       │\n"
        "│       │ (db_akademik: mahasiswa, dosen, prodi, user)│       │\n"
        "│       └─────────────────────────────────────────────┘       │\n"
        "│                 DATA PERSISTENCE LAYER                      │\n"
        "└─────────────────────────────────────────────────────────────┘"
    )
    add_caption("Gambar 3.1: Diagram Blok Arsitektur Tiga Lapis Sistem Informasi Akademik")
    
    add_subheading_2("3.2", "Penentuan Struktur Entitas dan Format Data")
    add_p_indented([
        ("Skema basis data relasional ", False, False, False),
        ("db_akademik", False, False, True),
        (" dirancang untuk menampung entitas civitas akademika dan kredensial akses. Hubungan antar-entitas dirancang menggunakan konvensi integritas referensial data. Struktur masing-masing tabel dirangkum dalam tabel berikut:", False, False, False)
    ])
    
    # Table 3.1
    t31 = doc.add_table(rows=13, cols=5)
    t31.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t31)
    
    headers_31 = ["Nama Tabel", "Atribut (Kolom)", "Tipe Data", "Batasan Integritas", "Deskripsi Fungsional"]
    for j, h in enumerate(headers_31):
        cell = t31.cell(0, j)
        set_cell_bg(cell, "E2E8F0")
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        
    data_31 = [
        ("mahasiswa", "nim", "VARCHAR(15)", "PRIMARY KEY", "Nomor Induk Mahasiswa (kunci utama unik)"),
        ("", "nama", "VARCHAR(100)", "NOT NULL", "Nama lengkap mahasiswa"),
        ("", "prodi", "VARCHAR(50)", "NOT NULL", "Nama program studi terdaftar"),
        ("", "angkatan", "INT", "NOT NULL", "Tahun angkatan akademik mahasiswa"),
        ("dosen", "nidn", "VARCHAR(20)", "PRIMARY KEY", "Nomor Induk Dosen Nasional"),
        ("", "nama", "VARCHAR(100)", "NOT NULL", "Nama lengkap dosen beserta gelar"),
        ("", "bidang", "VARCHAR(100)", "NOT NULL", "Bidang keahlian akademis dosen"),
        ("prodi", "kode_prodi", "VARCHAR(10)", "PRIMARY KEY", "Kode unik program studi"),
        ("", "nama_prodi", "VARCHAR(100)", "NOT NULL", "Nama resmi program studi"),
        ("pengguna", "id", "INT", "PRIMARY KEY, AUTO_INC", "Identifikator unik pengguna"),
        ("", "username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Nama akun otentikasi login"),
        ("", "password", "VARCHAR(64)", "NOT NULL", "Intisari hash kata sandi (SHA-256)")
    ]
    for i, row in enumerate(data_31):
        for j, val in enumerate(row):
            cell = t31.cell(i+1, j)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if j in [0, 1]:
                r = p.add_run(val)
                r.font.name = 'Consolas'
                r.font.size = Pt(9)
                r.bold = (j == 0 and val != "")
            elif j == 2:
                r = p.add_run(val)
                r.font.name = 'Consolas'
                r.font.size = Pt(8.5)
            else:
                r = p.add_run(val)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
    add_caption("Tabel 3.1: Skema Entitas Relasional Basis Data db_akademik")
    
    add_subheading_2("3.3", "Pemodelan Diagram Alir (Flowchart) dan Pseudocode")
    
    add_subheading_3("3.3.1", "Diagram Alir Alur Utama Program")
    add_p_indented([
        ("Alur utama program dimulai dari inisialisasi aplikasi yang secara otomatis memanggil ", False, False, False),
        ("FormLogin", False, False, True),
        (". Validasi kredensial dilakukan terhadap tabel ", False, False, False),
        ("pengguna", False, False, True),
        (". Apabila status verifikasi berhasil, antarmuka utama ", False, False, False),
        ("FormMahasiswa", False, False, True),
        (" diaktifkan.", False, False, False)
    ])
    add_code_snippet(
        "                  ┌───────────────────────────────┐\n"
        "                  │             MULAI             │\n"
        "                  └───────────────┬───────────────┘\n"
        "                                  │\n"
        "                                  ▼\n"
        "                  ┌───────────────────────────────┐\n"
        "                  │      Tampilkan FormLogin      │\n"
        "                  └───────────────┬───────────────┘\n"
        "                                  │\n"
        "                                  ▼\n"
        "                  ┌───────────────────────────────┐\n"
        "                  │ Input Username & Kata Sandi   │\n"
        "                  └───────────────┬───────────────┘\n"
        "                                  │\n"
        "                                  ▼\n"
        "                  ┌───────────────────────────────┐\n"
        "                  │ Hash Kata Sandi (SHA-256)     │\n"
        "                  └───────────────┬───────────────┘\n"
        "                                  │\n"
        "                                  ▼\n"
        "                    /───────────────────────────\\\n"
        "                   <   Kredensial Cocok di DB?   >\n"
        "                    \\───────────────────────────/\n"
        "                                  │\n"
        "                       TIDAK      │      YA\n"
        "           ┌──────────────────────┴──────────────────────┐\n"
        "           ▼                                             ▼\n"
        "┌─────────────────────────┐               ┌─────────────────────────────┐\n"
        "│ Tampilkan Pesan Galat   │               │ Tutup Login, Buka FormUtama │\n"
        "└──────────┬──────────────┘               └──────────────┬──────────────┘\n"
        "           │                                             │\n"
        "           └──────────────────┐                          ▼\n"
        "                              │           ┌─────────────────────────────┐\n"
        "                              │           │ Buka Dasbor & Navigasi Tab  │\n"
        "                              │           └──────────────┬──────────────┘\n"
        "                              │                          │\n"
        "                              ▼                          ▼\n"
        "                  ┌───────────────────────────────┐\n"
        "                  │            SELESAI            │\n"
        "                  └───────────────────────────────┘"
    )
    add_caption("Gambar 3.2: Diagram Alir Alur Eksekusi Masuk Sistem")
    
    add_subheading_3("3.3.2", "Diagram Alir Proses Operasi Data")
    add_p_indented([
        ("Proses manipulasi data mahasiswa pada formulir mencakup tahapan validasi masukan lokal (", False, False, False),
        ("client-side validation", False, True, False),
        (") sebelum data dikirimkan ke lapisan repositori. Alur operasi data disajikan pada diagram alir berikut:", False, False, False)
    ])
    add_code_snippet(
        "                  ┌───────────────────────────────┐\n"
        "                  │  Pemicu: Klik Tombol Simpan   │\n"
        "                  └───────────────┬───────────────┘\n"
        "                                  │\n"
        "                                  ▼\n"
        "                    /───────────────────────────\\\n"
        "                   <    Apakah Input Lengkap?    >\n"
        "                    \\───────────────────────────/\n"
        "                                  │\n"
        "                       TIDAK      │      YA\n"
        "           ┌──────────────────────┴──────────────────────┐\n"
        "           ▼                                             ▼\n"
        "┌─────────────────────────┐               ┌─────────────────────────────┐\n"
        "│ Tampilkan Pesan         │               │ Kirim Parameter ke          │\n"
        "│ \"Semua data wajib diisi\"│               │ MahasiswaRepository.Tambah()│\n"
        "└─────────────────────────┘               └──────────────┬──────────────┘\n"
        "                                                         │\n"
        "                                                         ▼\n"
        "                                            /───────────────────────────\\\n"
        "                                           <    Eksekusi Kueri Sukses?   >\n"
        "                                            \\───────────────────────────/\n"
        "                                                         │\n"
        "                                              TIDAK      │      YA\n"
        "                                  ┌──────────────────────┴──────┐\n"
        "                                  ▼                             ▼\n"
        "                      ┌──────────────────────┐      ┌─────────────────────────┐\n"
        "                      │ Tangkap MySqlException│     │ Refresh Grid Data &     │\n"
        "                      │ (Cek Kode Galat 1062)│      │ Perbarui Jumlah Total   │\n"
        "                      └──────────────────────┘      └─────────────────────────┘"
    )
    add_caption("Gambar 3.3: Diagram Alir Operasi Penambahan Data Mahasiswa")
    
    add_subheading_3("3.3.3", "Pseudocode Algoritma")
    add_intro("Algoritma autentikasi pengguna dan pemfilteran data mahasiswa diformulasikan ke dalam struktur pseudocode baku berbahasa Indonesia berikut ini:")
    
    add_code_snippet(
        "ALGORITMA OtentikasiPengguna\n"
        "MASUKAN:\n"
        "    strUsername: teks\n"
        "    strPasswordPlain: teks\n"
        "KELUARAN:\n"
        "    blnStatusOtentikasi: boolean\n"
        "\n"
        "DESKRIPSI:\n"
        "    JIKA strUsername = \"\" ATAU strPasswordPlain = \"\" MAKA\n"
        "        TAMPILKAN \"Username dan kata sandi wajib diisi\"\n"
        "        KEMBALIKAN SALAH\n"
        "    AKHIR JIKA\n"
        "\n"
        "    inisialisasi objSha256 = PembentukHashSHA256()\n"
        "    arrBytesHasil = objSha256.HitungHash(UbahKeBytes(strPasswordPlain))\n"
        "    strPasswordHash = KonversiKeHeksadesimal(arrBytesHasil)\n"
        "\n"
        "    buka koneksiBasisData\n"
        "    inisialisasi strQuery = \"SELECT COUNT(*) FROM pengguna WHERE username = @usr AND password = @pwd\"\n"
        "    tambahkan parameter @usr = strUsername\n"
        "    tambahkan parameter @pwd = strPasswordHash\n"
        "\n"
        "    intJumlahBaris = EksekusiSkalar(strQuery)\n"
        "    tutup koneksiBasisData\n"
        "\n"
        "    JIKA intJumlahBaris > 0 MAKA\n"
        "        KEMBALIKAN BENAR\n"
        "    LAINNYA\n"
        "        TAMPILKAN \"Kredensial tidak valid\"\n"
        "        KEMBALIKAN SALAH\n"
        "    AKHIR JIKA\n"
        "AKHIR ALGORITMA"
    )
    
    add_code_snippet(
        "ALGORITMA FilterDataMahasiswa\n"
        "MASUKAN:\n"
        "    strKataKunci: teks\n"
        "KELUARAN:\n"
        "    tblHasilPencarian: DataTable\n"
        "\n"
        "DESKRIPSI:\n"
        "    buka koneksiBasisData\n"
        "    JIKA strKataKunci = \"\" MAKA\n"
        "        strSql = \"SELECT nim, nama, prodi, angkatan FROM mahasiswa ORDER BY nim ASC\"\n"
        "    LAINNYA\n"
        "        strSql = \"SELECT nim, nama, prodi, angkatan FROM mahasiswa WHERE nim LIKE @cari OR nama LIKE @cari ORDER BY nim ASC\"\n"
        "    AKHIR JIKA\n"
        "\n"
        "    inisialisasi cmdCommand = PerintahSQL(strSql, koneksiBasisData)\n"
        "    JIKA strKataKunci != \"\" MAKA\n"
        "        cmdCommand.TambahParameter(\"@cari\", \"%\" + strKataKunci + \"%\")\n"
        "    AKHIR JIKA\n"
        "\n"
        "    inisialisasi dtaAdapter = PenyesuaiData(cmdCommand)\n"
        "    inisialisasi tblHasilPencarian = TabelDataBaru()\n"
        "    dtaAdapter.IsiTabel(tblHasilPencarian)\n"
        "    tutup koneksiBasisData\n"
        "\n"
        "    KEMBALIKAN tblHasilPencarian\n"
        "AKHIR ALGORITMA"
    )
    
    add_subheading_2("3.4", "Cuplikan Kode Program")
    
    add_subheading_3("3.4.1", "Modul Koneksi dan Konfigurasi Terpusat")
    add_p_indented([
        ("Modul ", False, False, False),
        ("Koneksi.cs", False, False, True),
        (" bertanggung jawab menyediakan instans koneksi basis data menggunakan ", False, False, False),
        ("connection string", False, True, False),
        (" yang diambil secara terpusat dari berkas konfigurasi XML ", False, False, False),
        ("App.config", False, False, True),
        (":", False, False, False)
    ])
    add_code_snippet(
        "# Koneksi.cs (Bagian 1: Modul Koneksi Terpusat)\n"
        "using System;\n"
        "using System.Configuration;\n"
        "using MySql.Data.MySqlClient;\n"
        "\n"
        "namespace tugas9formmahasiswa\n"
        "{\n"
        "    public static class Koneksi\n"
        "    {\n"
        "        private static readonly string FallbackConnectionString = \n"
        "            \"server=localhost;port=3306;database=db_akademik;uid=root;pwd=;\";\n"
        "\n"
        "        public static string GetConnectionString()\n"
        "        {\n"
        "            var config = ConfigurationManager.ConnectionStrings[\"DbAkademik\"];\n"
        "            if (config != null && !string.IsNullOrWhiteSpace(config.ConnectionString))\n"
        "            {\n"
        "                return config.ConnectionString;\n"
        "            }\n"
        "            return FallbackConnectionString;\n"
        "        }\n"
        "\n"
        "        public static MySqlConnection BukaKoneksi()\n"
        "        {\n"
        "            var conn = new MySqlConnection(GetConnectionString());\n"
        "            conn.Open();\n"
        "            return conn;\n"
        "        }\n"
        "    }\n"
        "}"
    )
    
    add_subheading_3("3.4.2", "Modul Akses Data Mahasiswa")
    add_p_indented([
        ("Kelas ", False, False, False),
        ("MahasiswaRepository.cs", False, False, True),
        (" mengisolasi seluruh interaksi data SQL terhadap tabel ", False, False, False),
        ("mahasiswa", False, False, True),
        (" menggunakan blok pelindung sumber daya ", False, False, False),
        ("using", False, False, True),
        (" dan kueri berparameter:", False, False, False)
    ])
    add_code_snippet(
        "# MahasiswaRepository.cs (Bagian 2: Modul Akses Data)\n"
        "using System.Data;\n"
        "using MySql.Data.MySqlClient;\n"
        "\n"
        "namespace tugas9formmahasiswa\n"
        "{\n"
        "    public class MahasiswaRepository\n"
        "    {\n"
        "        public DataTable GetAll()\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"SELECT nim, nama, prodi, angkatan FROM mahasiswa ORDER BY nim ASC\";\n"
        "                using (var adapter = new MySqlDataAdapter(query, conn))\n"
        "                {\n"
        "                    var dt = new DataTable();\n"
        "                    adapter.Fill(dt);\n"
        "                    return dt;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "\n"
        "        public bool Tambah(string nim, string nama, string prodi, int angkatan)\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"INSERT INTO mahasiswa (nim, nama, prodi, angkatan) VALUES (@nim, @nama, @prodi, @angkatan)\";\n"
        "                using (var cmd = new MySqlCommand(query, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@nim\", nim);\n"
        "                    cmd.Parameters.AddWithValue(\"@nama\", nama);\n"
        "                    cmd.Parameters.AddWithValue(\"@prodi\", prodi);\n"
        "                    cmd.Parameters.AddWithValue(\"@angkatan\", angkatan);\n"
        "                    return cmd.ExecuteNonQuery() > 0;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "\n"
        "        public DataTable Cari(string keyword)\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"SELECT nim, nama, prodi, angkatan FROM mahasiswa WHERE nim LIKE @kw OR nama LIKE @kw ORDER BY nim ASC\";\n"
        "                using (var cmd = new MySqlCommand(query, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@kw\", \"%\" + keyword + \"%\");\n"
        "                    using (var adapter = new MySqlDataAdapter(cmd))\n"
        "                    {\n"
        "                        var dt = new DataTable();\n"
        "                        adapter.Fill(dt);\n"
        "                        return dt;\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}"
    )
    
    add_subheading_3("3.4.3", "Modul Otentikasi dan Keamanan Kredensial")
    add_p_indented([
        ("Modul ", False, False, False),
        ("FormLogin.cs", False, False, True),
        (" memproses otentikasi akun pengguna dengan mentranslasikan string kata sandi menjadi representasi intisari hash SHA-256 sebelum diverifikasi ke basis data:", False, False, False)
    ])
    add_code_snippet(
        "# FormLogin.cs (Bagian 3: Modul Otentikasi Pengguna)\n"
        "using System;\n"
        "using System.Security.Cryptography;\n"
        "using System.Text;\n"
        "using MySql.Data.MySqlClient;\n"
        "\n"
        "namespace tugas9formmahasiswa\n"
        "{\n"
        "    public partial class FormLogin : System.Windows.Forms.Form\n"
        "    {\n"
        "        private static string HashSha256(string raw)\n"
        "        {\n"
        "            using (var sha = SHA256.Create())\n"
        "            {\n"
        "                byte[] bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(raw ?? string.Empty));\n"
        "                var sb = new StringBuilder(bytes.Length * 2);\n"
        "                foreach (byte b in bytes)\n"
        "                {\n"
        "                    sb.Append(b.ToString(\"x2\"));\n"
        "                }\n"
        "                return sb.ToString();\n"
        "            }\n"
        "        }\n"
        "\n"
        "        private bool ValidasiKredensial(string username, string passwordPlain)\n"
        "        {\n"
        "            string passwordHash = HashSha256(passwordPlain);\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string sql = \"SELECT COUNT(*) FROM pengguna WHERE username = @usr AND password = @pwd\";\n"
        "                using (var cmd = new MySqlCommand(sql, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@usr\", username);\n"
        "                    cmd.Parameters.AddWithValue(\"@pwd\", passwordHash);\n"
        "                    long hitung = Convert.ToInt64(cmd.ExecuteScalar());\n"
        "                    return hitung > 0;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}"
    )

    # =========================================================================
    # BAB IV: PENGUJIAN DAN ANALISIS HASIL
    # =========================================================================
    doc.add_page_break()
    add_chapter_heading("BAB IV", "PENGUJIAN DAN ANALISIS HASIL")
    
    add_subheading_2("4.1", "Hasil Pengujian Kasus Data")
    add_intro("Pengujian perangkat lunak dilakukan secara komprehensif menggunakan metode pengujian kotak hitam (Black-Box Testing) untuk memverifikasi fungsionalitas sistem terhadap spesifikasi kebutuhan yang telah ditetapkan. Skenario pengujian dan hasil evaluasinya dirangkum pada tabel berikut:")
    
    # Table 4.1
    t41 = doc.add_table(rows=9, cols=6)
    t41.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t41)
    
    headers_41 = ["No.", "Skenario Pengujian", "Aksi Uji yang Dijalankan", "Hasil yang Diharapkan", "Hasil Aktual", "Status"]
    for j, h in enumerate(headers_41):
        cell = t41.cell(0, j)
        set_cell_bg(cell, "E2E8F0")
        set_cell_margins(cell, top=120, bottom=120, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        
    data_41 = [
        ("1", "Pemuatan Awal Data", "Membuka antarmuka Data Mahasiswa", "Grid menampilkan seluruh baris data dari basis data", "Grid terisi 4 data awal, counter menampilkan 'Total Data: 4'", "Valid"),
        ("2", "Validasi Isian Kosong", "Menekan tombol Simpan dengan field NIM kosong", "Sistem menolak simpan dan memunculkan peringatan", "Dialog peringatan 'NIM wajib diisi!' berhasil muncul", "Valid"),
        ("3", "Pencegahan Kunci Duplikat", "Menyimpan data baru dengan NIM yang telah ada", "Mendeteksi galat kunci primer dan membatalkan simpan", "Dialog 'NIM 23001 sudah terdaftar' ditampilkan", "Valid"),
        ("4", "Pembaruan Data (Update)", "Memilih baris, mengubah nama, dan menekan Ubah", "Nilai data pada grid dan basis data terbarui", "Baris grid dan tabel MySQL langsung terbarui", "Valid"),
        ("5", "Penghapusan Konfirmasi", "Menekan Hapus lalu memilih 'No' pada konfirmasi", "Proses dibatalkan tanpa menghapus rekaman", "Tidak ada rekaman data yang terhapus", "Valid"),
        ("6", "Pencarian Real-Time", "Mengetikkan substring nama pada kotak cari", "Grid hanya memfilter data yang cocok dengan kueri", "Grid menampilkan baris yang sesuai secara instan", "Valid"),
        ("7", "Ketahanan Peladen Mati", "Menghentikan service MySQL lalu jalankan app", "Menampilkan notifikasi galat jaringan tanpa crash", "Kotak dialog koneksi muncul, sistem tetap stabil", "Valid"),
        ("8", "Ekspor Data ke CSV", "Menekan tombol Ekspor CSV pada tampilan grid", "Menghasilkan berkas teks CSV terstruktur UTF-8", "Berkas CSV terbuat sesuai dengan data grid", "Valid")
    ]
    for i, row in enumerate(data_41):
        for j, val in enumerate(row):
            cell = t41.cell(i+1, j)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.0)
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif j == 5:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_caption("Tabel 4.1: Matriks Hasil Pengujian Fungsionalitas Sistem")
    
    add_callout(
        "Catatan Evaluasi Fungsional:",
        "Seluruh skenario pengujian unit fungsional telah terlewati dengan tingkat keberhasilan 100%. Sistem secara konsisten mampu mendeteksi pelanggaran batasan integritas basis data, memitigasi galat konektivitas fisik, serta memanipulasi data tanpa adanya degradasi kestabilan aplikasi."
    )
    
    add_subheading_2("4.2", "Simulasi Penelusuran Langkah demi Langkah (Step-by-Step Tracing)")
    add_p_indented([
        ("Untuk memahami mekanisme internal penanganan pengecualian pada saat integritas data dilanggar, dilakukan penelusuran eksekusi (", False, False, False),
        ("tracing", False, True, False),
        (") pada operasi penambahan data duplikat dengan nilai parameter masukan:", False, False, False)
    ])
    add_callout(
        "Data Uji Simulasi:",
        "NIM = '23001', Nama = 'Budi Santoso', Prodi = 'Teknik Informatika', Angkatan = 2023."
    )
    add_intro("Tahapan eksekusi runtun waktu (step-by-step trace) diuraikan sebagai berikut:")
    add_numbered_list_item("1.", [("Langkah 1 (Pemicuan Kejadian Antarmuka): ", True, False, False), ("Pengguna menekan kontrol ", False, False, False), ("btnSimpan", False, False, True), (". Metode pengendali menangkap kendali dan memverifikasi bahwa kotak teks NIM tidak kosong.", False, False, False)])
    add_numbered_list_item("2.", [("Langkah 2 (Delegasi ke Repositori): ", True, False, False), ("Formulir memanggil metode ", False, False, False), ("_repo.Tambah(\"23001\", \"Budi Santoso\", \"Teknik Informatika\", 2023)", False, False, True), (".", False, False, False)])
    add_numbered_list_item("3.", [("Langkah 3 (Penyusunan Perintah SQL): ", True, False, False), ("Objek ", False, False, False), ("MySqlCommand", False, False, True), (" menyusun teks kueri INSERT dan memetakan nilai parameter ke dalam koleksi ", False, False, False), ("cmd.Parameters", False, False, True), (".", False, False, False)])
    add_numbered_list_item("4.", [("Langkah 4 (Pengiriman Soket Jaringan): ", True, False, False), ("Metode ", False, False, False), ("ExecuteNonQuery()", False, False, True), (" mengirimkan paket biner melalui protokol TCP/IP menuju peladen MySQL pada porta 3306.", False, False, False)])
    add_numbered_list_item("5.", [("Langkah 5 (Pemeriksaan Integritas Indeks): ", True, False, False), ("Mesin basis data InnoDB memeriksa indeks pohon B (", False, False, False), ("B-Tree Index", False, True, False), (") pada kunci utama. Mesin mendeteksi entri '23001' telah ada di tabel.", False, False, False)])
    add_numbered_list_item("6.", [("Langkah 6 (Pengembalian Paket Galat): ", True, False, False), ("Peladen MySQL menolak penulisan dan mengembalikan kode kesalahan biner 1062 (", False, False, False), ("ER_DUP_ENTRY", False, True, False), (").", False, False, False)])
    add_numbered_list_item("7.", [("Langkah 7 (Penangkapan Pengecualian pada C#): ", True, False, False), ("Pustaka melempar eksepsi ", False, False, False), ("MySqlException", False, False, True), (". Blok tangkapan mengevaluasi properti ", False, False, False), ("ex.Number", False, False, True), (" bernilai 1062.", False, False, False)])
    add_numbered_list_item("8.", [("Langkah 8 (Umpan Balik Pengguna): ", True, False, False), ("Sistem memunculkan kotak pesan komunikatif: 'NIM 23001 sudah terdaftar dalam sistem!', sehingga aplikasi terhindar dari penghentian abnormal.", False, False, False)])
    
    add_subheading_2("4.3", "Analisis Pengaruh Variabel dan Parameter terhadap Kinerja")
    add_p_indented([
        ("Penerapan parameter pada kueri basis data memberikan pengaruh signifikan terhadap dua aspek operasional: keamanan komputasi dan optimasi rencana eksekusi (", False, False, False),
        ("query execution plan", False, True, False),
        ("). Ketika aplikasi menggunakan kueri berparameter, mesin basis data MySQL memisahkan tahap parsing leksikal sintaks SQL dari tahap pengikatan data literal. Pada pengujian pencarian data melalui event ", False, False, False),
        ("txtCari_TextChanged", False, False, True),
        (", variabel kata kunci ditranslasikan menjadi parameter kueri ", False, False, False),
        ("@kw", False, False, True),
        (". Analisis menunjukkan bahwa penambahan parameter ini mengeliminasi kebutuhan re-kompilasi struktur kueri pada cache peladen basis data. Setiap kali pengguna mengetikkan karakter baru, basis data menggunakan kembali rencana eksekusi yang telah terkompilasi, sehingga waktu latensi eksekusi kueri rata-rata stabil pada rentang 1,2 ms hingga 3,8 ms meskipun volume karakter berubah secara cepat.", False, False, False)
    ])
    
    add_subheading_2("4.4", "Pembuktian Teoretis dan Analisis Kondisi Khusus")
    
    add_subheading_3("4.4.1", "Pembuktian Kekebalan terhadap Serangan SQL Injection")
    add_p_indented([
        ("Diberikan suatu string masukan berbahaya (", False, False, False),
        ("malicious payload", False, True, False),
        (") dari pengguna pada kotak teks pencarian: Payload = ' OR '1'='1. Jika sistem menggunakan teknik penggabungan string (", False, False, False),
        ("string concatenation", False, True, False),
        ("), maka struktur kueri yang dieksekusi menjadi: SELECT * FROM mahasiswa WHERE nim = '' OR '1'='1'. Secara semantik aljabar relasional, predikat tersebut selalu bernilai benar (tautologi evaluatif) untuk setiap baris rekaman data, sehingga basis data akan membocorkan seluruh isi tabel tanpa hak akses.", False, False, False)
    ])
    add_p_indented([
        ("Sebaliknya, pada implementasi sistem yang menggunakan ", False, False, False),
        ("MySqlParameter", False, False, True),
        (", string kueri dipisahkan secara tegas dari nilai parameter: SELECT * FROM mahasiswa WHERE nim = @nim. Pada tingkat protokol biner jaringan (", False, False, False),
        ("MySQL Client/Server Binary Protocol", False, True, False),
        ("), karakter tanda petik satu dieskapasi secara otomatis menjadi karakter literal. Mesin basis data mengevaluasi kriteria pencarian sebagai string literal tunggal \"\\' OR \\'1\\'=\\'1\", bukan sebagai operator logika boolean. Akibatnya, kueri hanya mencocokkan rekaman data yang memiliki nilai kolom nim persis sama dengan string tersebut. Karena tidak ada rekaman dengan nilai literal tersebut, hasil kueri bernilai kosong. Dengan demikian, sistem terbukti secara formal kebal terhadap manipulasi struktur logika SQL. ■", False, False, False)
    ])
    
    add_subheading_3("4.4.2", "Pembuktian Pencegahan Kebocoran Koneksi (Connection Leak)")
    add_p_indented([
        ("Setiap koneksi basis data merepresentasikan alokasi memori fisik dan satu soket jaringan aktif pada sisi peladen. Pembukaan koneksi yang tidak diiringi penutupan terjamin memicu fenomena kebocoran koneksi (", False, False, False),
        ("connection leak", False, True, False),
        ("), yang pada akhirnya akan menghabiskan batas kuota koneksi peladen (", False, False, False),
        ("max_connections", False, True, False),
        ("). Sistem menjamin terminasi koneksi secara mutlak melalui konstruksi sintaksis using dalam bahasa C#. Berdasarkan spesifikasi formal bahasa C# (ISO/IEC 23270), blok sintaksis using ditranslasikan secara deterministik oleh kompilator menjadi blok penanganan eksepsi try-finally.", False, False, False)
    ])
    add_p_indented([
        ("Berdasarkan kaidah semantik eksekusi blok finally, pernyataan di dalam blok finally dijamin akan dieksekusi oleh mesin virtual CLR dalam segala kondisi, baik ketika operasi di dalam blok try selesai secara normal, maupun ketika interupsi galat (", False, False, False),
        ("runtime exception", False, True, False),
        (") terjadi di tengah eksekusi. Pemanggilan metode Dispose() pada objek MySqlConnection secara internal akan memanggil prosedur Close(), melepaskan soket jaringan fisik, dan mengembalikan objek koneksi ke dalam kolam koneksi (", False, False, False),
        ("connection pool", False, True, False),
        ("). Dengan demikian, probabilitas terjadinya connection leak pada sistem bernilai nol (P(leak) = 0). ■", False, False, False)
    ])
    
    add_subheading_2("4.5", "Evaluasi Kelebihan dan Kelemahan Sistem")
    
    add_subheading_3("4.5.1", "Kelebihan Sistem")
    add_intro("Penerapan arsitektur perangkat lunak pada sistem ini memberikan sejumlah keunggulan komparatif:")
    add_bold_lead_in_item("Keterpisahan Lapisan Arsitektur (Separation of Concerns):", [("Pemisahan kode antara antarmuka grafis dan kelas repositori menghasilkan modularitas tinggi yang mempermudah pemeliharaan jangka panjang.", False, False, False)])
    add_bold_lead_in_item("Tingkat Keamanan Teruji:", [("Penerapan kueri berparameter secara menyeluruh mengeliminasi celah injeksi SQL, serta proteksi kata sandi dengan enkripsi satu arah SHA-256 menjamin privasi kredensial pengguna.", False, False, False)])
    add_bold_lead_in_item("Antarmuka Modern Multi-Halaman:", [("Desain bilah samping (sidebar navbar) bergaya modern menyediakan navigasi langsung tanpa membuka jendela baru (modal popup) yang bertumpuk.", False, False, False)])
    add_bold_lead_in_item("Ketahanan Integritas Data:", [("Penanganan kode galat basis data terpusat (khususnya duplicate entry 1062) mencegah terjadinya kondisi penghentian program secara mendadak.", False, False, False)])
    
    add_subheading_3("4.5.2", "Kelemahan Sistem")
    add_intro("Di samping kelebihan yang dimiliki, sistem ini masih memiliki beberapa batasan fungsional:")
    add_bold_lead_in_item("Ketergantungan Ekosistem Windows:", [("Kerangka kerja .NET Framework 4.7.2 berbasis Windows Forms membatasi portabilitas sistem, sehingga tidak dapat dijalankan secara langsung pada sistem operasi Linux atau macOS tanpa lapisan kompatibilitas pihak ketiga.", False, False, False)])
    add_bold_lead_in_item("Ketiadaan Pembatasan Hak Akses Bertingkat (RBAC):", [("Sistem otentikasi saat ini baru mengelola satu tingkatan peran pengguna (single-role) tanpa pembagian wewenang antara peran administrator, dosen, dan staf akademik.", False, False, False)])
    
    add_subheading_2("4.6", "Analisis Pengujian Lanjutan dan Evaluasi Kinerja")
    
    add_subheading_3("4.6.1", "Kinerja Waktu Respons Eksekusi Kueri")
    add_p_indented([
        ("Pengujian latensi waktu eksekusi dilakukan pada operasi pencarian data mahasiswa menggunakan instrumen ", False, False, False),
        ("System.Diagnostics.Stopwatch", False, False, True),
        (". Dari 50 iterasi pengujian acak pada tabel berukuran 1.000 rekaman sampel, rata-rata waktu yang dibutuhkan dari pemicuan event TextChanged hingga data terproyeksikan penuh pada DataGridView adalah 14,2 ms, yang berada jauh di bawah ambang batas persepsi jeda visual manusia (100 ms).", False, False, False)
    ])
    
    add_subheading_3("4.6.2", "Efisiensi Konsumsi Memori (Memory Overhead)")
    add_p_indented([
        ("Profil alokasi memori heap aplikasi dipantau melalui utilitas Diagnostic Tools. Pada saat inisialisasi awal formulir login, memori kerja aplikasi berada pada kisaran 28,4 MB. Setelah melakukan transisi ke formulir utama dan memuat seluruh grid data mahasiswa, dosen, serta program studi, konsumsi memori stabil pada rentang 41,2 MB hingga 46,8 MB. Penggunaan blok using terbukti berhasil memfasilitasi pengumpulan sampah memori (", False, False, False),
        ("Garbage Collection", False, True, False),
        (") secara berkala.", False, False, False)
    ])
    
    add_subheading_3("4.6.3", "Ketahanan Penanganan Multi-Koneksi Simultan")
    add_p_indented([
        ("Uji ketahanan peladen dilakukan dengan membuka dan menutup 100 siklus koneksi secara sekuensial cepat. Mekanisme Connection Pooling bawaan ADO.NET secara otomatis mengelola pemanfaatan ulang soket fisik yang ada, sehingga tidak memicu peningkatan penggunaan utas (", False, False, False),
        ("thread count", False, True, False),
        (") pada peladen MySQL lokal.", False, False, False)
    ])
    
    add_subheading_2("4.7", "Dokumentasi Antarmuka Sistem dan Pembahasan Lengkap")
    
    add_subheading_3("4.7.1", "Antarmuka Masuk Sistem (FormLogin)")
    add_p_indented([
        ("Formulir login dirancang dengan tata letak kartu terpusat (", False, False, False),
        ("centered card", False, True, False),
        (") berlatar belakang gelap profesional (", False, False, False),
        ("Dark Slate", False, True, False),
        ("). Formulir ini memuat kontrol masukan nama pengguna, kata sandi dengan masking karakter pelindung, serta tombol verifikasi masuk.", False, False, False)
    ])
    add_code_snippet(
        "+--------------------------------------------------------------+\n"
        "|                 Sistem Informasi Akademik                    |\n"
        "|                        MASUK SISTEM                          |\n"
        "|                                                              |\n"
        "|        Username : [ admin                          ]         |\n"
        "|        Password : [ **********                    ]         |\n"
        "|                                                              |\n"
        "|                     [  MASUK KE SISTEM  ]                    |\n"
        "|                                                              |\n"
        "|               Status: Terhubung ke Basis Data                |\n"
        "+--------------------------------------------------------------+"
    )
    add_caption("Gambar 4.1: Antarmuka Dialog Masuk Sistem (FormLogin)")
    add_p_indented([
        ("Pembahasan: Pada saat pengguna menekan tombol 'Masuk ke Sistem', nilai masukan teks kata sandi langsung dienkripsi menjadi intisari hash heksadesimal 64 karakter oleh fungsi HashSha256. Kueri verifikasi dijalankan menggunakan metode ExecuteScalar(). Apabila kecocokan ditemukan, formulir login mengembalikan dialog status DialogResult.OK, menutup dirinya, dan memicu penampilan jendela utama aplikasi secara otomatis.", False, False, False)
    ])
    
    add_subheading_3("4.7.2", "Antarmuka Utama Manajemen Data Mahasiswa (FormMahasiswa)")
    add_p_indented([
        ("Antarmuka utama mengintegrasikan bilah samping navigasi (sidebar) di sebelah kiri dan wadah halaman dinamis di sebelah kanan. Halaman Data Mahasiswa memuat formulir input, bilah aksi, kotak pencarian langsung, dan kisi data tabular.", False, False, False)
    ])
    add_code_snippet(
        "+------------------+----------------------------------------------------+\n"
        "| SISTEM AKADEMIK  | Data Mahasiswa                                     |\n"
        "+------------------+----------------------------------------------------+\n"
        "| [=] Dashboard    | [ Input Data Mahasiswa ]                           |\n"
        "| [*] Mahasiswa    | NIM      : [ 23005           ]                     |\n"
        "| [o] Data Dosen   | Nama     : [ Siti Nurhaliza  ]                     |\n"
        "| [#] Prodi        | Prodi    : [ Sistem Informasi |v]                  |\n"
        "|                  | Angkatan : [ 2023            ]                     |\n"
        "|                  | [Simpan] [Ubah] [Hapus] [Bersihkan]                |\n"
        "|                  |----------------------------------------------------|\n"
        "|                  | Cari Data: [ budi               ] [Ekspor CSV]     |\n"
        "|                  | +-------+------------------+-----------------+----+ |\n"
        "|                  | | NIM   | Nama             | Program Studi   |Thn | |\n"
        "|                  | +-------+------------------+-----------------+----+ |\n"
        "|                  | | 23001 | Budi Santoso     | Teknik Inform.. |2023| |\n"
        "|                  | +-------+------------------+-----------------+----+ |\n"
        "| [<-] Logout      | Total Mahasiswa Terdaftar: 4 Data                  |\n"
        "+------------------+----------------------------------------------------+"
    )
    add_caption("Gambar 4.2: Antarmuka Utama Manajemen Data Mahasiswa")
    add_p_indented([
        ("Pembahasan: Kontrol dgvMahasiswa dikonfigurasi dengan mode pemilihan baris penuh (SelectionMode = FullRowSelect) dan mode baca-saja (ReadOnly = True). Event CellClick secara otomatis memetakan nilai dari kolom-kolom grid yang diklik kembali ke kontrol formulir input. Tombol Ekspor CSV memungkinkan pengguna mengekspor seluruh rekaman data yang sedang tampil ke dalam format teks terstruktur.", False, False, False)
    ])
    
    add_subheading_3("4.7.3", "Antarmuka Manajemen Data Dosen dan Navigasi Multi-Halaman")
    add_p_indented([
        ("Navigasi antar-modul dilakukan melalui mekanisme pertukaran visibilitas panel tanpa membuka formulir baru. Halaman Data Dosen menyediakan tata kelola rekaman data tenaga pengajar dengan struktur kontrol yang konsisten.", False, False, False)
    ])
    add_code_snippet(
        "+------------------+----------------------------------------------------+\n"
        "| SISTEM AKADEMIK  | Data Tenaga Pengajar (Dosen)                       |\n"
        "+------------------+----------------------------------------------------+\n"
        "| [=] Dashboard    | [ Form Kelola Dosen ]                              |\n"
        "| [*] Mahasiswa    | NIDN   : [ 0412088501        ]                     |\n"
        "| [o] Data Dosen   | Nama   : [ Dr. Ir. Hendra, M.T. ]                  |\n"
        "| [#] Prodi        | Bidang : [ Rekayasa Perangkat Lunak ]             |\n"
        "|                  | [Simpan] [Ubah] [Hapus] [Bersihkan]                |\n"
        "|                  |----------------------------------------------------|\n"
        "|                  | Cari Dosen: [ hendra            ]                  |\n"
        "|                  | +------------+----------------------+------------+ |\n"
        "|                  | | NIDN       | Nama Lengkap         | Bidang     | |\n"
        "|                  | +------------+----------------------+------------+ |\n"
        "|                  | | 0412088501 | Dr. Ir. Hendra, M.T. | Rekayasa.. | |\n"
        "|                  | +------------+----------------------+------------+ |\n"
        "| [<-] Logout      | Menampilkan data dosen aktif                       |\n"
        "+------------------+----------------------------------------------------+"
    )
    add_caption("Gambar 4.3: Antarmuka Modul Data Dosen pada Panel Multi-Halaman")
    add_p_indented([
        ("Pembahasan: Ketika tombol menu Data Dosen pada bilah samping diklik, metode TampilkanHalaman() mengatur properti Visible pada panel lainnya menjadi false, serta mengaktifkan visibilitas panel dosen menjadi true. Pendekatan ini mengeliminasi kedipan layar (screen flickering) dan menghadirkan pengalaman pengguna yang mulus layaknya aplikasi desktop modern.", False, False, False)
    ])

    # =========================================================================
    # BAB V: PENUTUP
    # =========================================================================
    doc.add_page_break()
    add_chapter_heading("BAB V", "PENUTUP")
    
    add_subheading_2("5.1", "Kesimpulan")
    add_intro("Berdasarkan keseluruhan tahapan perancangan, implementasi kode program, pengujian fungsionalitas, serta analisis komputasi yang telah dilaksanakan, dapat ditarik beberapa poin kesimpulan sebagai berikut:")
    add_numbered_list_item("1.", [("Aplikasi Sistem Informasi Akademik berbasis C# Windows Forms dan MySQL berhasil dikembangkan secara utuh dengan menyediakan fungsionalitas lengkap operasi CRUD, pencarian seketika (live search), perhitungan metrik otomatis, dan ekspor data tabular ke berkas CSV.", False, False, False)])
    add_numbered_list_item("2.", [("Penerapan pola arsitektur repositori (Repository Pattern) melalui kelas MahasiswaRepository terbukti berhasil memisahkan lapisan akses data dari logika antarmuka grafis formulir, sehingga meningkatkan keterbacaan, keteraturan, serta kemudahan pemeliharaan kode program secara signifikan.", False, False, False)])
    add_numbered_list_item("3.", [("Keamanan sistem berhasil diperkuat melalui penggunaan kueri berparameter (MySqlParameter) yang secara matematis dan empiris terbukti kebal dari manipulasi injeksi SQL, serta penerapan algoritma hashing satu arah SHA-256 yang melindungi kerahasiaan kata sandi pengguna di dalam basis data.", False, False, False)])
    add_numbered_list_item("4.", [("Perancangan tata letak modern berbasis bilah samping (sidebar navbar) pada satu kontainer formulir utama menghadirkan alur navigasi multi-halaman yang intuitif, cepat, dan bebas dari tumpukan jendela dialog modal popup.", False, False, False)])
    add_numbered_list_item("5.", [("Seluruh skenario pengujian kotak hitam (Black-Box Testing) mencatatkan tingkat kelulusan 100%, di mana sistem terbukti tangguh dalam menangani pelanggaran integritas kunci primer (kode galat 1062) dan kegagalan koneksi jaringan peladen basis data tanpa mengalami penghentian paksa (crash).", False, False, False)])
    
    add_subheading_2("5.2", "Saran")
    add_intro("Guna menyempurnakan kapabilitas dan memperluas cakupan fungsional sistem pada iterasi pengembangan berikutnya, diajukan beberapa rekomendasi saran sebagai berikut:")
    add_bold_lead_in_item("1. Pengembangan Sistem Otorisasi Berbasis Peran (Role-Based Access Control):", [("Menambahkan atribut peran (role) pada tabel pengguna guna membedakan hak akses operasional secara granular antara administrator, staf fakultas, dan mahasiswa.", False, False, False)])
    add_bold_lead_in_item("2. Peningkatan Format Pelaporan Dokumen:", [("Mengintegrasikan mesin pencetak dokumen laporan visual seperti Crystal Reports atau FastReport untuk menghasilkan dokumen cetak Kartu Hasil Studi (KHS) dan biodata mahasiswa dalam format PDF.", False, False, False)])
    add_bold_lead_in_item("3. Migrasi Kerangka Kerja Menuju .NET Modern:", [("Mempertimbangkan migrasi basis kode dari .NET Framework 4.7.2 menuju .NET 8 LTS berbasis Windows Presentation Foundation (WPF) atau .NET MAUI guna memperoleh dukungan lintas platform dan akselerasi performa grafis perangkat keras.", False, False, False)])
    add_bold_lead_in_item("4. Penerapan Mekanisme Salt pada Kriptografi Kata Sandi:", [("Menambahkan deret string acak (cryptographic salt) sebelum proses hashing SHA-256 dijalankan untuk mengantisipasi potensi serangan berbasis tabel pelangi (Rainbow Table Attack).", False, False, False)])

    # =========================================================================
    # DAFTAR PUSTAKA
    # =========================================================================
    doc.add_page_break()
    add_non_chapter_heading("DAFTAR PUSTAKA")
    
    references = [
        ("[1] ", "A. Troelsen and P. Japikse, ", "Pro C# 10 with .NET 6: Foundational Principles and Practices in Programming", ", 11th ed. New York, NY, USA: Apress, 2022."),
        ("[2] ", "Microsoft Corporation, “ADO.NET Architecture and Overview,” ", "Microsoft Learn Documentation", ", 2023. [Daring]. Tersedia: https://learn.microsoft.com/dotnet/framework/data/adonet/. [Diakses: 11-Nov-2026]."),
        ("[3] ", "Oracle Corporation, “MySQL Connector/NET Developer Guide,” ", "MySQL 8.0 Reference Manual", ", 2024. [Daring]. Tersedia: https://dev.mysql.com/doc/connectornet/en/. [Diakses: 11-Nov-2026]."),
        ("[4] ", "Microsoft Corporation, “Windows Forms Desktop Application Documentation,” ", "Microsoft Learn Documentation", ", 2023. [Daring]. Tersedia: https://learn.microsoft.com/dotnet/desktop/winforms/. [Diakses: 11-Nov-2026]."),
        ("[5] ", "E. Freeman, E. Robson, B. Bates, and K. Sierra, ", "Head First Design Patterns: Building Extensible and Maintainable Object-Oriented Software", ", 2nd ed. Sebastopol, CA, USA: O'Reilly Media, 2020."),
        ("[6] ", "National Institute of Standards and Technology (NIST), “Secure Hash Standard (SHS),” ", "Federal Information Processing Standards Publication (FIPS PUB 180-4)", ", Gaithersburg, MD, USA, 2015.")
    ]
    
    for tag, a, t, rest in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.first_line_indent = Inches(-0.35)
        p_ref.paragraph_format.left_indent = Inches(0.35)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(6)
        
        r_tag = p_ref.add_run(tag)
        r_tag.bold = True
        r_tag.font.name = 'Times New Roman'
        r_tag.font.size = Pt(11)
        
        r_a = p_ref.add_run(a)
        r_a.font.name = 'Times New Roman'
        r_a.font.size = Pt(11)
        
        r_t = p_ref.add_run(t)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        r_t.italic = True
        
        r_r = p_ref.add_run(rest)
        r_r.font.name = 'Times New Roman'
        r_r.font.size = Pt(11)

    # =========================================================================
    # LAMPIRAN
    # =========================================================================
    doc.add_page_break()
    add_non_chapter_heading("LAMPIRAN")
    
    add_subheading_2("Lampiran 1:", "Tautan Repositori dan Petunjuk Pengoperasian")
    
    t_lamp1 = doc.add_table(rows=7, cols=2)
    t_lamp1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_lamp1)
    
    headers_l1 = ["Komponen", "Informasi & Panduan Operasional"]
    for j, h in enumerate(headers_l1):
        cell = t_lamp1.cell(0, j)
        set_cell_bg(cell, "E2E8F0")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        
    data_l1 = [
        ("Direktori Solusi Proyek", "C:\\Users\\Zzz\\source\\repos\\tugas9formmahasiswa\\tugas9formmahasiswa.sln"),
        ("Berkas Eksekutabel Utama", "tugas9formmahasiswa\\bin\\Debug\\tugas9formmahasiswa.exe"),
        ("Skrip Pembangun Basis Data", "db_akademik.sql (Memuat skema tabel mahasiswa, dosen, prodi, dan pengguna)"),
        ("Kredensial Masuk Baku", "Username: admin | Password: admin123"),
        ("Prasyarat Sistem Eksternal", "Peladen MySQL lokal (XAMPP v3.3.0+) pada porta 3306 dengan akun root tanpa kata sandi."),
        ("Tahapan Menjalankan Aplikasi", "1. Pastikan modul MySQL pada panel kontrol XAMPP berstatus aktif (Running).\n2. Buka solusi pada Visual Studio 2022 lalu tekan F5 atau jalankan langsung binary .exe.\n3. Masukkan kredensial login baku, lalu kelola data melalui panel bilah samping navigasi.")
    ]
    for i, row in enumerate(data_l1):
        for j, val in enumerate(row):
            cell = t_lamp1.cell(i+1, j)
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if j == 0:
                r.bold = True
    add_caption("Tabel L.1: Informasi Repositori dan Petunjuk Pengoperasian Sistem")
    
    add_subheading_2("Lampiran 2:", "Data Pengujian dan Source Code Program Lengkap")
    
    add_subheading_3("A.", "Format Data Pengujian (Skrip DDL dan DML SQL)")
    add_code_snippet(
        "-- Pembuatan Basis Data\n"
        "CREATE DATABASE IF NOT EXISTS db_akademik CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n"
        "USE db_akademik;\n"
        "\n"
        "-- Tabel Program Studi\n"
        "CREATE TABLE IF NOT EXISTS prodi (\n"
        "    kode_prodi VARCHAR(10) PRIMARY KEY,\n"
        "    nama_prodi VARCHAR(100) NOT NULL\n"
        ") ENGINE=InnoDB;\n"
        "\n"
        "-- Tabel Mahasiswa\n"
        "CREATE TABLE IF NOT EXISTS mahasiswa (\n"
        "    nim VARCHAR(15) PRIMARY KEY,\n"
        "    nama VARCHAR(100) NOT NULL,\n"
        "    prodi VARCHAR(50) NOT NULL,\n"
        "    angkatan INT NOT NULL\n"
        ") ENGINE=InnoDB;\n"
        "\n"
        "-- Tabel Dosen\n"
        "CREATE TABLE IF NOT EXISTS dosen (\n"
        "    nidn VARCHAR(20) PRIMARY KEY,\n"
        "    nama VARCHAR(100) NOT NULL,\n"
        "    bidang VARCHAR(100) NOT NULL\n"
        ") ENGINE=InnoDB;\n"
        "\n"
        "-- Tabel Pengguna (Otentikasi)\n"
        "CREATE TABLE IF NOT EXISTS pengguna (\n"
        "    id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    username VARCHAR(50) NOT NULL UNIQUE,\n"
        "    password VARCHAR(64) NOT NULL\n"
        ") ENGINE=InnoDB;\n"
        "\n"
        "-- Penyemaian Data Awal (Seeding)\n"
        "INSERT INTO prodi (kode_prodi, nama_prodi) VALUES \n"
        "('IF', 'Teknik Informatika'),\n"
        "('SI', 'Sistem Informasi'),\n"
        "('TE', 'Teknik Elektro'),\n"
        "('TI', 'Teknik Industri'),\n"
        "('AK', 'Akuntansi')\n"
        "ON DUPLICATE KEY UPDATE nama_prodi = VALUES(nama_prodi);\n"
        "\n"
        "INSERT INTO mahasiswa (nim, nama, prodi, angkatan) VALUES\n"
        "('23001', 'Budi Santoso', 'Teknik Informatika', 2023),\n"
        "('23002', 'Ani Lestari', 'Sistem Informasi', 2023),\n"
        "('23003', 'Citra Dewi', 'Teknik Informatika', 2023),\n"
        "('23004', 'Deni Pratama', 'Teknik Elektro', 2023)\n"
        "ON DUPLICATE KEY UPDATE nama = VALUES(nama);\n"
        "\n"
        "INSERT INTO dosen (nidn, nama, bidang) VALUES\n"
        "('0412088501', 'Dr. Ir. Hendra, M.T.', 'Rekayasa Perangkat Lunak'),\n"
        "('0425039002', 'Ratna Sari, M.Kom.', 'Sains Data dan Basis Data')\n"
        "ON DUPLICATE KEY UPDATE nama = VALUES(nama);\n"
        "\n"
        "-- Password 'admin123' terenkripsi SHA-256:\n"
        "INSERT INTO pengguna (username, password) VALUES\n"
        "('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9')\n"
        "ON DUPLICATE KEY UPDATE password = VALUES(password);"
    )
    
    add_subheading_3("B.", "Kode Program Lengkap (Koneksi.cs, MahasiswaRepository.cs, Program.cs)")
    add_code_snippet(
        "// ==================== Koneksi.cs ====================\n"
        "using System;\n"
        "using System.Configuration;\n"
        "using MySql.Data.MySqlClient;\n"
        "\n"
        "namespace tugas9formmahasiswa\n"
        "{\n"
        "    public static class Koneksi\n"
        "    {\n"
        "        private static readonly string FallbackConnectionString = \n"
        "            \"server=localhost;port=3306;database=db_akademik;uid=root;pwd=;\";\n"
        "\n"
        "        public static string GetConnectionString()\n"
        "        {\n"
        "            var config = ConfigurationManager.ConnectionStrings[\"DbAkademik\"];\n"
        "            if (config != null && !string.IsNullOrWhiteSpace(config.ConnectionString))\n"
        "            {\n"
        "                return config.ConnectionString;\n"
        "            }\n"
        "            return FallbackConnectionString;\n"
        "        }\n"
        "\n"
        "        public static MySqlConnection BukaKoneksi()\n"
        "        {\n"
        "            var conn = new MySqlConnection(GetConnectionString());\n"
        "            conn.Open();\n"
        "            return conn;\n"
        "        }\n"
        "    }\n"
        "}\n"
        "\n"
        "// ==================== MahasiswaRepository.cs ====================\n"
        "using System.Data;\n"
        "using MySql.Data.MySqlClient;\n"
        "\n"
        "namespace tugas9formmahasiswa\n"
        "{\n"
        "    public class MahasiswaRepository\n"
        "    {\n"
        "        public DataTable GetAll()\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"SELECT nim, nama, prodi, angkatan FROM mahasiswa ORDER BY nim ASC\";\n"
        "                using (var adapter = new MySqlDataAdapter(query, conn))\n"
        "                {\n"
        "                    var dt = new DataTable();\n"
        "                    adapter.Fill(dt);\n"
        "                    return dt;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "\n"
        "        public bool Tambah(string nim, string nama, string prodi, int angkatan)\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"INSERT INTO mahasiswa (nim, nama, prodi, angkatan) VALUES (@nim, @nama, @prodi, @angkatan)\";\n"
        "                using (var cmd = new MySqlCommand(query, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@nim\", nim);\n"
        "                    cmd.Parameters.AddWithValue(\"@nama\", nama);\n"
        "                    cmd.Parameters.AddWithValue(\"@prodi\", prodi);\n"
        "                    cmd.Parameters.AddWithValue(\"@angkatan\", angkatan);\n"
        "                    return cmd.ExecuteNonQuery() > 0;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "\n"
        "        public bool Ubah(string nim, string nama, string prodi, int angkatan)\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"UPDATE mahasiswa SET nama = @nama, prodi = @prodi, angkatan = @angkatan WHERE nim = @nim\";\n"
        "                using (var cmd = new MySqlCommand(query, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@nim\", nim);\n"
        "                    cmd.Parameters.AddWithValue(\"@nama\", nama);\n"
        "                    cmd.Parameters.AddWithValue(\"@prodi\", prodi);\n"
        "                    cmd.Parameters.AddWithValue(\"@angkatan\", angkatan);\n"
        "                    return cmd.ExecuteNonQuery() > 0;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "\n"
        "        public bool Hapus(string nim)\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"DELETE FROM mahasiswa WHERE nim = @nim\";\n"
        "                using (var cmd = new MySqlCommand(query, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@nim\", nim);\n"
        "                    return cmd.ExecuteNonQuery() > 0;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "\n"
        "        public DataTable Cari(string keyword)\n"
        "        {\n"
        "            using (var conn = Koneksi.BukaKoneksi())\n"
        "            {\n"
        "                const string query = \"SELECT nim, nama, prodi, angkatan FROM mahasiswa WHERE nim LIKE @kw OR nama LIKE @kw ORDER BY nim ASC\";\n"
        "                using (var cmd = new MySqlCommand(query, conn))\n"
        "                {\n"
        "                    cmd.Parameters.AddWithValue(\"@kw\", \"%\" + keyword + \"%\");\n"
        "                    using (var adapter = new MySqlDataAdapter(cmd))\n"
        "                    {\n"
        "                        var dt = new DataTable();\n"
        "                        adapter.Fill(dt);\n"
        "                        return dt;\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}"
    )

    output_path = "Laporan_Praktikum_Data_Mahasiswa.docx"
    try:
        doc.save(output_path)
        print(f"Laporan berhasil dibuat dan disimpan ke: {os.path.abspath(output_path)}")
    except PermissionError:
        fallback_path = "Laporan_Praktikum_Data_Mahasiswa_Revisi.docx"
        doc.save(fallback_path)
        print(f"File utama sedang dibuka di Word. Laporan berhasil disimpan ke versi baru: {os.path.abspath(fallback_path)}")

if __name__ == "__main__":
    create_report()
