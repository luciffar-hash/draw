import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 版本資訊
VERSION = "v0.1.1"

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

    # 使用 session_state 來保存上傳的圖片，防止重置
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

    # 1. 圖片上傳區塊
    uploaded_file = st.file_uploader("選擇一張原始圖檔 (作為禁書素材)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.session_state.uploaded_image = Image.open(uploaded_file)

    # 2. 編輯區塊
    if st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, caption="原始素材", use_column_width=True)
        
        user_text = st.text_input("輸入你想刻印的咒語 (文字)：", "在此輸入...")
        
        if st.button("進行顯影刻印"):
            # 建立副本進行處理
            img_editable = st.session_state.uploaded_image.copy()
            draw = ImageDraw.Draw(img_editable)
            
            # 簡單的文字繪製 (暫時使用預設字體)
            draw.text((20, 20), user_text, fill="white")
            
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
