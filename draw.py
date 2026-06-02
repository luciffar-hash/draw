# draw.py - v4.3.3.8 天啟畫廊 Streamlit 終極精準重置版
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import urllib.request

# 嘗試引入點擊座標組件，若未安裝則優雅降級
try:
    from streamlit_image_coordinates import streamlit_image_coordinates
    HAS_COORDINATES = True
except ImportError:
    HAS_COORDINATES = False

# 設定網頁標題與排版
st.set_page_config(page_title="天啟畫廊 網頁操控台", layout="wide")

# 1. 建立安全的底圖獲取機制
def get_current_image():
    """獲取當前底圖，若無則建立預設畫布"""
    if "base_image" in st.session_state and st.session_state.base_image is not None:
        return st.session_state.base_image.copy()
        
    input_path = "input.jpg"
    if os.path.exists(input_path):
        try:
            img = Image.open(input_path).convert("RGBA")
            st.session_state.base_image = img
            return img.copy()
        except Exception:
            pass
            
    return Image.new("RGBA", (800, 600), (40, 40, 40, 255))

# 先行取得真實底圖以得知基礎寬高
current_bg = get_current_image()
native_w, native_h = current_bg.width, current_bg.height

# 2. 初始化核心控制變數 (放在 state 中作為唯一真相來源)
if "val_x" not in st.session_state:
    st.session_state.val_x = int(native_w // 2)
if "val_y" not in st.session_state:
    st.session_state.val_y = int(native_h // 2)
if "val_rot" not in st.session_state:
    st.session_state.val_rot = 0

# 【核心修正】重置按鈕專用的回呼函式：直接動態讀取當前最真實的底圖寬高，絕不抓錯尺寸
def reset_coords():
    active_bg = get_current_image()
    st.session_state.val_x = int(active_bg.width // 2)
    st.session_state.val_y = int(active_bg.height // 2)
    st.session_state.val_rot = 0

@st.cache_data
def load_cloud_font(font_size):
    """從網路安全下載開源中文字體（思源黑體）"""
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

# --- 側邊控制面板 ---
with st.sidebar:
    # 置頂版號
    st.caption("⚙️ 系統版本號：#v4.3.3.8")
    st.title("🔮 天啟畫廊")
    st.markdown("---")
    
    # 檔案上傳
    uploaded_file = st.file_uploader("🖼️ 選擇更換自訂底圖 (JPG / PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        if "last_uploaded_name" not in st.session_state or uploaded_file.name != st.session_state.last_uploaded_name:
            new_img = Image.open(uploaded_file).convert("RGBA")
            st.session_state.base_image = new_img
            st.session_state.last_uploaded_name = uploaded_file.name
            st.session_state.val_x = int(new_img.width // 2)
            st.session_state.val_y = int(new_img.height // 2)
            st.rerun()

    # 文字輸入
    text_input = st.text_input("輸入文字内容:", value="貓貓abc")
    st.caption("💡 提示：換行請打 \\n")
    
    font_size = st.slider("字體大小 (px):", min_value=10, max_value=300, value=80)
    
    # 讀取與即時回寫，確保滑桿與底層變數百分之百同步
    rotation = st.slider("旋轉角度 (度):", min_value=-180, max_value=180, value=st.session_state.val_rot)
    st.session_state.val_rot = rotation
    
    pos_x = st.slider("水平位置 (X 軸):", min_value=0, max_value=native_w, value=st.session_state.val_x)
    st.session_state.val_x = pos_x
    
    pos_y = st.slider("垂直位置 (Y 軸):", min_value=0, max_value=native_h, value=st.session_state.val_y)
    st.session_state.val_y = pos_y

    # 紅色重置按鈕：綁定動態定位函式
    st.markdown(" ")
    st.button("↩ 重設定位與角度 (回正中央)", type="primary", use_container_width=True, on_click=reset_coords)

# --- 主預覽區域處理與合成 ---
font = load_cloud_font(font_size)
safe_text = str(text_input or "").replace("\\n", "\n")

# 計算文字大小邊界
temp_img = Image.new("RGBA", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.multiline_textbbox((0, 0), safe_text, font=font, align="center")
text_w = max(1, bbox[2] - bbox[0])
text_h = max(1, bbox[3] - bbox[1])

# 建立文字圖層並強制轉整數
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
rotated_text = text_layer.rotate(st.session_state.val_rot, resample=Image.Resampling.BICUBIC, expand=True)

# 合成圖片
final_image = Image.new("RGBA", current_bg.size)
final_image.paste(current_bg, (0, 0))

paste_x = int(st.session_state.val_x - (rotated_text.width / 2))
paste_y = int(st.session_state.val_y - (rotated_text.height / 2))
final_image.paste(rotated_text, (paste_x, paste_y), mask=rotated_text)

output_img = final_image.convert("RGB")

# --- 顯示預覽與點擊事件捕捉 ---
st.subheader("📷 即時預覽效果")
if HAS_COORDINATES:
    st.caption("💡 提示：除了拉桿，您也可以【直接點擊下方圖片】來改變文字位置！")
    # 捕捉圖片點擊座標
    value = streamlit_image_coordinates(output_img, key="gallery_canvas", use_column_width=True)
    
    if value is not None:
        clicked_x = int(value["x"])
        clicked_y = int(value["y"])
        
        # 點擊後直接更新真相來源變數，並觸發 rerun 重新渲染
        if clicked_x != st.session_state.val_x or clicked_y != st.session_state.val_y:
            st.session_state.val_x = max(0, min(native_w, clicked_x))
            st.session_state.val_y = max(0, min(native_h, clicked_y))
            st.rerun()
else:
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
