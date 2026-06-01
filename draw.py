import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 版本資訊
VERSION = "v0.1.7"

def main():
    st.set_page_config(page_title="Luciffar AI: Apocalypse Gallery", page_icon="🎨", layout="wide")
    st.title("路西法智庫：天啟畫廊")
    st.subheader("Luciffar AI: Apocalypse Gallery")
    st.caption(f"版本號: {VERSION}")
    st.divider()

    uploaded_file = st.file_uploader("上傳禁書素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        w, h = img.size
        
        # 預設長方形設定為 1/5
        default_rect_w = w / 5
        default_rect_h = h / 5
        default_x = (w - default_rect_w) / 2
        default_y = (h - default_rect_h) / 2

        col1, col2 = st.columns([2, 1])

        with col2:
            st.write("### 參數調整")
            text_input = st.text_input("輸入文字：", "AAA")
            rect_x = st.number_input("左上角 X 座標", value=int(default_x))
            rect_y = st.number_input("左上角 Y 座標", value=int(default_y))
            rect_w = st.number_input("框框寬度", value=int(default_rect_w))
            rect_h = st.number_input("框框高度", value=int(default_rect_h))
            font_size = st.slider("字體大小", 20, 200, 60)
            text_color = st.color_picker("選擇文字顏色", "#FF0000")
            
            if st.button("生成禁忌畫作"):
                img_draw = img.copy()
                draw = ImageDraw.Draw(img_draw)
                
                # 1. 畫出紅框
                draw.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], outline="red", width=5)
                
                # 2. 畫出文字 (嘗試載入預設字體)
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                draw.text((rect_x + 10, rect_y + 10), text_input, fill=text_color, font=font)
                
                st.session_state.result_img = img_draw
                st.success("繪製完成！")

        with col1:
            st.image(img, caption="原始禁書頁面", use_column_width=True)
            if "result_img" in st.session_state:
                st.image(st.session_state.result_img, caption="最終效果", use_column_width=True)
                
                buf = io.BytesIO()
                st.session_state.result_img.save(buf, format="PNG")
                st.download_button("下載此畫作", data=buf.getvalue(), file_name="result.png")

    else:
        st.warning("請先上傳圖片。")

if __name__ == "__main__":
    main()
