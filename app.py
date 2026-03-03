import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想いを形にする最高の図解が作れます✨")

# --- UIとAIへの英語指示の変換辞書（V1から今までの「正解」を全復旧） ---
composition_dict = {
    "Zの法則（左上から右下へ視線を誘導・王道）": "CRITICAL: A definitive Z-shaped visual path. Guide the eye strictly from Top-Left to Top-Right, then diagonally down to Bottom-Left, and finally to Bottom-Right. Elements MUST be positioned to reinforce this specific scanning pattern. Ensure strong visual weight at each corner of the Z-path to anchor the viewer's attention. [cite: 2026-03-04]",
    "Fの法則（上から下へ項目を読ませる・リスト向け）": "CRITICAL: A definitive F-shaped scanning pattern. Focus on a strong horizontal line at the top, followed by a shorter horizontal line further down, and a clear vertical line along the left side. This is a strict hierarchy for information processing. Arrange headers, bullets, and icons to perfectly mimic an F-shaped eye-tracking heat map. [cite: 2026-03-04]",
    "三分割法・黄金比・白銀比（安定と美しさの比率）": "Strict composition adherence to the Rule of Thirds or Golden Ratio logic to place key elements and focus. TEXT ELEMENTS (title, details) MUST BE ARRANGED to balance the negative space. Zero centered objects. ABSOLUTELY NO VISIBLE GRID LINES OR CROSSHAIRS.",
    "中央集中型・日の丸構図（視線をど真ん中に集める）": "A precise direct centered composition with all focus exclusively on the central subject and title, minimal distractions. Achieve perfect focus on the core message. Perfect symmetry around the vertical axis.",
    "対角線・斜め分割（動きとリズム、スピード感を出す）": "A dynamic composition with key elements arranged strictly along strong diagonal lines, conveying movement and speed. Use the diagonal split to separate text and character for a high-impact visual. Ensure no vertical alignment.",
    "額縁構図（外枠で囲って中央を際立たせる）": "CRITICAL RULE: A visible, distinct decorative frame or border surrounding the entire composition, emphasizing the central content. The frame style must match the chosen genre and art style perfectly. Ensure the content inside is clearly separated from the frame style.",
    "マス目・タイル配置（均等に枠を分けて情報を整理する）": "A clean, organized composition structured by a precise grid or tile layout, conveying a strong sense of unity and structure. Balance each tile with consistent visual weight and ensure clear borders between information blocks.",
    "破れグリッド・非対称バランス（あえて崩しておしゃれ感や動きを出す）": "CRITICAL RULE: Extreme 'broken grid' editorial layout. TEXT BOXES, SHAPES, AND THE CHARACTER MUST HEAVILY OVERLAP AND INTERSECT. Completely destroy traditional straight alignment. Use a highly dynamic, asymmetrical collage style (like a modern fashion magazine spread). Elements must break out of their invisible boundaries. ZERO neat rows or simple stacking.",
    "余白重視（ネガティブスペース）（空白を活かして上品さや高級感を演出）": "A minimalist composition prioritizing a very large amount of clean negative space, creating a profound sense of elegance, luxury, and focus. Keep the elements small and refined. Negative space is the main feature.",
    "シンメトリー（左右対称）（誠実さや静寂を伝える）": "A perfectly symmetrical composition, creating a sense of visual integrity, solemnity, and peace. Ensure the left and right sides are mirror-balanced around a central axis with mathematical precision.",
    "トライアングル（三角構図）（圧倒的な安定感や成長を出す）": "CRITICAL RULE: Strict implied triangle composition created ONLY by the non-linear, dynamic placement of elements. ABSOLUTELY NO VISIBLE TRIANGLE SHAPES OR OUTLINES. Conveying extreme stability and harmonized structure through powerful diagonal flow. Focal point (e.g., character/cat) MUST BE PLACED at a dynamically staggered apex, and supporting elements (e.g., text blocks) MUST BE ARRANGED to form a distinct, wide base with clear diagonal lines connecting to the apex. DO NOT align character and text blocks vertically; use strong diagonal angles to create a visual pyramid flow.",
    "ブロック配置（情報をエリアに分ける）": "A clean, structured infographic layout divided into distinct, equal areas or numbered blocks. CRITICAL: Match the number of areas EXACTLY to the number of items provided in the details list. Each block must have unique content and sequential numbering. ABSOLUTELY NO DUPLICATE TEXT IN BLOCKS.",
    "ステップ・感情フロー（手順や道のりを自由な数で見せる）": "A chronological infographic showing a sequence of steps or a 'journey'. Use a wavy path or dynamic line connecting unique icons and text blocks. Include visual indicators of emotional high/low points (e.g., icons or facial expressions) along the path. CRITICAL: Generate the EXACT number of steps provided in the input details list. Each step MUST have unique, non-repeating text. Do not duplicate titles as body text within the same step.",
    "レーダーチャート（クモの巣）（複数の評価軸で総合力を可視化）": "A precise radar chart infographic (spider chart) showing multiple evaluation axes to visualize overall strength. Clearly label each axis based on the provided text.",
    "ロジックツリー（「なぜ？」「どうやって？」を枝状に分解）": "A branched issue tree infographic layout strictly decomposing a main concept into detailed 'Why?' or 'How?' steps. Ensure a clear horizontal or vertical flow of information with logical connections.",
    "--- ストーリー4コマ・カルーセル絵巻 ---": "A narrative composition structured for an Instagram carousel, where each image is a strictly connected 'panel' in a continuous 4-panel story or picture scroll effect across multiple frames. Maintain visual continuity of the character and style.",
    "数字・データビジュアル（大きな数字で事実をガツンと伝える）": "A graphic composition focusing heavily on very large, bold numbers to powerfully present facts. Make the numerical data the absolute visual hero, using contrast and size to demand attention.",
    "ヒーローショット・ズームイン（主役を全画面でドーンと見せる）": "An epic hero shot where the main subject and title fill the entire screen, with extreme detail, zoom-in focus, and impact. No distractions, just pure visual power.",
    "重ね合わせ（レイヤー）（写真や文字を重ねて奥行きや深みを出す）": "A layered composition with multiple overlapping elements of photo, character, and text, creating profound depth and dimension. Use shadows, lighting, and transparency to enhance the 3D effect.",
    "シルエット・逆光（余韻や神秘的なムードを演出）": "A moody composition using strong backlighting and strictly silhouettes to create lingering emotion and profound mystery. Enhance the contrast between light and shadow to create a dramatic, atmospheric effect.",
    "鏡面・リフレクション（反射で二面性や夢幻的な美しさを出す）": "A dreamlike composition with a perfect mirror-like reflection (e.g., in water), creating a powerful sense of dreamlike beauty, integrity, and dualism.",
    "タロットカード・星座マッピング（占い・スピリチュアルな独自の世界観）": "A mystical composition adhering strictly to a tarot card-like or celestial constellation-mapping worldview, with symbolic, esoteric, and magical elements integrated into the design.",
    "モノクロ＋1色スポットライト（白黒の中で点だけカラーにして強烈に強調）": "A dramatic composition in mostly monochrome, with strictly one specific element or character highlighted in a single, vibrant, contrasting color to create an instant focal point and emotional impact.",
    "問い→答え開示（リビール）（疑問を投げてスワイプで答えを出す）": "A teaser composition designed strictly for a multi-image reveal, where the first image poses a powerful question and subsequent images reveal the clear answer in a satisfying, visually rewarding way.",
    "タイポグラフィ主役（文字そのものをアートとして見せる）": "An artful typography-first composition where the title text is treated as the main visual artwork, with character and background integrated seamlessly into the letterforms themselves."
}

# --- 1. 基本設定 ---
st.header("1. 作りたい画像の設定")
use_case = st.selectbox("用途", ["図解（SNS・プレゼン用）", "サムネイル（YouTube・記事用）", "汎用画像生成（自由設定）"])
col1, col2 = st.columns(2)
with col1:
    ratio_selection = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)", "その他（自由入力）"])
    ratio = st.text_input("比率（例：3:4）", value="3:4") if ratio_selection == "その他（自由入力）" else ratio_selection
with col2:
    num_images = st.selectbox("出力枚数", list(range(1, 11)))
genre = st.selectbox("ターゲットジャンル", ["指定なし", "1. 美容・コスメ", "2. 健康・ダイエット", "3. 恋愛・婚活", "4. 育児・ファミリー", "5. スピリチュアル・占い", "6. マネー・投資", "7. ビジネス・自己啓発", "8. エンタメ・ゲーム"])

# --- 2. 伝える内容 ---
st.header("2. 伝える内容")
text_strictness = st.radio("テキストのアレンジ", ["🚫 指定した文字だけを厳格に入れる（勝手な追加NG）", "✨ AIにいい感じのサブタイトル等の追加をお任せする"])
content_list = []
for i in range(num_images):
    with st.expander(f"📝 {i+1}枚目のテキスト入力", expanded=(i==0)):
        title = st.text_area(f"タイトル・見出し", key=f"t_{i}", placeholder="例：メンタルが強い人は", height=68)
        details = st.text_area(f"詳細テキスト（1項目ずつ改行）", key=f"d_{i}", placeholder="1. 視点の切り替えが上手い\n2. 溜め込まない\n3. 自分を責めない")
        content_list.append({"slide_number": i+1, "title": title, "details": details.split('\n') if details else []})

# --- 3. 被写体と配置 ---
col3, col4 = st.columns(2)
with col3:
    subject_type = st.selectbox("メインの被写体", ["AIにおまかせ", "自分のキャラクターを使う（画像アップロード）", "入れない"])
with col4:
    char_placement = st.selectbox("キャラクターの配置位置", ["おまかせ", "右下に配置", "左下に配置", "中央に大きく配置", "見切れるように配置"])

# --- 4. デザインの方向性 ---
st.header("3. デザインと構図 🎨")
comp_options = list(composition_dict.keys())
comp_ui = st.selectbox("神・構図リスト", comp_options)
comp_instruction = composition_dict.get(comp_ui, "")

col5, col6 = st.columns(2)
with col5:
    font = st.selectbox("フォント・書体", ["おまかせ", "ゴシック体", "明朝体", "丸ゴシック", "手書き風"])
with col6:
    text_bg = st.selectbox("文字の下敷き", ["✨ おまかせ", "🏷️ タイトルのみ強調", "☁️ 雲の形", "⬜️ 角丸長方形", "なし"])

# --- 🚀 生成（魂の監査・全お説教再実装） ---
if st.button("🪄 読者の心を動かすプロンプトを生成"):
    # 💡 🚨 魂の復旧！キャラクター抽出の厳格ルール 🚨 💡
    if subject_type == "自分のキャラクターを使う（画像アップロード）":
        subject_instruction = "CRITICAL RULE: Extract and reproduce ONLY the character itself from the attached image. You MUST strictly EXCLUDE all props, objects (like laptops, desks, cups, plants), and the original background."
    else:
        subject_instruction = subject_type

    placement_instruction = f"{char_placement}. CRITICAL RULE: This character placement has HIGHEST absolute priority. The design must adapt to this location. DO NOT move the character to fit a grid; move the design to fit the character."
    
    data = {
        "role": "Exclusive AI Image Generation Expert",
        "format": "image_generation",
        "design_concept": {
            "composition_structure": comp_instruction,
            "typography": f"{font}. CRITICAL: Establish a strict visual hierarchy. TITLE MUST BE VISUALLY DOMINANT, SIGNIFICANTLY LARGER AND BOLDER THAN DETAILS.",
            "text_background": text_bg,
            "aspect_ratio": ratio
        },
        "content_per_image": content_list,
        "character_instructions": {"subject": subject_instruction, "placement": placement_instruction},
        "rules": [
            "CRITICAL: Generate EXACTLY the number of sections as detail items provided.",
            "ABSOLUTELY NO DUPLICATE TEXT across steps or blocks. Each element must have unique content.",
            "NEVER draw visible grid lines or crosshairs unless specifically part of the design.",
            "Visual hierarchy must be crystal clear: Large Title, Smaller Details."
        ]
    }
    st.success("究極の完全復旧！全てのこだわりを1文字も漏らさず詰め込んだよ✨")
    st.code(json.dumps(data, indent=4, ensure_ascii=False), language='json')
