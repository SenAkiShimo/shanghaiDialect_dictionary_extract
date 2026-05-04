import random
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import cv2

OUTPUT_DIR = "fake_dictionary_dataset"
if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

FONT_REG = "./Songti.ttf"
FONT_BOLD = "./Songti_bold.ttf"

WIDTH, HEIGHT = 1200, 1600
COL_WIDTH = 480
MARGIN = 80

def get_random_chinese(min_l, max_l):
    pool = "的一是了我不人在他有这个上们来到时大地为子中你说生国年着就那和要她出也得里后自以会家可下而过天去能对小多然于心学么之都好看起发当没成只如事把还用第样道想作种开美总从无情己面最女但现前些所同日手又行意动方期它头经长儿回位分爱老因很给名法间斯知世什两次使身者被高已亲其进此话常与活正感见明问力理尔点文几定本公特做外孩相西果走将月十实向声车全信重三机工物气每并别真打太新比才便夫再书部水像眼等体却加电主界门利海受听表德少克代员许稜先口由死安写性马光白或住难望教命花结乐色更拉东神记处让母父应直字场平报友关放至张认接告入笑内英军候民岁往何度山觉路带万男边风解叫任金快原吃妈变通师立象数四失满战远格士音轻目条呢病始达深完今提求清王化空业思切怎非找片罗钱紶吗语元喜曾离飞科言干流欢约各即指合反题必该论交终林请医晚制球决窢传画保读运及则房早院量苦火布品近坐产答星精视五连司巴奇管类未朋且婚台夜青北队久乎越观落尽形影红爸百令周吧识步希亚术留市半热送兴造谈容极随演收首根讲整式取照办强石古华諣拿计您装似足双妻尼转诉米称丽客南领节衣站黑刻统断福城故历惊脸选包紧争另建维绝树系伤示愿持千史谁准联妇纪基买志静阿诗独复痛消社算义竟确酒需单治卡幸兰念举仅钟怕共毛句息功官待究跟穿室易游程号居考突皮哪费倒价图具刚脑永歌响商礼细专黄块脚味灵改据般破引食仍存众注笔甚某沉血备习校默务土微娘须试怀料调广蜖苏显赛查密议底列富梦错座参八除跑亮假印设线温虽掉京初养香停际致阳纸李纳验助激够严证帝饭忘趣支春集丈木研班普导顿睡展跳获艺六波察群皇段急庭创区奥器谢弟店否害草排背止组州朝封睛板角况曲馆育忙质河续哥呼若推境遇雨标姐充围案伦护冷警贝著雪索剧啊船险烟依斗值帮汉慢佛肯闻唱沙局伯族低玩资屋击速顾泪洲团圣旁堂兵七露园牛哭旅街劳型烈姑陈莫鱼异抱宝权鲁简态级票怪寻杀律胜份汽右洋范床舞秘午登楼贵吸责例追较职属渐左录丝牙党继托赶章智冲叶胡吉卖坚喝肉遗救修松临藏担戏善卫药悲敢靠伊村戴词森耳差短祖云规窗散迷油旧适乡架恩投弹铁博雷府压超负勒杂醒洗采毫嘴毕九冰既状乱景席珍童顶派素脱农疑练野按犯拍征坏骨余承置臓彩灯巨琴免环姆暗换技翻束增忍餐洛塞缺忆判欧层付阵玛批岛项狗休懂武革良恶恋委拥娜妙探呀营退摇弄桌熟诺宣银势奖宫忽套康供优课鸟喊降夏困刘罪亡鞋健模败伴守挥鲜财孤枪禁恐伙杰迹妹藸遍盖副坦牌江顺秋萨菜划授归浪听凡预奶雄升碃编典袋莱含盛济蒙棋端腿招释介烧误"
    return "".join(random.choice(pool) for _ in range(random.randint(min_l, max_l)))

def generate_title(draw):
    style = random.randint(1, 3)
    title_text = get_random_chinese(2, 6)
    f_title = ImageFont.truetype(FONT_REG, 22)
    
    w_title = draw.textlength(title_text, font=f_title)

    rect_w = 1200
    rect_h = 40
    rect_x1 = (WIDTH - rect_w) // 2
    rect_y1 = random.randint(30, 45)
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h
    
    if random.random() < 0.8:
        draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=(235, 235, 235))
        if random.random() < 0.3:
            draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], outline=(200, 200, 200), width=1)

    text_x = rect_x1 + (rect_w - w_title) // 2
    text_y = rect_y1 + (rect_h - 26) // 2
    
    if style == 1:
        draw.text((text_x, text_y), title_text, font=f_title, fill=(50,50,50))
    elif style == 2:
        full_text = f"—— {title_text} ——"
        w_full = draw.textlength(full_text, font=f_title)
        draw.text(((WIDTH - w_full)//2, text_y), full_text, font=f_title, fill=(50,50,50))
    else:
        sections = ["一", "二", "三", "四", "五", "六"]
        full_text = f"{random.choice(sections)}、{title_text}"
        draw.text(((WIDTH - draw.textlength(full_text, f_title))//2, text_y), full_text, font=f_title, fill=(0,0,0))
    return [float(rect_x1), float(rect_y1), float(rect_x2), float(rect_y2)]

def generate_one_page(page_num):
    img_pil = Image.new('RGB', (WIDTH, HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img_pil)

    page_labels = []

    if random.random() > 0.15:
        title_box = generate_title(draw)
        page_labels.append({
            "class": 3, 
            "box": title_box
        })
    
    f_word = ImageFont.truetype(FONT_BOLD, 28)
    f_small = ImageFont.truetype(FONT_REG, 20)
    f_main = ImageFont.truetype(FONT_REG, 24)
    

    #if random.random() > 0.2:
    #    header = f"—— {get_random_chinese(2, 4)} {random.choice(['·', '|'])} 第 {page_num} 页 ——"
    #    draw.text((WIDTH//2 - 120, 40), header, font=f_small, fill=(100,100,100))
    #draw.text((WIDTH//2 - 10, HEIGHT - 70), str(page_num), font=f_main, fill=(50,50,50))
    #draw.line([(WIDTH//2, 80), (WIDTH//2, HEIGHT-80)], fill=(220, 220, 220), width=1)

    columns = [MARGIN, WIDTH // 2 + MARGIN // 2]
    for col_x in columns:
        current_y = 120
        while current_y < HEIGHT - 180:
            word = get_random_chinese(2, 4)
            ipa_len = random.randint(4, 10)
            ipa = "".join(random.choice("abcdefghijklm") for _ in range(ipa_len)) + str(random.randint(11, 55))
            if random.random() < 0.3: ipa = f"[{ipa}]"
            
            tag = random.choice(["〈名〉", "〈动〉", "〈形〉", "名", "动", "形", ""])
            
            r = random.random()
            if r < 0.15: m_len = 0 
            elif r < 0.45: m_len = random.randint(80, 200)
            else: m_len = random.randint(10, 40)
            
            meaning = tag + get_random_chinese(m_len//2, m_len) if m_len > 0 else ""

            entry_start_y = current_y
            
            draw.text((col_x, current_y), word, font=f_word, fill=(0,0,0))
            w_word = draw.textlength(word, font=f_word)
            page_labels.append({
                "class": 0, 
                "box": [col_x, current_y, col_x + w_word, current_y + 30]
                })
            
            ipa_x = col_x + w_word + 10
            draw.text((ipa_x, current_y + 4), ipa, font=f_small, fill=(60,60,60))
            w_ipa = draw.textlength(ipa, font=f_small)
            
            page_labels.append({
                "class": 1,
                "box": [ipa_x - 2, current_y, ipa_x + w_ipa + 2, current_y + 30]
            })

            content_to_draw = meaning
            is_first_line = True
            if content_to_draw:
                while len(content_to_draw) > 0:
                    start_x_off = w_word + w_ipa + 25 if is_first_line else 45
                    max_w = COL_WIDTH - start_x_off
                    line_text = ""
                    for char in content_to_draw:
                        if draw.textlength(line_text + char, font=f_main) <= max_w:
                            line_text += char
                        else:
                            break
                    
                    this_line_x = col_x + start_x_off
                    this_line_y = current_y + 2
                    
                    draw.text((this_line_x, this_line_y), line_text, font=f_main, fill=(0,0,0))
                    
                    w_line = draw.textlength(line_text, font=f_main)
                    page_labels.append({
                        "class": 2,
                        "box": [
                            float(this_line_x), 
                            float(this_line_y), 
                            float(this_line_x + w_line), 
                            float(this_line_y + 28)
                        ]
                    })
                    content_to_draw = content_to_draw[len(line_text):]
                    if len(content_to_draw) > 0:
                        current_y += 34
                        is_first_line = False

            entry_end_y = current_y + 32
            #page_labels.append({
            #    "class": 0,
            #    "box": [col_x - 4, entry_start_y - 2, col_x + COL_WIDTH + 4, entry_end_y + 2]
            #})
            
            current_y = entry_end_y + random.randint(10, 25)

    final_img = np.array(img_pil)

    angle = random.uniform(-2.0, 2.0)
    center = (WIDTH // 2, HEIGHT // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    final_img = cv2.warpAffine(final_img, M, (WIDTH, HEIGHT), borderValue=(255, 255, 255))

    if random.random() < 0.20:
        noise = np.random.randint(235, 256, (HEIGHT, WIDTH, 3), dtype='uint8')
        final_img = cv2.addWeighted(final_img, 0.9, noise, 0.1, 0)
        gauss = np.random.normal(0, 2, (HEIGHT, WIDTH, 3)).astype('uint8')
        final_img = cv2.add(final_img, gauss)

    rotated_labels = []
    for label in page_labels:
        box = label["box"]
        pts = np.array([
            [box[0], box[1]], # 左上
            [box[2], box[1]], # 右上
            [box[2], box[3]], # 右下
            [box[0], box[3]]  # 左下
        ])
        
        ones = np.ones(shape=(len(pts), 1))
        pts_ones = np.concatenate([pts, ones], axis=1)
        tr_pts = M.dot(pts_ones.T).T
        
        nx1, ny1 = tr_pts[:, 0].min(), tr_pts[:, 1].min()
        nx2, ny2 = tr_pts[:, 0].max(), tr_pts[:, 1].max()

        nx1 = max(0, min(WIDTH, nx1))
        nx2 = max(0, min(WIDTH, nx2))
        ny1 = max(0, min(HEIGHT, ny1))
        ny2 = max(0, min(HEIGHT, ny2))

        if (nx2 - nx1) < 2 or (ny2 - ny1) < 2:
            continue

        new_label = label.copy()
        new_label["box"] = [float(nx1), float(ny1), float(nx2), float(ny2)]
        rotated_labels.append(new_label)

    return final_img, rotated_labels

def default_converter(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

all_data = {}
for i in range(1, 2):
    img_array, labels = generate_one_page(i)
    cv2.imwrite(f"{OUTPUT_DIR}/page_{i}.jpg", img_array)
    all_data[f"page_{i}"] = labels 

with open(f"{OUTPUT_DIR}/labels.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2, default=default_converter)

print(f"模拟数据已生成。请查看 {OUTPUT_DIR} 文件夹。")
