import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想いを形にする最高の図解が作れます✨")

# --- 1. 基本設定（用途・サイズ・ジャンル・枚数） ---
st.header("1. 作りたい画像の設定")
use_case = st.selectbox("用途", [
    "図解（SNS・プレゼン用）", 
    "サムネイル（YouTube・記事用）", 
    "汎用画像生成（自由設定）"
])

col1, col2 = st.columns(2)
with col1:
    ratio_selection = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)", "その他（自由入力）"])
    if ratio_selection == "その他（自由入力）":
        ratio = st.text_input("比率を入力（例：3:4、2:1など）", value="3:4")
    else:
        ratio = ratio_selection

with col2:
    num_images = st.selectbox("出力枚数", list(range(1, 11)))

genre = st.selectbox("ターゲットジャンル・世界観", [
    "指定なし（標準）",
    "1. 美容・コスメ（透明感・洗練・女性向け）",
    "2. 健康・ダイエット（爽やか・エネルギッシュ）",
    "3. 恋愛・婚活（エモーショナル・温かみ）",
    "4. 育児・ファミリー（優しい・柔らかい）",
    "5. スピリチュアル・占い（神秘的・宇宙）",
    "6. マネー・投資（知的・信頼・図解多め）",
    "7. ビジネス・自己啓発（スタイリッシュ・説得力）",
    "8. エンタメ・ゲーム（ポップ・派手・コミカル）"
])

# --- 2. 伝える内容とキャラクター ---
st.header("2. 伝える内容と被写体")

text_strictness = st.radio("テキストの追加アレンジ", [
    "🚫 指定した文字だけを厳格に入れる（勝手な追加NG）",
    "✨ AIにいい感じのサブタイトル等の追加をお任せする"
])

content_list = []
for i in range(num_images):
    with st.expander(f"📝 {i+1}枚目のテキスト入力", expanded=(i==0)):
        # 💡 ここを修正！自動生成指示は完全に削除！入力された文字を絶対に使います！
        img_title = st.text_area(f"タイトル・見出し", key=f"title_{i}", placeholder="例：メンタルが強い人は\n（改行できます）", height=68)
        img_details = st.text_area(f"具体的なテキスト（詳細・箇条書きなど）", key=f"details_{i}", placeholder="視点の切り替えが上手い\n出来ないより出来ることを考える\n小さな一歩を認められる")
        
        content_list.append({
            "slide_number": i+1,
            "title": img_title, # 入力された文字をそのまま渡す
            "details": img_details.split('\n') if img_details else []
        })

col3, col4 = st.columns(2)
with col3:
    subject_type = st.selectbox("メインの被写体（キャラクター）", [
        "自分のキャラクターを使う（画像アップロード）",
        "入れない（キャラなし）",
        "AIに任せる"
    ])
with col4:
    char_placement = st.selectbox("キャラクターの配置位置", [
        "おまかせ（構図に合わせて最適化）",
        "右下に配置",
        "左下に配置",
        "中央に大きく配置",
        "見切れるように配置（ひょっこり感）"
    ])

if subject_type == "自分のキャラクターを使う（画像アップロード）":
    st.info("💡 生成する時、Geminiにキャラ画像を一緒に添付するのを忘れないでね！")

# --- 3. 読者の感情とテキスト装飾 ---
st.header("3. 読者の感情とテキスト装飾 🎨")

emotion = st.selectbox("読者にどうなってほしい？（感情トリガー）", [
    "🤖 おまかせ（AIに最適な感情表現を任せる）",
    "💡「なるほど！」と思わず保存・メモしたくなる",
    "🥺 共感してウルっとくる・勇気が出る",
    "😂 クスッと笑える・ツッコミたくなる",
    "🔥 モチベ爆上がり！すぐに行動したくなる"
])

col5, col6 = st.columns(2)
with col5:
    font_choice = st.selectbox("フォント・文字の書体", [
        "おまかせ（画風に合わせて最適化）",
        "ゴシック体（王道・読みやすさバツグン）",
        "明朝体（高級感・知的・大人っぽい）",
        "丸ゴシック（ポップ・かわいい・親しみ）",
        "手書き風（エモい・親近感・パーソナル）"
    ])
    
    text_align = st.selectbox("文字の揃え位置", [
        "おまかせ（デザインに合わせて最適化）",
        "左揃え（箇条書きや長文にピッタリ）",
        "中央揃え（タイトルや短い言葉に）",
        "右揃え（レイアウトのアクセントに）"
    ])

with col6:
    # 💡 あなたのアイデア「下敷きはおまかせがいい」を反映！
    # V8の全項目を復活させた上で、一番上に「✨おまかせ」を追加し、デフォルトにしました！
    text_background = st.selectbox("文字の下敷き（座布団）", [
        "✨ おまかせ（AIが一番読みやすいデザインを自動で選ぶ！）",
        "🏷️ タイトルのみ強調（見出しだけリボンやバナー風にする）",
        "☁️ モワモワした雲の形（ポップ・かわいい）",
        "⬛️ ペンキでサッと塗ったブラシ風（エモい）",
        "📌 付箋・マスキングテープ風（メモ感）",
        "📄 破れた紙・ノートの切れ端風（レトロ）",
        "⬜️ シンプルな角丸長方形（王道・スッキリ）",
        "すりガラス風（スタイリッシュ）",
        "なし（文字のみ・背景に溶け込ませる）"
    ])
    
    # 不透明度スライダーもちゃんと復活！「なし」と「おまかせ」以外の時に出ます。
    if text_background not in ["なし（文字のみ・背景に溶け込ませる）", "✨ おまかせ（AIが一番読みやすいデザインを自動で選ぶ！）"]:
        bg_opacity = st.slider("下敷きの不透明度（透け感）", min_value=10, max_value=100, value=70, step=10, format="%d%%")
        st.caption("100%でくっきり、数字が小さいほど背景が透けます✨")
    else:
        bg_opacity = "なし"

brand_color = st.text_input("あなたのテーマカラー（任意）", placeholder="例：淡いブルーとピンク")

# --- 4. デザインの方向性 ---
st.header("4. デザインの方向性")
composition = st.selectbox("神・構図リスト（目的で選んでね！）", [
    "Zの法則（王道スタイル）：視線を左上から右下へ誘導。",
    "左右分割（テキスト左・キャラ右）：情報をしっかり整理！",
    "中央ドカン！（放射・中央配置）：インパクト重視！",
    "上下分割（タイトル上・キャラ下）：雑誌の表紙風安定スタイル。",
    "ビフォーアフター（変化で魅せる！）：違いをクッキリ見せる！",
    "タイムライン（手順・流れ）：ステップや歴史を順番に！"
])

style = st.selectbox("メインテイスト（画風）", [
    "1. ほのぼの可愛い水彩画風",
    "2. かわい系（ちびキャラ・パステル）",
    "3. ビジネス系（誠実・青基調・信頼感）",
    "4. エモい写真風",
    "5. ゲーム風ドット絵",
    "6. ネオンサイン系"
])

mood = st.select_slider("雰囲気のトーン", options=["ふんわり", "ナチュラル", "普通", "ドラマチック", "ビビッド"])

# --- 🚀 プロンプト生成（命令書の錬成） ---
if st.button("🪄 読者の心を動かす図解プロンプトを生成する"):
    
    final_color = brand_color if brand_color else "Auto-select the best colors based on genre and emotion."
    
    # 🚫 勝手な文字NGの時は、一文字も足さないように裏側の英語指示をキツくしたよ！
    if text_strictness == "🚫 指定した文字だけを厳格に入れる（勝手な追加NG）":
        text_rule = "CRITICAL: DO NOT add any extra text, titles, or subtitles. Use ONLY the exact text provided in the content_list. Do not generate a title if it is empty."
    else:
        text_rule = "Feel free to add highly relevant, short subtitles or catchphrases to enhance the design if it fits the context."

    if subject_type == "自分のキャラクターを使う（画像アップロード）":
        subject_instruction = "CRITICAL RULE: Extract and reproduce ONLY the character itself from the attached image. You MUST strictly EXCLUDE all props, objects (like laptops, desks, cups, plants), and the original background."
    else:
        subject_instruction = subject_type

    # 💡 下敷き「おまかせ」の時の、AIへの具体的な指示を裏側に実装！
    if text_background == "✨ おまかせ（AIが一番読みやすいデザインを自動で選ぶ！）":
        # ここ重要。AIに「吹き出し、パネルなど、構成に合わせてお前がいい感じの下敷きデザインを選べ」と指示。
        bg_instruction = "Auto-select the best readable text box styles (e.g., speech bubbles, clean panels) that fit the composition and emotional goal."
    elif text_background == "🏷️ タイトルのみ強調（見出しだけリボンやバナー風にする）":
        bg_instruction = "Apply a stylish background (like a banner or ribbon) ONLY to the title. Keep detail texts clean without heavy backgrounds."
    elif text_background == "なし（文字のみ・背景に溶け込ませる）":
        bg_instruction = "None (text only)"
    else:
        # それ以外（雲、テープなど）は、選んだスタイルと不透明度をそのまま指示
        bg_instruction = f"Style: {text_background}, Opacity: {bg_opacity}"

    # 🚨 バグ修正！ここを "image_generation" に戻したから、絶対に画像が出る！！
    data_for_gemini = {
        "role": "Exclusive AI Image Generation Expert",
        "format": "image_generation",
        "objective": f"Generate {num_images} high-quality images for {use_case}",
        "design_concept": {
            "genre_worldview": genre,
            "style": style,
            "mood_tone": mood,
            "typography": {
                "font_style": font_choice,
                "alignment": text_align
            },
            "text_background": bg_instruction, # ここに洗練された下敷き指示が入る！
            "composition_structure": composition,
            "brand_color_theme": final_color,
            "emotional_goal": emotion,
            "aspect_ratio": ratio
        },
        "content_per_image": content_list,
        "character_instructions": {
            "subject": subject_instruction,
            "placement": char_placement
        },
        "generation_rules": [
            f"Generate exactly {num_images} images based on the content_per_image array.",
            "Generate completely NEW backgrounds and poses. Keep the character consistent but in fresh contexts.",
            "NEVER draw any props or items from the reference image.",
            text_rule
        ]
    }

    st.success(f"✨ {num_images}枚分の最強プロンプトが完成したよ！黒い枠の中身だけをコピーしてね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
