# draw.py - Streamlit 雲端生產環境專用版 (解決字體與底圖缺失問題)
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# 設定網頁標題與排版
st.set_page_config(page_title="Inkscape 仿製網頁操控台", layout="wide")

# 初始化 Session State，用來記憶使用者上傳的底圖
if "base_image" not in st.session_state:
    st.session_state.base_image = None

def get_current_image():
    """獲取當前底圖，若無則建立預設畫布，確保雲端絕不噴錯"""
    if st.session_state.base_image is not None:
        return st.session_state.base_image.copy()
        
    input_path = "input.jpg"
    if os.path.exists(input_path):
        try:
            img = Image.open(input_path).convert("RGBA")
            st.session_state.base_image = img
            return img.copy()
        except Exception:
            pass
            
    # 如果雲端沒有 input.jpg，自動生成一個精美的 800x600 暗色畫布當背景，防止網頁死掉
    return Image.new("RGBA", (800, 600), (40, 40, 40, 255))

# 取得當前底圖以計算寬高
current_bg = get_current_image()
native_w, native_h = current_bg.width, current_bg.height

# --- 側邊控制面板 ---
with st.sidebar:
    st.title("Inkscape 仿製工具")
    st.caption("版本號：v4.3.3.4 Streamlit 雲端版")
    st.markdown("---")
    
    # 1. 點擊自選底圖
    uploaded_file = st.file_uploader("🖼️ 選擇更換自訂底圖 (JPG / PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        new_img = Image.open(uploaded_file).convert("RGBA")
        if st.session_state.base_image is None or st.session_state.base_image.size != new_img.size or uploaded_file.name != st.session_state.get("last_uploaded_name", ""):
            st.session_state.base_image = new_img
            st.session_state.last_uploaded_name = uploaded_file.name
            st.rerun()

    # 2. 輸入文字内容
    text_input = st.text_input("輸入文字内容:", value="貓貓abc")
    st.caption("💡 提示：換行請打 \\n")
    
    # 3. 字體大小
    font_size = st.slider("字體大小 (px):", min_value=10, max_value=300, value=80)
    
    # 4. 旋轉角度
    rotation = st.slider("旋轉角度 (度):", min_value=-180, max_value=180, value=0)
    
    # 5. 水平與垂直位置 (動態對應圖片寬高)
    pos_x = st.slider("水平位置 (X 軸):", min_value=0, max_value=native_w, value=native_w // 2)
    pos_y = st.slider("垂直位置 (Y 軸):", min_value=0, max_value=native_h, value=native_h // 2)

# --- 主預覽區域 ---
# 雲端字體安全相容邏輯：Linux 伺服器沒有 Windows 字體，若載入失敗自動切換為系統預設字體
try:
    font = ImageFont.truetype("C:\\Windows\\Fonts\\msjh.ttc", font_size)
except Exception:
    try:
        # 嘗試載入 Linux 雲端常見的預設字體
        font = ImageFont.load_default(size=font_size)
    except Exception:
        font = ImageFont.load_default()

safe_text = str(text_input or "").replace("\\n", "\n")

# 計算文字大小邊界
temp_img = Image.new("RGBA", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.multiline_textbbox((0, 0), safe_text, font=font, align="center")
text_w = max(1, bbox[2] - bbox[0])
text_h = max(1, bbox[3] - bbox[1])

# 建立文字圖層
pad = int(max(text_w, text_h) * 0.6) + 150
text_layer_size = (text_w + pad, text_h + pad)
text_layer = Image.new("RGBA", text_layer_size, (0, 0, 0, 0))
draw = ImageDraw.Draw(text_layer)

draw.multiline_text(
    (text_layer_size[0] // 2, text_layer_size[1] // 2),
    safe_text,
    font=font,
    fill=(255, 255, 255, 255),
    align="center",
    anchor="mm"
)

# 旋轉文字
rotated_text = text_layer.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)

# 合成底圖
final_image = Image.new("RGBA", current_bg.size)
final_image.paste(current_bg, (0, 0))

paste_x = int(pos_x - (rotated_text.width / 2))
paste_y = int(pos_y - (rotated_text.height / 2))
final_image.paste(rotated_text, (paste_x, paste_y), mask=rotated_text)

# 輸出 JPEG 格式
output_img = final_image.convert("RGB")

st.subheader("📷 即時預覽效果")
st.image(output_img, use_container_width=True)

st.markdown("---")

# 雲端下載優化：將儲存按鈕改成網路專用的「下載按鈕」，直接下載到使用者的電腦或手機裡！
buffered = BytesIO()
output_img.save(buffered, format="JPEG", quality=95)
img_bytes = buffered.getvalue()

st.download_button(
    label="📥 下載高品質產出檔 (output.jpg)",
    data=img_bytes,
    file_name="output.jpg",
    mime="image/jpeg",
    use_container_width=True
)
