#!/usr/bin/env python3
"""
OpenPark — Advanced Founder Pitch Video Generator
Enhanced Motion Graphics Edition:
- Kinetic Typography Subtitles with Electric Yellow / Cyan Keyword Highlighting
- Dynamic Bengaluru Map with Rotating Radar Sweep Beam & Sonar Wave Pulses
- Elastic Spring Marker Popups & Glowing Route Telemetry with Moving Vehicle
- Founder Portrait Integration (Large Profile + Floating PIP Speaker Badge)
- 5-Act Structured Pitch matching the Stage 1 Competition Guidelines
"""

import os
import sys
import math
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMISSION_DIR = os.path.join(BASE_DIR, "submission")
OUTPUT_VIDEO = os.path.join(SUBMISSION_DIR, "02_OpenPark_Founder_Video_Introduction.mp4")
FOUNDER_IMG_PATH = os.path.join(SUBMISSION_DIR, "assets", "founder_dhairya.jpg")

# Video Specs
WIDTH = 1280
HEIGHT = 720
FPS = 30

# Color Palette (Obsidian / Emerald / Cyan / Electric Yellow / Coral)
BG_DARK = (10, 15, 29)             # Deep obsidian
CARD_BG = (16, 26, 48)             # Navy glass
CARD_BORDER = (35, 60, 100)        # Border
CYAN_ACCENT = (6, 182, 212)        # #06b6d4
EMERALD_ACCENT = (16, 185, 129)    # #10b981
CORAL_ACCENT = (244, 63, 94)       # #f43f5e
AMBER_ACCENT = (245, 158, 11)      # #f59e0b
YELLOW_HL = (250, 204, 21)         # #facc15 Electric yellow for kinetic subtitle highlights
WHITE = (255, 255, 255)
GRAY_TEXT = (148, 163, 184)
LIGHT_TEXT = (226, 232, 240)

# Fonts setup
FONT_REG_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
if not os.path.exists(FONT_REG_PATH):
    FONT_REG_PATH = "/System/Library/Fonts/Helvetica.ttc"
    FONT_BOLD_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size, bold=False):
    try:
        p = FONT_BOLD_PATH if bold else FONT_REG_PATH
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()

F_TITLE = get_font(34, bold=True)
F_HEADING = get_font(23, bold=True)
F_SUB = get_font(18, bold=True)
F_BODY = get_font(15, bold=False)
F_BODY_BOLD = get_font(15, bold=True)
F_STAT_BIG = get_font(46, bold=True)
F_CAPTION = get_font(20, bold=True)
F_TINY = get_font(12, bold=False)
F_TINY_BOLD = get_font(12, bold=True)

# Cache pre-cropped founder portraits
FOUNDER_LARGE = None
FOUNDER_PIP = None

def load_founder_portraits():
    global FOUNDER_LARGE, FOUNDER_PIP
    if not os.path.exists(FOUNDER_IMG_PATH):
        return
    try:
        raw = Image.open(FOUNDER_IMG_PATH).convert("RGBA")
        w, h = raw.size
        crop_sz = min(w, h)
        left = (w - crop_sz) // 2
        cropped = raw.crop((left, 0, left + crop_sz, crop_sz))

        # 1. Large 240x240 for Scene 2
        large_sz = 240
        c_large = cropped.resize((large_sz, large_sz), Image.Resampling.LANCZOS)
        mask_l = Image.new("L", (large_sz, large_sz), 0)
        draw_l = ImageDraw.Draw(mask_l)
        draw_l.ellipse([0, 0, large_sz, large_sz], fill=255)
        FOUNDER_LARGE = Image.new("RGBA", (large_sz, large_sz), (0, 0, 0, 0))
        FOUNDER_LARGE.paste(c_large, (0, 0), mask_l)

        # 2. PIP 110x110 for other scenes
        pip_sz = 110
        c_pip = cropped.resize((pip_sz, pip_sz), Image.Resampling.LANCZOS)
        mask_p = Image.new("L", (pip_sz, pip_sz), 0)
        draw_p = ImageDraw.Draw(mask_p)
        draw_p.ellipse([0, 0, pip_sz, pip_sz], fill=255)
        FOUNDER_PIP = Image.new("RGBA", (pip_sz, pip_sz), (0, 0, 0, 0))
        FOUNDER_PIP.paste(c_pip, (0, 0), mask_p)
    except Exception as e:
        print(f"Warning: Failed to load founder portrait: {e}")

load_founder_portraits()

# 21 Structured Segments with Kinetic Subtitle Tokens
# Tokens format: List of (word, is_highlighted)
SEGMENTS = [
    # Act 1: The Urban Mobility Crisis
    {
        "id": "s01", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "Welcome to OpenPark",
        "text": "Namaste and hello everyone. Welcome to OpenPark.",
        "tokens": [("Namaste", False), ("and", False), ("hello", False), ("everyone.", False), ("Welcome", False), ("to", False), ("OPENPARK.", True)],
        "type": "title_intro"
    },
    {
        "id": "s02", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "The Daily Urban Commute Struggle",
        "text": "Picture this: you drive forty-five minutes to reach a meeting in Indiranagar or Connaught Place.",
        "tokens": [("Picture", False), ("this:", False), ("you", False), ("drive", False), ("45 MINUTES", True), ("to", False), ("reach", False), ("Indiranagar", True), ("or", False), ("Connaught Place.", True)],
        "type": "traffic_grid"
    },
    {
        "id": "s03", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "Cruising in Endless Circles",
        "text": "For the next twenty-five minutes, you crawl through bumper-to-bumper traffic, circling blocks hunting for parking.",
        "tokens": [("For", False), ("the", False), ("next", False), ("25 MINUTES,", True), ("you", False), ("crawl", False), ("through", False), ("traffic,", False), ("CIRCLING BLOCKS", True), ("hunting", False), ("for", False), ("parking.", False)],
        "type": "circling_crawl"
    },
    {
        "id": "s04", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "The Alarming Traffic Reality",
        "text": "In India's top metropolitan cities, thirty to forty percent of peak traffic is caused solely by vehicles cruising for parking.",
        "tokens": [("In", False), ("Indian", False), ("metros,", False), ("30% TO 40%", True), ("of", False), ("all", False), ("peak", False), ("traffic", False), ("is", False), ("CRUISING FOR PARKING.", True)],
        "type": "stat_35pct"
    },
    {
        "id": "s05", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "The Staggering Macro Cost",
        "text": "That equates to billions of rupees in wasted fuel, tons of toxic emissions, and countless lost hours every day.",
        "tokens": [("That", False), ("equates", False), ("to", False), ("BILLIONS IN FUEL,", True), ("MILLIONS OF TONS CO2,", True), ("and", False), ("countless", False), ("lost", False), ("hours", False), ("daily.", False)],
        "type": "macro_impact"
    },

    # Act 2: Founder & Core Team Introduction
    {
        "id": "s06", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "Founder Introduction",
        "text": "I am Dhairya, Founder and Lead Systems Architect of OpenPark.",
        "tokens": [("I", False), ("am", False), ("DHAIRYA,", True), ("Founder", False), ("and", False), ("Lead", False), ("Systems", False), ("Architect", False), ("of", False), ("OPENPARK.", True)],
        "type": "founder_profile"
    },
    {
        "id": "s07", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "Engineering Background",
        "text": "My background is in full stack distributed systems, geospatial infrastructure, and cloud engineering.",
        "tokens": [("My", False), ("background", False), ("is", False), ("in", False), ("DISTRIBUTED SYSTEMS,", True), ("GEOSPATIAL ENGINES,", True), ("and", False), ("cloud", False), ("engineering.", False)],
        "type": "tech_stack"
    },
    {
        "id": "s08", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "High-Performance Spatial Engines",
        "text": "Over the past year, I have built spatial routing engines combining OpenStreetMap, Overture Maps, and GPS telemetry.",
        "tokens": [("Over", False), ("the", False), ("past", False), ("year,", False), ("I've", False), ("built", False), ("SPATIAL ENGINES", True), ("combining", False), ("OpenStreetMap", False), ("and", False), ("LIVE GPS TELEMETRY.", True)],
        "type": "spatial_engine"
    },
    {
        "id": "s09", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "Multidisciplinary Core Team",
        "text": "Beside me, our core team brings specialized experience across spatial data science, edge computer vision, and fleet operations.",
        "tokens": [("Beside", False), ("me,", False), ("our", False), ("team", False), ("spans", False), ("SPATIAL DATA SCIENCE,", True), ("COMPUTER VISION,", True), ("and", False), ("fleet", False), ("operations.", False)],
        "type": "core_team"
    },

    # Act 3: Motivation & The Urban Paradox
    {
        "id": "s10", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "The Bengaluru Paradox",
        "text": "Our motivation started from a profound paradox we noticed right here in Bengaluru.",
        "tokens": [("Our", False), ("motivation", False), ("started", False), ("from", False), ("a", False), ("PROFOUND PARADOX", True), ("right", False), ("here", False), ("in", False), ("BENGALURU.", True)],
        "type": "paradox_intro"
    },
    {
        "id": "s11", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "Clogged Roads vs. Invisible Supply",
        "text": "While street curbs are overflowing with chaotic double parking, hundreds of private basements and vacant micro-plots sit empty just three hundred meters away.",
        "tokens": [("While", False), ("curbs", False), ("overflow,", False), ("PRIVATE BASEMENTS", True), ("and", False), ("VACANT MICRO-PLOTS", True), ("sit", False), ("empty", False), ("300M AWAY.", True)],
        "type": "split_paradox"
    },
    {
        "id": "s12", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "The Hardware Boom-Barrier Trap",
        "text": "Legacy parking systems demand millions in proprietary boom barriers that Indian cities cannot afford to retrofit.",
        "tokens": [("Legacy", False), ("systems", False), ("demand", False), ("MILLIONS IN BOOM-BARRIERS", True), ("that", False), ("Indian", False), ("cities", False), ("CANNOT RETROFIT.", True)],
        "type": "barrier_flaw"
    },
    {
        "id": "s13", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "The Software-First Antidote",
        "text": "We knew there had to be a software-first, zero-hardware alternative.",
        "tokens": [("We", False), ("knew", False), ("there", False), ("had", False), ("to", False), ("be", False), ("a", False), ("SOFTWARE-FIRST,", True), ("ZERO-HARDWARE ALTERNATIVE.", True)],
        "type": "zero_hardware"
    },

    # Act 4: The OpenPark Solution & Live Demo
    {
        "id": "s14", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "The OpenPark Platform",
        "text": "That is why we built OpenPark: an open-source, AI-powered smart mobility platform.",
        "tokens": [("That", False), ("is", False), ("why", False), ("we", False), ("built", False), ("OPENPARK:", True), ("an", False), ("AI-POWERED", True), ("smart", False), ("mobility", False), ("platform.", False)],
        "type": "solution_hero"
    },
    {
        "id": "s15", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "1 km AI Micro-Space Scanner",
        "text": "First, our strict one-kilometer AI Space Scanner dynamically indexes unindexed micro-pockets and commercial basements.",
        "tokens": [("First,", False), ("our", False), ("1 KM AI SPACE SCANNER", True), ("indexes", False), ("UNINDEXED MICRO-POCKETS", True), ("and", False), ("commercial", False), ("basements.", False)],
        "type": "map_scanner"
    },
    {
        "id": "s16", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "15-Minute Guaranteed Slot Lock",
        "text": "Second, our fifteen-minute reservation hold guarantees your spot before you arrive, eliminating full-lot uncertainty.",
        "tokens": [("Second,", False), ("our", False), ("15-MINUTE RESERVATION HOLD", True), ("guarantees", False), ("your", False), ("spot", False), ("BEFORE YOU ARRIVE.", True)],
        "type": "map_lock"
    },
    {
        "id": "s17", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "Live Turn-by-Turn GPS Navigation",
        "text": "And third, live Traccar GPS telemetry and turn-by-turn routing guide drivers directly to their bay with full offline support.",
        "tokens": [("Third,", False), ("live", False), ("TRACCAR GPS TELEMETRY", True), ("and", False), ("ROUTING", True), ("guide", False), ("drivers", False), ("with", False), ("OFFLINE SUPPORT.", True)],
        "type": "map_routing"
    },

    # Act 5: Scaled Vision & Call to Action
    {
        "id": "s18", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "Eliminating Cruising Across India",
        "text": "Our long-term vision is bold: to eliminate cruising for parking across India.",
        "tokens": [("Our", False), ("long-term", False), ("vision", False), ("is", False), ("bold:", False), ("to", False), ("ELIMINATE CRUISING", True), ("across", False), ("India.", False)],
        "type": "pan_india"
    },
    {
        "id": "s19", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "100,000+ Unified Micro-Bays",
        "text": "Expanding from Bengaluru to Mumbai, Delhi NCR, and Hyderabad, OpenPark will unlock over one hundred thousand hidden bays.",
        "tokens": [("Expanding", False), ("to", False), ("Mumbai,", False), ("Delhi,", False), ("and", False), ("Hyderabad,", False), ("OpenPark", False), ("will", False), ("unlock", False), ("100,000+ HIDDEN BAYS.", True)],
        "type": "scale_grid"
    },
    {
        "id": "s20", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "Verified Live Production Prototype",
        "text": "Our prototype is live on Railway today with thirty-eight passing verification test suites.",
        "tokens": [("Our", False), ("prototype", False), ("is", False), ("LIVE ON RAILWAY TODAY", True), ("with", False), ("38 PASSING TEST SUITES.", True)],
        "type": "live_status"
    },
    {
        "id": "s21", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "Solving Congestion at the Root",
        "text": "We have the architectural clarity and the drive to solve urban congestion at its root. Thank you for considering OpenPark!",
        "tokens": [("We", False), ("have", False), ("the", False), ("drive", False), ("to", False), ("solve", False), ("urban", False), ("congestion.", False), ("THANK YOU FOR CONSIDERING OPENPARK!", True)],
        "type": "closing_hero"
    }
]

def synthesize_audio_tracks(temp_dir):
    """Synthesizes speech narration via macOS say and measures exact timings."""
    ffmpeg_exe = os.path.join(
        BASE_DIR, "backend/venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    )
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    audio_files = []
    segment_timings = []
    current_time = 0.0

    print("Generating voice narration tracks with Rishi (English (India))...")
    for i, seg in enumerate(SEGMENTS):
        aiff_path = os.path.join(temp_dir, f"{seg['id']}.aiff")
        wav_path = os.path.join(temp_dir, f"{seg['id']}.wav")

        # Speak with natural rate (170 wpm)
        subprocess.run(["/usr/bin/say", "-v", "Rishi (English (India))", "-r", "170", "-o", aiff_path, seg["text"]], check=True)

        # Append 0.18s silence padding for breathing cadence
        pad_filter = "apad=pad_dur=0.18"
        subprocess.run([ffmpeg_exe, "-y", "-i", aiff_path, "-af", pad_filter, "-ar", "44100", "-ac", "2", wav_path], capture_output=True, check=True)

        res = subprocess.run([ffmpeg_exe, "-i", wav_path], capture_output=True, text=True)
        dur = 0.0
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                dur = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                break

        start_frame = int(round(current_time * FPS))
        end_frame = int(round((current_time + dur) * FPS))
        segment_timings.append({
            "seg": seg,
            "start_time": current_time,
            "end_time": current_time + dur,
            "duration": dur,
            "start_frame": start_frame,
            "end_frame": end_frame,
            "wav_path": wav_path
        })
        current_time += dur
        audio_files.append(wav_path)

    # Master audio concatenation
    concat_list_path = os.path.join(temp_dir, "concat_audio.txt")
    with open(concat_list_path, "w") as f:
        for p in audio_files:
            f.write(f"file '{p}'\n")

    master_wav = os.path.join(temp_dir, "master_audio.wav")
    subprocess.run([
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path,
        "-c:a", "pcm_s16le", master_wav
    ], capture_output=True, check=True)

    total_duration = current_time
    total_frames = int(round(total_duration * FPS))
    return master_wav, segment_timings, total_frames, total_duration

# ----------------- KINETIC SUBTITLE & HUD DRAWING -----------------

def draw_header(draw, act_num, act_title, seg_title):
    """Draws sleek top navigation bar."""
    draw.rectangle([0, 0, WIDTH, 54], fill=(12, 18, 34))
    draw.line([(0, 54), (WIDTH, 54)], fill=(28, 46, 78), width=1)

    # Logo
    draw.ellipse([24, 12, 54, 42], fill=EMERALD_ACCENT)
    draw.text((34, 15), "P", fill=WHITE, font=F_HEADING)
    draw.text((64, 16), "OPENPARK", fill=WHITE, font=F_HEADING)

    # Act Badge
    badge_x = 230
    draw.rounded_rectangle([badge_x, 14, badge_x + 320, 40], radius=6, fill=(18, 32, 60), outline=CYAN_ACCENT, width=1)
    act_str = f"ACT {act_num:02d} / 05 • {act_title}"
    draw.text((badge_x + 12, 19), act_str, fill=CYAN_ACCENT, font=F_TINY_BOLD)

    # Live Production Badge
    status_w = 260
    status_x = WIDTH - status_w - 24
    draw.rounded_rectangle([status_x, 14, status_x + status_w, 40], radius=13, fill=(15, 30, 55), outline=(40, 70, 110), width=1)
    draw.ellipse([status_x + 12, 23, status_x + 20, 31], fill=EMERALD_ACCENT)
    draw.text((status_x + 28, 19), "LIVE: Railway Production", fill=LIGHT_TEXT, font=F_TINY_BOLD)

def draw_kinetic_subtitles(draw, tokens, current_frame, total_frames):
    """
    Renders high-impact kinetic typography subtitles:
    - Frosted dark pill background with subtle glow
    - Speaker identification badge (Dhairya • Founder)
    - Electric yellow highlight on emphasis tokens, white on normal words
    """
    pill_w = 1140
    pill_h = 78
    pill_x = (WIDTH - pill_w) // 2
    pill_y = HEIGHT - pill_h - 20

    # Drop shadow
    draw.rounded_rectangle([pill_x + 3, pill_y + 3, pill_x + pill_w + 3, pill_y + pill_h + 3], radius=18, fill=(4, 7, 14))
    # Frosted pill container
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=18, fill=(14, 22, 42), outline=(45, 80, 130), width=2)

    # Speaker tag
    spk_w = 210
    draw.rounded_rectangle([pill_x + 16, pill_y + 18, pill_x + 16 + spk_w, pill_y + 44], radius=6, fill=(22, 38, 70))
    draw.ellipse([pill_x + 26, pill_y + 27, pill_x + 34, pill_y + 35], fill=EMERALD_ACCENT)
    draw.text((pill_x + 42, pill_y + 24), "DHAIRYA (FOUNDER)", fill=CYAN_ACCENT, font=F_TINY_BOLD)

    # Render tokens
    space_w = 8
    total_text_w = 0
    token_widths = []
    for word, hl in tokens:
        bbox = F_CAPTION.getbbox(word)
        tw = bbox[2] - bbox[0]
        token_widths.append(tw)
        total_text_w += tw + space_w
    total_text_w -= space_w

    avail_w = pill_w - spk_w - 60
    start_x = pill_x + spk_w + 40
    if total_text_w < avail_w:
        start_x = pill_x + spk_w + 40 + (avail_w - total_text_w) // 2

    tx = start_x
    ty = pill_y + 24
    for i, (word, hl) in enumerate(tokens):
        col = YELLOW_HL if hl else WHITE
        draw.text((tx + 1, ty + 1), word, fill=(0, 0, 0), font=F_CAPTION)
        draw.text((tx, ty), word, fill=col, font=F_CAPTION)
        tx += token_widths[i] + space_w

    # Bottom progress bar
    progress = min(1.0, max(0.0, current_frame / float(total_frames)))
    draw.rectangle([0, HEIGHT - 5, WIDTH, HEIGHT], fill=(20, 30, 50))
    bar_w = int(WIDTH * progress)
    if bar_w > 0:
        draw.rectangle([0, HEIGHT - 5, bar_w, HEIGHT], fill=EMERALD_ACCENT)

def draw_pip_founder(img, draw):
    """Draws a floating PIP founder avatar in the bottom-right corner."""
    if FOUNDER_PIP is None:
        return
    pip_x = WIDTH - 150
    pip_y = HEIGHT - 200
    draw.ellipse([pip_x - 4, pip_y - 4, pip_x + 114, pip_y + 114], fill=(15, 30, 55), outline=CYAN_ACCENT, width=2)
    img.paste(FOUNDER_PIP, (pip_x, pip_y), FOUNDER_PIP)
    draw.rounded_rectangle([pip_x + 12, pip_y + 95, pip_x + 98, pip_y + 115], radius=5, fill=(10, 20, 38), outline=EMERALD_ACCENT, width=1)
    draw.text((pip_x + 22, pip_y + 98), "● SPEAKER", fill=EMERALD_ACCENT, font=F_TINY_BOLD)

# ----------------- SCENE RENDERERS -----------------

def render_title_intro(img, draw, progress, frame_in_seg):
    """Scene 1: Grand Hero Title Card."""
    cx, cy = WIDTH // 2, HEIGHT // 2 - 20
    card_w, card_h = 920, 430
    x0, y0 = cx - card_w // 2, cy - card_h // 2

    draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)

    tag = "STAGE 1 FOUNDER VIDEO INTRODUCTION • DEMO DAY 2026"
    draw.rounded_rectangle([cx - 240, y0 + 35, cx + 240, y0 + 68], radius=8, fill=(24, 45, 82), outline=EMERALD_ACCENT, width=1)
    draw.text((cx - 215, y0 + 44), tag, fill=EMERALD_ACCENT, font=F_TINY_BOLD)

    draw.text((cx - 220, y0 + 95), "OPENPARK", fill=WHITE, font=get_font(52, bold=True))
    draw.text((cx - 310, y0 + 165), "AI-Powered Smart Mobility & Micro-Parking Network", fill=CYAN_ACCENT, font=F_HEADING)

    draw.line([(cx - 250, y0 + 215), (cx + 250, y0 + 215)], fill=(40, 70, 115), width=2)

    b1 = "• 1 km AI Small-Ground & Basement Space Scanner"
    b2 = "• 15-Minute Guaranteed Slot Lock Reservation"
    b3 = "• Live Traccar GPS Telemetry & OSRM Routing Grid"
    draw.text((cx - 240, y0 + 240), b1, fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.text((cx - 240, y0 + 275), b2, fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.text((cx - 240, y0 + 310), b3, fill=LIGHT_TEXT, font=F_BODY_BOLD)

    draw.text((cx - 190, y0 + 365), "Founder: Dhairya  |  Bengaluru, India", fill=GRAY_TEXT, font=F_SUB)
    draw_pip_founder(img, draw)

def render_traffic_grid(img, draw, progress, frame_in_seg):
    """Scene 2: Bengaluru traffic congestion grid simulation with moving vehicle headlights."""
    draw.rounded_rectangle([80, 80, 600, 560], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 110), "THE URBAN COMMUTE CRISIS", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((110, 145), "Bengaluru & Delhi NCR Metro Corridors", fill=GRAY_TEXT, font=F_BODY)

    draw.text((110, 200), "Trip Phase 1: High-Speed Commute (Indiranagar)", fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.rounded_rectangle([110, 230, 560, 270], radius=8, fill=(25, 45, 80))
    draw.rounded_rectangle([110, 230, 450, 270], radius=8, fill=(34, 197, 94))
    draw.text((130, 242), "45 Minutes: 18 km Travel Distance (Smooth Arterial)", fill=WHITE, font=F_TINY_BOLD)

    draw.text((110, 310), "Trip Phase 2: Parking Search Cruising (Final 500m)", fill=CORAL_ACCENT, font=F_BODY_BOLD)
    draw.rounded_rectangle([110, 340, 560, 380], radius=8, fill=(25, 45, 80))
    crawl_w = int(110 + (450 - 110) * min(1.0, progress * 1.5))
    draw.rounded_rectangle([110, 340, crawl_w, 380], radius=8, fill=CORAL_ACCENT)
    draw.text((130, 352), "+25 Minutes: Crawling 4 Blocks (Zero Vacant Spots)", fill=WHITE, font=F_TINY_BOLD)

    draw.rounded_rectangle([110, 420, 560, 520], radius=12, fill=(35, 20, 30), outline=CORAL_ACCENT, width=1)
    draw.text((130, 435), "RESULT: TRIP TIME INFLATED BY +55%", fill=CORAL_ACCENT, font=F_SUB)
    draw.text((130, 465), "Drivers spend over a third of their journey in search panic,", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((130, 488), "burning fuel and choking arterial traffic corridors.", fill=LIGHT_TEXT, font=F_BODY)

    # Right Card: Traffic simulation
    draw.rounded_rectangle([630, 80, 1200, 560], radius=18, fill=(14, 22, 40), outline=CYAN_ACCENT, width=2)
    draw.text((660, 110), "SIMULATION: INDIRANAGAR 100 FT ROAD", fill=CYAN_ACCENT, font=F_HEADING)

    draw.rectangle([680, 280, 1150, 340], fill=(25, 38, 65))
    draw.line([(680, 310), (1150, 310)], fill=(80, 100, 140), width=2)
    draw.text((690, 260), "Indiranagar 100 Feet Road (Congested Arterial)", fill=GRAY_TEXT, font=F_TINY)

    draw.rectangle([780, 160, 830, 520], fill=(22, 32, 55))
    draw.rectangle([980, 160, 1030, 520], fill=(22, 32, 55))

    phase = (frame_in_seg % 60) / 60.0
    for idx, x_base in enumerate(range(700, 1140, 55)):
        vx = int(x_base + phase * 40) % 450 + 690
        col = CORAL_ACCENT if idx % 2 == 0 else AMBER_ACCENT
        draw.rounded_rectangle([vx, 292, vx + 22, 304], radius=3, fill=col)
        draw.polygon([(vx + 22, 294), (vx + 34, 290), (vx + 34, 306), (vx + 22, 302)], fill=(255, 255, 200))
        draw.rounded_rectangle([vx - 20, 316, vx + 2, 328], radius=3, fill=(100, 140, 200))

    draw.rounded_rectangle([820, 200, 1120, 255], radius=10, fill=(40, 15, 25), outline=CORAL_ACCENT, width=2)
    draw.text((835, 212), "CRUISING FOR PARKING DETECTED", fill=CORAL_ACCENT, font=F_TINY_BOLD)
    draw.text((835, 230), "Speed: 6 km/h  |  Delay: +25 mins", fill=WHITE, font=F_TINY)

def render_circling_crawl(img, draw, progress, frame_in_seg):
    """Scene 3: Endless block circling animation with perimeter trail."""
    draw.rounded_rectangle([80, 80, 680, 560], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 110), "THE CRUISING PARKING TRAP", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((110, 145), "Repetitive block circling without real-time vacancy data", fill=GRAY_TEXT, font=F_BODY)

    bx0, by0 = 200, 200
    bw, bh = 360, 260
    draw.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=(18, 30, 52), outline=(40, 70, 110), width=3)
    draw.text((bx0 + 80, by0 + 115), "COMMERCIAL BLOCK", fill=(60, 95, 150), font=F_SUB)
    draw.text((bx0 + 105, by0 + 145), "All Curbs Full", fill=CORAL_ACCENT, font=F_TINY_BOLD)

    perimeter = 2 * (bw + bh)
    loop_pos = (frame_in_seg * 12) % perimeter
    if loop_pos < bw:
        car_x = bx0 + loop_pos
        car_y = by0
    elif loop_pos < bw + bh:
        car_x = bx0 + bw
        car_y = by0 + (loop_pos - bw)
    elif loop_pos < 2 * bw + bh:
        car_x = bx0 + bw - (loop_pos - (bw + bh))
        car_y = by0 + bh
    else:
        car_x = bx0
        car_y = by0 + bh - (loop_pos - (2 * bw + bh))

    draw.rectangle([bx0 - 15, by0 - 15, bx0 + bw + 15, by0 + bh + 15], outline=(60, 30, 45), width=6)
    draw.rounded_rectangle([car_x - 14, car_y - 14, car_x + 14, car_y + 14], radius=6, fill=CORAL_ACCENT, outline=WHITE, width=2)
    draw.text((car_x - 6, car_y - 8), "V", fill=WHITE, font=F_TINY_BOLD)

    # Right Card
    draw.rounded_rectangle([710, 80, 1200, 560], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((740, 110), "DRIVER TELEMETRY IN SEARCH MODE", fill=WHITE, font=F_HEADING)

    blocks_circled = int(1 + progress * 5)
    fuel_wasted = 0.3 + progress * 0.9

    metrics = [
        ("BLOCKS CIRCLED", f"{blocks_circled} Loops", CORAL_ACCENT),
        ("TIME WASTED", f"{int(12 + progress * 13)} Minutes", AMBER_ACCENT),
        ("FUEL BURNED IN IDLE", f"{fuel_wasted:.2f} Litres", WHITE),
        ("SEARCH STRESS LEVEL", "CRITICAL (High)", CORAL_ACCENT),
    ]

    for i, (m_lbl, m_val, m_col) in enumerate(metrics):
        my = 180 + i * 85
        draw.rounded_rectangle([740, my, 1170, my + 68], radius=10, fill=(22, 34, 60), outline=(40, 65, 105), width=1)
        draw.text((760, my + 14), m_lbl, fill=GRAY_TEXT, font=F_TINY_BOLD)
        draw.text((760, my + 32), m_val, fill=m_col, font=F_SUB)

def render_stat_35pct(img, draw, progress, frame_in_seg):
    """Scene 4: Huge 30-40% cruising traffic spotlight."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CORAL_ACCENT, width=3)

    draw.text((cx - 380, 115), "THE HIDDEN SOURCE OF METRO GRIDLOCK", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((cx - 320, 150), "Peer-reviewed urban transport data across India's top metros", fill=GRAY_TEXT, font=F_BODY)

    draw.text((cx - 240, 195), "30% - 40%", fill=WHITE, font=get_font(72, bold=True))
    draw.text((cx - 390, 300), "OF ALL PEAK-HOUR TRAFFIC IS DRIVERS CRUISING FOR PARKING", fill=AMBER_ACCENT, font=F_HEADING)

    draw.text((160, 370), "Vehicles Traveling to Final Destination", fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.rounded_rectangle([160, 395, 1120, 425], radius=6, fill=(24, 40, 70))
    draw.rounded_rectangle([160, 395, 760, 425], radius=6, fill=(59, 130, 246))
    draw.text((180, 402), "65% Commuters Moving Forward", fill=WHITE, font=F_TINY_BOLD)

    draw.text((160, 445), "Vehicles Ready to Park, but Crawling Street Blocks (The OpenPark Target)", fill=CORAL_ACCENT, font=F_BODY_BOLD)
    draw.rounded_rectangle([160, 470, 1120, 500], radius=6, fill=(24, 40, 70))
    draw.rounded_rectangle([160, 470, 540, 500], radius=6, fill=CORAL_ACCENT)
    draw.text((180, 477), "35% Cruising & Circling (Eliminated with OpenPark)", fill=WHITE, font=F_TINY_BOLD)

    draw.text((cx - 310, 520), "Eliminating this cruising load immediately unlocks 35% arterial capacity.", fill=EMERALD_ACCENT, font=F_BODY_BOLD)

def render_macro_impact(img, draw, progress, frame_in_seg):
    """Scene 5: 3 Macro-economic & environmental impact cards."""
    draw.text((100, 95), "THE MACRO SCALE OF URBAN PARKING WASTE", fill=WHITE, font=F_TITLE)
    draw.text((100, 140), "Annualized cumulative toll on Indian metropolitan economies and the environment", fill=GRAY_TEXT, font=F_BODY)

    cards = [
        ("1.3+ BILLION", "LITRES OF FUEL WASTED", "Burned idling and crawling blocks while searching for vacant spots.", CORAL_ACCENT),
        ("3.2 MILLION", "TONS OF CO2 EMISSIONS", "Unnecessary tailpipe pollution concentrated at pedestrian street level.", AMBER_ACCENT),
        ("Rs. 22,000 CR", "ANNUAL ECONOMIC DRAIN", "Lost human productivity, delayed logistics, and gridlock congestion.", EMERALD_ACCENT)
    ]

    for i, (stat_top, stat_sub, desc, col) in enumerate(cards):
        x = 90 + i * 370
        y = 190
        w = 350
        h = 350

        draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([x + 20, y + 25, x + 160, y + 55], radius=6, fill=(24, 38, 68))
        draw.text((x + 30, y + 33), f"IMPACT {i+1:02d}", fill=col, font=F_TINY_BOLD)

        draw.text((x + 20, y + 80), stat_top, fill=col, font=F_STAT_BIG)
        draw.text((x + 20, y + 145), stat_sub, fill=WHITE, font=F_SUB)

        draw.line([(x + 20, y + 185), (x + w - 20, y + 185)], fill=(40, 60, 95), width=1)

        words = desc.split()
        draw.text((x + 20, y + 210), " ".join(words[:6]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 20, y + 240), " ".join(words[6:12]), fill=LIGHT_TEXT, font=F_BODY)
        if len(words) > 12:
            draw.text((x + 20, y + 270), " ".join(words[12:]), fill=LIGHT_TEXT, font=F_BODY)

def render_founder_profile(img, draw, progress, frame_in_seg):
    """Scene 6: Founder card featuring the actual founder portrait photo."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)

    port_x = 150
    port_y = 135
    port_sz = 240
    draw.ellipse([port_x - 6, port_y - 6, port_x + port_sz + 6, port_y + port_sz + 6], fill=(20, 40, 75), outline=EMERALD_ACCENT, width=3)
    if FOUNDER_LARGE is not None:
        img.paste(FOUNDER_LARGE, (port_x, port_y), FOUNDER_LARGE)
    else:
        draw.ellipse([port_x, port_y, port_x + port_sz, port_y + port_sz], fill=(22, 45, 80), outline=EMERALD_ACCENT, width=3)
        draw.text((port_x + 75, port_y + 85), "DK", fill=WHITE, font=get_font(60, bold=True))

    draw.rounded_rectangle([port_x + 20, port_y + port_sz + 15, port_x + port_sz - 20, port_y + port_sz + 50], radius=8, fill=EMERALD_ACCENT)
    draw.text((port_x + 40, port_y + port_sz + 24), "FOUNDER & ARCHITECT", fill=WHITE, font=F_TINY_BOLD)

    draw.text((430, 125), "DHAIRYA", fill=WHITE, font=get_font(44, bold=True))
    draw.text((430, 180), "Founder & Lead Systems Architect • OpenPark", fill=CYAN_ACCENT, font=F_HEADING)

    badges = ["Distributed Spatial Systems", "PostGIS & Cloud Architecture", "Bengaluru, India"]
    bx = 430
    for b in badges:
        bw = len(b) * 9 + 24
        draw.rounded_rectangle([bx, 225, bx + bw, 257], radius=6, fill=(20, 40, 72), outline=(50, 80, 130), width=1)
        draw.text((bx + 12, 233), b, fill=LIGHT_TEXT, font=F_TINY_BOLD)
        bx += bw + 12

    draw.line([(430, 280), (1120, 280)], fill=(40, 65, 105), width=2)

    draw.text((430, 305), "CORE CAPABILITIES & FOCUS:", fill=WHITE, font=F_SUB)
    c1 = "• Architected high-performance spatial routing and slot-indexing engines."
    c2 = "• Integrated OpenStreetMap, Overture Maps, and Traccar GPS telemetry pipeline."
    c3 = "• Shipped zero-hardware PWA architecture deployed on Railway with 38 verified tests."
    c4 = "• Dedicated to eliminating urban congestion through software-first infrastructure."

    draw.text((430, 340), c1, fill=LIGHT_TEXT, font=F_BODY)
    draw.text((430, 375), c2, fill=LIGHT_TEXT, font=F_BODY)
    draw.text((430, 410), c3, fill=LIGHT_TEXT, font=F_BODY)
    draw.text((430, 445), c4, fill=LIGHT_TEXT, font=F_BODY)

    draw.text((430, 495), "Contact: dhairyakhandelwal880@gmail.com  |  GitHub: @dhaiirryyaa", fill=GRAY_TEXT, font=F_TINY)

def render_tech_stack(img, draw, progress, frame_in_seg):
    """Scene 7: Technical architecture stack."""
    draw.text((100, 95), "SYSTEMS ARCHITECTURE & TECHNICAL STACK", fill=WHITE, font=F_TITLE)
    draw.text((100, 140), "Engineered for microsecond spatial lookups and ultra-low latency mobile telemetry", fill=GRAY_TEXT, font=F_BODY)

    stacks = [
        ("FASTAPI & PYTHON", "High-Concurrency Async Core", "Asynchronous ASGI backend handling high-volume driver telemetry & reservation locks.", CYAN_ACCENT),
        ("POSTGIS & SPATIAL DB", "Sub-15ms Spatial Indexing", "Geospatial KNN radius queries indexing micro-parking grounds in real time.", EMERALD_ACCENT),
        ("MAPLIBRE GL & PWA", "60 FPS Client Map Engine", "Offline-first PWA caching vector tiles and navigation even in concrete basements.", AMBER_ACCENT),
        ("TRACCAR & OSRM", "Live GPS Telemetry & Routing", "High-frequency 10 Hz vehicle telemetry tracking with optimal turn-by-turn routing.", CORAL_ACCENT),
    ]

    for i, (name, role, desc, col) in enumerate(stacks):
        x = 90 + i * 275
        y = 190
        w = 260
        h = 350
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([x + 16, y + 20, x + 80, y + 46], radius=6, fill=(24, 40, 70))
        draw.text((x + 28, y + 26), f"0{i+1}", fill=col, font=F_TINY_BOLD)

        draw.text((x + 16, y + 65), name, fill=WHITE, font=F_SUB)
        draw.text((x + 16, y + 95), role, fill=col, font=F_TINY_BOLD)

        draw.line([(x + 16, y + 125), (x + w - 16, y + 125)], fill=(35, 55, 90), width=1)

        words = desc.split()
        draw.text((x + 16, y + 145), " ".join(words[:4]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 16, y + 172), " ".join(words[4:8]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 16, y + 199), " ".join(words[8:12]), fill=LIGHT_TEXT, font=F_BODY)
        if len(words) > 12:
            draw.text((x + 16, y + 226), " ".join(words[12:]), fill=LIGHT_TEXT, font=F_BODY)

def render_spatial_engine(img, draw, progress, frame_in_seg):
    """Scene 8: Geospatial search engine pipeline."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=EMERALD_ACCENT, width=2)
    draw.text((140, 115), "GEOSPATIAL INGESTION & SEARCH ENGINE", fill=EMERALD_ACCENT, font=F_HEADING)
    draw.text((140, 150), "Multi-source map synthesis for unindexed urban micro-spaces", fill=GRAY_TEXT, font=F_BODY)

    steps = [
        ("1. INGESTION", "OpenStreetMap + Overture", "Extracts road network, building footprints, and off-street parking boundaries."),
        ("2. AI SCANNER", "1 km Spatial Radius", "Executes strict KD-tree proximity filters to find available micro-lots within 850m."),
        ("3. ROUTING & LOCK", "15-Min Guaranteed Hold", "Locks slot via Redis/DB and dispatches live turn-by-turn route to driver."),
    ]

    for i, (st_name, st_sub, st_desc) in enumerate(steps):
        sx = 140 + i * 320
        sy = 210
        sw = 300
        sh = 260
        draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=14, fill=(18, 30, 56), outline=CYAN_ACCENT, width=1)
        draw.text((sx + 20, sy + 25), st_name, fill=CYAN_ACCENT, font=F_SUB)
        draw.text((sx + 20, sy + 55), st_sub, fill=WHITE, font=F_BODY_BOLD)
        draw.line([(sx + 20, sy + 85), (sx + sw - 20, sy + 85)], fill=(40, 65, 105), width=1)

        words = st_desc.split()
        draw.text((sx + 20, sy + 105), " ".join(words[:5]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((sx + 20, sy + 132), " ".join(words[5:10]), fill=LIGHT_TEXT, font=F_BODY)
        if len(words) > 10:
            draw.text((sx + 20, sy + 159), " ".join(words[10:]), fill=LIGHT_TEXT, font=F_BODY)

    draw.rounded_rectangle([140, 495, 1140, 535], radius=8, fill=(24, 45, 80))
    draw.text((160, 506), "Benchmark: 12ms average response time across 10,000 synthetic high-density parking queries.", fill=WHITE, font=F_TINY_BOLD)

def render_core_team(img, draw, progress, frame_in_seg):
    """Scene 9: Core team disciplines."""
    draw.text((100, 95), "THE CORE TEAM DISCIPLINES", fill=WHITE, font=F_TITLE)
    draw.text((100, 140), "Complementary strengths purpose-built for high-density metropolitan mobility", fill=GRAY_TEXT, font=F_BODY)

    pillars = [
        ("SPATIAL SYSTEMS", "Lead: Dhairya", "Distributed infrastructure, routing engine, PostGIS spatial pipelines, and backend cloud API.", CYAN_ACCENT),
        ("COMPUTER VISION", "AI & Edge Verification", "Zero-hardware CCTV video stream inference to detect vacant slot occupancy accurately.", EMERALD_ACCENT),
        ("FLEET & CITY OPS", "Urban Operations", "Merchant & landowner onboarding for micro-plots (45-550 m²), compliance, and PWA UX.", AMBER_ACCENT),
    ]

    for i, (p_title, p_lead, p_desc, col) in enumerate(pillars):
        px = 90 + i * 370
        py = 190
        pw = 350
        ph = 350
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=18, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([px + 20, py + 25, px + 160, py + 55], radius=6, fill=(24, 40, 70))
        draw.text((px + 30, py + 33), f"PILLAR 0{i+1}", fill=col, font=F_TINY_BOLD)

        draw.text((px + 20, py + 80), p_title, fill=WHITE, font=F_SUB)
        draw.text((px + 20, py + 115), p_lead, fill=col, font=F_TINY_BOLD)

        draw.line([(px + 20, py + 145), (px + pw - 20, py + 145)], fill=(40, 65, 105), width=1)

        words = p_desc.split()
        draw.text((px + 20, py + 170), " ".join(words[:6]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((px + 20, py + 198), " ".join(words[6:12]), fill=LIGHT_TEXT, font=F_BODY)
        if len(words) > 12:
            draw.text((px + 20, py + 226), " ".join(words[12:]), fill=LIGHT_TEXT, font=F_BODY)

def render_paradox_intro(img, draw, progress, frame_in_seg):
    """Scene 10: The Bengaluru Paradox intro."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=AMBER_ACCENT, width=2)

    draw.text((cx - 280, 115), "THE URBAN PARKING PARADOX", fill=AMBER_ACCENT, font=F_TITLE)
    draw.text((cx - 320, 160), "Observed in Bengaluru (Indiranagar, Koramangala, MG Road)", fill=GRAY_TEXT, font=F_BODY)

    draw.rounded_rectangle([160, 210, 1120, 360], radius=16, fill=(20, 34, 60), outline=(50, 85, 140), width=1)
    q1 = '"While curbs are choked with double-parked vehicles,'
    q2 = 'there are vacant private plots and half-empty basements'
    q3 = 'just 300 meters away that drivers simply cannot see."'
    draw.text((cx - 290, 235), q1, fill=WHITE, font=F_HEADING)
    draw.text((cx - 330, 275), q2, fill=WHITE, font=F_HEADING)
    draw.text((cx - 300, 315), q3, fill=CYAN_ACCENT, font=F_HEADING)

    draw.text((cx - 330, 400), "The problem is NOT lack of physical asphalt in cities.", fill=CORAL_ACCENT, font=F_SUB)
    draw.text((cx - 365, 435), "The problem is INVISIBLE, UNINDEXED, DECENTRALIZED SUPPLY.", fill=EMERALD_ACCENT, font=F_HEADING)
    draw_pip_founder(img, draw)

def render_split_paradox(img, draw, progress, frame_in_seg):
    """Scene 11: Clogged arterial road vs hidden supply 300m away."""
    draw.rounded_rectangle([80, 80, 620, 560], radius=18, fill=CARD_BG, outline=CORAL_ACCENT, width=2)
    draw.text((110, 110), "WHAT DRIVERS SEE: CHOKED CURBS", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((110, 145), "Main High Streets & Arterials", fill=GRAY_TEXT, font=F_BODY)

    draw.rectangle([110, 190, 590, 360], fill=(25, 18, 25), outline=(70, 30, 45), width=1)
    for cy in [215, 275, 335]:
        draw.rectangle([130, cy - 12, 570, cy + 12], fill=(50, 20, 30))
        for cx in range(150, 560, 75):
            draw.rounded_rectangle([cx, cy - 8, cx + 55, cy + 8], radius=4, fill=CORAL_ACCENT)
            draw.text((cx + 12, cy - 6), "FULL", fill=WHITE, font=F_TINY_BOLD)

    draw.text((110, 390), "• 100% Street curb occupancy", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((110, 420), "• Illegal double-parking choking lanes", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((110, 450), "• 25+ min circling delay & road rage", fill=LIGHT_TEXT, font=F_BODY)

    # Right: Invisible Supply
    draw.rounded_rectangle([660, 80, 1200, 560], radius=18, fill=CARD_BG, outline=EMERALD_ACCENT, width=2)
    draw.text((690, 110), "WHAT OPENPARK UNLOCKS: HIDDEN BAYS", fill=EMERALD_ACCENT, font=F_HEADING)
    draw.text((690, 145), "300m Away (45 to 550 m² Micro-Pockets)", fill=GRAY_TEXT, font=F_BODY)

    plots = [
        ("Commercial Basement Bay", "8 Free Slots • Rs 40/hr", "220m from High St"),
        ("Vacant Micro-Ground (120m²)", "5 Free Slots • Rs 30/hr", "310m from High St"),
        ("Gated Institution Courtyard", "6 Free Slots • Rs 25/hr", "180m from High St"),
    ]

    for i, (p_name, p_slots, p_dist) in enumerate(plots):
        py = 190 + i * 90
        draw.rounded_rectangle([690, py, 1170, py + 75], radius=10, fill=(18, 38, 48), outline=EMERALD_ACCENT, width=1)
        draw.text((710, py + 14), p_name, fill=WHITE, font=F_SUB)
        draw.text((710, py + 42), p_slots, fill=EMERALD_ACCENT, font=F_TINY_BOLD)
        draw.text((1000, py + 26), p_dist, fill=CYAN_ACCENT, font=F_TINY_BOLD)

    draw.text((690, 480), "OpenPark bridges this gap through digital verification.", fill=WHITE, font=F_BODY_BOLD)

def render_barrier_flaw(img, draw, progress, frame_in_seg):
    """Scene 12: Why legacy hardware fails."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CORAL_ACCENT, width=2)
    draw.text((140, 115), "THE FLAW OF LEGACY PARKING HARDWARE", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((140, 150), "Why inductive sensors & boom barriers fail in developing metro cities", fill=GRAY_TEXT, font=F_BODY)

    draw.rounded_rectangle([140, 195, 1140, 310], radius=14, fill=(35, 18, 25), outline=CORAL_ACCENT, width=1)
    draw.text((160, 215), "CAPITAL EXPENDITURE: $15,000+ PER ENTRANCE GATE", fill=CORAL_ACCENT, font=F_SUB)
    draw.text((160, 245), "• Expensive boom-barriers require road trenching, continuous power, and constant repair.", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((160, 275), "• Unfeasible for 95% of small private grounds, church lots, or independent basements.", fill=LIGHT_TEXT, font=F_BODY)

    draw.rounded_rectangle([140, 335, 1140, 450], radius=14, fill=(24, 30, 50), outline=(50, 75, 120), width=1)
    draw.text((160, 355), "SLOW ONBOARDING & HARDWARE OBSOLESCENCE", fill=WHITE, font=F_SUB)
    draw.text((160, 385), "• Installation takes 6 to 12 weeks of municipal civil work.", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((160, 415), "• Loop sensors degrade quickly under heavy monsoon rains and road re-tarring.", fill=LIGHT_TEXT, font=F_BODY)

    draw.text((140, 480), "Result: Cities remain 90% uninstrumented, relying on chaotic manual gate attendants.", fill=GRAY_TEXT, font=F_BODY_BOLD)

def render_zero_hardware(img, draw, progress, frame_in_seg):
    """Scene 13: Zero-hardware thesis."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=EMERALD_ACCENT, width=2)

    draw.text((cx - 290, 115), "THE OPENPARK ANTIDOTE: ZERO-HARDWARE", fill=EMERALD_ACCENT, font=F_TITLE)
    draw.text((cx - 240, 160), "100% Software-First & Mobile PWA Infrastructure", fill=GRAY_TEXT, font=F_BODY)

    points = [
        ("5-MINUTE ONBOARDING", "Any landowner registers vacant micro-ground with zero upfront capex.", CYAN_ACCENT),
        ("OFFLINE-READY PWA", "Drivers reserve & navigate without needing app-store downloads or data signals.", EMERALD_ACCENT),
        ("AI COMPUTER VISION", "Existing security CCTVs turn into autonomous vacancy sensors.", AMBER_ACCENT),
    ]

    for i, (title, desc, col) in enumerate(points):
        y = 210 + i * 95
        draw.rounded_rectangle([160, y, 1120, y + 80], radius=12, fill=(18, 30, 55), outline=col, width=1)
        draw.text((185, y + 16), title, fill=col, font=F_SUB)
        draw.text((185, y + 44), desc, fill=LIGHT_TEXT, font=F_BODY)

    draw.text((cx - 300, 500), "Infinite scalability without laying a single meter of cable or concrete.", fill=WHITE, font=F_BODY_BOLD)

def render_solution_hero(img, draw, progress, frame_in_seg):
    """Scene 14: Solution hero card & live prototype announcement."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)

    draw.text((cx - 200, 115), "THE OPENPARK SOLUTION", fill=CYAN_ACCENT, font=F_TITLE)
    draw.text((cx - 320, 160), "An Open-Source, AI-Powered Smart Mobility Platform", fill=WHITE, font=F_HEADING)

    draw.rounded_rectangle([200, 220, 1080, 280], radius=30, fill=(24, 40, 75), outline=CYAN_ACCENT, width=2)
    draw.ellipse([225, 238, 255, 268], outline=GRAY_TEXT, width=2)
    draw.line([(248, 260), (258, 270)], fill=GRAY_TEXT, width=2)
    draw.text((275, 242), "Search destination (e.g. MG Road, Indiranagar, Taj Mahal)...", fill=WHITE, font=F_BODY)

    draw.rounded_rectangle([200, 310, 1080, 460], radius=16, fill=(15, 25, 45), outline=(40, 70, 115), width=1)
    draw.text((225, 330), "KEY SYSTEM CAPABILITIES LIVE TODAY:", fill=EMERALD_ACCENT, font=F_SUB)
    draw.text((225, 365), "1. 1 km AI Radius Scanner: Automatic micro-lot detection within 850m walking range.", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((225, 395), "2. 15-Minute Slot Hold: Guaranteed reservation eliminating destination arrival panic.", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((225, 425), "3. Turn-by-Turn GPS: Real-time Traccar telemetry with turn guidance directly to slot.", fill=LIGHT_TEXT, font=F_BODY)

    draw.text((cx - 280, 495), "LIVE DEMO: openpark-web-production.up.railway.app", fill=CYAN_ACCENT, font=F_SUB)

# ----------------- ENHANCED BENGALURU MAP ANIMATIONS -----------------

def render_bengaluru_map_advanced(draw, scan_angle=0, active_pin=None, show_route=False, route_pct=0.0):
    """
    Renders realistic vector map with:
    - Rotating radar sweep beam (360 degrees)
    - Concentric pulsing sonar rings
    - Spring bounce micro-parking pins
    - Animated photon pulse route line
    """
    map_x0, map_y0 = 100, 75
    map_w, map_h = 1080, 485
    map_x1, map_y1 = map_x0 + map_w, map_y0 + map_h

    # Base map background
    draw.rectangle([map_x0, map_y0, map_x1, map_y1], fill=(13, 20, 36))

    # Cubbon Park
    draw.polygon([
        (map_x0 + 40, map_y0 + 40),
        (map_x0 + 260, map_y0 + 50),
        (map_x0 + 220, map_y0 + 280),
        (map_x0 + 60, map_y0 + 240)
    ], fill=(18, 42, 38))
    draw.text((map_x0 + 80, map_y0 + 130), "CUBBON PARK", fill=(45, 95, 80), font=F_TINY_BOLD)

    # Street Grid
    mg_y = map_y0 + 260
    draw.line([(map_x0, mg_y), (map_x1, mg_y)], fill=(35, 55, 90), width=18)
    draw.line([(map_x0, mg_y), (map_x1, mg_y)], fill=(50, 75, 120), width=12)
    draw.text((map_x0 + 780, mg_y - 20), "MAHATMA GANDHI ROAD", fill=(100, 135, 185), font=F_TINY_BOLD)

    church_y = map_y0 + 180
    draw.line([(map_x0 + 200, church_y), (map_x1 - 100, church_y)], fill=(30, 45, 75), width=10)
    draw.text((map_x0 + 220, church_y - 16), "CHURCH STREET", fill=(80, 110, 155), font=F_TINY)

    res_y = map_y0 + 360
    draw.line([(map_x0, res_y), (map_x1, res_y)], fill=(30, 45, 75), width=12)
    draw.text((map_x0 + 780, res_y + 16), "RESIDENCY ROAD", fill=(80, 110, 155), font=F_TINY)

    brigade_x = map_x0 + 620
    draw.line([(brigade_x, map_y0), (brigade_x, map_y1)], fill=(35, 55, 90), width=16)
    draw.line([(brigade_x, map_y0), (brigade_x, map_y1)], fill=(50, 75, 120), width=10)
    draw.text((brigade_x + 12, map_y0 + 400), "BRIGADE ROAD", fill=(100, 135, 185), font=F_TINY_BOLD)

    museum_x = map_x0 + 380
    draw.line([(museum_x, map_y0 + 80), (museum_x, map_y1)], fill=(28, 42, 70), width=8)
    draw.text((museum_x + 10, map_y0 + 420), "MUSEUM ROAD", fill=(70, 95, 135), font=F_TINY)

    rest_y = map_y0 + 310
    draw.line([(museum_x, rest_y), (brigade_x, rest_y)], fill=(24, 36, 60), width=6)

    # Metro Station POI
    draw.rectangle([map_x0 + 650, mg_y + 15, map_x0 + 760, mg_y + 75], fill=(22, 34, 58), outline=(40, 65, 105), width=1)
    draw.text((map_x0 + 660, mg_y + 35), "MG Metro Stn", fill=GRAY_TEXT, font=F_TINY)

    # Center origin
    center_x = brigade_x - 120
    center_y = mg_y

    # Rotating Radar Sweep Needle & Sector
    if scan_angle is not None:
        sweep_radius = 280
        for r_step in [90, 180, 270]:
            draw.ellipse([center_x - r_step, center_y - r_step, center_x + r_step, center_y + r_step], outline=(20, 50, 80), width=1)

        fan_pts = [(center_x, center_y)]
        for a in range(int(scan_angle - 35), int(scan_angle)):
            rad = math.radians(a)
            fan_pts.append((center_x + sweep_radius * math.cos(rad), center_y + sweep_radius * math.sin(rad)))
        fan_pts.append((center_x, center_y))
        draw.polygon(fan_pts, fill=(6, 182, 212))

        lead_rad = math.radians(scan_angle)
        lead_x = center_x + sweep_radius * math.cos(lead_rad)
        lead_y = center_y + sweep_radius * math.sin(lead_rad)
        draw.line([(center_x, center_y), (lead_x, lead_y)], fill=CYAN_ACCENT, width=2)

    # Micro-Lots
    spots = [
        {"id": "p1", "name": "Church St Basement", "x": map_x0 + 440, "y": church_y - 2, "slots": 4, "rate": "Rs 30/hr"},
        {"id": "p2", "name": "Brigade Rd Micro-Ground", "x": brigade_x + 80, "y": map_y0 + 220, "slots": 6, "rate": "Rs 40/hr"},
        {"id": "p3", "name": "Rest House Rd Courtyard", "x": museum_x + 110, "y": rest_y - 2, "slots": 3, "rate": "Rs 25/hr"},
        {"id": "p4", "name": "Residency Micro-Bay", "x": map_x0 + 520, "y": res_y - 2, "slots": 8, "rate": "Rs 35/hr"},
    ]

    for sp in spots:
        is_active = (active_pin == sp["id"])
        pin_col = (34, 197, 94) if is_active else EMERALD_ACCENT
        if is_active:
            draw.ellipse([sp["x"] - 22, sp["y"] - 22, sp["x"] + 22, sp["y"] + 22], outline=pin_col, width=2)

        draw.ellipse([sp["x"] - 14, sp["y"] - 14, sp["x"] + 14, sp["y"] + 14], fill=pin_col, outline=WHITE, width=2)
        draw.text((sp["x"] - 5, sp["y"] - 9), "P", fill=WHITE, font=F_BODY_BOLD)

        badge_w = 175
        bx = sp["x"] + 20
        by = sp["y"] - 25
        draw.rounded_rectangle([bx, by, bx + badge_w, by + 46], radius=6, fill=(15, 26, 48), outline=pin_col, width=1)
        draw.text((bx + 8, by + 6), sp["name"], fill=WHITE, font=F_TINY_BOLD)
        draw.text((bx + 8, by + 24), f"{sp['slots']} Free • {sp['rate']}", fill=EMERALD_ACCENT, font=F_TINY)

    # Route polyline & moving vehicle
    if show_route:
        route_nodes = [
            (center_x, center_y),
            (brigade_x, mg_y),
            (brigade_x, church_y),
            (map_x0 + 440, church_y)
        ]

        segs = []
        tot_dist = 0.0
        for i in range(len(route_nodes) - 1):
            n1 = route_nodes[i]
            n2 = route_nodes[i+1]
            d = math.hypot(n2[0] - n1[0], n2[1] - n1[1])
            segs.append((n1, n2, d))
            tot_dist += d

        for n1, n2, _ in segs:
            draw.line([n1, n2], fill=(20, 80, 110), width=6)

        target_dist = tot_dist * route_pct
        accum = 0.0
        curr_pos = route_nodes[0]

        for n1, n2, d in segs:
            if accum + d <= target_dist:
                draw.line([n1, n2], fill=CYAN_ACCENT, width=6)
                accum += d
                curr_pos = n2
            else:
                rem = target_dist - accum
                if rem > 0:
                    f = rem / d
                    nx = n1[0] + (n2[0] - n1[0]) * f
                    ny = n1[1] + (n2[1] - n1[1]) * f
                    draw.line([n1, (nx, ny)], fill=CYAN_ACCENT, width=6)
                    curr_pos = (nx, ny)
                break

        vx, vy = int(curr_pos[0]), int(curr_pos[1])
        draw.ellipse([vx - 12, vy - 12, vx + 12, vy + 12], fill=WHITE, outline=CYAN_ACCENT, width=3)
        draw.text((vx - 5, vy - 7), "V", fill=(10, 20, 40), font=F_TINY_BOLD)

    # Driver Origin Marker
    draw.ellipse([center_x - 8, center_y - 8, center_x + 8, center_y + 8], fill=WHITE, outline=CORAL_ACCENT, width=2)
    draw.text((center_x - 20, center_y + 12), "Current Position", fill=LIGHT_TEXT, font=F_TINY_BOLD)

    draw.rectangle([map_x0, map_y0, map_x1, map_y1], outline=(40, 70, 115), width=2)

def render_map_scanner(img, draw, progress, frame_in_seg):
    """Scene 15: 1 km AI Space Scanner with 360-degree rotating radar sweep."""
    scan_angle = (frame_in_seg * 8) % 360
    render_bengaluru_map_advanced(draw, scan_angle=scan_angle)

    draw.rounded_rectangle([130, 95, 560, 165], radius=12, fill=(15, 25, 45), outline=CYAN_ACCENT, width=2)
    draw.text((150, 110), "1 KM AI SPACE SCANNER: ACTIVE", fill=CYAN_ACCENT, font=F_SUB)
    draw.text((150, 138), f"Sweep Angle: {int(scan_angle)}°  |  Indexed 4 Verified Micro-Grounds (850m)", fill=WHITE, font=F_TINY)
    draw_pip_founder(img, draw)

def render_map_lock(img, draw, progress, frame_in_seg):
    """Scene 16: 15-Minute Guaranteed Slot Lock."""
    render_bengaluru_map_advanced(draw, scan_angle=None, active_pin="p1")

    draw.rounded_rectangle([130, 95, 620, 195], radius=14, fill=(16, 32, 50), outline=EMERALD_ACCENT, width=2)
    draw.text((150, 110), "SLOT RESERVED & GUARANTEED", fill=EMERALD_ACCENT, font=F_HEADING)
    draw.text((150, 142), "Location: Church St Basement • Bay #B-03", fill=WHITE, font=F_BODY_BOLD)

    sec_left = max(0, int(900 - progress * 40))
    m = sec_left // 60
    s = sec_left % 60
    draw.text((150, 168), f"Hold Timer: {m:02d}:{s:02d} mins  |  Rate: Rs 30/hr  |  Zero Cruising", fill=AMBER_ACCENT, font=F_TINY_BOLD)
    draw_pip_founder(img, draw)

def render_map_routing(img, draw, progress, frame_in_seg):
    """Scene 17: Turn-by-Turn GPS Navigation polyline with animated vehicle."""
    route_pct = min(1.0, max(0.05, progress * 1.1))
    render_bengaluru_map_advanced(draw, scan_angle=None, active_pin="p1", show_route=True, route_pct=route_pct)

    draw.rounded_rectangle([130, 95, 660, 185], radius=14, fill=(14, 24, 45), outline=CYAN_ACCENT, width=2)
    draw.text((150, 110), "TURN RIGHT ONTO BRIGADE ROAD IN 120M", fill=WHITE, font=F_HEADING)
    eta_mins = max(1, int(4 - progress * 3))
    draw.text((150, 145), f"Distance: 550m  |  ETA: {eta_mins} mins  |  Telemetry: Traccar GPS (10 Hz)", fill=CYAN_ACCENT, font=F_BODY_BOLD)
    draw_pip_founder(img, draw)

# ----------------- ACT 5 SCENES -----------------

def render_pan_india(img, draw, progress, frame_in_seg):
    """Scene 18: Pan-India expansion roadmap."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)
    draw.text((140, 115), "OUR LONG-TERM VISION: ZERO-CRUISING INDIAN CITIES", fill=CYAN_ACCENT, font=F_TITLE)
    draw.text((140, 160), "Expanding the open-source decentralized micro-parking grid nationwide", fill=GRAY_TEXT, font=F_BODY)

    cities = [
        ("BENGALURU", "Phase 1 (Live Today)", "Indiranagar, Koramangala, MG Road micro-clusters.", EMERALD_ACCENT),
        ("MUMBAI METRO", "Phase 2 (Q2 2027)", "BKC, Lower Parel, Bandra commercial basements.", CYAN_ACCENT),
        ("DELHI NCR", "Phase 3 (Q3 2027)", "Connaught Place, Cyber City, Saket micro-grounds.", AMBER_ACCENT),
        ("HYDERABAD", "Phase 4 (Q4 2027)", "Hitec City & Gachibowli high-density corridors.", (168, 85, 247)),
    ]

    for i, (c_name, c_ph, c_desc, col) in enumerate(cities):
        cx = 140 + i * 255
        cy = 215
        cw = 240
        ch = 290
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=(18, 28, 52), outline=col, width=2)
        draw.text((cx + 16, cy + 25), f"STAGE 0{i+1}", fill=col, font=F_TINY_BOLD)
        draw.text((cx + 16, cy + 55), c_name, fill=WHITE, font=F_SUB)
        draw.text((cx + 16, cy + 85), c_ph, fill=col, font=F_TINY_BOLD)
        draw.line([(cx + 16, cy + 115), (cx + cw - 16, cy + 115)], fill=(35, 55, 90), width=1)

        words = c_desc.split()
        draw.text((cx + 16, cy + 135), " ".join(words[:4]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((cx + 16, cy + 162), " ".join(words[4:8]), fill=LIGHT_TEXT, font=F_BODY)
        if len(words) > 8:
            draw.text((cx + 16, cy + 189), " ".join(words[8:]), fill=LIGHT_TEXT, font=F_BODY)

def render_scale_grid(img, draw, progress, frame_in_seg):
    """Scene 19: 100,000+ Micro-Bays target."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=EMERALD_ACCENT, width=2)
    draw.text((140, 115), "TARGET SYSTEM IMPACT AT SCALE", fill=EMERALD_ACCENT, font=F_TITLE)
    draw.text((140, 160), "Unlocking private land supply into a unified municipal mobility grid", fill=GRAY_TEXT, font=F_BODY)

    metrics = [
        ("100,000+", "MICRO-BAYS DIGITIZED", "Aggregating private plots and commercial basements without city capex.", EMERALD_ACCENT),
        ("30% - 40%", "CRUISING TRAFFIC ELIMINATED", "Freeing up vital road capacity for buses, emergency vehicles, and transit.", CYAN_ACCENT),
        ("EV READY", "AUTONOMOUS DEPOT STAGING", "Intelligence layer guiding autonomous & electric fleets to charging hubs.", AMBER_ACCENT),
    ]

    for i, (top, mid, desc, col) in enumerate(metrics):
        x = 140 + i * 350
        y = 215
        w = 320
        h = 290
        draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=(18, 30, 56), outline=col, width=2)
        draw.text((x + 20, y + 25), top, fill=col, font=F_STAT_BIG)
        draw.text((x + 20, y + 85), mid, fill=WHITE, font=F_SUB)
        draw.line([(x + 20, y + 120), (x + w - 20, y + 120)], fill=(40, 65, 105), width=1)

        words = desc.split()
        draw.text((x + 20, y + 145), " ".join(words[:5]), fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 20, y + 172), " ".join(words[5:10]), fill=LIGHT_TEXT, font=F_BODY)
        if len(words) > 10:
            draw.text((x + 20, y + 199), " ".join(words[10:]), fill=LIGHT_TEXT, font=F_BODY)

def render_live_status(img, draw, progress, frame_in_seg):
    """Scene 20: Verified Live Prototype Status on Railway."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)
    draw.text((140, 115), "PRODUCTION STATUS & VERIFICATION", fill=CYAN_ACCENT, font=F_TITLE)
    draw.text((140, 160), "Live on Railway Cloud Infrastructure with 100% Passing Test Suites", fill=WHITE, font=F_HEADING)

    checks = [
        ("RAILWAY DEPLOYMENT", "SUCCESSFUL (Deployment ID: 458d7bde-0de7-4029)", "https://openpark-web-production.up.railway.app/app/", EMERALD_ACCENT),
        ("PYTEST TEST SUITE", "38 PASSED IN 0.81s", "100% test pass rate across geo-indexing, locks, routing, and PWA caches.", EMERALD_ACCENT),
        ("MAP GESTURE STABILITY", "DISCRIMINATION COOLDOWN 320ms", "Zero false clicks on pan/zoom; seamless high-density navigation.", CYAN_ACCENT),
    ]

    for i, (title, status, desc, col) in enumerate(checks):
        y = 215 + i * 95
        draw.rounded_rectangle([140, y, 1140, y + 80], radius=12, fill=(18, 30, 55), outline=col, width=1)
        draw.ellipse([165, y + 25, 177, y + 37], fill=col)
        draw.text((190, y + 20), title, fill=WHITE, font=F_SUB)
        draw.text((450, y + 22), status, fill=col, font=F_TINY_BOLD)
        draw.text((190, y + 48), desc, fill=LIGHT_TEXT, font=F_BODY)
    draw_pip_founder(img, draw)

def render_closing_hero(img, draw, progress, frame_in_seg):
    """Scene 21: Closing Founder Pitch Slide."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=EMERALD_ACCENT, width=3)

    draw.ellipse([cx - 45, 110, cx + 45, 200], fill=EMERALD_ACCENT)
    draw.text((cx - 15, 128), "P", fill=WHITE, font=get_font(48, bold=True))

    draw.text((cx - 150, 215), "OPENPARK", fill=WHITE, font=get_font(42, bold=True))
    draw.text((cx - 280, 275), "Eliminating Cruising Congestion in High-Density Indian Cities", fill=CYAN_ACCENT, font=F_HEADING)

    draw.line([(cx - 260, 320), (cx + 260, 320)], fill=(40, 70, 115), width=2)

    draw.text((cx - 180, 345), "Founder & Lead Architect: Dhairya", fill=WHITE, font=F_SUB)
    draw.text((cx - 210, 380), "Live Prototype: openpark-web-production.up.railway.app", fill=EMERALD_ACCENT, font=F_BODY_BOLD)
    draw.text((cx - 180, 415), "Email: dhairyakhandelwal880@gmail.com", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((cx - 150, 445), "GitHub: github.com/dhaiirryyaa/openpark", fill=GRAY_TEXT, font=F_BODY)

    draw.rounded_rectangle([cx - 220, 485, cx + 220, 525], radius=8, fill=(24, 48, 85), outline=EMERALD_ACCENT, width=1)
    draw.text((cx - 195, 496), "STAGE 1 CANDIDATE • READY FOR EVALUATION", fill=EMERALD_ACCENT, font=F_TINY_BOLD)
    draw_pip_founder(img, draw)

# Dispatch map
RENDERERS = {
    "title_intro": render_title_intro,
    "traffic_grid": render_traffic_grid,
    "circling_crawl": render_circling_crawl,
    "stat_35pct": render_stat_35pct,
    "macro_impact": render_macro_impact,
    "founder_profile": render_founder_profile,
    "tech_stack": render_tech_stack,
    "spatial_engine": render_spatial_engine,
    "core_team": render_core_team,
    "paradox_intro": render_paradox_intro,
    "split_paradox": render_split_paradox,
    "barrier_flaw": render_barrier_flaw,
    "zero_hardware": render_zero_hardware,
    "solution_hero": render_solution_hero,
    "map_scanner": render_map_scanner,
    "map_lock": render_map_lock,
    "map_routing": render_map_routing,
    "pan_india": render_pan_india,
    "scale_grid": render_scale_grid,
    "live_status": render_live_status,
    "closing_hero": render_closing_hero
}

def render_segment_frame(seg_info, frame_idx, total_frames):
    """Renders a single frame with geometric background, header, scene graphics, and kinetic subtitles."""
    seg = seg_info["seg"]
    seg_start = seg_info["start_frame"]
    seg_end = seg_info["end_frame"]
    seg_len = max(1, seg_end - seg_start)

    frame_in_seg = frame_idx - seg_start
    progress = frame_in_seg / float(seg_len)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Grid background
    grid_spacing = 40
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=(16, 26, 48), width=1)
    for y in range(0, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=(16, 26, 48), width=1)

    # Header
    draw_header(draw, seg["act"], seg["act_title"], seg["title"])

    # Scene Content
    render_func = RENDERERS.get(seg["type"], render_title_intro)
    render_func(img, draw, progress, frame_in_seg)

    # Kinetic Subtitles
    draw_kinetic_subtitles(draw, seg["tokens"], frame_idx, total_frames)

    return img

def render_video():
    """Main pipeline execution."""
    import imageio

    temp_dir = tempfile.mkdtemp(prefix="openpark_advanced_vid_")
    print(f"Working in temp directory: {temp_dir}")

    # 1. Synthesize Audio
    master_wav, segment_timings, total_frames, total_duration = synthesize_audio_tracks(temp_dir)

    # 2. Render Frames
    temp_video = os.path.join(temp_dir, "video_stream.mp4")
    print(f"Rendering {total_frames} frames ({total_duration:.2f}s) to video stream at {FPS} FPS...")

    writer = imageio.get_writer(
        temp_video,
        fps=FPS,
        codec="libx264",
        quality=8,
        pixelformat="yuv420p",
        ffmpeg_log_level="error"
    )

    current_seg_idx = 0
    num_segs = len(segment_timings)
    CROSSFADE_FRAMES = 10
    prev_frame_img = None

    for f in range(total_frames):
        while current_seg_idx < num_segs - 1 and f >= segment_timings[current_seg_idx]["end_frame"]:
            current_seg_idx += 1

        seg_info = segment_timings[current_seg_idx]
        frame_in_seg = f - seg_info["start_frame"]

        img = render_segment_frame(seg_info, f, total_frames)

        if frame_in_seg < CROSSFADE_FRAMES and current_seg_idx > 0 and prev_frame_img is not None:
            alpha = frame_in_seg / float(CROSSFADE_FRAMES)
            img = Image.blend(prev_frame_img, img, alpha)

        frame_np = np.array(img, dtype=np.uint8)
        writer.append_data(frame_np)
        prev_frame_img = img

        if f % 150 == 0 or f == total_frames - 1:
            pct = (f / float(total_frames)) * 100
            print(f"  Frame {f:04d}/{total_frames} ({pct:.1f}%) rendered...")

    writer.close()
    print("Video stream rendering complete.")

    # 3. Mux Video and Audio
    ffmpeg_exe = os.path.join(
        BASE_DIR, "backend/venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    )
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    os.makedirs(SUBMISSION_DIR, exist_ok=True)
    print(f"Muxing into final MP4: {OUTPUT_VIDEO}")
    cmd = [
        ffmpeg_exe, "-y",
        "-i", temp_video,
        "-i", master_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd, check=True)

    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"SUCCESS! Advanced Video created at: {OUTPUT_VIDEO}")
    print(f"Duration: {total_duration:.2f} seconds ({total_duration/60:.2f} mins)")
    print(f"Resolution: {WIDTH}x{HEIGHT} (16:9 720p HD)")
    print(f"File Size: {size_mb:.2f} MB")
    print(f"=======================================================\n")

if __name__ == "__main__":
    render_video()
