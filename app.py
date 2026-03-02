import streamlit as st
import json

st.set_page_config(page_title="画像生成プロンプトメーカー for Gemini", layout="centered")

st.title("🧵 画像生成プロンプトメーカー for Gemini")
st.write("キャラはキープ、背景は新しく！最高の命令書を錬成しよう！")

# --- 1. 作りたい画像の設定 ---
st.header("1. 作りたい画像の設定")
col1, col2 = st.columns(2)
with col1:
    use_case = st.selectbox("用途", ["サムネイル（YouTube・記事用）", "図解（SNS・プレゼン用）", "Threads画像投稿", "Instagram投稿"])
with col2:
    ratio = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)"])

# --- 2. 伝える内容と被写体 ---
st.header("2. 伝える内容と被写体")
title = st.text_input("タイトル・見出し（一番伝えたいこと）", placeholder="例：ファン化＝才能？")
details = st.text_area("内容の具体的なテキスト（詳細・箇条書きなど）", placeholder="①技術である\n②思想である\n③在り方である")

subject_type = st.selectbox("メインの被写体（キャラクター）", [
    "自分のキャラクターを使う（画像アップロード）",
    "入れない（キャラなし）",
    "AIに任せる"
])

if subject_type == "自分のキャラクターを使う（画像アップロード）":
    st.info("💡 生成する時、Geminiにキャラ画像を一緒に添付するのを忘れないでね！")

# --- 3. デザインの方向性 ---
st.header("3. デザインの方向性")
composition = st.selectbox("図解・構図の構造", ["Zの法則", "Fの法則", "左右分割", "中央配置"])

style = st.selectbox("メインテイスト（画風）", [
    "ほのぼの可愛い水彩画風",
    "かわい系（ちびキャラ・パステル）",
    "ビジネス系（誠実・青基調・信頼感）",
    "超リアルな実写写真",
    "おしゃれな3Dアニメ風",
    "レトロなフィルム写真風",
    "スタイリッシュなベクターアート",
    "エモい写真風",
    "ゲーム風ドット絵",
    "ネオンサイン系"
])

mood = st.select_slider("雰囲気のトーン", options=["ふんわり", "ナチュラル", "普通", "ドラマチック", "ビビッド"])

# --- 🚀 プロンプト生成（命令書の錬成） ---
if st.button("🔥 オリジナル・プロンプトを錬成する"):
    
    # 動画で成功していたJSON構造をベースに、背景とポーズを一新する指示を追加
    data_for_gemini = {
        "role": "Exclusive AI Creative Director",
        "objective": f"Generate a high-quality image for {use_case}",
        "format": "json",
        "design_concept": {
            "style": style,
            "composition_structure": composition,
            "mood_tone": mood,
            "aspect_ratio": ratio
        },
        "content": {
            "title": title,
            "details": details.split('\n') if details else [],
            # ここがポイント！「キャラには画像を使うけど、背景は元のを使わないで」と指示
            "subject": "Use the attached image ONLY for the character's identity. Do NOT use the original background." if subject_type == "自分のキャラクターを使う（画像アップロード）" else subject_type
        },
        # instructionにも「新しい背景とポーズを作って」と追加
        "instruction": "Make it stand out on social media. Follow the structure and style exactly. Generate a completely NEW background and pose suitable for the concept."
    }

    st.success("✨ プロンプトが完成したよ！")
    
    st.subheader("📋 これをコピーしてGeminiに貼ってね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
