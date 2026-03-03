import streamlit as st
import json

st.set_page_config(page_title="プロンプトメーカー 真・進化版", layout="centered")

st.title("🧵 プロンプトメーカー 真・進化版")
st.write("専門用語は不要！「どう見せたいか」を選ぶだけで、競合超えの最高な画像が作れるよ✨")

# --- 1. 基本設定（用途・サイズ・ジャンル・枚数） ---
st.header("1. 作りたい画像の設定")
col1, col2 = st.columns(2)
with col1:
    use_case = st.selectbox("用途", ["図解（SNS・プレゼン用）", "サムネイル（YouTube・記事用）", "Threads画像投稿", "Instagram投稿"])
with col2:
    ratio = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)"])

col3, col4 = st.columns(2)
with col3:
    # 競合の分かりにくいカルーセル表記をやめて、シンプルに枚数指定！
    num_images = st.selectbox("作成する画像の枚数", list(range(1, 11)))
with col4:
    # 競合の分かりやすいジャンル指定を追加！
    genre = st.selectbox("ターゲットジャンル・世界観", [
        "指定なし（おまかせ）",
        "1. 美容・コスメ（透明感・洗練）",
        "2. 健康・ダイエット（爽やか・活発）",
        "3. 恋愛・婚活（エモい・温かみ）",
        "4. 育児・ファミリー（優しい・柔らかい）",
        "5. スピリチュアル・占い（神秘的・宇宙）",
        "6. マネー・投資（知的・信頼感）",
        "7. ビジネス・自己啓発（スタイリッシュ・説得力）",
        "8. エンタメ・ゲーム（ポップ・派手）"
    ])

# --- 2. 伝える内容とキャラクター（枚数に合わせて入力欄が変化！） ---
st.header("2. 伝える内容と被写体")

content_list = []
# 選んだ枚数分だけ、自動で入力欄を作成する魔法のループ！
for i in range(num_images):
    # expanderを使って、画面が長くなりすぎないようにスッキリ見せる
    with st.expander(f"📝 {i+1}枚目のテキスト入力", expanded=(i==0)):
        img_title = st.text_input(f"タイトル・見出し", key=f"title_{i}", placeholder="例：ファン化＝才能？")
        img_details = st.text_area(f"具体的なテキスト（詳細・箇条書きなど）", key=f"details_{i}", placeholder="①技術である\n②思想である\n③在り方である")
        
        # データをリストに追加
        content_list.append({
            "slide_number": i+1,
            "title": img_title,
            "details": img_details.split('\n') if img_details else []
        })

subject_type = st.selectbox("メインの被写体（キャラクター）", [
    "自分のキャラクターを使う（画像アップロード）",
    "入れない（キャラなし）",
    "AIに任せる"
])

if subject_type == "自分のキャラクターを使う（画像アップロード）":
    st.info("💡 生成する時、Geminiにキャラ画像を一緒に添付するのを忘れないでね！")

# --- 3. 感情トリガーとブランドカラー ---
st.header("3. 読者の感情とブランドカラー 🎨")
emotion = st.selectbox("読者にどうなってほしい？（感情トリガー）", [
    "💡「なるほど！」と思わず保存・メモしたくなる",
    "🥺 共感してウルっとくる・勇気が出る",
    "😂 クスッと笑える・ツッコミたくなる",
    "🔥 モチベ爆上がり！すぐに行動したくなる"
])

# 任意入力！空欄ならAIが空気を読んでくれる
brand_color = st.text_input("あなたのテーマカラー（任意）", placeholder="例：淡いブルーとピンク（空欄ならジャンルに合わせてAIが自動選択！）")

# --- 4. 神・構図と画風 ---
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
    "エモい写真風",
    "ゲーム風ドット絵",
    "ネオンサイン系"
])

# --- 🚀 プロンプト生成（命令書の錬成） ---
if st.button("🔥 競合越えのオリジナル・プロンプトを錬成する"):
    
    # カラーが空欄だった場合、AIに「ジャンルと感情に合わせて最高のカラーを自動で選んで！」と指示する
    auto_color_prompt = f"Auto-select the most effective and visually appealing color palette suitable for the '{genre}' genre and the emotional goal '{emotion}'."
    final_color = brand_color if brand_color else auto_color_prompt

    data_for_gemini = {
        "role": "Exclusive AI Creative Director",
        "objective": f"Generate {num_images} high-quality images for {use_case} that perfectly triggers this reader emotion: {emotion}",
        "format": "json",
        "design_concept": {
            "genre_worldview": genre,
            "style": style,
            "composition_structure": composition,
            "brand_color_theme": final_color,
            "aspect_ratio": ratio
        },
        "content_per_image": content_list, # ここに1〜10枚目までの全テキストデータが入る！
        "subject_management": "Use the attached image ONLY for the character's identity. Do NOT use the original background." if subject_type == "自分のキャラクターを使う（画像アップロード）" else subject_type,
        "instruction": f"Generate a total of {num_images} distinct images. For each image, strictly follow the provided text content, maintaining visual consistency across all images. Make them stand out on social media. Generate completely NEW backgrounds and poses suitable for the concepts. Keep the character consistent but give them fresh contexts for each slide."
    }

    st.success(f"✨ {num_images}枚分の進化版プロンプトが完成したよ！")
    
    st.subheader("📋 これをコピーしてGeminiに貼ってね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
