import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

VERSION = "v0.1.9"

def main():
    st.set_page_config(page_title="Luciffar AI: Apocalypse Gallery", page_icon="🎨", layout="wide")
    st.title("路西法智庫：天啟畫廊")
    
    uploaded_file = st.file_uploader("上傳素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        # 不強制轉換模式，保持原圖格式
        img = Image.open(uploaded_file)
        w, h = img.size
        
        col1, col2 = st.columns([2, 1])
        with col2:
            text_input = st.text_input("輸入文字：", "AAA")
            rect_x = st.number_input("X 座標", value=int(w/2 - w/10))
            rect_y = st.number_input("Y 座標", value=int(h/2 - h/10))
            rect_w = st.number_input("寬度", value=int(w/5))
            rect_h = st.number_input("高度", value=int(h/5))
            font_size = st.slider("字體大小", 20, 500, 150)
            text_color = st.color_picker("文字顏色", "#FF0000")
            
            if st.button("生成最終畫作"):
                final_img = img.copy().convert("RGBA") # 確保支援透明度與色彩
                draw = ImageDraw.Draw(final_img)
                
                # 使用系統路徑載入字體 (Linux/Streamlit Cloud 常見路徑)
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                try:
                    font = ImageFont.truetype(font_path, font_size)
                except:
                    font = ImageFont.truetype("arial.ttf", font_size)
                
                draw.text((rect_x, rect_y), text_input, fill=text_color, font=font)
                st.session_state.result_img = final_img.convert("RGB")
                st.success("繪製完成！")

        with col1:
            preview_img = img.copy()
            draw_prev = ImageDraw.Draw(preview_img)
            draw_prev.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], outline="red", width=10)
            st.image(preview_img, caption="預覽 (紅框為參考範圍)", use_column_width=True)
            
            if "result_img" in st.session_state:
                st.image(st.session_state.result_img, caption="最終輸出結果", use_column_width=True)
                buf = io.BytesIO()
                st.session_state.result_img.save(buf, format="PNG", quality=100)
                st.download_button("下載此畫作", data=buf.getvalue(), file_name="result.png")

if __name__ == "__main__":
    main()
