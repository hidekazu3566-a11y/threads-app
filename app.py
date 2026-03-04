import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想りを形にする最高の図解が作れます✨")

# --- UIとAIへの英語指示の変換辞書 ---
composition_dict = {
    "Zの法則（左上から右下へ視線を誘導・王道）": "A strong visual hierarchy designed to guide the viewer's eye in a clear Z-shaped pattern across the image.",
    "Fの法則（上から下へ項目を読ませる・リスト向け）": "A strong visual hierarchy designed to guide the viewer's eye in a clear F-shaped pattern across the image, ideal for reading lists.",
    "三分割法・黄金比・白銀比（安定と美しさの比率）": "Strict composition adherence to the Rule of Thirds or Golden Ratio logic to place key elements and focus. TEXT ELEMENTS (title, details) MUST BE ARRANGED to balance the negative space. Zero centered objects. ABSOLUTELY NO VISIBLE GRID LINES OR CROSSHAIRS.",
  "中央集中型（日の丸構図・感情ポーズ連動）": (
        "A precise, direct centered composition (Hinomaru style) with all focus exclusively on the central subject. "
        "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST analyze the specific conceptual meaning of the Japanese text provided for each individual image in the sequence. "
        "DRAMATICALLY adapt the main subject's facial expression, body language, and pose to perfectly match the mood of that specific text (e.g., transition from doubt/sadness to clarity/joy across the sequence). "
        "Avoid generic expressions or frozen smiles. "
        "TEXT PLACEMENT: If text is to be rendered, place it clearly above or below the subject, ensuring it NEVER obscures the face. "
        "Maintain high consistency of the subject and style across all generated images without adding any unrequested elements."
    ),
    "対角線・斜め分割（動きとリズム、スピード感を出す）": "A dynamic composition with key elements arranged strictly along strong diagonal lines, conveying movement and speed.",
    "額縁構図（外枠で囲って中央を際立たせる）": "CRITICAL RULE: A visible, distinct decorative frame or border surrounding the entire composition, emphasizing the central content. The frame style must match the chosen genre and art style.",
    "マス目・タイル配置（均等に枠を分けて情報を整理する）": "A clean, organized composition structured by a precise grid or tile layout, conveying a strong sense of unity and structure.",
    "雑誌風コラージュ（あえて崩しておしゃれ感や動きを出す）": "CRITICAL RULE: Extreme 'broken grid' editorial collage layout. TEXT BOXES MUST HAVE TORN PAPER EDGES and appear like paper scraps pinned to a background. THE CHARACTER AND TEXT BOXES MUST HEAVILY OVERLAP each other to create depth. Use asymmetrical, irregular placement where elements break out of an invisible grid. The overall feel must be like a creative, layered scrapbook or a high-fashion magazine spread with watercolor textures. Add decorative elements like small flowers, leaves, or cute doodles in the empty spaces to balance the composition.",
    "余白重視（ネガティブスペース）（空白を活かして上品さや高級感を演出）": "A minimalist composition prioritizing a very large amount of clean negative space, creating a profound sense of elegance, luxury, and focus.",
    "シンメトリー（左右対称）（誠実さや静寂を伝える）": "A perfectly symmetrical composition, creating a sense of visual integrity, solemnity, and peace.",
    "トライアングル（三角構図）（圧倒的な安定感や成長を出す）": "CRITICAL RULE: Strict implied triangle composition created ONLY by the non-linear, dynamic placement of elements. ABSOLUTELY NO VISIBLE TRIANGLE SHAPES, OUTLINES, ARROWS, OR CONNECTING LINES. The connection between elements must be completely invisible and purely psychological. Conveying extreme stability through powerful diagonal flow. Focal point (e.g., character/cat) MUST BE PLACED at a dynamically staggered apex, and supporting elements (e.g., text blocks) MUST BE ARRANGED to form a distinct, wide base. DO NOT draw any lines between the character and the text. DO NOT align character and text blocks vertically; use strong diagonal angles to create a visual pyramid flow.",
    "4分割・ブロック配置（情報を4つのエリアに分ける）": "A clean, structured infographic layout divided into four distinct, equal quadrants. TEXT ELEMENTS are ARRANGED sequentially. CRITICAL: DO NOT add any extra numbering icons or labels if the input text already includes numbers. Place the provided text exactly as it is within each block.",
   "サクセス・ストーリー（成功への道のりと感情の変化）": (
        "A strict linear, horizontal (left-to-right) infographic journey toward a successful goal. " # 👈 「厳格な水平（左から右）」に修正！
        "The number of steps MUST EXACTLY MATCH the content list. CRITICAL LAYOUT RULE: Elements MUST NEVER cross back over previous steps. " # 👈 「絶対に前のステップを横切らない」という禁止ルールを追加！
        "Arrange the character-text pairs sequentially along a clean, smooth wavy path that progresses clearly from left to right across the screen. "
        "Each character and text pair must be tightly integrated as a single visual unit, especially at the start and end of the path. "
        "Include emotional sun/cloud/heart icons and a 'SUCCESS!' element at the final point. NO REPEATING TEXT. Reiterate: STRICT left-to-right horizontal linear sequence."
       ),
    "ステータス画面風（ゲームみたいに能力を可視化）": (
        "A game-inspired character status screen layout where the character is the protagonist. "
        "CRITICAL GAUGE RULE: The length (fill-level) of each horizontal status bar MUST strictly correlate with the numerical value provided at the end of each text item (e.g., 'Power 80' or 'Speed (5)'). Higher numbers produce longer, fuller bars. "
        "TEXT RENDERING RULE: DO NOT render the numerical values, percentages, or parentheses used for control on the image. " # 👈 ここで「数字は書くな」と指示！
        "ONLY render the label text itself. For example, if the input is 'Power 80', the image should show a bar at 80% length but ONLY display the word 'Power'. "
        "Use vibrant, distinct colors for each bar and ensure a clean, modern gaming UI feel. NO REPEATING TEXT."
    ),
   "スペクトル・グラデーション（0〜100%など段階的な変化を表現）": (
        "A full-background gradient infographic on textured paper, flowing smoothly from cool blue (representing low/0%) on the far left to hot red (representing high/100%) on the far right. " # 👈 「背景全体を青から赤へ」に修正！
        "The number of steps MUST EXACTLY MATCH the content list, arranged horizontally from left to right along this color spectrum. " # 👈 「横に並べる」と指示！
        "A central cat protagonist is integrated tightly with each step's corresponding text box. " # 👈 一体感を維持！
        "Clear labels for '0%' and '100%' must be visible. Include subtle emotional icons. DO NOT repeat any text. "
        "Prioritize seamless, tight character-text proximity. The overall feel is balanced and instructional." # 👈 密着と分かりやすさを強調！
        ),
"深掘りツリー（「なぜ？」「どうやる？」を枝分けして解説）": (
        "An organic, tree-like infographic with a strict visual hierarchy. "
        "The Title is the root/trunk. "
        "AI TASK: Treat the content list as a STRICT INVENTORY of unique items. " # 👈 「在庫（インベントリ）」として扱わせる
        "PLACEMENT RULE: Each item from the list is a SINGLE-USE asset. Once an item is placed, it is EXHAUSTED and MUST NOT be used again in any other part of the image. " # 👈 「一回使ったら在庫切れ」ルール
        "CRITICAL VISUAL HIERARCHY: Group names MUST be in 'Wooden Signboards'. Detail items MUST be 'Leaves'. "
        "CATEGORY CREATION: AI must generate BRIEF, UNIQUE category names (e.g., 'Nature', 'Actions') that are NOT present in the detail list. " # 👈 「看板の文字はリストから選ぶな、AIが新しく考えろ」と指示
        "CRITICAL ANTI-REDUNDANCY: Absolutely zero word-for-word repetition. The total count of labels must equal the list length plus new categories. "
        "The cat should be interacting with the tree. NO REPEATING TEXT."
    ),
    "放射型（中心から外に広がる）": "A concentric circles infographic layout, like ripples expanding outwards, to clearly show influence, scope, or importance.",
    "ルービックキューブ（立体ブロック）（複雑な要素の組み合わせを表現）": (
        "A 3D Rubik's cube structure composition where the individual block panels are SIGNIFICANTLY ENLARGED to maximize surface area. " # 👈 ブロックサイズを「大幅に拡大」する！
        "Prioritize text readability above all. Render all detail text (from the content list) in a VERY LARGE, BOLD, highly legible font (e.g., ゴシック体) within the enlarged panels. " # 👈 「文字の大きさ、太さ、読みやすさ」を最優先！
        "The Title is visually dominant at the top. Use a STRONG visual hierarchy, making the main 'title' significantly LARGER and BOLDER than the 'details' text. " # 👈 タイトルと詳細のメリハリを強化！
        "CRITICAL TEXT RULE: The content list is a STRICT SINGLE-USE INVENTORY. Absolutely zero word-for-word repetition across the entire image. Once an item is placed, it is EXHAUSTED. " # 👈 重複絶対禁止は維持！
        "ILLUSTRATIVE FILLING RULE: If a panel needs filling, add a theme-relevant small illustrative element (icon, prop, or decorative object), NEVER repeated text. Replace exhausted panels with fresh visuals like balls of yarn, paw prints, fish bones, keeping the visuals fresh. " # 👈 小物の埋め草は維持！
        "INTEGRATION: The cat characters should be actively interacting with the block panels. Ensure clean, instructional aesthetics with clear text hierarchy. "
    ),
    "4コマストーリー（文字くっきり＆背景はそのまま）": (
        "A sequence of exactly four connected story panels, optimized for a comic strip or carousel layout. "
        "Each panel MUST represent a single step in a logical narrative arc (起承転結). "
        "CRITICAL READABILITY RULE: The chosen background style and character must be fully visible. However, to ensure text readability, create a distinct, CLEAN, SOLID WHITE text box (or speech bubble) at the bottom or top of each panel. "
        "Render the provided text EXCLUSIVELY inside these white boxes. "
        "CRITICAL TYPOGRAPHY: Text MUST be VERY LARGE, BOLD, and highly legible. Ensure extreme contrast between the text and the white box. "
        "Do not repeat any text across panels. The main subject must appear consistently across panels to convey the story flow, without obstructing the text boxes."
    ),
   "数字・データビジュアル（大きな数字で事実をガツンと伝える）": (
        "A striking infographic layout designed to powerfully present data, rankings, or shocking facts. "
        "CRITICAL VISUAL RULE: Extract the primary numerical values from the content list and render them as HUGE, 3D, or highly stylized focal points. These numbers MUST visually dominate the composition. "
        "The central character (e.g., the cat) should be actively interacting with these giant numbers (e.g., sitting on a giant '90%', hugging a large '5', or leaning against them). "
        "CRITICAL READABILITY: For the explanatory text corresponding to each number, use a CLEAN, SOLID WHITE text box (like a simple panel or banner) to ensure extreme contrast and high readability. "
        "Render the text in a VERY LARGE, BOLD, legible font inside these white boxes. DO NOT repeat any text. Ensure a sleek, impactful editorial aesthetic."
    ),
   "ヒーローショット・ズームイン（主役を全アップでドーン！エモさ重視）": (
        "An epic, dramatic HERO SHOT composition focusing intensely on the main subject. "
        "CRITICAL CAMERA RULE: Extreme close-up / zoom-in on the core subject. The subject MUST fill at least 80% of the entire screen with incredible detail, sharp focus, depth of field, and cinematic lighting. " # 猫の例示を削除！
        "TEXT RULE: This composition is for dramatic visual IMPACT, not long explanations. Render the provided text as a powerful catchphrase. "
        "To ensure text readability against the highly detailed background, use a stylish, CLEAN SOLID WHITE text box (like a simple banner) or a sleek semi-transparent dark banner at the bottom or side. "
        "Render the text in a VERY LARGE, BOLD, cinematic font. NO REPEATING TEXT. The overall vibe should be like a high-end editorial spread, a dramatic movie poster, or a sleek product reveal."
    ),
  "シルエット・逆光（半透明テロップ・表情連動）": (
        "A highly emotional, moody composition focusing heavily on strong BACKLIGHTING and SILHOUETTES. "
        "The main subject MUST be silhouetted against a dramatic, luminous background (e.g., a breathtaking twilight, glowing neon, or cinematic light rays) to create lingering emotion and profound mystery. "
        "CRITICAL READABILITY & MOOD: The text MUST enhance the atmospheric mood. Use elegant, clean text boxes that look like a soft, semi-transparent, or gently glowing background pane (e.g., a subtle dark or light wash). "
        "Render the provided text highly legible with extreme contrast within these semi-transparent panes. DO NOT repeat any text. "
        "The overall vibe is a profound movie poster or an emotional quote visual. "
        "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST analyze the specific content of the Japanese text in each list item/panel. Adapt the main subject's facial expression, body language, and pose to DRAMATICALLY match the corresponding mood. Avoid generic expressions."
    ),
    "鏡面・リフレクション（水面反射・表情連動）": (
        "A dreamlike composition featuring a perfect, crystal-clear mirror-like reflection of the main subject on a surface (e.g., still water or a highly polished floor) to create a powerful sense of dreamlike beauty and integrity. "
        "CRITICAL BODY INTEGRITY RULE: Ensure anatomically correct and structurally sound body representation for the main subject. Poses should be natural, avoiding unnatural distortion or extra/missing limbs. The reflection must perfectly and accurately mirror this correct anatomy. "
        "CRITICAL TEXT RULE: You MUST clearly render ALL provided Japanese text items in the image. DO NOT skip, drop, or shorten any lines. Use elegant, semi-transparent text boxes or softly glowing panels that blend with the dreamlike atmosphere, ensuring extreme contrast and high legibility. "
        "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST analyze the specific content of the text. Adapt the main subject's facial expression, body language, and pose to DRAMATICALLY match the corresponding mood. Avoid generic expressions. This applies to both the real subject and its reflection."
    ),
    "タロット・星座マッピング（表情連動・文字くっきり）": (
        "A mystical composition adhering strictly to a tarot card-like or celestial constellation-mapping worldview, rich with esoteric symbols, Zodiac motifs, and stardust textures. "
        "CRITICAL READABILITY & TEXT PLACEMENT RULE: Render ALL provided Japanese text clearly and legibly. The text MUST NOT obscure the face or core symbolic elements of the main subject. Use distinct, clean text boxes that look like soft, semi-transparent background panes, gently glowing celestial scrolls, or old parchment labels pinned to the composition. Place these text elements in balanced negative space, typically in the corners, top/bottom banners, or separate 'card segments'. DO NOT repeat any text. "
        "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST analyze the specific content of the Japanese text in each list item/panel. Adapt the main subject's facial expression, body language, and pose to DRAMATICALLY match the corresponding mood. Poses should be natural and structurally sound. Avoid generic expressions. This rule applies to both the central figure and any depicted 'card characters'. "
        "Adapt with appropriate decorative motifs, ensuring a profound, spiritual feel, regardless of the theme."
    ),
    "モノクロ＋1色スポットライト（感情同期最強版）": (
        "A dramatic composition where the entire scene is rendered in stark, powerful monochrome. "
        "AI TASK: Extract ALL provided Japanese text items clearly and legibly. Place ALL text elements to ensure that NO portion of any text is obscured or covered by the main subject's body. "
        "CRITICAL SPOTLIGHT RULE: Precisely one, single element in the image MUST be highlighted in a single, vibrant, contrasting color. This spotlight effect MUST highlight the Title text banner or background. DO NOT apply this color effect to the face, body, or any organic part of the main subject. "
        "To ensure maximum visibility and aesthetic coherence, use stylish, CLEAN, SOLID text boxes or banners for all text, with the Title element having the color highlight. "
        "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST analyze the specific content of the Japanese text items. MUST identifiy the core emotion of each statement (e.g., contemplation of the past, discovery of truth, somber decision, or soothing tiredness). Adapt the main subject's facial expression, body language, and pose to DRAMATICALLY and unmistakably change the face and full body pose to match the corresponding mood. Poses should be natural, structurally sound, and deeply integrated with the content. Zero tolerance for the default generic smile. " # 👈 感情同期を最強レベルに強化！
    ),
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
    comp_index = comp_options.index("Zの法則（左上から右下へ視線を誘導・王道）")
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
            f"Generate each of the {num_images} requested items as a strictly independent, separate image file.",
            "DO NOT combine, merge, or grid multiple content items into a single image canvas.",
            "Generate completely NEW backgrounds and poses for each image while keeping the character consistent.",
            text_rule,
            "CRITICAL TYPOGRAPHY RULE: Establish a strict visual hierarchy. The main 'title' MUST be visually dominant."
        ]
    }

    st.success(f"✨ {num_images}枚分の最強プロンプトが完成したよ！黒い枠の中身だけをコピーしてね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
