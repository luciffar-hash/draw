# draw.py - Streamlit 雲端生產環境專用版 (徹底修正浮點數尺寸錯誤與中文字體問題)
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import urllib.request

# 設定網頁標題與排版
st.set_page_config(page_title="Inkscape 仿製網頁操控台", layout="wide")

# 初始化 Session State，用來記憶使用者上傳的底圖
if "base_image" not in st.session_state:
    st.session_state.base_image = None

@st.cache_data
def load_cloud_font(font_size):
    """從網路安全下載開源中文字體（思源黑體），解決 Linux 雲端無中文細節問題"""
    font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf"
    font_path = "NotoSansCJKtc-Regular.otf"
    if not os.path.exists(font_path):
        try:
            with st.spinner("首次啟動，正在載入雲端中文字體..."):
                urllib.request.urlretrieve(font_url, font_path)
        except Exception:
            return ImageFont.load_default()
    try:
        return ImageFont.truetype(font_path, font_size)
    except Exception:
        return ImageFont.load_default()

def get_current_image():
    """獲取當前底圖，若無則建立預設畫布"""
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
            
    # 如果雲端沒有 input.jpg，自動生成一個 800x600 暗色畫布當背景
    return Image.new("RGBA", (800, 600), (40, 40, 40, 255))

# 取得當前底圖以計算寬高
current_bg = get_current_image()
native_w, native_h = current_bg.width, current_bg.height

# --- 側邊控制面板 ---
with st.sidebar:
    st.title("Inkscape 仿製工具")
    st.caption("版本號：v4.3.3.5 Streamlit 雲端抗震版")
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
    
    # 5. 水平與垂直位置
    pos_x = st.slider("水平位置 (X 軸):", min_value=0, max_value=native_w, value=native_w // 2)
    pos_y = st.slider("垂直位置 (Y 軸):", min_value=0, max_value=native_h, value=native_h // 2)

# --- 主預覽區域 ---
# 載入雲端安全中文字體
font = load_cloud_font(font_size)

# 處理換行符號
safe_text = str(text_input or "").replace("\\n", "\n")

# 計算文字大小邊界
temp_img = Image.new("RGBA", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.multiline_textbbox((0, 0), safe_text, font=font, align="center")
text_w = max(1, bbox[2] - bbox[0])
text_h = max(1, bbox[3] - bbox[1])

# 【核心修復】加上 int() 確保絕對是整數，阻絕浮點數導致的 TypeError 閃退
pad = int(max(text_w, text_h) * 0.6) + 150
text_layer_size = (int(text_w + pad), int(text_h + pad))

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

# 網路專用下載按鈕
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
