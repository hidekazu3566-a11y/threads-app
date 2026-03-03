import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想いを形にする最高の図解が作れます✨")

# --- UIとAIへの英語指示の変換辞書 ---
composition_dict = {
    "Zの法則（左上から右下へ視線を誘導・王道）": "A strong visual hierarchy designed to guide the viewer's eye in a clear Z-shaped pattern across the image.",
    "Fの法則（上から下へ項目を読ませる・リスト向け）": "A strong visual hierarchy designed to guide the viewer's eye in a clear F-shaped pattern across the image, ideal for reading lists.",
    "三分割法・黄金比・白銀比（安定と美しさの比率）": "Strict composition adherence to the Rule of Thirds or Golden Ratio logic to place key elements and focus. TEXT ELEMENTS (title, details) MUST BE ARRANGED to balance the negative space. Zero centered objects. ABSOLUTELY NO VISIBLE GRID LINES OR CROSSHAIRS.",
    "中央集中型・日の丸構図（視線をど真ん中に集める）": "A precise direct centered composition with all focus exclusively on the central subject and title, minimal distractions.",
    "対角線・斜め分割（動きとリズム、スピード感を出す）": "A dynamic composition with key elements arranged strictly along strong diagonal lines, conveying movement and speed.",
    "額縁構図（外枠で囲って中央を際立たせる）": "CRITICAL RULE: A visible, distinct decorative frame or border surrounding the entire composition, emphasizing the central content. The frame style must match the chosen genre and art style.",
    "マス目・タイル配置（均等に枠を分けて情報を整理する）": "A clean, organized composition structured by a precise grid or tile layout, conveying a strong sense of unity and structure.",
    "破れグリッド・非対称バランス（あえて崩しておしゃれ感や動きを出す）": "CRITICAL RULE: Extreme 'broken grid' editorial layout. TEXT BOXES, SHAPES, AND THE CHARACTER MUST HEAVILY OVERLAP AND INTERSECT. Completely destroy traditional straight alignment. Use a highly dynamic, asymmetrical collage style (like a modern fashion magazine spread). Elements must break out of their invisible boundaries. ZERO neat rows or simple stacking.",
    "余白重視（ネガティブスペース）（空白を活かして上品さや高級感を演出）": "A minimalist composition prioritizing a very large amount of clean negative space, creating a profound sense of elegance, luxury, and focus.",
    "シンメトリー（左右対称）（誠実さや静寂を伝える）": "A perfectly symmetrical composition, creating a sense of visual integrity, solemnity, and peace.",
    # 💡 🚨 ここを極限まで強化！Imagen Imagen「斜めの視線」を強制発動！🚨
    "トライアングル（三角構図）（圧倒的な安定感や成長を出す）": "CRITICAL RULE: Strict implied triangle composition created ONLY by the non-linear, dynamic placement of elements. ABSOLUTELY NO VISIBLE TRIANGLE SHAPES OR OUTLINES. Conveying extreme stability and harmonized structure through powerful diagonal flow. Focal point (e.g., character/cat) MUST BE PLACED at a dynamically staggered apex, and supporting elements (e.g., text blocks) MUST BE ARRANGED to form a distinct, wide base with clear diagonal lines connecting to the apex. DO NOT align character and text blocks vertically; use strong diagonal angles to create a visual pyramid flow.",
    "--- SWOT分析図（強み・弱み・機会・脅威の4ブロック） ---": "A clean infographic layout divided into four distinct, numbered quadrants clearly labeled Strength, Weakness, Opportunity, and Threat.",
    "--- ジャーニーマップ（時系列と感情の起伏を波で表現） ---": "A chronological infographic timeline showing emoij-based emotional ups and downs along a visual wave-like chart.",
    "レーダーチャート（クモの巣）（複数の評価軸で総合力を可視化）": "A precise radar chart infographic (spider chart) showing multiple evaluation axes to visualize overall strength.",
    "スペクトル・グラデーション（0〜100%など段階的な変化を表現）": "A visual spectrum or gradient infographic showing a progressive, phased change, strictly labeled from 0% to 100%.",
    "ロジックツリー（「なぜ？」「どうやって？」を枝状に分解）": "A branchedロジックツリー or issue tree infographic layout strictly decomposing a main concept into detailed 'Why?' or 'How?' steps.",
    "同心円型（波紋）（中心から外に広がる影響や重要度を表現）": "A concentric circles infographic layout, like ripples expanding outwards, to clearly show influence, scope, or importance.",
    "ルービックキューブ（立体ブロック）（複雑な要素の組み合わせを表現）": "A conceptual composition visualizing a multi-element structure as an interlocking, complex 3D Rubik's cube puzzle block.",
    "--- ストーリー4コマ・カルーセル絵巻（スワイプ前提の物語展開） ---": "A narrative composition structured for an Instagram carousel, where each image is a strictly connected 'panel' in a continuous 4-コマ story or continuous絵巻 (picture scroll).",
    "数字・データビジュアル（大きな数字で事実をガツンと伝える）": "A graphic composition focusing heavily on very large, bold numbers to powerfully present facts.",
    "ヒーローショット・ズームイン（主役を全画面でドーンと見せる、細部を拡大する）": "An epic hero shot where the main subject and title fill the entire screen, with extreme detail, zoom-in focus, and impact.",
    "重ね合わせ（レイヤー）（写真や文字を重ねて奥行きや深みを出す）": "A layered composition with multiple overlapping elements of photo, character, and text, creating profound depth and dimension.",
    "シルエット・逆光（余韻や神秘的なムードを演出）": "A moody composition using strong backlighting and strictly silhouettes to create lingering emotion and profound mystery.",
    "鏡面・リフレクション（水面などの反射で二面性や夢幻的な美しさを出す）": "A dreamlike composition with a perfect mirror-like reflection (e.g., in water), creating a powerful sense of dreamlike beauty and integrity.",
    "タロットカード・星座マッピング（占い・スピリチュアルな独自の世界観）": "A mystical composition adhering strictly to a tarot card-like or celestial constellation-mapping worldview, with symbolic elements.",
    "モノクロ＋1色スポットライト（白黒の中で点だけカラーにして強烈に強調）": "A dramatic composition in mostly monochrome, with strictly one specific element or character highlighted in a single, vibrant, contrasting color.",
    "問い→答え開示（リビール）（疑問を投げてスワイプで答えを出す）": "A teaser composition designed strictly for a multi-image reveal, where the first image poses a powerful question and subsequent images reveal the clear answer.",
    "タイポグラフィ主役（文字そのものをアートとして見せる）": "An artful typography-first composition where the title text is treated as the main visual artwork, with character and background integrated seamlessly."
}

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
        img_title = st.text_area(f"タイトル・見出し", key=f"title_{i}", placeholder="例：メンタルが強い人は\n（改行できます）", height=68)
        img_details = st.text_area(f"具体的なテキスト（詳細・箇条書きなど）", key=f"details_{i}", placeholder="視点の切り替えが上手い\n出来ないより出来ることを考える\n小さな一歩を認められる")
        
        content_list.append({
            "slide_number": i+1,
            "title": img_title,
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
    "🔥 モチベ爆上がり！すぐ行動したくなる"
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
    
    if text_background not in ["なし（文字のみ・背景に溶け込ませる）", "✨ おまかせ（AIが一番読みやすいデザインを自動で選ぶ！）"]:
        bg_opacity = st.slider("下敷きの不透明度（透け感）", min_value=10, max_value=100, value=70, step=10, format="%d%%")
        st.caption("100%でくっきり、数字が小さいほど背景が透けます✨")
    else:
        bg_opacity = "なし"

brand_color = st.text_input("あなたのテーマカラー（任意）", placeholder="例：淡いブルーとピンク")

# --- 4. デザインの方向性 ---
st.header("4. デザインの方向性")

comp_options = [k for k in composition_dict.keys()]

if "Zの法則（左上から右下へ視線を誘導・王道）" in comp_options:
    comp_index = comp_options.index("Zの法則（左上から右上へ視線を誘導・王道）")
else:
    comp_index = 0

composition_ui = st.selectbox("神・構図リスト（目的で選んでね！）", comp_options, index=comp_index)
composition_instruction = composition_dict.get(composition_ui, "")

style = st.selectbox("メインテイスト（画風）", [
    "1.ほのぼの可愛い水彩画風",
    "2.かわい系（ちびキャラ・パステル）",
    "3.ビジネス系（誠実・青基調・信頼感）",
    "4.エモい写真風",
    "5.ゲーム風ドット絵",
    "6.ネオンサイン系"
])

mood = st.select_slider("雰囲気のトーン", options=["ふんわり", "ナチュラル", "普通", "ドラマチック", "ビビッド"])

# --- 🚀 プロンプト生成（命令書の錬成） ---
if st.button("🪄 読者の心を動かす図解プロンプトを生成する"):
    
    final_color = brand_color if brand_color else "Auto-select the best colors based on genre and emotion."
    
    if text_strictness == "🚫 指定した文字だけを厳格に入れる（勝手な追加NG）":
        text_rule = "CRITICAL: DO NOT add any extra text, titles, or subtitles. Use ONLY the exact text provided in the content_list. Do not generate a title if it is empty."
    else:
        text_rule = "Feel free to add highly relevant, short subtitles or catchphrases to enhance the design if it fits the context."

    if subject_type == "自分のキャラクターを使う（画像アップロード）":
        subject_instruction = "CRITICAL RULE: Extract and reproduce ONLY the character itself from the attached image. You MUST strictly EXCLUDE all props, objects (like laptops, desks, cups, plants), and the original background."
    else:
        subject_instruction = subject_type

    if text_background == "✨ おまかせ（AIが一番読みやすいデザインを自動で選ぶ！）":
        bg_instruction = "Auto-select the best readable text box styles (e.g., speech bubbles, clean panels) that fit the composition and emotional goal."
    elif text_background == "🏷️ タイトルのみ強調（見出しだけリボンやバナー風にする）":
        bg_instruction = "Apply a stylish background (like a banner or ribbon) ONLY to the title. Keep detail texts clean without heavy backgrounds."
    elif text_background == "なし（文字のみ・背景に溶け込ませる）":
        bg_instruction = "None (text only)"
    else:
        bg_instruction = f"Style: {text_background}, Opacity: {bg_opacity}"

    placement_instruction = f"{char_placement}. CRITICAL RULE: This requested character placement has the HIGHEST absolute priority. The design and 'composition_structure' MUST adapt to this specific character location. Do not move the character to fit a grid; move the design to fit the character."

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
            "text_background": bg_instruction,
            "composition_structure": composition_instruction,
            "brand_color_theme": final_color,
            "emotional_goal": emotion,
            "aspect_ratio": ratio
        },
        "content_per_image": content_list,
        "character_instructions": {
            "subject": subject_instruction,
            "placement": placement_instruction
        },
        "generation_rules": [
            f"Generate exactly {num_images} images based on the content_per_image array.",
            "Generate completely NEW backgrounds and poses. Keep the character consistent but in fresh contexts.",
            "NEVER draw any props or items from the reference image.",
            text_rule,
            "CRITICAL TYPOGRAPHY RULE: Establish a strict visual hierarchy. The main 'title' MUST be visually dominant, significantly LARGER and BOLDER than the 'details' text."
        ]
    }

    st.success(f"✨ {num_images}枚分の最強プロンプトが完成したよ！黒い枠の中身だけをコピーしてね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
