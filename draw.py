import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64

# 版本資訊
VERSION = "v0.1.5"

def get_image_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

def main():
    st.set_page_config(page_title="Luciffar AI: Apocalypse Gallery", page_icon="🎨", layout="wide")
    st.title("路西法智庫：天啟畫廊")
    st.subheader("Luciffar AI: Apocalypse Gallery")
    st.caption(f"版本號: {VERSION}")
    st.divider()

    uploaded_file = st.file_uploader("上傳禁書素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        
        # 限制大小以利顯示
        max_width = 600
        if img.width > max_width:
            ratio = max_width / float(img.width)
            img = img.resize((max_width, int(float(img.height) * ratio)), Image.Resampling.LANCZOS)
        
        w, h = img.size
        bg_image_str = get_image_base64(img)

        st.write("調整紅框位置與大小：")
        
        # 簡化參數配置，移除不必要的 data 與 background_image 參數
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=2,
            stroke_color="#FF0000",
            background_image_url=bg_image_str,
            height=h,
            width=w,
            drawing_mode="transform",
            key="canvas",
            initial_drawing={
                "version": "4.4.0",
                "objects": [{
                    "type": "rect",
                    "left": w/2 - (w/10),
                    "top": h/2 - (h/10),
                    "width": w/5,
                    "height": h/5,
                    "fill": "rgba(255, 0, 0, 0.3)",
                    "stroke": "#FF0000",
                    "strokeWidth": 2
                }]
            }
        )
        
        st.info("畫布已載入。")

    else:
        st.warning("請先上傳圖片。")

if __name__ == "__main__":
    main()
