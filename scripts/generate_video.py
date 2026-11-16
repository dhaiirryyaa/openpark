#!/usr/bin/env python3
"""
OpenPark — Founder Video Introduction Generator
Renders a professional 1080p/720p 16:9 MP4 presentation video with:
- Word-for-word voiceover narration synthesized via native high-fidelity TTS
- Dynamic map animations (radar scanner, POI popups, vehicle routing)
- Smooth crossfades and scene transitions
- Real-time synchronized captions and HUD overlays
- Founder & core team introduction, motivation, paradox, and vision
"""

import os
import sys
import math
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Set paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMISSION_DIR = os.path.join(BASE_DIR, "submission")
OUTPUT_VIDEO = os.path.join(SUBMISSION_DIR, "02_OpenPark_Founder_Video_Introduction.mp4")

# Resolution & Framerate
WIDTH = 1280
HEIGHT = 720
FPS = 30

# Colors (Obsidian / Emerald / Cyan / Coral Palette)
BG_DARK = (10, 15, 29)          # Deep obsidian blue
CARD_BG = (17, 28, 53)          # Dark navy glass card
CARD_BORDER = (30, 58, 95)      # Subdued border
CYAN_ACCENT = (6, 182, 212)     # #06b6d4
EMERALD_ACCENT = (16, 185, 129) # #10b981
CORAL_ACCENT = (244, 63, 94)    # #f43f5e
AMBER_ACCENT = (245, 158, 11)   # #f59e0b
WHITE = (255, 255, 255)
GRAY_TEXT = (148, 163, 184)
LIGHT_TEXT = (226, 232, 240)

# Fonts setup
FONT_REG_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_REG_PATH):
    FONT_REG_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size, bold=False):
    try:
        if bold and os.path.exists("/System/Library/Fonts/Supplemental/Arial Bold.ttf"):
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
        return ImageFont.truetype(FONT_REG_PATH, size)
    except Exception:
        return ImageFont.load_default()

# Preload fonts
F_TITLE = get_font(34, bold=True)
F_HEADING = get_font(24, bold=True)
F_SUB = get_font(18, bold=True)
F_BODY = get_font(15, bold=False)
F_BODY_BOLD = get_font(15, bold=True)
F_STAT_BIG = get_font(48, bold=True)
F_STAT_MED = get_font(28, bold=True)
F_CAPTION = get_font(18, bold=True)
F_TINY = get_font(12, bold=False)
F_TINY_BOLD = get_font(12, bold=True)

# 21 Structured Segments matching Master Script
SEGMENTS = [
    # Act 1: The Urban Mobility Crisis (Why This Problem Matters)
    {
        "id": "s01", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "Welcome to OpenPark",
        "text": "Namaste and hello everyone. Welcome to OpenPark.",
        "caption": "Namaste and hello everyone. Welcome to OpenPark.",
        "type": "title_intro"
    },
    {
        "id": "s02", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "The Daily Urban Commute Struggle",
        "text": "Picture this: you drive forty-five minutes to reach a meeting in Indiranagar or Connaught Place.",
        "caption": "Picture this: you drive 45 minutes to reach a meeting in Indiranagar or Connaught Place.",
        "type": "traffic_grid"
    },
    {
        "id": "s03", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "Cruising in Endless Circles",
        "text": "For the next twenty-five minutes, you crawl through bumper-to-bumper traffic, circling blocks hunting for parking.",
        "caption": "For the next 25 minutes, you crawl through traffic, circling blocks hunting for parking.",
        "type": "circling_crawl"
    },
    {
        "id": "s04", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "The Alarming Traffic Reality",
        "text": "In India's top metropolitan cities, thirty to forty percent of peak traffic is caused solely by vehicles cruising for parking.",
        "caption": "In India's metro cities, 30% to 40% of peak traffic is caused by vehicles searching for parking.",
        "type": "stat_35pct"
    },
    {
        "id": "s05", "act": 1, "act_title": "THE URBAN MOBILITY CRISIS",
        "title": "The Staggering Macro Cost",
        "text": "That equates to billions of rupees in wasted fuel, tons of toxic emissions, and countless lost hours every day.",
        "caption": "That equates to billions in wasted fuel, tons of toxic emissions, and countless lost hours daily.",
        "type": "macro_impact"
    },

    # Act 2: Founder & Core Team Introduction
    {
        "id": "s06", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "Founder Introduction",
        "text": "I am Dhairya, Founder and Lead Systems Architect of OpenPark.",
        "caption": "I am Dhairya, Founder and Lead Systems Architect of OpenPark.",
        "type": "founder_profile"
    },
    {
        "id": "s07", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "Engineering Background",
        "text": "My background is in full stack distributed systems, geospatial infrastructure, and cloud engineering.",
        "caption": "My background is in distributed systems, geospatial infrastructure, and cloud engineering.",
        "type": "tech_stack"
    },
    {
        "id": "s08", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "High-Performance Spatial Engines",
        "text": "Over the past year, I have built spatial routing engines combining OpenStreetMap, Overture Maps, and GPS telemetry.",
        "caption": "Over the past year, I've built spatial engines combining OpenStreetMap and GPS telemetry.",
        "type": "spatial_engine"
    },
    {
        "id": "s09", "act": 2, "act_title": "FOUNDER & CORE TEAM",
        "title": "Multidisciplinary Core Team",
        "text": "Beside me, our core team brings specialized experience across spatial data science, edge computer vision, and fleet operations.",
        "caption": "Our core team brings specialized experience across spatial AI, computer vision, and fleet ops.",
        "type": "core_team"
    },

    # Act 3: Motivation & The Urban Paradox
    {
        "id": "s10", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "The Bengaluru Paradox",
        "text": "Our motivation started from a profound paradox we noticed right here in Bengaluru.",
        "caption": "Our motivation started from a profound paradox we noticed right here in Bengaluru.",
        "type": "paradox_intro"
    },
    {
        "id": "s11", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "Clogged Roads vs. Invisible Supply",
        "text": "While street curbs are overflowing with chaotic double parking, hundreds of private basements and vacant micro-plots sit empty just three hundred meters away.",
        "caption": "While curbs overflow with double parking, private basements and micro-plots sit empty 300m away.",
        "type": "split_paradox"
    },
    {
        "id": "s12", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "The Hardware Boom-Barrier Trap",
        "text": "Legacy parking systems demand millions in proprietary boom barriers that Indian cities cannot afford to retrofit.",
        "caption": "Legacy systems demand millions in proprietary boom barriers Indian cities cannot retrofit.",
        "type": "barrier_flaw"
    },
    {
        "id": "s13", "act": 3, "act_title": "MOTIVATION & THE PARADOX",
        "title": "The Software-First Antidote",
        "text": "We knew there had to be a software-first, zero-hardware alternative.",
        "caption": "We knew there had to be a software-first, zero-hardware alternative.",
        "type": "zero_hardware"
    },

    # Act 4: The OpenPark Solution & Live Demo
    {
        "id": "s14", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "The OpenPark Platform",
        "text": "That is why we built OpenPark: an open-source, AI-powered smart mobility platform.",
        "caption": "That is why we built OpenPark: an open-source, AI-powered smart mobility platform.",
        "type": "solution_hero"
    },
    {
        "id": "s15", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "1 km AI Micro-Space Scanner",
        "text": "First, our strict one-kilometer AI Space Scanner dynamically indexes unindexed micro-pockets and commercial basements.",
        "caption": "First, our 1 km AI Space Scanner indexes unindexed micro-pockets and commercial basements.",
        "type": "map_scanner"
    },
    {
        "id": "s16", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "15-Minute Guaranteed Slot Lock",
        "text": "Second, our fifteen-minute reservation hold guarantees your spot before you arrive, eliminating full-lot uncertainty.",
        "caption": "Second, our 15-minute reservation hold guarantees your spot before you arrive.",
        "type": "map_lock"
    },
    {
        "id": "s17", "act": 4, "act_title": "SOLUTION & LIVE DEMO",
        "title": "Live Turn-by-Turn GPS Navigation",
        "text": "And third, live Traccar GPS telemetry and turn-by-turn routing guide drivers directly to their bay with full offline support.",
        "caption": "Third, live Traccar GPS telemetry and turn-by-turn routing guide drivers with full offline support.",
        "type": "map_routing"
    },

    # Act 5: Scaled Vision & Call to Action
    {
        "id": "s18", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "Eliminating Cruising Across India",
        "text": "Our long-term vision is bold: to eliminate cruising for parking across India.",
        "caption": "Our long-term vision is bold: to eliminate cruising for parking across India.",
        "type": "pan_india"
    },
    {
        "id": "s19", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "100,000+ Unified Micro-Bays",
        "text": "Expanding from Bengaluru to Mumbai, Delhi NCR, and Hyderabad, OpenPark will unlock over one hundred thousand hidden bays.",
        "caption": "Expanding to Mumbai, Delhi, and Hyderabad, OpenPark will unlock 100,000+ hidden bays.",
        "type": "scale_grid"
    },
    {
        "id": "s20", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "Verified Live Production Prototype",
        "text": "Our prototype is live on Railway today with thirty-eight passing verification test suites.",
        "caption": "Our prototype is live on Railway today with 38 passing verification test suites.",
        "type": "live_status"
    },
    {
        "id": "s21", "act": 5, "act_title": "VISION & CONCLUSION",
        "title": "Solving Congestion at the Root",
        "text": "We have the architectural clarity and the drive to solve urban congestion at its root. Thank you for considering OpenPark!",
        "caption": "We have the architectural clarity and drive to solve urban congestion. Thank you!",
        "type": "closing_hero"
    }
]

def synthesize_audio_tracks(temp_dir):
    """Synthesizes all speech segments using macOS say and concats them with ffmpeg."""
    ffmpeg_exe = os.path.join(
        BASE_DIR, "backend/venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    )
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    audio_files = []
    segment_timings = []
    current_time = 0.0

    print("Generating speech narration with Rishi (English (India))...")
    for i, seg in enumerate(SEGMENTS):
        aiff_path = os.path.join(temp_dir, f"{seg['id']}.aiff")
        wav_path = os.path.join(temp_dir, f"{seg['id']}.wav")

        # Synthesize using say
        subprocess.run(["/usr/bin/say", "-v", "Rishi (English (India))", "-r", "170", "-o", aiff_path, seg["text"]], check=True)

        # Convert to WAV with 0.15s silence padding at the end for natural breathing cadence
        pad_filter = "apad=pad_dur=0.15"
        subprocess.run([ffmpeg_exe, "-y", "-i", aiff_path, "-af", pad_filter, "-ar", "44100", "-ac", "2", wav_path], capture_output=True, check=True)

        # Measure exact duration
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
        print(f"  [{i+1}/{len(SEGMENTS)}] {seg['id']}: {dur:.2f}s | {seg['caption'][:40]}...")

    # Concatenate all audio files into master audio
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
    print(f"\nNarration Complete: Total Duration = {total_duration:.2f}s ({total_frames} frames @ {FPS} fps)\n")
    return master_wav, segment_timings, total_frames, total_duration

# Drawing helper functions
def draw_gradient_bg(draw, w, h):
    """Draws sleek obsidian gradient background with soft grid lines."""
    # Radial glow from center
    cx, cy = w // 2, h // 2
    # Base background
    draw.rectangle([0, 0, w, h], fill=BG_DARK)
    
    # Subtle geometric grid pattern
    grid_spacing = 40
    for x in range(0, w, grid_spacing):
        draw.line([(x, 0), (x, h)], fill=(16, 26, 48), width=1)
    for y in range(0, h, grid_spacing):
        draw.line([(0, y), (w, y)], fill=(16, 26, 48), width=1)

def draw_header(draw, act_num, act_title, seg_title):
    """Draws persistent header bar with logo, category, and live badge."""
    # Top bar background
    draw.rectangle([0, 0, WIDTH, 54], fill=(12, 19, 36))
    draw.line([(0, 54), (WIDTH, 54)], fill=(30, 48, 80), width=1)

    # OpenPark Logo
    draw.ellipse([24, 12, 54, 42], fill=EMERALD_ACCENT)
    draw.text((34, 15), "P", fill=WHITE, font=F_HEADING)
    draw.text((64, 16), "OPENPARK", fill=WHITE, font=F_HEADING)

    # Act Badge
    badge_x = 230
    draw.rounded_rectangle([badge_x, 14, badge_x + 310, 40], radius=6, fill=(20, 36, 68), outline=CYAN_ACCENT, width=1)
    act_str = f"ACT {act_num:02d} / 05 • {act_title}"
    draw.text((badge_x + 12, 19), act_str, fill=CYAN_ACCENT, font=F_TINY_BOLD)

    # Live Prototype Status Pill
    status_w = 260
    status_x = WIDTH - status_w - 24
    draw.rounded_rectangle([status_x, 14, status_x + status_w, 40], radius=13, fill=(15, 30, 55), outline=(40, 70, 110), width=1)
    # Pulsing green dot
    draw.ellipse([status_x + 12, 23, status_x + 20, 31], fill=EMERALD_ACCENT)
    draw.text((status_x + 28, 19), "LIVE: Railway Production", fill=LIGHT_TEXT, font=F_TINY_BOLD)

def draw_bottom_bar(draw, caption_text, current_frame, total_frames):
    """Draws floating subtitle pill with speaker tag and animated progress bar."""
    # Floating subtitle pill
    pill_w = 1120
    pill_h = 76
    pill_x = (WIDTH - pill_w) // 2
    pill_y = HEIGHT - pill_h - 22

    # Shadow
    draw.rounded_rectangle([pill_x + 3, pill_y + 3, pill_x + pill_w + 3, pill_y + pill_h + 3], radius=16, fill=(5, 8, 16))
    # Glass pill
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=16, fill=(15, 23, 42), outline=(45, 80, 130), width=2)

    # Speaker badge
    draw.rounded_rectangle([pill_x + 16, pill_y + 16, pill_x + 230, pill_y + 42], radius=6, fill=(24, 40, 75))
    draw.ellipse([pill_x + 26, pill_y + 25, pill_x + 34, pill_y + 33], fill=EMERALD_ACCENT)
    draw.text((pill_x + 42, pill_y + 22), "DHAIRYA (FOUNDER)", fill=CYAN_ACCENT, font=F_TINY_BOLD)

    # Subtitle Text (multi-line wrap if needed)
    draw.text((pill_x + 248, pill_y + 24), caption_text, fill=WHITE, font=F_CAPTION)

    # Bottom edge progress bar
    progress = min(1.0, max(0.0, current_frame / float(total_frames)))
    draw.rectangle([0, HEIGHT - 5, WIDTH, HEIGHT], fill=(20, 30, 50))
    bar_w = int(WIDTH * progress)
    if bar_w > 0:
        draw.rectangle([0, HEIGHT - 5, bar_w, HEIGHT], fill=EMERALD_ACCENT)

# ----------------- SCENE RENDERERS -----------------

def render_title_intro(draw, progress, frame_in_seg):
    """Scene 1: Grand Hero Title Card with dynamic pulsing grid."""
    cx, cy = WIDTH // 2, HEIGHT // 2 - 20

    # Glowing outer border card
    card_w, card_h = 920, 430
    x0, y0 = cx - card_w // 2, cy - card_h // 2
    draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=24, fill=(16, 26, 48), outline=CYAN_ACCENT, width=2)

    # Stage 1 Tag
    tag = "STAGE 1 FOUNDER VIDEO INTRODUCTION • DEMO DAY 2026"
    draw.rounded_rectangle([cx - 240, y0 + 35, cx + 240, y0 + 68], radius=8, fill=(24, 45, 82), outline=EMERALD_ACCENT, width=1)
    draw.text((cx - 215, y0 + 44), tag, fill=EMERALD_ACCENT, font=F_TINY_BOLD)

    # Title
    draw.text((cx - 220, y0 + 95), "OPENPARK", fill=WHITE, font=F_STAT_BIG)
    draw.text((cx - 310, y0 + 165), "AI-Powered Smart Mobility & Micro-Parking Network", fill=CYAN_ACCENT, font=F_HEADING)

    # Divider
    draw.line([(cx - 250, y0 + 215), (cx + 250, y0 + 215)], fill=(40, 70, 115), width=2)

    # Bullets
    b1 = "• 1 km AI Small-Ground & Basement Space Scanner"
    b2 = "• 15-Minute Guaranteed Slot Lock Reservation"
    b3 = "• Live Traccar GPS Telemetry & OSRM Routing Grid"
    draw.text((cx - 240, y0 + 240), b1, fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.text((cx - 240, y0 + 275), b2, fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.text((cx - 240, y0 + 310), b3, fill=LIGHT_TEXT, font=F_BODY_BOLD)

    # Founder byline
    draw.text((cx - 190, y0 + 365), "Founder: Dhairya  |  Bengaluru, India", fill=GRAY_TEXT, font=F_SUB)

def render_traffic_grid(draw, progress, frame_in_seg):
    """Scene 2: Bengaluru traffic congestion grid simulation."""
    # Left Card: Commute vs Search
    draw.rounded_rectangle([80, 80, 600, 560], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 110), "THE URBAN COMMUTE CRISIS", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((110, 145), "Bengaluru & Delhi NCR Metro Corridors", fill=GRAY_TEXT, font=F_BODY)

    # Timeline comparison bars
    # Segment 1: Drive to destination
    draw.text((110, 200), "Trip Phase 1: High-Speed Commute (Indiranagar)", fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.rounded_rectangle([110, 230, 560, 270], radius=8, fill=(25, 45, 80))
    draw.rounded_rectangle([110, 230, 450, 270], radius=8, fill=(34, 197, 94))
    draw.text((130, 242), "45 Minutes: 18 km Travel Distance (Smooth Arterial)", fill=WHITE, font=F_TINY_BOLD)

    # Segment 2: Parking Search Crawl
    draw.text((110, 310), "Trip Phase 2: Parking Search Cruising (Final 500m)", fill=CORAL_ACCENT, font=F_BODY_BOLD)
    draw.rounded_rectangle([110, 340, 560, 380], radius=8, fill=(25, 45, 80))
    crawl_w = int(110 + (450 - 110) * min(1.0, progress * 1.5))
    draw.rounded_rectangle([110, 340, crawl_w, 380], radius=8, fill=CORAL_ACCENT)
    draw.text((130, 352), "+25 Minutes: Crawling 4 Blocks (Zero Vacant Spots)", fill=WHITE, font=F_TINY_BOLD)

    # Summary
    draw.rounded_rectangle([110, 420, 560, 520], radius=12, fill=(35, 20, 30), outline=CORAL_ACCENT, width=1)
    draw.text((130, 435), "RESULT: TRIP TIME INFLATED BY +55%", fill=CORAL_ACCENT, font=F_SUB)
    draw.text((130, 465), "Drivers spend over a third of their journey in search panic,", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((130, 488), "burning fuel and choking arterial traffic corridors.", fill=LIGHT_TEXT, font=F_BODY)

    # Right Card: Traffic Simulation Grid
    draw.rounded_rectangle([630, 80, 1200, 560], radius=18, fill=(14, 22, 40), outline=CYAN_ACCENT, width=2)
    draw.text((660, 110), "SIMULATION: INDIRANAGAR 100 FT ROAD", fill=CYAN_ACCENT, font=F_HEADING)

    # Draw simulated road network
    # Main avenue
    draw.rectangle([680, 280, 1150, 340], fill=(25, 38, 65))
    draw.line([(680, 310), (1150, 310)], fill=(80, 100, 140), width=2)
    draw.text((690, 260), "Indiranagar 100 Feet Road (Congested Arterial)", fill=GRAY_TEXT, font=F_TINY)

    # Side streets
    draw.rectangle([780, 160, 830, 520], fill=(22, 32, 55))
    draw.rectangle([980, 160, 1030, 520], fill=(22, 32, 55))

    # Moving vehicles (dots)
    phase = (frame_in_seg % 60) / 60.0
    for idx, x_base in enumerate(range(700, 1140, 55)):
        vx = int(x_base + phase * 40) % 450 + 690
        # Color: red for cruising, amber for slowed
        col = CORAL_ACCENT if idx % 2 == 0 else AMBER_ACCENT
        draw.rounded_rectangle([vx, 292, vx + 22, 304], radius=3, fill=col)
        draw.rounded_rectangle([vx - 20, 316, vx + 2, 328], radius=3, fill=(100, 140, 200))

    # Cruising alert bubble
    draw.rounded_rectangle([820, 200, 1120, 255], radius=10, fill=(40, 15, 25), outline=CORAL_ACCENT, width=2)
    draw.text((835, 212), "CRUISING FOR PARKING DETECTED", fill=CORAL_ACCENT, font=F_TINY_BOLD)
    draw.text((835, 230), "Speed: 6 km/h  |  Delay: +25 mins", fill=WHITE, font=F_TINY)

def render_circling_crawl(draw, progress, frame_in_seg):
    """Scene 3: Endless block circling animation with HUD ticker."""
    # Left Card: Animated Block Loop
    draw.rounded_rectangle([80, 80, 680, 560], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 110), "THE CRUISING PARKING TRAP", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((110, 145), "Repetitive block circling without real-time vacancy data", fill=GRAY_TEXT, font=F_BODY)

    # City block representation
    bx0, by0 = 200, 200
    bw, bh = 360, 260
    draw.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=(18, 30, 52), outline=(40, 70, 110), width=3)
    draw.text((bx0 + 80, by0 + 115), "COMMERCIAL BLOCK", fill=(60, 95, 150), font=F_SUB)
    draw.text((bx0 + 105, by0 + 145), "All Curbs Full", fill=CORAL_ACCENT, font=F_TINY_BOLD)

    # Vehicle tracing the perimeter
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

    # Draw trail
    draw.rectangle([bx0 - 15, by0 - 15, bx0 + bw + 15, by0 + bh + 15], outline=(60, 30, 45), width=6)
    # Draw car
    draw.rounded_rectangle([car_x - 12, car_y - 12, car_x + 12, car_y + 12], radius=6, fill=CORAL_ACCENT, outline=WHITE, width=2)
    draw.text((car_x - 6, car_y - 8), "V", fill=WHITE, font=F_TINY_BOLD)

    # Right Card: Real-time telemetry ticker
    draw.rounded_rectangle([710, 80, 1200, 560], radius=18, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((740, 110), "DRIVER TELEMETRY IN SEARCH MODE", fill=WHITE, font=F_HEADING)

    blocks_circled = int(1 + progress * 5)
    fuel_wasted = 0.3 + progress * 0.9
    co2_emitted = 0.7 + progress * 2.1

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

def render_stat_35pct(draw, progress, frame_in_seg):
    """Scene 4: Huge 30-40% cruising traffic spotlight."""
    cx = WIDTH // 2

    # Giant Spotlight Card
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CORAL_ACCENT, width=3)

    draw.text((cx - 380, 115), "THE HIDDEN SOURCE OF METRO GRIDLOCK", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((cx - 320, 150), "Peer-reviewed urban transport data across India's top metros", fill=GRAY_TEXT, font=F_BODY)

    # Massive 30% - 40%
    draw.text((cx - 240, 195), "30% - 40%", fill=WHITE, font=get_font(72, bold=True))
    draw.text((cx - 390, 300), "OF ALL PEAK-HOUR TRAFFIC IS DRIVERS CRUISING FOR PARKING", fill=AMBER_ACCENT, font=F_HEADING)

    # Comparison Graphic
    # Bar 1: Cruising vehicles
    draw.text((160, 370), "Vehicles Traveling to Final Destination", fill=LIGHT_TEXT, font=F_BODY_BOLD)
    draw.rounded_rectangle([160, 395, 1120, 425], radius=6, fill=(24, 40, 70))
    draw.rounded_rectangle([160, 395, 760, 425], radius=6, fill=(59, 130, 246))
    draw.text((180, 402), "65% Commuters Moving Forward", fill=WHITE, font=F_TINY_BOLD)

    # Bar 2: Cruising load
    draw.text((160, 445), "Vehicles Ready to Park, but Crawling Street Blocks (The OpenPark Target)", fill=CORAL_ACCENT, font=F_BODY_BOLD)
    draw.rounded_rectangle([160, 470, 1120, 500], radius=6, fill=(24, 40, 70))
    draw.rounded_rectangle([160, 470, 540, 500], radius=6, fill=CORAL_ACCENT)
    draw.text((180, 477), "35% Cruising & Circling (Eliminated with OpenPark)", fill=WHITE, font=F_TINY_BOLD)

    draw.text((cx - 310, 520), "Eliminating this cruising load immediately unlocks 35% arterial capacity.", fill=EMERALD_ACCENT, font=F_BODY_BOLD)

def render_macro_impact(draw, progress, frame_in_seg):
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
        # Top pill
        draw.rounded_rectangle([x + 20, y + 25, x + 160, y + 55], radius=6, fill=(24, 38, 68))
        draw.text((x + 30, y + 33), f"IMPACT {i+1:02d}", fill=col, font=F_TINY_BOLD)

        draw.text((x + 20, y + 80), stat_top, fill=col, font=F_STAT_BIG)
        draw.text((x + 20, y + 145), stat_sub, fill=WHITE, font=F_SUB)

        draw.line([(x + 20, y + 185), (x + w - 20, y + 185)], fill=(40, 60, 95), width=1)

        # Word wrap desc
        words = desc.split()
        l1 = " ".join(words[:6])
        l2 = " ".join(words[6:12])
        l3 = " ".join(words[12:])
        draw.text((x + 20, y + 210), l1, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 20, y + 240), l2, fill=LIGHT_TEXT, font=F_BODY)
        if l3:
            draw.text((x + 20, y + 270), l3, fill=LIGHT_TEXT, font=F_BODY)

def render_founder_profile(draw, progress, frame_in_seg):
    """Scene 6: Founder card for Dhairya (Founder & Systems Architect)."""
    # Profile Card
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)

    # Left: Avatar / Badge
    draw.ellipse([160, 140, 340, 320], fill=(22, 45, 80), outline=EMERALD_ACCENT, width=4)
    # Monogram
    draw.text((220, 190), "DK", fill=WHITE, font=get_font(64, bold=True))
    draw.rounded_rectangle([180, 345, 320, 380], radius=8, fill=EMERALD_ACCENT)
    draw.text((205, 354), "FOUNDER", fill=WHITE, font=F_TINY_BOLD)

    # Right: Bio & Credentials
    draw.text((380, 130), "DHAIRYA", fill=WHITE, font=get_font(42, bold=True))
    draw.text((380, 185), "Founder & Lead Systems Architect • OpenPark", fill=CYAN_ACCENT, font=F_HEADING)

    # Badges
    badges = ["Distributed Spatial Systems", "PostGIS & Cloud Architecture", "Bengaluru, India"]
    bx = 380
    for b in badges:
        bw = len(b) * 9 + 24
        draw.rounded_rectangle([bx, 230, bx + bw, 262], radius=6, fill=(20, 40, 72), outline=(50, 80, 130), width=1)
        draw.text((bx + 12, 238), b, fill=LIGHT_TEXT, font=F_TINY_BOLD)
        bx += bw + 12

    draw.line([(380, 285), (1120, 285)], fill=(40, 65, 105), width=2)

    # Core Accomplishments
    draw.text((380, 310), "CORE CAPABILITIES & FOCUS:", fill=WHITE, font=F_SUB)
    c1 = "• Architected high-performance spatial routing and slot-indexing engines."
    c2 = "• Integrated OpenStreetMap, Overture Maps, and Traccar GPS telemetry pipeline."
    c3 = "• Shipped zero-hardware PWA architecture deployed on Railway with 38 verified tests."
    c4 = "• Dedicated to eliminating urban congestion through software-first infrastructure."

    draw.text((380, 345), c1, fill=LIGHT_TEXT, font=F_BODY)
    draw.text((380, 380), c2, fill=LIGHT_TEXT, font=F_BODY)
    draw.text((380, 415), c3, fill=LIGHT_TEXT, font=F_BODY)
    draw.text((380, 450), c4, fill=LIGHT_TEXT, font=F_BODY)

    # Contact footer
    draw.text((380, 500), "Contact: dhairyakhandelwal880@gmail.com  |  GitHub: @dhaiirryyaa", fill=GRAY_TEXT, font=F_TINY)

def render_tech_stack(draw, progress, frame_in_seg):
    """Scene 7: Technical architecture stack (FastAPI, PostGIS, MapLibre, Traccar)."""
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
        l1 = " ".join(words[:4])
        l2 = " ".join(words[4:8])
        l3 = " ".join(words[8:12])
        l4 = " ".join(words[12:])
        draw.text((x + 16, y + 145), l1, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 16, y + 172), l2, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 16, y + 199), l3, fill=LIGHT_TEXT, font=F_BODY)
        if l4:
            draw.text((x + 16, y + 226), l4, fill=LIGHT_TEXT, font=F_BODY)

def render_spatial_engine(draw, progress, frame_in_seg):
    """Scene 8: High-performance spatial engine pipeline."""
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=EMERALD_ACCENT, width=2)
    draw.text((140, 115), "GEOSPATIAL INGESTION & SEARCH ENGINE", fill=EMERALD_ACCENT, font=F_HEADING)
    draw.text((140, 150), "Multi-source map synthesis for unindexed urban micro-spaces", fill=GRAY_TEXT, font=F_BODY)

    # 3 Pipeline stages
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
        l1 = " ".join(words[:5])
        l2 = " ".join(words[5:10])
        l3 = " ".join(words[10:])
        draw.text((sx + 20, sy + 105), l1, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((sx + 20, sy + 132), l2, fill=LIGHT_TEXT, font=F_BODY)
        if l3:
            draw.text((sx + 20, sy + 159), l3, fill=LIGHT_TEXT, font=F_BODY)

    # Bottom status badge
    draw.rounded_rectangle([140, 495, 1140, 535], radius=8, fill=(24, 45, 80))
    draw.text((160, 506), "Benchmark: 12ms average response time across 10,000 synthetic high-density parking queries.", fill=WHITE, font=F_TINY_BOLD)

def render_core_team(draw, progress, frame_in_seg):
    """Scene 9: Core team capabilities and operational synergy."""
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
        l1 = " ".join(words[:6])
        l2 = " ".join(words[6:12])
        l3 = " ".join(words[12:])
        draw.text((px + 20, py + 170), l1, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((px + 20, py + 198), l2, fill=LIGHT_TEXT, font=F_BODY)
        if l3:
            draw.text((px + 20, py + 226), l3, fill=LIGHT_TEXT, font=F_BODY)

def render_paradox_intro(draw, progress, frame_in_seg):
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

def render_split_paradox(draw, progress, frame_in_seg):
    """Scene 11: Split screen showing clogged arterial road vs hidden supply 300m away."""
    # Left: Clogged Arterial
    draw.rounded_rectangle([80, 80, 620, 560], radius=18, fill=CARD_BG, outline=CORAL_ACCENT, width=2)
    draw.text((110, 110), "WHAT DRIVERS SEE: CHOKED CURBS", fill=CORAL_ACCENT, font=F_HEADING)
    draw.text((110, 145), "Main High Streets & Arterials", fill=GRAY_TEXT, font=F_BODY)

    draw.rectangle([110, 190, 590, 360], fill=(25, 18, 25), outline=(70, 30, 45), width=1)
    # Double parked cars representation
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

def render_barrier_flaw(draw, progress, frame_in_seg):
    """Scene 12: Why legacy hardware solutions fail."""
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

def render_zero_hardware(draw, progress, frame_in_seg):
    """Scene 13: OpenPark zero-hardware software-first thesis."""
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

def render_solution_hero(draw, progress, frame_in_seg):
    """Scene 14: Solution hero card & live prototype announcement."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=CYAN_ACCENT, width=2)

    draw.text((cx - 200, 115), "THE OPENPARK SOLUTION", fill=CYAN_ACCENT, font=F_TITLE)
    draw.text((cx - 320, 160), "An Open-Source, AI-Powered Smart Mobility Platform", fill=WHITE, font=F_HEADING)

    # Search bar preview
    draw.rounded_rectangle([200, 220, 1080, 280], radius=30, fill=(24, 40, 75), outline=CYAN_ACCENT, width=2)
    draw.ellipse([225, 238, 255, 268], outline=GRAY_TEXT, width=2)
    draw.line([(248, 260), (258, 270)], fill=GRAY_TEXT, width=2)
    draw.text((275, 242), "Search destination (e.g. MG Road, Indiranagar, Taj Mahal)...", fill=WHITE, font=F_BODY)

    # 3 Pillars banner
    draw.rounded_rectangle([200, 310, 1080, 460], radius=16, fill=(15, 25, 45), outline=(40, 70, 115), width=1)
    draw.text((225, 330), "KEY SYSTEM CAPABILITIES LIVE TODAY:", fill=EMERALD_ACCENT, font=F_SUB)
    draw.text((225, 365), "1. 1 km AI Radius Scanner: Automatic micro-lot detection within 850m walking range.", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((225, 395), "2. 15-Minute Slot Hold: Guaranteed reservation eliminating destination arrival panic.", fill=LIGHT_TEXT, font=F_BODY)
    draw.text((225, 425), "3. Turn-by-Turn GPS: Real-time Traccar telemetry with turn guidance directly to slot.", fill=LIGHT_TEXT, font=F_BODY)

    # Railway URL
    draw.text((cx - 280, 495), "LIVE DEMO: openpark-web-production.up.railway.app", fill=CYAN_ACCENT, font=F_SUB)

# ----------------- DETAILED BENGALURU MAP ANIMATIONS -----------------

def render_bengaluru_map_base(draw, scan_r=0, active_pin=None, show_route=False, route_pct=0.0):
    """Draws realistic dark-mode vector map centered on Bengaluru (MG Rd / Church St)."""
    # Map container
    map_x0, map_y0 = 100, 75
    map_w, map_h = 1080, 485
    map_x1, map_y1 = map_x0 + map_w, map_y0 + map_h

    # Base map background
    draw.rectangle([map_x0, map_y0, map_x1, map_y1], fill=(13, 20, 36))

    # Green Park Area (Cubbon Park)
    draw.polygon([
        (map_x0 + 40, map_y0 + 40),
        (map_x0 + 260, map_y0 + 50),
        (map_x0 + 220, map_y0 + 280),
        (map_x0 + 60, map_y0 + 240)
    ], fill=(18, 42, 38))
    draw.text((map_x0 + 80, map_y0 + 130), "CUBBON PARK", fill=(45, 95, 80), font=F_TINY_BOLD)

    # Street Network (Avenues and Crosses)
    # MG Road (Main horizontal arterial)
    mg_y = map_y0 + 260
    draw.line([(map_x0, mg_y), (map_x1, mg_y)], fill=(35, 55, 90), width=18)
    draw.line([(map_x0, mg_y), (map_x1, mg_y)], fill=(50, 75, 120), width=12)
    draw.text((map_x0 + 780, mg_y - 20), "MAHATMA GANDHI ROAD", fill=(100, 135, 185), font=F_TINY_BOLD)

    # Church Street (Parallel side street)
    church_y = map_y0 + 180
    draw.line([(map_x0 + 200, church_y), (map_x1 - 100, church_y)], fill=(30, 45, 75), width=10)
    draw.text((map_x0 + 220, church_y - 16), "CHURCH STREET", fill=(80, 110, 155), font=F_TINY)

    # Residency Road
    res_y = map_y0 + 360
    draw.line([(map_x0, res_y), (map_x1, res_y)], fill=(30, 45, 75), width=12)
    draw.text((map_x0 + 780, res_y + 16), "RESIDENCY ROAD", fill=(80, 110, 155), font=F_TINY)

    # Brigade Road (Vertical connecting avenue)
    brigade_x = map_x0 + 620
    draw.line([(brigade_x, map_y0), (brigade_x, map_y1)], fill=(35, 55, 90), width=16)
    draw.line([(brigade_x, map_y0), (brigade_x, map_y1)], fill=(50, 75, 120), width=10)
    draw.text((brigade_x + 12, map_y0 + 400), "BRIGADE ROAD", fill=(100, 135, 185), font=F_TINY_BOLD)

    # Museum Road (Vertical secondary)
    museum_x = map_x0 + 380
    draw.line([(museum_x, map_y0 + 80), (museum_x, map_y1)], fill=(28, 42, 70), width=8)
    draw.text((museum_x + 10, map_y0 + 420), "MUSEUM ROAD", fill=(70, 95, 135), font=F_TINY)

    # Rest House Road (Connecting lane)
    rest_y = map_y0 + 310
    draw.line([(museum_x, rest_y), (brigade_x, rest_y)], fill=(24, 36, 60), width=6)

    # Landmark POIs
    draw.rectangle([map_x0 + 650, mg_y + 15, map_x0 + 760, mg_y + 75], fill=(22, 34, 58), outline=(40, 65, 105), width=1)
    draw.text((map_x0 + 660, mg_y + 35), "MG Metro Stn", fill=GRAY_TEXT, font=F_TINY)

    # Center origin: User / Target Location (MG Road / Brigade corner)
    center_x = brigade_x - 120
    center_y = mg_y

    # If radar scanner active, draw expanding circle
    if scan_r > 0:
        # Outer ring
        draw.ellipse([center_x - scan_r, center_y - scan_r, center_x + scan_r, center_y + scan_r], outline=CYAN_ACCENT, width=2)
        # Inner glow ring
        inner_r = max(10, scan_r - 20)
        draw.ellipse([center_x - inner_r, center_y - inner_r, center_x + inner_r, center_y + inner_r], outline=(20, 90, 120), width=1)

    # Parking Spots (Micro-Lots)
    spots = [
        {"id": "p1", "name": "Church St Basement", "x": map_x0 + 440, "y": church_y - 2, "slots": 4, "rate": "Rs 30/hr", "dist": "340m"},
        {"id": "p2", "name": "Brigade Rd Micro-Ground", "x": brigade_x + 80, "y": map_y0 + 220, "slots": 6, "rate": "Rs 40/hr", "dist": "480m"},
        {"id": "p3", "name": "Rest House Rd Courtyard", "x": museum_x + 110, "y": rest_y - 2, "slots": 3, "rate": "Rs 25/hr", "dist": "260m"},
        {"id": "p4", "name": "Residency Micro-Bay", "x": map_x0 + 520, "y": res_y - 2, "slots": 8, "rate": "Rs 35/hr", "dist": "620m"},
    ]

    for sp in spots:
        dx = sp["x"] - center_x
        dy = sp["y"] - center_y
        dist_px = math.sqrt(dx * dx + dy * dy)

        # Show pin if scanner has reached it
        if scan_r == 0 or scan_r >= dist_px:
            is_active = (active_pin == sp["id"])
            pin_col = EMERALD_ACCENT if not is_active else (34, 197, 94)

            # Pin circle
            draw.ellipse([sp["x"] - 14, sp["y"] - 14, sp["x"] + 14, sp["y"] + 14], fill=pin_col, outline=WHITE, width=2)
            draw.text((sp["x"] - 5, sp["y"] - 9), "P", fill=WHITE, font=F_BODY_BOLD)

            # Info badge
            badge_w = 175
            bx = sp["x"] + 20
            by = sp["y"] - 25
            draw.rounded_rectangle([bx, by, bx + badge_w, by + 46], radius=6, fill=(15, 26, 48), outline=pin_col, width=1)
            draw.text((bx + 8, by + 6), sp["name"], fill=WHITE, font=F_TINY_BOLD)
            draw.text((bx + 8, by + 24), f"{sp['slots']} Free • {sp['rate']}", fill=EMERALD_ACCENT, font=F_TINY)

    # Draw Route Polyline if requested
    if show_route:
        # Route path: Driver origin on MG Road -> right onto Brigade -> left onto Church St -> into P1 (Church St Basement)
        route_nodes = [
            (center_x, center_y),                     # Start on MG Road
            (brigade_x, mg_y),                        # Intersection MG & Brigade
            (brigade_x, church_y),                    # Turn onto Church St
            (map_x0 + 440, church_y)                  # Arrive at P1
        ]

        # Calculate cumulative distances
        segs = []
        tot_dist = 0.0
        for i in range(len(route_nodes) - 1):
            n1 = route_nodes[i]
            n2 = route_nodes[i+1]
            d = math.hypot(n2[0] - n1[0], n2[1] - n1[1])
            segs.append((n1, n2, d))
            tot_dist += d

        # Draw full route trace in faint cyan
        for n1, n2, _ in segs:
            draw.line([n1, n2], fill=(20, 80, 110), width=6)

        # Draw animated active route segment based on route_pct
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

        # Draw vehicle icon at curr_pos
        vx, vy = int(curr_pos[0]), int(curr_pos[1])
        draw.ellipse([vx - 10, vy - 10, vx + 10, vy + 10], fill=WHITE, outline=CYAN_ACCENT, width=3)
        draw.text((vx - 4, vy - 6), "V", fill=(10, 20, 40), font=F_TINY_BOLD)

    # Driver Origin Marker
    draw.ellipse([center_x - 8, center_y - 8, center_x + 8, center_y + 8], fill=WHITE, outline=CORAL_ACCENT, width=2)
    draw.text((center_x - 20, center_y + 12), "Current Position", fill=LIGHT_TEXT, font=F_TINY_BOLD)

    # Border
    draw.rectangle([map_x0, map_y0, map_x1, map_y1], outline=(40, 70, 115), width=2)

def render_map_scanner(draw, progress, frame_in_seg):
    """Scene 15: 1 km AI Space Scanner animation with expanding radar wave."""
    # Expanding radar radius (cycles up to 340 pixels, representing ~1 km)
    scan_r = int((frame_in_seg * 6) % 360) + 30
    render_bengaluru_map_base(draw, scan_r=scan_r)

    # HUD Overlay: Scanner Active
    draw.rounded_rectangle([130, 95, 540, 165], radius=12, fill=(15, 25, 45), outline=CYAN_ACCENT, width=2)
    draw.text((150, 110), "1 KM AI SPACE SCANNER: ACTIVE", fill=CYAN_ACCENT, font=F_SUB)
    draw.text((150, 138), f"Radius: {int(scan_r * 2.8)}m  |  Indexed 4 Verified Micro-Grounds", fill=WHITE, font=F_TINY)

def render_map_lock(draw, progress, frame_in_seg):
    """Scene 16: 15-Minute Guaranteed Slot Lock animation."""
    render_bengaluru_map_base(draw, scan_r=400, active_pin="p1")

    # HUD Overlay: Slot Locked
    draw.rounded_rectangle([130, 95, 600, 195], radius=14, fill=(16, 32, 50), outline=EMERALD_ACCENT, width=2)
    draw.text((150, 110), "SLOT RESERVED & GUARANTEED", fill=EMERALD_ACCENT, font=F_HEADING)
    draw.text((150, 142), "Location: Church St Basement • Bay #B-03", fill=WHITE, font=F_BODY_BOLD)

    # Countdown timer
    sec_left = max(0, int(900 - progress * 40))
    m = sec_left // 60
    s = sec_left % 60
    draw.text((150, 168), f"Hold Timer: {m:02d}:{s:02d} mins  |  Rate: Rs 30/hr  |  Zero Cruising", fill=AMBER_ACCENT, font=F_TINY_BOLD)

def render_map_routing(draw, progress, frame_in_seg):
    """Scene 17: Turn-by-Turn GPS Navigation polyline animation."""
    route_pct = min(1.0, max(0.05, progress * 1.1))
    render_bengaluru_map_base(draw, scan_r=400, active_pin="p1", show_route=True, route_pct=route_pct)

    # Navigation HUD banner
    draw.rounded_rectangle([130, 95, 640, 185], radius=14, fill=(14, 24, 45), outline=CYAN_ACCENT, width=2)
    draw.text((150, 110), "TURN RIGHT ONTO BRIGADE ROAD IN 120M", fill=WHITE, font=F_HEADING)
    eta_mins = max(1, int(4 - progress * 3))
    draw.text((150, 145), f"Distance: 550m  |  ETA: {eta_mins} mins  |  Telemetry: Traccar GPS (10 Hz)", fill=CYAN_ACCENT, font=F_BODY_BOLD)

# ----------------- ACT 5 SCENES -----------------

def render_pan_india(draw, progress, frame_in_seg):
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
        l1 = " ".join(words[:4])
        l2 = " ".join(words[4:8])
        l3 = " ".join(words[8:])
        draw.text((cx + 16, cy + 135), l1, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((cx + 16, cy + 162), l2, fill=LIGHT_TEXT, font=F_BODY)
        if l3:
            draw.text((cx + 16, cy + 189), l3, fill=LIGHT_TEXT, font=F_BODY)

def render_scale_grid(draw, progress, frame_in_seg):
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
        l1 = " ".join(words[:5])
        l2 = " ".join(words[5:10])
        l3 = " ".join(words[10:])
        draw.text((x + 20, y + 145), l1, fill=LIGHT_TEXT, font=F_BODY)
        draw.text((x + 20, y + 172), l2, fill=LIGHT_TEXT, font=F_BODY)
        if l3:
            draw.text((x + 20, y + 199), l3, fill=LIGHT_TEXT, font=F_BODY)

def render_live_status(draw, progress, frame_in_seg):
    """Scene 20: Verified Live Prototype Status on Railway with 38 passing tests."""
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

def render_closing_hero(draw, progress, frame_in_seg):
    """Scene 21: Closing Founder Pitch Slide."""
    cx = WIDTH // 2
    draw.rounded_rectangle([100, 80, 1180, 560], radius=24, fill=CARD_BG, outline=EMERALD_ACCENT, width=3)

    # Logo
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
    """Renders a single frame for a specific segment."""
    seg = seg_info["seg"]
    seg_start = seg_info["start_frame"]
    seg_end = seg_info["end_frame"]
    seg_len = max(1, seg_end - seg_start)

    frame_in_seg = frame_idx - seg_start
    progress = frame_in_seg / float(seg_len)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Base background
    draw_gradient_bg(draw, WIDTH, HEIGHT)

    # Top Header
    draw_header(draw, seg["act"], seg["act_title"], seg["title"])

    # Scene Content
    render_func = RENDERERS.get(seg["type"], render_title_intro)
    render_func(draw, progress, frame_in_seg)

    # Bottom Subtitle & Progress Bar
    draw_bottom_bar(draw, seg["caption"], frame_idx, total_frames)

    return img

def render_video():
    """Main execution function to synthesize audio, render frames, and encode MP4."""
    import imageio

    temp_dir = tempfile.mkdtemp(prefix="openpark_vid_")
    print(f"Working in temp directory: {temp_dir}")

    # Step 1: Synthesize Audio
    master_wav, segment_timings, total_frames, total_duration = synthesize_audio_tracks(temp_dir)

    # Step 2: Render Frames to Temp Video
    temp_video = os.path.join(temp_dir, "video_stream.mp4")
    print(f"Encoding {total_frames} frames ({total_duration:.2f}s) to video stream at {FPS} FPS...")

    # We use imageio ffmpeg writer with high quality libx264
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

    CROSSFADE_FRAMES = 10  # 1/3 second smooth dissolve between segments

    prev_frame_img = None

    for f in range(total_frames):
        # Determine active segment
        while current_seg_idx < num_segs - 1 and f >= segment_timings[current_seg_idx]["end_frame"]:
            current_seg_idx += 1

        seg_info = segment_timings[current_seg_idx]
        frame_in_seg = f - seg_info["start_frame"]

        img = render_segment_frame(seg_info, f, total_frames)

        # Crossfade transition if near segment start
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

    # Step 3: Combine Video + Audio using ffmpeg
    ffmpeg_exe = os.path.join(
        BASE_DIR, "backend/venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
    )
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = "ffmpeg"

    os.makedirs(SUBMISSION_DIR, exist_ok=True)

    print(f"Muxing video and audio into final MP4: {OUTPUT_VIDEO}")
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
    print(f"SUCCESS! Video created at: {OUTPUT_VIDEO}")
    print(f"Duration: {total_duration:.2f} seconds ({total_duration/60:.2f} mins)")
    print(f"Resolution: {WIDTH}x{HEIGHT} (16:9 720p HD)")
    print(f"File Size: {size_mb:.2f} MB")
    print(f"=======================================================\n")

if __name__ == "__main__":
    render_video()
