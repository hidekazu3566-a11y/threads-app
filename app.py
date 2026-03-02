import streamlit as st

# 画面の設定
st.set_page_config(page_title="Threadsプロンプトメーカー", layout="centered")

# 見た目をオシャレにする設定
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 25px; background-color: #ff4b4b; color: white; font-weight: bold; border: none; height: 3.5em; }
    .step-header { background-color: #333; color: white; padding: 10px 20px; border-radius: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧵 Threads画像プロンプトメーカー")
st.write("ステップに沿って選ぶだけで、バズる画像プロンプトが完成！")

# --- STEP 1 ---
st.markdown('<div class="step-header">STEP 1. キャンバスの設定</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    use_case = st.selectbox("用途", ["Threads画像投稿", "YouTubeサムネイル", "インスタ投稿"])
with col2:
    aspect_ratio = st.selectbox("サイズ", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)"])

# --- STEP 2 ---
st.markdown('<div class="step-header">STEP 2. 内容を入力</div>', unsafe_allow_html=True)
subject = st.text_input("メインの被写体（例：カフェでパソコンを打つ猫）")
text_content = st.text_area("画像に入れる文字（例：AIで人生激変した方法）")

# --- STEP 3 ---
st.markdown('<div class="step-header">STEP 3. デザインの方向性</div>', unsafe_allow_html=True)
style = st.radio("テイスト", ["🎨 ほのぼの水彩画", "📊 スッキリ図解", "📸 エモい写真", "🎮 ゲーム風ドット絵"], horizontal=True)

st.divider()

# --- 生成ボタン ---
if st.button("🔥 オリジナル・プロンプトを錬成する"):
    if subject:
        prompt_json = f"""
{{
  "role": "Threads Creative Director",
  "content": {{
    "subject": "{subject}",
    "text": "{text_content}",
    "style": "{style}",
    "ratio": "{aspect_ratio}"
  }},
  "instruction": "Make it stand out on Threads feed. Text must be easy to read."
}}
        """
        st.success("✨ プロンプトが完成しました！")
        st.code(prompt_json, language="json")
        st.info("↑これをコピーしてGeminiに貼ってね！")
    else:
        st.error("被写体を入力してね！")