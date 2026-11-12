import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
GITHUB_URL = "https://github.com/your-username/spacex-falcon9-landing-prediction"

# Theme colors
COLOR_PRIMARY = RGBColor(26, 54, 93)     # #1A365D Dark Navy
COLOR_SECONDARY = RGBColor(43, 108, 176) # #2B6CB0 Accent Blue
COLOR_DARK_TEXT = RGBColor(45, 55, 72)   # #2D3748 Dark Gray
COLOR_LIGHT_BG = RGBColor(247, 250, 252) # #F7FAFC Soft Gray
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BORDER = RGBColor(226, 232, 240)

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text=None, github_url=None):
    # Header title box
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(7.5), Inches(1.2))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if category_text:
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_SECONDARY
        p_title = tf.add_paragraph()
    else:
        p_title = tf.paragraphs[0]

    p_title.text = title_text
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY

    # GitHub URL badge on the top right
    if github_url:
        badge_box = slide.shapes.add_textbox(Inches(8.2), Inches(0.4), Inches(4.3), Inches(0.8))
        btf = badge_box.text_frame
        btf.word_wrap = True
        btf.margin_left = btf.margin_top = btf.margin_right = btf.margin_bottom = 0
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.RIGHT
        bp.text = f"GitHub: {github_url}"
        bp.font.size = Pt(9)
        bp.font.color.rgb = COLOR_SECONDARY

def add_card(slide, left, top, width, height, title, items, bg_color=COLOR_WHITE, border_color=COLOR_BORDER):
    # Card shape
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)

    # Content
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(14)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY
    p_title.space_after = Pt(8)

    for item in items:
        p = tf.add_paragraph()
        p.text = f"- {item}"
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(4)

def add_image_slide(slide, title, category, img_path, left, top, width, height, bullets, github_url=None):
    add_header(slide, title, category, github_url)
    
    # Add Image preserving aspect ratio
    if os.path.exists(img_path):
        try:
            from PIL import Image
            with Image.open(img_path) as im:
                orig_w, orig_h = im.size
            aspect = orig_w / orig_h
            box_aspect = width / height
            if aspect > box_aspect:
                actual_w = width
                actual_h = width / aspect
            else:
                actual_h = height
                actual_w = height * aspect
            y_offset = top + (height - actual_h) / 2
            x_offset = left + (width - actual_w) / 2
            slide.shapes.add_picture(img_path, x_offset, y_offset, actual_w, actual_h)
        except Exception:
            slide.shapes.add_picture(img_path, left, top, width, height)
    
    # Add bullet card on the side
    card_left = left + width + Inches(0.4)
    card_width = Inches(12.5) - card_left
    if card_width > Inches(2.5):
        add_card(slide, card_left, top, card_width, height, "Key Insights & Analysis", bullets)
    else:
        add_card(slide, Inches(0.8), top + height + Inches(0.2), Inches(11.7), Inches(7.0) - (top + height), "Key Insights & Analysis", bullets)

