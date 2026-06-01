import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

# 版本資訊
VERSION = "v0.1.3"

def main():
    st.set_page_config(page_title="Luciffar AI: Apocalypse Gallery", page_icon="🎨", layout="wide")
    st.title("路西法智庫：天啟畫廊")
    st.subheader("Luciffar AI: Apocalypse Gallery")
    st.caption(f"版本號: {VERSION}")
    st.divider()

    uploaded_file = st.file_uploader("上傳禁書素材", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        w, h = img.size
        
        # 計算 1/5 大小的長方形
        rect_w, rect_h = w / 5, h / 5
        center_x, center_y = (w - rect_w) / 2, (h - rect_h) / 2

        st.write("在下方畫布操作，完成後點擊左側工具列的選取箭頭，即可拖動或調整長方形大小：")
        
        # 建立可繪圖畫布
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # 紅色半透明
            stroke_width=2,
            stroke_color="#FF0000",
            background_image=img,
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
            },
            height=h,
            width=w,
            drawing_mode="transform", # 允許拖動和變形
            key="canvas",
        )

        user_text = st.text_input("輸入你想刻印的咒語：", "AAA")

        if st.button("確認刻印 (產生最終圖)"):
            # 注意：此處僅為基礎演示，若要將畫布文字與圖片合成，需進一步解析 canvas_result.json_data
            st.success("長方形位置已記錄，請參照畫布預覽圖。")
            st.info("此版本已成功啟用畫布互動功能。")

    else:
        st.warning("請上傳圖片以開啟儀式。")

if __name__ == "__main__":
    main()
