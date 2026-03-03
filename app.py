import streamlit as st
import json

st.set_page_config(page_title="プロンプトメーカー 真・進化版", layout="centered")

st.title("🧵 プロンプトメーカー 真・進化版")
st.write("専門用語は不要！「どう見せたいか」を選ぶだけで、競合超えの最高な画像が作れるよ✨")

# --- 1. 基本設定 ---
st.header("1. 作りたい画像の設定")
col1, col2 = st.columns(2)
with col1:
    use_case = st.selectbox("用途", ["図解（SNS・プレゼン用）", "サムネイル（YouTube・記事用）", "Threads画像投稿", "Instagram投稿"])
with col2:
    ratio = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)"])

# --- 2. 伝える内容とキャラクター ---
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

# --- 3. 【新機能】感情トリガーとブランドカラー ---
st.header("3. 読者の感情とブランドカラー 🎨")
emotion = st.selectbox("読者にどうなってほしい？（感情トリガー）", [
    "💡「なるほど！」と思わず保存・メモしたくなる",
    "🥺 共感してウルっとくる・勇気が出る",
    "😂 クスッと笑える・ツッコミたくなる",
    "🔥 モチベ爆上がり！すぐに行動したくなる"
])

brand_color = st.text_input("あなたのテーマカラー（任意）", placeholder="例：淡いブルーとピンク、温かみのあるオレンジ系")

# --- 4. 【進化版】神・構図と画風 ---
st.header("4. デザインの方向性")
composition = st.selectbox("神・構図リスト（目的で選んでね！）", [
    "Zの法則（王道スタイル）：視線を左上から右下へ誘導。ストーリーっぽく読ませたい時に！",
    "左右分割（テキスト左・キャラ右）：箇条書きとか、情報をしっかり整理して読ませたい時に最強！",
    "中央ドカン！（放射・中央配置）：真ん中にキャラとタイトルを置いて、パッと見のインパクト重視！",
    "上下分割（タイトル上・キャラ下）：雑誌の表紙みたいに、上が見出しで下にドシッとキャラを置く安定スタイル。",
    "ビフォーアフター（変化で魅せる！）：過去と現在、NGとOKなど、2つを並べて違いをクッキリ見せたい時に！",
    "タイムライン（手順・流れ）：1→2→3のステップや歴史を順番に追って、スッキリ解説したい時に！"
])

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

# --- 🚀 プロンプト生成（命令書の錬成） ---
if st.button("🔥 競合越えのオリジナル・プロンプトを錬成する"):
    
    # ユーザーの使いやすさを極めた設定を、AIへの強力な指示に変換
    data_for_gemini = {
        "role": "Exclusive AI Creative Director",
        "objective": f"Generate a high-quality image for {use_case} that perfectly triggers this reader emotion: {emotion}",
        "format": "json",
        "design_concept": {
            "style": style,
            "composition_structure": composition,
            "brand_color_theme": brand_color if brand_color else "Match the chosen style perfectly",
            "aspect_ratio": ratio
        },
        "content": {
            "title": title,
            "details": details.split('\n') if details else [],
            # これまでの苦労の結晶！「キャラのアイデンティティは保つけど背景は一新する」指示
            "subject": "Use the attached image ONLY for the character's identity. Do NOT use the original background." if subject_type == "自分のキャラクターを使う（画像アップロード）" else subject_type
        },
        "instruction": "Make it stand out on social media. Follow the structure, color theme, and emotional goal exactly. Generate a completely NEW background and pose suitable for the concept. Keep the character consistent but give them a fresh context."
    }

    st.success("✨ 進化版プロンプトが完成したよ！")
    
    st.subheader("📋 これをコピーしてGeminiに貼ってね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
