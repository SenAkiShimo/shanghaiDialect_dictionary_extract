import random
import os
import json
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "fake_dictionary_dataset"
if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

WIDTH, HEIGHT = 1200, 1600
COL_WIDTH = 480
MARGIN = 80

# 模拟词性标签
TAGS = ["〈名〉", "〈动〉", "〈形〉", "〈副〉", "〈连〉", ""]

def get_random_chinese(min_l, max_l):
    pool = "的一是在不了有和人这中大来上个国得以说们到为最子上海话普通话阴阳天风雨雷电走跑跳看听吃喝东西南北"
    return "".join(random.choice(pool) for _ in range(random.randint(min_l, max_l)))

def generate_one_page(page_num):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    f_word = ImageFont.truetype(FONT_BOLD, 28)
    f_small = ImageFont.truetype(FONT_REG, 20)
    f_main = ImageFont.truetype(FONT_REG, 24)
    
    page_labels = []
    
    columns = [MARGIN, WIDTH // 2 + MARGIN // 2]
    
    for col_x in columns:
        current_y = 100
        while current_y < HEIGHT - 150:
            word = get_random_chinese(2, 4)
            ipa = "".join(random.choice("abcdefg") for _ in range(3)) + str(random.randint(11, 55))
            tag = random.choice(TAGS)
            meaning = tag + get_random_chinese(10, 25)
            
            draw.text((col_x, current_y), word, font=f_word, fill=(0,0,0))
            w_word = draw.textlength(word, font=f_word)
            
            draw.text((col_x + w_word + 8, current_y + 4), ipa, font=f_small, fill=(80,80,80))
            w_ipa = draw.textlength(ipa, font=f_small)
            
            content_start_x = col_x + w_word + w_ipa + 20
            remaining_w = (col_x + COL_WIDTH) - content_start_x
            
            first_line = ""
            second_line = ""
            for char in meaning:
                if draw.textlength(first_line + char, font=f_main) < remaining_w:
                    first_line += char
                else:
                    second_line += char
            
            draw.text((content_start_x, current_y + 2), first_line, font=f_main, fill=(0,0,0))
            
            entry_label = {"word": word, "meaning": meaning, "box": [col_x, current_y, col_x + COL_WIDTH, current_y + 30]}
            
            if second_line:
                current_y += 35
                draw.text((col_x + 30, current_y + 2), second_line, font=f_main, fill=(0,0,0))
                entry_label["box"][3] += 35
            
            page_labels.append(entry_label)
            current_y += 55
            
    draw.line([(WIDTH//2, 50), (WIDTH//2, HEIGHT-50)], fill=(200,200,200), width=1)
    draw.text((WIDTH//2 - 10, HEIGHT-60), str(page_num), font=f_main, fill=(0,0,0))
    
    img.save(f"{OUTPUT_DIR}/page_{page_num}.png")
    return page_labels

all_data = {}
for i in range(1, 501):
    all_data[f"page_{i}"] = generate_one_page(i)

with open(f"{OUTPUT_DIR}/labels.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"模拟数据已生成。请查看 {OUTPUT_DIR} 文件夹。")
