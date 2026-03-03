import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想いを形にする最高の図解が作れます✨")

# --- UIとAIへの英語指示の変換辞書 ---
composition_dict = {
    "Zの法則（左上から右下へ視線を誘導・王道）": "A strong visual hierarchy designed to guide the viewer's eye in a clear Z-shaped pattern across the image.",
    "Fの法則（上から下へ項目を読ませる・リスト向け）": "A strong visual hierarchy designed to guide the viewer's eye in a clear F-shaped pattern across the image, ideal for reading lists.",
    "三分割法・黄金比・白銀比（安定と美しさの比率）": "Strict composition adherence to the Rule of Thirds or Golden Ratio logic to place key elements and focus. TEXT ELEMENTS MUST BE ARRANGED to balance the negative space. ABSOLUTELY NO VISIBLE GRID LINES.",
    "中央集中型・日の丸構図（視線をど真ん中に集める）": "A precise direct centered composition with all focus exclusively on the central subject and title.",
    "対角線・斜め分割（動きとリズム、スピード感を出す）": "A dynamic composition with key elements arranged strictly along strong diagonal lines, conveying movement and speed.",
    "額縁構図（外枠で囲って中央を際立たせる）": "CRITICAL RULE: A visible, distinct decorative frame or border surrounding the entire composition.",
    "マス目・タイル配置（均等に枠を分けて情報を整理する）": "A clean, organized composition structured by a precise grid or tile layout.",
    "破れグリッド・非対称バランス（あえて崩しておしゃれ感や動きを出す）": "CRITICAL RULE: Extreme 'broken grid' editorial layout. TEXT BOXES AND THE CHARACTER MUST HEAVILY OVERLAP. Collage style like a fashion magazine spread.",
    "余白重視（ネガティブスペース）（空白を活かして上品さや高級感を演出）": "A minimalist composition prioritizing a very large amount of clean negative space.",
    "シンメトリー（左右対称）（誠実さや静寂を伝える）": "A perfectly symmetrical composition, creating a sense of visual integrity and peace.",
    "トライアングル（三角構図）（圧倒的な安定感や成長を出す）": "CRITICAL RULE: Implied triangle composition created ONLY by element placement. NO VISIBLE TRIANGLES. Apex character, base text blocks.",
    "4分割・ブロック配置（情報を4つのエリアに分ける）": "A clean infographic layout divided into four distinct, equal quadrants. Arrange text elements sequentially. ABSOLUTELY NO DUPLICATE TEXT IN BLOCKS. Each block must have unique content.",
    "ステップ・感情フロー（手順と気持ちの変化を見せる）": "A chronological infographic showing a sequence of steps or a 'journey'. Use a wavy path or line connecting unique icons and text blocks. Include visual indicators of emotional high/low points (e.g., small heart or star icons) along the path. Each step MUST have unique, non-repeating text.",
    "レーダーチャート（クモの巣）（複数の評価軸で総合力を可視化）": "A precise radar chart infographic (spider chart) showing multiple evaluation axes.",
    "ロジックツリー（「なぜ？」「どうやって？」を枝状に分解）": "A branched issue tree infographic layout strictly decomposing a main concept.",
    "--- ストーリー4コマ・カルーセル絵巻 ---": "A narrative composition structured for a continuous story or carousel spread.",
    "数字・データビジュアル（大きな数字で事実をガツンと伝える）": "A graphic composition focusing heavily on very large, bold numbers.",
    "ヒーローショット（主役を全画面でドーンと見せる）": "An epic hero shot where the subject and title fill the entire screen with maximum impact.",
    "重ね合わせ（レイヤー）（奥行きや深みを出す）": "A layered composition with overlapping elements to create depth.",
    "シルエット・逆光（エモいムードを演出）": "A moody composition using strong backlighting and silhouettes for mysterious beauty.",
    "鏡面・リフレクション（二面性や夢幻的な美しさを出す）": "A dreamlike composition with a mirror-like reflection (e.g., in water).",
    "タロットカード・星座マッピング（神秘的な世界観）": "A mystical composition adhering to a tarot card or celestial map layout.",
    "モノクロ＋1色スポットライト（強烈に強調）": "mostly monochrome with strictly one specific element highlighted in a single vibrant color.",
    "問い→答え開示（スワイプ前提のギミック）": "A teaser composition where the main image poses a question, designed for a swipe-to-reveal effect.",
    "タイポグラフィ主役（文字をアートとして見せる）": "An artful typography-first composition where the text itself is the main visual art."
}

# --- 画風の変換辞書 ---
style_dict = {
    "ほのぼの可愛い水彩画風": "Soft, warm watercolor illustration style with gentle brush strokes and pastel tones.",
    "かわい系（ちびキャラ・パステル）": "Cute chibi character style with pastel color palette and kawaii aesthetics.",
    "ビジネス系（誠実・青基調・信頼感）": "Professional corporate style with a blue-based color scheme conveying trust and reliability.",
    "超リアルな実写写真": "Hyper-realistic photographic style, indistinguishable from a real photograph.",
    "おしゃれな3Dアニメ風": "Stylish 3D anime-inspired rendering with smooth shading and vibrant colors.",
    "レトロなフィルム写真風": "Vintage retro film photography style with grain, warm tones, and nostalgic atmosphere.",
    "スタイリッシュなベクターアート": "Clean, modern vector art style with flat design elements and bold shapes.",
    "エモい写真風": "Emotional, atmospheric photography style with cinematic lighting and mood.",
    "ゲーム風ドット絵": "Retro pixel art style inspired by classic video games.",
    "ネオンサイン系": "Neon sign aesthetic with glowing lights against a dark background."
}

# --- 1. 基本設定（用途・サイズ・ジャンル・枚数） ---
st.header("1. 作りたい画像の設定")
use_case = st.selectbox("用途", ["図解（SNS・プレゼン用）", "サムネイル（YouTube・記事用）", "汎用画像生成（自由設定）"])

col1, col2 = st.columns(2)
with col1:
    ratio_selection = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)", "その他（自由入力）"])
    ratio = st.text_input("比率（例：3:4）", value="3:4") if ratio_selection == "その他（自由入力）" else ratio_selection

with col2:
    num_images = st.selectbox("出力枚数", list(range(1, 11)))

genre = st.selectbox("ターゲットジャンル", ["指定なし", "美容", "健康", "恋愛", "育児", "スピリチュアル", "マネー", "ビジネス", "エンタメ"])

# --- 2. 伝える内容 ---
st.header("2. 伝える内容")
text_strictness = st.radio("テキストのアレンジ", ["🚫 指定した文字だけを厳格に入れる（勝手な追加NG）", "✨ AIにいい感じのサブタイトル等の追加をお任せする"])

content_list = []
for i in range(num_images):
    with st.expander(f"📝 {i+1}枚目"):
        title = st.text_area(f"タイトル", key=f"t_{i}", placeholder="例：メンタルが強い人は", height=68)
        details = st.text_area(f"詳細テキスト", key=f"d_{i}", placeholder="1つずつ改行してね")
        content_list.append({"slide_number": i+1, "title": title, "details": details.split('\n') if details else []})

# --- 3. 被写体と配置 ---
col3, col4 = st.columns(2)
with col3:
    subject = st.selectbox("被写体", ["自分のキャラ（画像添付）", "AIにおまかせ", "なし"])
with col4:
    placement = st.selectbox("配置", ["おまかせ", "右下", "左下", "中央"])

# --- 4. デザインの方向性 ---
st.header("3. デザインと構図 🎨")

# 🎨 メインテイスト（画風）
style = st.selectbox("メインテイスト（画風）", list(style_dict.keys()))
style_instruction = style_dict.get(style, "")

comp_options = [k for k in composition_dict.keys()]
comp_ui = st.selectbox("神・構図リスト", comp_options)
comp_instruction = composition_dict.get(comp_ui, "")

col5, col6 = st.columns(2)
with col5:
    font = st.selectbox("書体", ["おまかせ", "ゴシック", "明朝", "丸ゴシック", "手書き風"])
with col6:
    text_bg = st.selectbox("文字の下敷き", ["✨ おまかせ", "🏷️ タイトルのみ強調", "☁️ 雲", "⬜️ 角丸", "なし"])

# --- 🚀 生成 ---
if st.button("🪄 プロンプト生成"):
    data = {
        "role": "Exclusive AI Image Generation Expert",
        "format": "image_generation",
        "design_concept": {
            "style": style_instruction,
            "composition": comp_instruction,
            "typography": f"{font}, title must be much LARGER than details. NO DUPLICATE TEXT ALLOWED.",
            "text_background": text_bg,
            "aspect_ratio": ratio
        },
        "content": content_list,
        "character": {"subject": subject, "placement": placement},
        "rules": ["NO REPEATING TEXT.", "Distinct visual hierarchy.", "Unique icons for steps."]
    }
    st.success("完成！コピーしてGeminiに貼ってね✨")
    st.code(json.dumps(data, indent=4, ensure_ascii=False), language='json')
