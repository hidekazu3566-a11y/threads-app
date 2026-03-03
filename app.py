import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想いを形にする最高の図解が作れます✨")

# --- UIとAIへの英語指示の変換辞書（スクショ完全再現！） ---
composition_dict = {
    "Zの法則（左上から右下へ視線を誘導・王道）": "A strong visual hierarchy designed to guide the viewer's eye in a clear Z-shaped pattern across the image.",
    "Fの法則（上から下へ項目を読ませる・リスト向け）": "A strong visual hierarchy designed to guide the viewer's eye in a clear F-shaped pattern across the image, ideal for reading lists.",
    "三分割法・黄金比・白銀比（安定と美しさの比率）": "Strict composition adherence to the Rule of Thirds or Golden Ratio logic to place key elements and focus. TEXT ELEMENTS MUST BE ARRANGED to balance the negative space. ABSOLUTELY NO VISIBLE GRID LINES.",
    "中央集中型・日の丸構図（視線をど真ん中に集める）": "A precise direct centered composition with all focus exclusively on the central subject and title.",
    "対角線・斜め分割（動きとリズム、スピード感を出す）": "A dynamic composition with key elements arranged strictly along strong diagonal lines, conveying movement and speed.",
    "額縁構図（外枠で囲って中央を際立たせる）": "CRITICAL RULE: A visible, distinct decorative frame or border surrounding the entire composition.",
    "マス目・タイル配置（均等に枠を分けて情報を整理する）": "A clean, organized composition structured by a precise grid or tile layout.",
    "破れグリッド・非対称バランス（あえて崩しておしゃれ感や動きを出す）": "CRITICAL RULE: Extreme 'broken grid' editorial layout. TEXT BOXES AND THE CHARACTER MUST HEAVILY OVERLAP. Collage style like a fashion magazine spread.",
    "余白重視（ネガティブスペース）（空白を活かして上品さや高級感を演出）": "A minimalist composition prioritizing a very large amount of clean negative space, creating a profound sense of elegance, luxury, and focus.",
    "シンメトリー（左右対称）（誠実さや静寂を伝える）": "A perfectly symmetrical composition, creating a sense of visual integrity, solemnity, and peace.",
    # スクショのトライアングル！
    "トライアングル（三角構図）（圧倒的な安定感や成長を出す）": "CRITICAL RULE: Strict implied triangle composition created ONLY by the non-linear, dynamic placement of elements. ABSOLUTELY NO VISIBLE TRIANGLE SHAPES OR OUTLINES. Conveying extreme stability and harmonized structure through powerful diagonal flow. Focal point (e.g., character/cat) MUST BE PLACED at a dynamically staggered apex, and supporting elements (e.g., text blocks) MUST BE ARRANGED to form a distinct, wide base with clear diagonal lines connecting to the apex. DO NOT align character and text blocks vertically; use strong diagonal angles to create a visual pyramid flow.",
    
    # 💡 🚨 スクショ完全再現！SWOTの改造コメントも！
    # 💡 🚨 ここを大改造！SWOTを汎用的な「4分割」に変更！🚨
    "4分割・ブロック配置（情報を4つのエリアに分ける）": "A clean, structured infographic layout divided into four distinct, equal quadrants or numbered blocks. TEXT ELEMENTS (from the details list) are ARRANGED sequentially within these four sections, ensuring a clear and balanced division of information. No specific labeling (like SWOT) is required; use generic numbering (1, 2, 3, 4) or simple titles based on the text provided.",
    
    # スクショ完全再現！名前も「ジャーニーマップ」に戻した！
    "--- ジャーニーマップ（時系列と感情の起伏を波で表現） ---": "A chronological infographic timeline showing emoji-based emotional ups and downs along a visual wave-like chart.",
    
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

# --- 1. 基本設定 ---
st.header("1. 作りたい画像の設定")
use_case = st.selectbox("用途", ["図解（SNS・プレゼン用）", "サムネイル（YouTube・記事用）", "汎用画像生成（自由設定）"])
col1, col2 = st.columns(2)
with col1:
    ratio_selection = st.selectbox("キャンバス比率", ["1:1 (正方形)", "4:5 (縦長)", "16:9 (横長)", "9:16 (縦長フル)", "その他（自由入力）"])
    ratio = st.text_input("比率（例：3:4）", value="3:4") if ratio_selection == "その他（自由入力）" else ratio_selection
with col2:
    num_images = st.selectbox("出力枚数", list(range(1, 11)))
genre = st.selectbox("ターゲットジャンル", ["指定なし", "美容", "健康", "恋愛", "育児", "スピリチュアル", "マネー", "ビジネス", "エンタメ"])

# 🚨 スクショ通り、余計な「スタイル」とかはナシ！

# --- 2. 伝える内容 ---
st.header("2. 伝える内容")
text_strictness = st.radio("アレンジ", ["🚫 厳格（文字のみ）", "✨ おまかせ（追加OK）"])
content_list = []
for i in range(num_images):
    with st.expander(f"📝 {i+1}枚目", expanded=(i==0)):
        title = st.text_area(f"タイトル", key=f"t_{i}", placeholder="例：メンタルが強い人は", height=68)
        details = st.text_area(f"詳細テキスト（1項目ずつ改行してね）", key=f"d_{i}", placeholder="1. 視点の切り替えが上手い\n2. 溜め込まない\n3. 自分を責めない")
        content_list.append({"slide_number": i+1, "title": title, "details": details.split('\n') if details else []})

# --- 3. 被写体と配置 ---
col3, col4 = st.columns(2)
with col3:
    subject = st.selectbox("被写体", ["AIにおまかせ", "自分のキャラ（画像添付）", "なし"])
with col4:
    placement = st.selectbox("キャラクターの配置位置", ["おまかせ", "右下", "左下", "中央"]) # スクショのUI名に修正

# --- 4. デザインと構図 ---
st.header("3. デザインと構図 🎨")
comp_options = list(composition_dict.keys())
comp_ui = st.selectbox("神・構図リスト", comp_options)
comp_instruction = composition_dict.get(comp_ui, "")

col5, col6 = st.columns(2)
with col5:
    font = st.selectbox("フォント・書体", ["おまかせ", "ゴシック", "明朝", "丸ゴシック", "手書き風"])
with col6:
    text_bg = st.selectbox("文字の下敷き", ["✨ おまかせ", "🏷️ タイトルのみ強調", "☁️ 雲", "⬜️ 角丸", "なし"])

# --- 🚀 生成 ---
if st.button("🪄 読者の心を動かすプロンプトを生成"):
    # 💡 🚨 魂の復旧！キャラクター抽出の厳格ルール 🚨 💡
    if subject == "自分のキャラ（画像添付）":
        subject_instruction = "CRITICAL RULE: Extract and reproduce ONLY the character itself from the attached image. You MUST strictly EXCLUDE all props, objects (like laptops, desks, cups, plants), and the original background."
    else:
        subject_instruction = subject

    data = {
        "role": "Exclusive AI Image Generation Expert",
        "format": "image_generation",
        "design_concept": {
            "composition": comp_instruction,
            "typography": font,
            "text_background": text_bg,
            "aspect_ratio": ratio
        },
        "content": content_list,
        "character": {"subject": subject_instruction, "placement": placement},
        "rules": [
            "Use the exact layout described in 'composition'.",
            "Generate unique visual context for each detail item."
        ]
    }
    st.success("完成！コピーしてGeminiに貼ってね✨")
    st.code(json.dumps(data, indent=4, ensure_ascii=False), language='json')
