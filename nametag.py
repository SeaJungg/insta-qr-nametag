import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from math import ceil

# 설정
MM_TO_PX = lambda mm: int(mm * 11.811)  # 300dpi 기준
LABEL_WIDTH_MM, LABEL_HEIGHT_MM = 95, 64
LABEL_WIDTH_PX = MM_TO_PX(LABEL_WIDTH_MM)
LABEL_HEIGHT_PX = MM_TO_PX(LABEL_HEIGHT_MM)

A4_WIDTH_PX = MM_TO_PX(210)
A4_HEIGHT_PX = MM_TO_PX(297)

FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_SIZE = 200  # 이름을 크게 표시

# QR 코드 생성
def create_qr(instagram_id):
    url = f"https://instagram.com/{instagram_id}"
    qr_size = LABEL_HEIGHT_PX // 3  # 작은 QR (약 250px)
    qr = qrcode.make(url)
    return qr.resize((qr_size, qr_size))


# 이름표 생성 함수
def create_label(name, instagram_id, font):
    label = Image.new("RGB", (LABEL_WIDTH_PX, LABEL_HEIGHT_PX), "white")
    draw = ImageDraw.Draw(label)

    # 테두리
    draw.rectangle(
        [(0, 0), (LABEL_WIDTH_PX - 1, LABEL_HEIGHT_PX - 1)],
        outline="#CCCCCC",
        width=2
    )

    # QR 코드
    qr = create_qr(instagram_id)
    qr_x = LABEL_WIDTH_PX - qr.width - 20
    qr_y = (LABEL_HEIGHT_PX - qr.height) // 2
    label.paste(qr, (qr_x, qr_y))

    # 이름 텍스트
    LEFT_MARGIN = MM_TO_PX(5)
    name_text_size = draw.textbbox((0, 0), name, font=font)
    text_width = name_text_size[2] - name_text_size[0]
    text_height = name_text_size[3] - name_text_size[1]
    text_x = LEFT_MARGIN
    text_y = (LABEL_HEIGHT_PX - text_height) // 2
    draw.text((text_x, text_y), name, font=font, fill="black")

    return label



# PDF로 저장
def generate_name_tags_pdf(csv_path, output_pdf="name_tags_output.pdf"):
    df = pd.read_csv(csv_path)
    FONT_INDEX_FOR_BOLD = 2  # Apple SD Gothic Neo Bold

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE, index=FONT_INDEX_FOR_BOLD)

    labels_per_row = A4_WIDTH_PX // LABEL_WIDTH_PX
    labels_per_col = A4_HEIGHT_PX // LABEL_HEIGHT_PX
    labels_per_page = labels_per_row * labels_per_col

    pages = []
    for page_idx in range(ceil(len(df) / labels_per_page)):
        a4 = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")
        for i in range(labels_per_page):
            idx = page_idx * labels_per_page + i
            if idx >= len(df):
                break
            row = df.iloc[idx]
            name, instagram_id = str(row["성함"]), str(row["인스타그램ID"])

            label = create_label(name, instagram_id, font)

            row_idx = i // labels_per_row
            col_idx = i % labels_per_row
            x = col_idx * LABEL_WIDTH_PX
            y = row_idx * LABEL_HEIGHT_PX

            a4.paste(label, (x, y))
        pages.append(a4)

    # PDF 저장
    pages[0].save(output_pdf, "PDF", resolution=300, save_all=True, append_images=pages[1:])
    print(f"PDF 저장 완료: {output_pdf}")

# 실행 예시
generate_name_tags_pdf("이름표_데이터.csv")
