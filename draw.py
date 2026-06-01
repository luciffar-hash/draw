import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 版本資訊
VERSION = "v0.1.2"

def main():
    # 設定頁面配置
    st.set_page_config(
        page_title="Luciffar AI: Apocalypse Gallery",
        page_icon="🎨",
        layout="centered"
    )

    # 網站標題區塊
    st.title("路西法智庫：天啟畫廊")
    st.subheader("Luciffar AI: Apocalypse Gallery")
    st.caption(f"版本號: {VERSION}")
    
    st.divider()

    # 初始化 session_state
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

    # 1. 圖片上傳
    uploaded_file = st.file_uploader("選擇一張原始圖檔 (作為禁書素材)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.session_state.uploaded_image = Image.open(uploaded_file)

    # 2. 編輯區塊
    if st.session_state.uploaded_image:
        img_width, img_height = st.session_state.uploaded_image.size
        st.image(st.session_state.uploaded_image, caption=f"原始素材 (尺寸: {img_width}x{img_height})", use_column_width=True)
        
        # 文字設定欄位
        user_text = st.text_input("輸入你想刻印的咒語 (文字)：", "AAA")
        text_x = st.number_input("文字水平位置 (X)", value=50, min_value=0, max_value=img_width)
        text_y = st.number_input("文字垂直位置 (Y)", value=50, min_value=0, max_value=img_height)
        font_size = st.number_input("字體大小", value=40, min_value=10, max_value=200)
        text_color = st.color_picker("選擇文字顏色", "#FFFFFF") # 預設白色
        
        if st.button("進行顯影刻印"):
            # 建立副本進行處理
            img_editable = st.session_state.uploaded_image.copy()
            draw = ImageDraw.Draw(img_editable)
            
            # 嘗試載入字體，若失敗則使用預設
            try:
                # 注意：Streamlit Cloud 環境通常需要額外安裝中文字體檔案，
                # 若無特殊字體檔，這裡會使用預設字體
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # 繪製文字
            draw.text((text_x, text_y), user_text, fill=text_color, font=font)
            
            st.image(img_editable, caption="刻印完成的禁書頁面", use_column_width=True)
            
            # 提供下載
            buf = io.BytesIO()
            img_editable.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="下載此禁忌畫作",
                data=byte_im,
                file_name="apocalypse_art.png",
                mime="image/png"
            )
    else:
        st.warning("請先上傳一張圖片以開啟天啟儀式。")

if __name__ == "__main__":
    main()
