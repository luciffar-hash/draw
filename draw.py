import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import base64

# 版本資訊
VERSION = "v0.1.4"

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
        # 為了避免畫面過大，限制最大寬度
        max_width = 700
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        w, h = img.size
        
        # 計算 1/5 大小
        rect_w, rect_h = w / 5, h / 5
        center_x, center_y = (w - rect_w) / 2, (h - rect_h) / 2

        st.write("操作畫布以調整文字區塊：")
        
        # 轉換圖片為 base64 字串給畫布使用
        bg_image_str = get_image_base64(img)
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=2,
            stroke_color="#FF0000",
            background_image=None, # 不直接傳 img 物件
            data=None,
            height=h,
            width=w,
            drawing_mode="transform",
            key="canvas",
            background_image_url=bg_image_str, # 使用轉換過的 URL
            initial_drawing={
                "version": "4.4.0",
                "objects": [{
                    "type": "rect",
                    "left": center_x,
                    "top": center_y,
                    "width": rect_w,
                    "height": rect_h,
                    "fill": "rgba(255, 0, 0, 0.3)",
                    "stroke": "#FF0000",
                    "strokeWidth": 2
                }]
            }
        )

        st.info("畫布已載入，請進行調整。下一步我們將進行文字合成。")

    else:
        st.warning("請上傳圖片以開啟儀式。")

if __name__ == "__main__":
    main()
