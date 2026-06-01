import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64

def get_image_base64(img):
    # 將圖片轉換為 Base64 字串，這是繞過 TypeError 的關鍵
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

def main():
    st.set_page_config(layout="wide")
    st.title("路西法智庫：天啟畫廊 (穩定版)")
    
    uploaded_file = st.file_uploader("上傳素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        # 開啟圖片並強制轉換為 RGB，統一格式
        img = Image.open(uploaded_file).convert("RGB")
        # 調整尺寸，確保畫布穩定
        img = img.resize((800, 600))
        bg_image_str = get_image_base64(img)

        # 模式選擇
        mode = st.selectbox("工具模式:", ["transform", "rect", "text"])
        
        # 穩定配置的畫布
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=2,
            stroke_color="#FF0000",
            background_image_url=bg_image_str,  # 使用 Base64 字串而非物件
            height=600,
            width=800,
            drawing_mode=mode,
            key="canvas",
        )
        
        if canvas_result.json_data is not None:
            st.success("畫布互動已啟用")
    else:
        st.warning("請上傳圖片。")

if __name__ == "__main__":
    main()
