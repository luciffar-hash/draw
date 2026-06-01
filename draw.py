import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64

def get_image_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

def main():
    st.set_page_config(layout="wide")
    st.title("路西法智庫：天啟畫廊 (互動版)")
    
    uploaded_file = st.file_uploader("上傳素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        # 強制將圖片統一縮放至 800x600，這是畫布穩定的關鍵
        img = Image.open(uploaded_file).convert("RGB").resize((800, 600))
        bg_image_str = get_image_base64(img)

        # 這裡設定互動模式
        drawing_mode = st.selectbox("選擇模式:", ("transform", "rect", "text"))
        
        # 建立畫布
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="#FF0000",
            background_image_url=bg_image_str,
            height=600,
            width=800,
            drawing_mode=drawing_mode,
            key="canvas",
        )
        
        if canvas_result.json_data is not None:
            st.info("畫布已就緒，您現在可以直接拖動畫面上的物件。")
    else:
        st.warning("請上傳圖片以開始繪製。")

if __name__ == "__main__":
    main()
