import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

VERSION = "v0.2.1"

def main():
    st.set_page_config(page_title="Luciffar AI: Apocalypse Gallery", page_icon="🎨", layout="wide")
    st.title("路西法智庫：天啟畫廊")
    st.caption(f"版本號: {VERSION}")
    
    uploaded_file = st.file_uploader("上傳素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        # 核心修改：強制轉換為 RGBA 並在處理前處理色彩空間
        img = Image.open(uploaded_file).convert("RGBA")
        w, h = img.size
        
        col1, col2 = st.columns([2, 1])
        with col2:
            text_input = st.text_input("輸入文字：", "555555")
            rect_x = st.number_input("X 座標", value=int(w/2 - w/10))
            rect_y = st.number_input("Y 座標", value=int(h/2 - h/10))
            rect_w = st.number_input("寬度", value=int(w/5))
            rect_h = st.number_input("高度", value=int(h/5))
            font_size = st.slider("字體大小", 20, 500, 100)
            text_color = st.color_picker("文字顏色", "#FF0000")
            
            if st.button("生成最終畫作"):
                # 建立一個與原圖尺寸相同的畫布
                final_img = img.copy()
                draw = ImageDraw.Draw(final_img)
                
                # 字體載入邏輯：優先讀取 font.ttf，失敗則用系統預設
                try:
                    font = ImageFont.truetype("font.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # 直接在圖片上繪製文字 (不繪製框框)
                draw.text((rect_x, rect_y), text_input, fill=text_color, font=font)
                
                # 存回 session 並轉回 RGB 以便儲存為 PNG
                st.session_state.result_img = final_img.convert("RGB")
                st.success("繪製完成！")

        with col1:
            # 預覽邏輯
            preview_img = img.copy()
            draw_prev = ImageDraw.Draw(preview_img)
            draw_prev.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], outline="red", width=5)
            st.image(preview_img, caption="預覽 (紅框僅供定位參考)", use_column_width=True)
            
            if "result_img" in st.session_state:
                st.image(st.session_state.result_img, caption="最終輸出", use_column_width=True)
                buf = io.BytesIO()
                st.session_state.result_img.save(buf, format="PNG")
                st.download_button("下載畫作", data=buf.getvalue(), file_name="result.png")
    else:
        st.warning("請上傳圖片。")

if __name__ == "__main__":
    main()
