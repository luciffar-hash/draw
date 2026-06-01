import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

VERSION = "v0.3.0"

def main():
    st.set_page_config(page_title="路西法 AI 生成器", layout="wide")
    st.title("路西法 AI：天啟生成器")
    
    uploaded_file = st.file_uploader("上傳底圖", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        w, h = img.size
        
        # 使用側邊欄進行精確調整
        with st.sidebar:
            st.header("編輯參數")
            text = st.text_input("輸入文字", "大的要來了!")
            pos_x = st.slider("水平位置", 0, w, int(w/2))
            pos_y = st.slider("垂直位置", 0, h, int(h/2))
            font_size = st.slider("字體大小", 20, 200, 80)
            text_color = st.color_picker("文字顏色", "#FFFFFF")
            
        # 繪圖邏輯
        canvas = img.copy()
        draw = ImageDraw.Draw(canvas)
        
        # 載入字體 (若無自訂字體則使用預設)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
            
        draw.text((pos_x, pos_y), text, fill=text_color, font=font, anchor="mm")
        
        # 顯示結果
        st.image(canvas, use_column_width=True)
        
        # 下載按鈕
        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        st.download_button("下載此 Meme", buf.getvalue(), "meme.png", "image/png")
    else:
        st.info("請上傳圖片開始編輯。")

if __name__ == "__main__":
    main()
