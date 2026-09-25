import requests
from PIL import Image, ImageDraw, ImageFont

GAS_URL = "https://script.google.com/macros/s/AKfycbw3fNeQEZluPDT4m3Pj-HtXL2wikqQEkYy65uPvu6QN4PDA7c357YIB6o2Ut8mIh33PJQ/exec" 

def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.replace('\n', ' ').split()
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip()) 
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def generate_image():
    try:
        resp = requests.get(GAS_URL).json()
        c2_text = resp.get("c2", "")
        d2_text = resp.get("d2", "")
    except Exception as e:
        c2_text = "Error fetching data"
        d2_text = str(e)

    # 0 = White background for ESP32 mapping
    img = Image.new('1', (800, 480), color=1)
    draw = ImageDraw.Draw(img)

    try:
        # We use a relative path now since it is in the same GitHub folder
        font_shloka = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", 42)
        font_meaning = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", 36)
    except Exception as e:
        print(f"Font error: {e}")
        font_shloka = font_meaning = ImageFont.load_default()

    # 1 = Black text/lines for ESP32 mapping
    draw.line((0, 240, 800, 240), fill=0, width=4)

    c2_lines = wrap_text(c2_text, font_shloka, 740, draw)
    total_height_c2 = len(c2_lines) * 60
    y = (240 - total_height_c2) // 2 
    for line in c2_lines:
        line_width = draw.textlength(line, font=font_shloka)
        x = (800 - line_width) // 2 
        draw.text((x, y), line, font=font_shloka, fill=0)
        y += 60 

    d2_lines = wrap_text(d2_text, font_meaning, 740, draw)
    total_height_d2 = len(d2_lines) * 50
    y = 240 + ((240 - total_height_d2) // 2) 
    for line in d2_lines:
        line_width = draw.textlength(line, font=font_meaning)
        x = (800 - line_width) // 2 
        draw.text((x, y), line, font=font_meaning, fill=0)
        y += 50

    # Save as a raw binary file instead of returning a web response
    with open("shloka.bin", "wb") as f:
        f.write(img.tobytes())

if __name__ == "__main__":
    generate_image()
