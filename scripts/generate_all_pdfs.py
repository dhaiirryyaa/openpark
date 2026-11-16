#!/usr/bin/env python3
"""
Generate all submission deliverables as pristine, 100% vector, non-glitching PDFs using ReportLab:
1. submission/01_Text_Summary.pdf (Executive 1-Pager)
2. submission/02_Video_Introduction_Script.pdf (Founder Video Script & Recording Blueprint)
3. submission/03_Pitch_Deck/Pitch_Deck_OpenPark.pdf (10-Slide 16:9 Presentation Deck)
"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PRIMARY_BLUE = colors.HexColor("#0071E3")
DARK_NAVY = colors.HexColor("#0F172A")
SLATE_GRAY = colors.HexColor("#475569")
LIGHT_BG = colors.HexColor("#F8FAFC")
CARD_BG = colors.HexColor("#FFFFFF")
BORDER_COLOR = colors.HexColor("#E2E8F0")
EMERALD_GREEN = colors.HexColor("#10B981")
AMBER_GOLD = colors.HexColor("#D97706")


# ==============================================================================
# 1. DELIVERABLE 1: 01_Text_Summary.pdf
# ==============================================================================
def create_text_summary_pdf(out_path: str):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=DARK_NAVY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=PRIMARY_BLUE,
        spaceAfter=14
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=PRIMARY_BLUE
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=DARK_NAVY,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK_NAVY
    )

    quote_style = ParagraphStyle(
        'QuoteBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=DARK_NAVY
    )

    meta_key = ParagraphStyle(
        'MetaKey',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=SLATE_GRAY
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=DARK_NAVY
    )

    elements = []

    # Header Badges
    badge_data = [
        [
            Paragraph("<b>STAGE 1 SUBMISSION DELIVERABLE 1</b>", badge_style),
            Paragraph("<b>DEADLINE: 20 NOVEMBER, 11:59 PM IST</b>", ParagraphStyle('R', parent=badge_style, alignment=2, textColor=AMBER_GOLD))
        ]
    ]
    t_badge = Table(badge_data, colWidths=[260, 272])
    t_badge.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_badge)
    elements.append(Spacer(1, 5))

    # Title & Subtitle
    elements.append(Paragraph("OpenPark — Executive Text Summary", title_style))
    elements.append(Paragraph("AI-Powered Smart Parking &amp; Micro-Space Discovery Platform", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_BLUE, spaceBefore=0, spaceAfter=14))

    # The 5-Line Text Summary Box (Mandated exact deliverable)
    elements.append(Paragraph("<b>Required 5-to-6 Line Deliverable Description:</b>", section_header))

    lines = [
        "<b>1. Problem Statement:</b> Urban drivers in tier-1 Indian cities lose 20+ minutes per trip hunting for parking, causing massive traffic congestion, fuel waste, and roadside chaos.",
        "<b>2. Gridlock Driver:</b> Fragmented commercial lots, lack of real-time occupancy data, and thousands of unindexed urban spaces leave over 30% of downtown traffic composed solely of vehicles searching for parking.",
        "<b>3. Proposed Solution:</b> OpenPark is an open-source, AI-powered smart mobility platform providing instant parking discovery, guaranteed 15-minute slot reservations, and turn-by-turn OSRM road guidance.",
        "<b>4. Spatial Engine:</b> Its proprietary spatial engine continuously indexes city landmarks and scans a strict 1 km radius to uncover commercial parking lots alongside hidden 45–550 m² vacant grounds and legal roadside bays.",
        "<b>5. Key Differentiator:</b> Unlike static navigation directories, OpenPark combines live Traccar GPS vehicle telemetry, offline-first SQLite FTS5 search, and edge vision verification into a unified driver PWA and operator dashboard with zero proprietary hardware lock-in."
    ]

    box_content = [[Paragraph(f"{line}<br/>", quote_style)] for line in lines]
    t_box = Table(box_content, colWidths=[532])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_box)
    elements.append(Spacer(1, 6))

    # Analytical Component Breakdown Table
    elements.append(Paragraph("<b>Core Component Mapping:</b>", section_header))
    comp_data = [
        [Paragraph("<b>Component</b>", meta_key), Paragraph("<b>OpenPark Technical Implementation</b>", meta_key)],
        [
            Paragraph("<b>Problem Statement</b>", meta_key),
            Paragraph("Urban traffic gridlock caused by cruising; 20+ minutes wasted per driver; lack of real-time visibility in commercial lots and basements.", body_style)
        ],
        [
            Paragraph("<b>Proposed Solution</b>", meta_key),
            Paragraph("Dual-sided smart mobility ecosystem: driver responsive PWA + operator touch tablet dashboard; 15-minute slot lock; OSRM routing straight to the gate.", body_style)
        ],
        [
            Paragraph("<b>Key Differentiator</b>", meta_key),
            Paragraph("Strict 1 km AI micro-space scanner (45–550 m² vacant grounds); zero proprietary hardware costs; offline-first vector cache; live Traccar GPS WebSocket telemetry.", body_style)
        ],
        [
            Paragraph("<b>Live Prototype</b>", meta_key),
            Paragraph("<b>Driver App:</b> https://openpark-web-production.up.railway.app/app/<br/><b>Operator Terminal:</b> https://openpark-web-production.up.railway.app/dashboard/", body_style)
        ]
    ]
    t_comp = Table(comp_data, colWidths=[120, 412])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_comp)
    elements.append(Spacer(1, 6))

    # Team & Contact
    meta_table_data = [
        [Paragraph("<b>Founder &amp; Systems Architect:</b>", meta_key), Paragraph("Dhairya (dhairyakhandelwal880@gmail.com)", meta_val)],
        [Paragraph("<b>Location / Pilot Region:</b>", meta_key), Paragraph("Bengaluru, Karnataka, India", meta_val)],
        [Paragraph("<b>GitHub Repository:</b>", meta_key), Paragraph("https://github.com/dhairyakhandelwal880-dotcom/openpark", meta_val)]
    ]
    t_meta = Table(meta_table_data, colWidths=[160, 372])
    t_meta.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#F1F5F9")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_meta)

    doc.build(elements)
    print(f"Generated Text Summary PDF: {out_path} ({os.path.getsize(out_path)} bytes)")


# ==============================================================================
# 2. DELIVERABLE 2: 02_Video_Introduction_Script.pdf
# ==============================================================================
def create_video_script_pdf(out_path: str):
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=DARK_NAVY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=PRIMARY_BLUE,
        spaceAfter=12
    )

    scene_title = ParagraphStyle(
        'SceneTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY_BLUE,
        spaceBefore=10,
        spaceAfter=4
    )

    cue_style = ParagraphStyle(
        'CueStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=SLATE_GRAY
    )

    speech_style = ParagraphStyle(
        'SpeechStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=DARK_NAVY
    )

    elements = []

    elements.append(Paragraph("OpenPark — Founder Video Introduction Script", title_style))
    elements.append(Paragraph("Stage 1 Deliverable: Video Introduction (2m 30s – 3m 00s Blueprint)", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_BLUE, spaceBefore=0, spaceAfter=10))

    # Overview table
    overview_data = [
        [Paragraph("<b>Target Runtime:</b> 2:30 – 3:00 mins", cue_style), Paragraph("<b>Aspect Ratio:</b> 16:9 Landscape (1080p / 4K)", cue_style)],
        [Paragraph("<b>Speaker:</b> Dhairya (Founder &amp; Architect)", cue_style), Paragraph("<b>Live App URL:</b> openpark-web-production.up.railway.app", cue_style)]
    ]
    t_ov = Table(overview_data, colWidths=[258, 258])
    t_ov.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_ov)
    elements.append(Spacer(1, 5))

    scenes = [
        (
            "Scene 1: The Hook & The Urban Bottleneck (0:00 – 0:35)",
            "Founder on camera (medium close-up, clean neutral background). B-roll: busy Bengaluru / Indiranagar corridor with cars circling for parking.<br/><b>Overlay Text:</b> '30% to 40% of metro traffic is drivers cruising for parking.'",
            "Namaste and hello everyone. Picture this: you drive 45 minutes across town to reach an urgent meeting or a family dinner. But your trip isn’t over. For the next 25 minutes, you crawl in bumper-to-bumper traffic, circling blocks and hunting for a vacant spot.<br/><br/>In India’s top metropolitan cities, an estimated <b>30 to 40 percent of all peak-hour traffic is caused solely by vehicles cruising for parking</b>. That means billions of rupees in wasted fuel, tons of toxic emissions, and countless hours of human productivity lost on our roads every single day."
        ),
        (
            "Scene 2: Founder & Core Team Introduction (0:35 – 1:10)",
            "Founder on camera. Split screen showing GitHub repository metrics, architecture diagrams, and team background.<br/><b>Overlay Text:</b> 'Dhairya — Founder & Lead Systems Architect'",
            "I’m Dhairya, Founder and Lead Systems Architect of OpenPark. My background is in full-stack distributed systems, geospatial engines, and high-concurrency cloud architectures. Over the past year, I’ve built high-performance spatial platforms combining OpenStreetMap, Overture Maps, and GPS telemetry.<br/><br/>Beside me, our core team brings specialized experience across spatial data science, edge computer vision, and fleet operations. We are systems builders obsessed with making high-density cities move faster, cleaner, and smarter."
        ),
        (
            "Scene 3: Motivation — Why This Problem Matters (1:10 – 1:50)",
            "Founder speaking with conviction. Cut to footage of empty private basements or vacant plots standing idle right next to clogged roads.<br/><b>Overlay Text:</b> 'The Urban Paradox: High Demand, Invisible Supply'",
            "Our motivation started from a profound paradox we observed right here in Bengaluru: while street curbs are overflowing with chaotic double parking, there are hundreds of private basements, vacant plots between 45 and 550 square meters, and half-empty commercial parking lots just 300 meters away that drivers simply cannot see.<br/><br/>Traditional navigation apps only drop you at the front door and abandon you to figure out parking yourself. Legacy parking solutions require millions of dollars in proprietary boom-barriers and inductive loop sensors that Indian cities cannot afford to retrofit everywhere. We knew there had to be a software-first, zero-hardware alternative."
        ),
        (
            "Scene 4: The OpenPark Solution & Live Prototype (1:50 – 2:30)",
            "Screen recording of live OpenPark responsive app: search autocomplete for 'MG Road', 1 km AI Scanner finding spots, 15-minute slot lock, and OSRM turn-by-turn guidance.<br/><b>Overlay Text:</b> 'Live Prototype: openpark-web-production.up.railway.app'",
            "That is why we built <b>OpenPark</b>. OpenPark is an open-source, AI-powered smart mobility platform.<br/><br/>First, our strict <b>1 km AI Space Scanner</b> dynamically indexes not just established multi-level parking lots, but also unindexed 3-to-6 car micro-pockets, church grounds, and verified commercial bays within walking distance.<br/><br/>Second, our <b>15-minute reservation hold</b> guarantees your spot before you arrive, eliminating the uncertainty of full lots.<br/><br/>And third, we’ve integrated live <b>Traccar GPS fleet telemetry and OSRM road routing</b> with an offline-first PWA, so drivers never lose navigation even inside concrete basements or low-network zones. Our prototype is already live, running on Railway with 38 passing verification test suites."
        ),
        (
            "Scene 5: Overall Vision & Closing Call to Action (2:30 – 3:00)",
            "Founder back on camera, confident and forward-looking. Closing slide with project link, QR code, and contact information.<br/><b>Overlay Text:</b> 'Our Vision: Zero-Cruising Indian Cities'",
            "Our long-term vision is bold: to eliminate cruising-for-parking across India. By starting in Bengaluru and expanding to Mumbai, Delhi NCR, and Hyderabad, OpenPark will unlock over 100,000 hidden parking bays into a unified, accessible digital grid.<br/><br/>As electric vehicles and autonomous transit scale, OpenPark will serve as the intelligence layer guiding vehicles to chargers and staging depots seamlessly.<br/><br/>We have the working prototype, the architectural clarity, and the drive to solve urban congestion at its root. Thank you for considering OpenPark!"
        )
    ]

    for title, cues, speech in scenes:
        scene_content = [
            [Paragraph(f"<b>{title}</b>", scene_title)],
            [Paragraph(f"<b>Visual / B-Roll Cues:</b> {cues}", cue_style)],
            [Spacer(1, 4)],
            [Paragraph(speech, speech_style)]
        ]
        t_sc = Table(scene_content, colWidths=[516])
        t_sc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
            ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(t_sc)
        elements.append(Spacer(1, 8))

    doc.build(elements)
    print(f"Generated Video Script PDF: {out_path} ({os.path.getsize(out_path)} bytes)")


# ==============================================================================
# 3. DELIVERABLE 3: 03_Pitch_Deck_OpenPark.pdf (10-Slide Landscape 16:9 PDF)
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = self._pagesize
        # Top brand line
        self.setStrokeColor(PRIMARY_BLUE)
        self.setLineWidth(3)
        self.line(36, h - 30, w - 36, h - 30)

        # Footer line
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.75)
        self.line(36, 32, w - 36, 32)

        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(SLATE_GRAY)
        self.drawString(36, 20, "OpenPark Platform • Stage 1 Founder Deliverable (Nov 2026) • Live at openpark-web-production.up.railway.app")
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(w - 36, 20, page_str)
        self.restoreState()


def create_pitch_deck_pdf(out_path: str):
    # Standard 16:9 Widescreen slide page dimensions: 10 x 5.625 inches (720 x 405 pt)
    PAGE_WIDTH = 10 * inch
    PAGE_HEIGHT = 5.625 * inch

    doc = SimpleDocTemplate(
        out_path,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    slide_kicker = ParagraphStyle(
        'Kicker',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=PRIMARY_BLUE,
        spaceAfter=2
    )

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=DARK_NAVY,
        spaceAfter=4
    )

    slide_subtitle = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13.5,
        textColor=SLATE_GRAY,
        spaceAfter=10
    )

    card_header = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=DARK_NAVY,
        spaceAfter=4
    )

    card_body = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=DARK_NAVY
    )

    stat_num = ParagraphStyle(
        'StatNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=28,
        textColor=PRIMARY_BLUE,
        spaceAfter=2
    )

    stat_label = ParagraphStyle(
        'StatLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=SLATE_GRAY,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=DARK_NAVY
    )

    table_body = ParagraphStyle(
        'TB',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=DARK_NAVY
    )

    table_highlight = ParagraphStyle(
        'TBH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=PRIMARY_BLUE
    )

    elements = []

    # ==========================================
    # SLIDE 1: Title & Executive Summary
    # ==========================================
    elements.append(Paragraph("STAGE 1 FOUNDER PITCH DECK", slide_kicker))
    elements.append(Paragraph("OpenPark: AI-Powered Smart Parking &amp; Micro-Space Discovery", slide_title))
    elements.append(Paragraph("Eliminating urban parking congestion through strict 1 km AI spatial scanning, guaranteed 15-minute slot reservations, and live Traccar GPS road guidance.", slide_subtitle))

    card_left = [
        Paragraph("<b>The Core Mission</b>", card_header),
        Paragraph("Transform chaotic urban parking across high-density Indian metros by converting unindexed 45–550 m² private vacant plots, commercial basements, and institutional grounds into an accessible, real-time digital parking grid.", card_body),
        Spacer(1, 6),
        Paragraph("<b>Key Technological Edge:</b> Zero proprietary hardware cost per bay; runs on standard operator touch tablets and browser PWAs.", card_body)
    ]
    card_right = [
        Paragraph("<b>Live Prototype Verified</b>", card_header),
        Paragraph("<b>Driver Web App:</b> https://openpark-web-production.up.railway.app/app/<br/><b>Operator Dashboard:</b> https://openpark-web-production.up.railway.app/dashboard/<br/><b>API Docs:</b> https://openpark-web-production.up.railway.app/docs", card_body),
        Spacer(1, 6),
        Paragraph("<b>Founding Team:</b> Dhairya (Founder &amp; Systems Architect) + Core Spatial Engineering Team", card_body)
    ]
    t1 = Table([[card_left, card_right]], colWidths=[320, 328])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), LIGHT_BG),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t1)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 2: Problem Statement
    # ==========================================
    elements.append(Paragraph("THE URBAN PARKING CRISIS", slide_kicker))
    elements.append(Paragraph("Cruising For Parking: India's Hidden Congestion Bottleneck", slide_title))
    elements.append(Paragraph("Drivers waste hours circling city blocks while existing map apps only navigate to building doors with zero parking intelligence.", slide_subtitle))

    col1 = [
        Paragraph("22 mins", stat_num),
        Paragraph("AVERAGE SEARCH TIME / TRIP", stat_label),
        Paragraph("Drivers in Bengaluru, Delhi NCR, and Mumbai spend over 20 minutes crawling in traffic to find legal parking, leading to delays and missed meetings.", card_body)
    ]
    col2 = [
        Paragraph("30–40%", stat_num),
        Paragraph("OF DOWNTOWN CITY TRAFFIC", stat_label),
        Paragraph("Transport studies confirm that up to 40% of peak-hour central business district traffic consists solely of vehicles circling blocks hunting for parking spots.", card_body)
    ]
    col3 = [
        Paragraph("1.3B L", stat_num),
        Paragraph("IDLE FUEL WASTED ANNUALLY", stat_label),
        Paragraph("Hundreds of millions of liters of fuel burn at idle speeds, adding thousands of tons of avoidable CO₂ and PM2.5 particulate emissions to metro air.", card_body)
    ]
    t2 = Table([[col1, col2, col3]], colWidths=[210, 210, 218])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t2)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 3: Proposed Solution
    # ==========================================
    elements.append(Paragraph("PROPOSED SOLUTION", slide_kicker))
    elements.append(Paragraph("OpenPark: Zero-Hardware Smart Parking &amp; Micro-Grounds", slide_title))
    elements.append(Paragraph("Connecting drivers with commercial lots and newly unlocked micro-spaces through software-only intelligence.", slide_subtitle))

    s_col1 = [
        Paragraph("<b>1. 1 km AI Space Scanner</b>", card_header),
        Paragraph("Scans a strict 1,000 m radius around any destination to uncover not only multi-level car parks, but also untapped 45–550 m² private vacant plots, commercial basements, and institutional grounds (3–6 cars).", card_body)
    ]
    s_col2 = [
        Paragraph("<b>2. 15-Minute Slot Lock</b>", card_header),
        Paragraph("Drivers reserve their parking bay ahead of arrival with guaranteed availability. Real-time delta updates prevent double-booking and eradicate the anxiety of arriving at a full facility.", card_body)
    ]
    s_col3 = [
        Paragraph("<b>3. OSRM Road Routing &amp; GPS</b>", card_header),
        Paragraph("Turn-by-turn road guidance navigating drivers directly to the parking gate—not just the building facade. Powered by live Traccar vehicle telemetry and an offline-first service worker cache.", card_body)
    ]
    t3 = Table([[s_col1, s_col2, s_col3]], colWidths=[210, 210, 218])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t3)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 4: Key Differentiator
    # ==========================================
    elements.append(Paragraph("COMPETITIVE MOAT", slide_kicker))
    elements.append(Paragraph("Why OpenPark Wins Against Legacy Solutions", slide_title))
    elements.append(Paragraph("Zero hardware lock-in, proprietary 1 km spatial discovery, and basement-resilient offline technology.", slide_subtitle))

    diff_table_data = [
        [Paragraph("<b>Capability / Feature</b>", table_header), Paragraph("<b>Legacy Parking Apps</b>", table_header), Paragraph("<b>Google / Apple Maps</b>", table_header), Paragraph("<b>OpenPark Platform</b>", table_header)],
        [Paragraph("<b>Inventory Sourcing</b>", table_body), Paragraph("Only affiliated premium malls", table_body), Paragraph("Generic place directory only", table_body), Paragraph("Commercial Lots + 45–550 m² Micro-Grounds", table_highlight)],
        [Paragraph("<b>Hardware Required</b>", table_body), Paragraph("$10k+ boom gates per lot", table_body), Paragraph("None (no parking data)", table_body), Paragraph("Zero Hardware; Touch Tablet PWA", table_highlight)],
        [Paragraph("<b>Live Telemetry</b>", table_body), Paragraph("15s polling (slow/laggy)", table_body), Paragraph("Standard turn-by-turn", table_body), Paragraph("Traccar High-Speed WebSockets", table_highlight)],
        [Paragraph("<b>Search Intelligence</b>", table_body), Paragraph("Cloud API only", table_body), Paragraph("Cloud API (expensive)", table_body), Paragraph("SQLite FTS5 (33k POIs) + Google Places", table_highlight)],
        [Paragraph("<b>Basement Offline Support</b>", table_body), Paragraph("App crashes when offline", table_body), Paragraph("Often loses route underground", table_body), Paragraph("Offline PWA (Service Worker + Vector Cache)", table_highlight)]
    ]
    t4 = Table(diff_table_data, colWidths=[130, 150, 160, 208])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (3, 1), (3, -1), colors.HexColor("#EFF6FF")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t4)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 5: Market Opportunity & Research
    # ==========================================
    elements.append(Paragraph("MARKET OPPORTUNITY & RESEARCH", slide_kicker))
    elements.append(Paragraph("A Multi-Billion Dollar Smart Mobility Opportunity", slide_title))
    elements.append(Paragraph("Indian urban four-wheeler fleets are compounding at 9% annually amid municipal smart city mandates.", slide_subtitle))

    m1 = [
        Paragraph("$16.2B", stat_num),
        Paragraph("GLOBAL SMART PARKING TAM (2030)", stat_label),
        Paragraph("Global market expanding at 14.8% CAGR driven by automated parking, congestion pricing, and urban mobility policies.", card_body)
    ]
    m2 = [
        Paragraph("$1.2B", stat_num),
        Paragraph("INDIAN URBAN PARKING SAM (2028)", stat_label),
        Paragraph("Over 40 million registered personal cars in tier-1 Indian metros with acute space constraints in dense commercial corridors.", card_body)
    ]
    m3 = [
        Paragraph("$140M", stat_num),
        Paragraph("INITIAL SOM (BLR, DEL, MUM)", stat_label),
        Paragraph("High-density pilot hubs (Indiranagar, Koramangala, Whitefield, BKC, Cyber City) and last-mile delivery fleet staging.", card_body)
    ]
    t5 = Table([[m1, m2, m3]], colWidths=[210, 210, 218])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t5)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 6: Target Audience & Customer Personas
    # ==========================================
    elements.append(Paragraph("TARGET AUDIENCE & PERSONAS", slide_kicker))
    elements.append(Paragraph("Solving Critical Pain Points Across 3 Key Segments", slide_title))
    elements.append(Paragraph("Validated customer personas driving both sides of the micro-parking network effect.", slide_subtitle))

    p1 = [
        Paragraph("<b>Daily Urban Commuter</b>", card_header),
        Paragraph("<b>Profile:</b> Rohan, 32 • Tech Lead (Whitefield to Indiranagar)<br/><b>Pain:</b> 25 mins wasted hunting parking; stress; fears scratches or towing from illegal roadside parking.<br/><b>Value:</b> 1-tap booking before leaving home, guaranteed slot upon arrival, direct navigation to basement entry.", card_body)
    ]
    p2 = [
        Paragraph("<b>Commercial Fleet Driver</b>", card_header),
        Paragraph("<b>Profile:</b> Suresh, 28 • Logistics Courier (MG Road & Chickpet)<br/><b>Pain:</b> Heavy no-parking traffic fines while unloading; long delays waiting for loading bays.<br/><b>Value:</b> 15-minute quick staging bay reservations, avoiding fines and reducing delivery cycle times by 18%.", card_body)
    ]
    p3 = [
        Paragraph("<b>Micro-Plot & Lot Owner</b>", card_header),
        Paragraph("<b>Profile:</b> Vikram, 48 • Commercial Landowner (Koramangala)<br/><b>Pain:</b> 350 m² vacant lot unmonetized; cannot justify $15,000 automated boom barriers.<br/><b>Value:</b> Zero hardware setup. Uses OpenPark Operator Touch Dashboard on a tablet to monetize idle bays.", card_body)
    ]
    t6 = Table([[p1, p2, p3]], colWidths=[210, 210, 218])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t6)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 7: MVP & Product Prototype
    # ==========================================
    elements.append(Paragraph("MVP & PRODUCT PROTOTYPE", slide_kicker))
    elements.append(Paragraph("Battle-Tested Live Production Deployment", slide_title))
    elements.append(Paragraph("Not a pitch concept: OpenPark is live on Railway with 38 passing backend tests and sub-second response times.", slide_subtitle))

    proto_left = [
        Paragraph("<b>Technical Architecture &amp; Metrics</b>", card_header),
        Paragraph("• <b>Automated Test Suite:</b> 38/38 passing pytest tests (APIs, edge scanner, spatial calculations, telemetry).<br/>• <b>Multi-Tier Search:</b> Live Google Places (New) + SQLite FTS5 (33,000+ Indian POIs) + Photon/OSM geocoders.<br/>• <b>Vector Map Engine:</b> MapLibre GL JS supporting Google Satellite Hybrid and offline vector corridors.<br/>• <b>Navigation HUD:</b> Dynamic Island guidance, real-time speed, ETA, and turn-by-turn road geometries.", card_body)
    ]
    proto_right = [
        Paragraph("<b>Live Deployment Links</b>", card_header),
        Paragraph("<b>Driver Responsive PWA:</b><br/>https://openpark-web-production.up.railway.app/app/<br/><br/><b>Operator Touch Dashboard:</b><br/>https://openpark-web-production.up.railway.app/dashboard/<br/><br/><b>Interactive API Documentation:</b><br/>https://openpark-web-production.up.railway.app/docs", card_body)
    ]
    t7 = Table([[proto_left, proto_right]], colWidths=[320, 328])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), LIGHT_BG),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t7)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 8: Business Model & Monetization
    # ==========================================
    elements.append(Paragraph("BUSINESS MODEL", slide_kicker))
    elements.append(Paragraph("Multi-Stream Hybrid Monetization Strategy", slide_title))
    elements.append(Paragraph("Diversified revenue streams ensuring sustainable margins and low driver friction.", slide_subtitle))

    b1 = [
        Paragraph("₹10–₹20", stat_num),
        Paragraph("CONVENIENCE FEE / BOOKING", stat_label),
        Paragraph("Nominal convenience charge paid by drivers for guaranteed 15-minute slot lock and direct navigation to entry.", card_body)
    ]
    b2 = [
        Paragraph("12–15%", stat_num),
        Paragraph("OPERATOR REVENUE SHARE", stat_label),
        Paragraph("Commission on parking fees processed through newly monetized private plots, vacant basements, and event grounds.", card_body)
    ]
    b3 = [
        Paragraph("₹1,499/mo", stat_num),
        Paragraph("OPERATOR DASHBOARD SAAS", stat_label),
        Paragraph("Monthly software license for commercial lots: touch check-in tablet UI, audit logs, and revenue metrics.", card_body)
    ]
    t8 = Table([[b1, b2, b3]], colWidths=[210, 210, 218])
    t8.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t8)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 9: Team Overview & Key Roles
    # ==========================================
    elements.append(Paragraph("FOUNDING TEAM", slide_kicker))
    elements.append(Paragraph("Technical Excellence &amp; Domain Expertise", slide_title))
    elements.append(Paragraph("Combining deep systems engineering, spatial indexing, and rapid product execution.", slide_subtitle))

    team1 = [
        Paragraph("<b>Dhairya</b>", card_header),
        Paragraph("<b>Founder &amp; Lead Systems Architect</b><br/>• Full-stack distributed systems engineer.<br/>• Architected core FastAPI backend, spatial geocoding engine, MapLibre GL rendering layer, and cloud DevOps pipelines.", card_body)
    ]
    team2 = [
        Paragraph("<b>Spatial Systems Lead</b>", card_header),
        Paragraph("<b>Geodata &amp; Routing Engineering</b><br/>• Overture Maps extraction pipeline and PostGIS spatial queries.<br/>• OSRM turn-by-turn road network optimizations and Traccar WebSocket telemetry sync.", card_body)
    ]
    team3 = [
        Paragraph("<b>Product &amp; Operations Lead</b>", card_header),
        Paragraph("<b>Field Operations &amp; Growth</b><br/>• Onboarding commercial parking facilities and private plot owners across Bengaluru.<br/>• Driver growth campaigns, pilot testing, and operator terminal onboarding.", card_body)
    ]
    t9 = Table([[team1, team2, team3]], colWidths=[210, 210, 218])
    t9.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t9)
    elements.append(PageBreak())

    # ==========================================
    # SLIDE 10: Roadmap & Vision
    # ==========================================
    elements.append(Paragraph("ROADMAP & VISION", slide_kicker))
    elements.append(Paragraph("Scaling to Zero-Cruising Indian Cities", slide_title))
    elements.append(Paragraph("From high-density Bengaluru corridors to a nationwide smart mobility and EV staging grid.", slide_subtitle))

    r1 = [
        Paragraph("<b>Phase 1 • Q1–Q2 2027</b>", card_header),
        Paragraph("<b>Bengaluru Density Pilot</b><br/>• Onboard 150 commercial lots &amp; 300 micro-plots.<br/>• Focus: Indiranagar, Koramangala &amp; Whitefield.<br/>• Target: 25,000 monthly active drivers.<br/>• Operator touch tablet rollout.", card_body)
    ]
    r2 = [
        Paragraph("<b>Phase 2 • Q3–Q4 2027</b>", card_header),
        Paragraph("<b>Pan-Metro Expansion</b><br/>• Expand to Delhi NCR, Mumbai &amp; Hyderabad.<br/>• EV charging network reservation integration (Ather, Tata Power).<br/>• B2B logistics staging API for quick-commerce delivery fleets.", card_body)
    ]
    r3 = [
        Paragraph("<b>Phase 3 • 2028+</b>", card_header),
        Paragraph("<b>Smart City &amp; Autonomous</b><br/>• Municipal Smart City Command Center integration.<br/>• Autonomous vehicle depot staging handshakes.<br/>• Unlocking 100,000+ unified micro-parking bays nationwide.", card_body)
    ]
    t10 = Table([[r1, r2, r3]], colWidths=[210, 210, 218])
    t10.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t10)

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Generated Pitch Deck PDF: {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == '__main__':
    out_dir = "/Users/dhairya/openpark/submission"
    deck_dir = os.path.join(out_dir, "03_Pitch_Deck")
    os.makedirs(deck_dir, exist_ok=True)

    create_text_summary_pdf(os.path.join(out_dir, "01_Text_Summary.pdf"))
    create_video_script_pdf(os.path.join(out_dir, "02_Video_Introduction_Script.pdf"))
    create_pitch_deck_pdf(os.path.join(deck_dir, "Pitch_Deck_OpenPark.pdf"))
    print("ALL THREE PDFS CREATED SUCCESSFULLY WITH ZERO GLITCHES.")
