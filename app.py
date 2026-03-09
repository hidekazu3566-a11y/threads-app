import streamlit as st
import json

st.set_page_config(page_title="図解プロンプトメーカー", layout="centered")

st.title("🧵 図解プロンプトメーカー")
st.write("専門用語は不要。「どう見せたいか」を選ぶだけで、あなたの想りを形にする最高の図解が作れます✨")

# --- UIとAIへの英語指示の変換辞書 ---
composition_dict = {
"zの法則（視線誘導 × 多キャラ感情同期 × 形状多様性）": (
        "ELITE Z-PATTERN LAYOUT WITH DYNAMIC SHAPE VARIETY & INDIVIDUAL EMOTIONAL GUIDES: "
        
        # 1. 【Z字の視線誘導と分散配置】左上→右上→左下→右下の「Z」の軌道に要素を配置する
        "1. STRICT Z-PATH WITH DISTRIBUTED GUIDES: Arrange visual elements along a clear 'Z' trajectory. "
        "Place a small, unique version of the character next to EACH individual text box as a guide. "

        # 2. 【強弱と視認性の絶対死守】タイトルは巨大、本文はスマホで読めるサイズと太さを維持
        "2. CLEAR VISUAL HIERARCHY: The 'TITLE' MUST be massive, bold, and heavy. "
        "Each detail box MUST contain clearly legible text with medium size and medium font weight for 100% mobile visibility. "

     # 3. 【柔軟な形状の多様性とリズム】全部同じ形にせず、文脈に合わせて自由に形を選ぶ
        "3. DYNAMIC & MEANINGFUL SHAPES: PROHIBIT repetitive box shapes. The AI MUST analyze the text and select from a wide variety of silhouettes. "
        "Prioritize visual rhythm by ensuring each adjacent box has a distinct shape (e.g., stylized panels, organic forms, bubbles, or functional arrows for flow). "
        "Do NOT restrict to a specific set; be creative while keeping it functional and clean. "
        
        # 4. 【個別ボックスごとの感情同期】キャラの表情を隣のテロップの内容に100%合わせる
        "4. INDIVIDUAL BOX EMOTION SYNC: Each character guide MUST have an expression and pose that reflects the specific content of its adjacent text box. "
        "If the text is serious, the character is serious; if it's positive, the character smiles. Use diverse poses (pointing, sleeping, etc.) to match. "

        # 5. 【洗練された密度の引き算】装飾は厳選し、背景には優雅な空気感（抜け感）を持たせる
        "5. SOPHISTICATED DENSITY: Use ONE high-quality visual metaphor/icon per box to avoid clutter. "
        "Maintain 'elegant whitespace' and use very faint background textures to make the unique shapes and characters pop. "
    ),
    "Fの法則（上から下へ項目を読ませる・リスト向け）": (
        "A structured, high-readability layout following the F-shaped reading pattern. "
        "LAYOUT RULE: "
        "1. Position the Title as a dominant horizontal bar across the top. "
        "2. Arrange the detail list items vertically, strictly ALIGNED TO THE LEFT side. "
        "3. Ensure the top few list items have more visual weight or length than the bottom ones. "
        "The character should be placed in the bottom-right corner or integrated as a vertical anchor on the left, but MUST NOT obstruct the left-aligned text path. "
        "Avoid scattered speech bubbles; use clean, structured list panels for a professional editorial feel."
    ),
 "三分割法・黄金比・白銀比（安定と美しさの比率）": (
    "Strict composition adherence to the Rule of Thirds logic. "
    "CRITICAL LAYOUT RULE: "
    # 👇 ここに「1匹制限」を完全復活！
    "1. STRICT SINGLE CHARACTER LIMIT: Under NO circumstances are multiple depictions of the character allowed in the same image frame. Exactly one instance of the main character MUST be present. DO NOT use multiple poses or frames of the same character. "
   # 👇 ここに「文字コントラスト」の指示を追加！（本文が小さくなりすぎないよう調整）
    "2. BALANCED TEXT CONTRAST: Render the title text in a MASSIVE, bold, heavy font. Render all body/detail text in a smaller, light, and clean font to ensure a clear size hierarchy, but CRITICAL: DO NOT make the body text too small. It MUST remain highly legible. "
    # 👇 ここから下は「single」を含め、元の文章を一言一句そのまま復活させたよ！
    "3. Position this single main character dynamically on ONE of the four grid intersection points (power points: top-left, top-right, bottom-left, bottom-right). This single location MUST be selected randomly for each generated image. "
    "4. Group and arrange ALL text elements neatly within the vertical third section opposite the chosen single character placement to perfectly balance the composition. Utilize remaining areas as clean, breathable negative space. "

    "EMOTION SYNC RULE: DRAMATICALLY adapt the single character's facial expressions, body language, and poses to perfectly match the mood. "
    "HIGHLIGHT ANALYSIS RULE: The AI MUST deeply analyze the SPECIFIC meaning of BOTH the LOCAL TITLE TEXT and LOCAL HIGHLIGHTED TEXT. "
    "SPECIFIC MEANING RULE: "
    "- If the SPECIFIC meaning implies struggle (e.g., 'not rewarded', 'tired'), depict visible internal conflict and knitted brows. ZERO TOLERANCE for smiles. "
    "- If the SPECIFIC meaning implies relief or joy (e.g., 'praise', 'warm drink'), depict a genuinely joyful smile. "

    "ABSOLUTELY NO VISIBLE GRID LINES OR CROSSHAIRS."
),
 "日の丸構図（視認性重視 × 密度強化）": (
        "PRECISE CENTERED COMPOSITION (HINOMARU STYLE) WITH RICH DECORATIVE ACCENTS & CONTEXTUAL FLAIR: "
        
        # 1. 【中央のアンカー】メインキャラを中央に配置。
        "1. CENTRAL CHARACTER ANCHOR: Place the main character precisely in the center. Ensure it remains the focal point while allowing decorations to surround it. "

        # 2. 【強弱と視認性】タイトルは巨大、本文は読みやすいサイズ。
        "2. CLEAR VISUAL HIERARCHY: The 'TITLE' MUST be massive and bold. The detail text inside shapes MUST be clearly legible (medium size) with medium font weight. "

        # 3. 【図形とあしらいの装飾（ここを強化！）】
        # ボックス自体を豪華にし、周りにテーマに合った「小道具（あしらい）」を散りばめる指示。
        "3. ORNATE CONTEXTUAL SHAPES: Analyze the text and render each block inside a highly detailed decorative container. "
        "IMPORTANT: Surround each container and the main character with subtle, theme-appropriate 'visual accents' and 'secondary props' (e.g., if the theme is 'home', add floating sparkles, soft leaves, or small interior items around the boxes). "
        "These decorations should fill the whitespace elegantly without cluttering the text. "

        # 4. 【文脈同期型・感情ミラーリング（さっきの柔軟なやつ！）】
        "4. NUANCED EMOTIONAL SYNCHRONIZATION (TITLE-ONLY): Analyze the specific vibe of the 'TITLE'. "
        "IF positive, use a gentle smile or bright joy depending on the intensity. IF negative or serious, ZERO TOLERANCE for smiles—use pensive, focused, or wistful expressions matching the severity. "

        # 5. 【背景と空気感の密度（新設！）】
        # 背景をただの単色にせず、薄っすらと物語を感じさせる装飾を入れる。
        "5. ATMOSPHERIC BACKGROUND DENSITY: Do not use a plain background. Add subtle, faded thematic elements or artistic textures (e.g., soft watercolor splashes, floating particles, or light silhouettes) that match the genre to increase overall visual richness and professionalism. "
    ),
    "対角線・斜め分割（動きとリズム、スピード感を出す）": (
        "A dynamic composition with key elements arranged strictly along strong diagonal lines, conveying movement and speed. "
        "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST deeply analyze the SPECIFIC meaning of the TITLE text first. "
        "SPECIFIC MEANING RULE: "
        "- If the TITLE implies struggle, worry, or pain (e.g., 'not rewarded', 'tired'), depict visible internal conflict and knitted brows. ZERO TOLERANCE for smiles. "
        "- If the TITLE implies joy, success, or excitement (e.g., 'happy', 'achieved'), depict a genuinely joyful and bright smile. "
        "- The character's emotion must strictly reflect the core mood stated in the title to maintain empathy with the viewer."
    ),
    "額縁構図（外枠で囲って中央を際立たせる）": (
        "CRITICAL FRAME & SINGLE SUBJECT RULE: "
        "1. DO NOT draw a literal, physical wooden picture frame. Create a 'decorative border' (e.g., botanical vines, patterns, or motifs) framing the outer edges. "
        "2. STRICT SINGLE SUBJECT LIMIT: Exactly ONE main subject from the provided image MUST be placed as the central focus. DO NOT depict multiple versions of the subject. "

        "EMOTION SYNC RULE: The AI MUST analyze the overall sentiment and energy of the ACTUAL TEXT CONTENT provided in the 'TITLE' and 'HIGHLIGHTS' fields. "
        # ↑【ここ重要！】「TITLE」という単語を探すんじゃなく、そこに入力された「具体的な文章（中身）」を読み取れ、と指示したよ！

        "Adapt the subject's facial expression and pose to perfectly match the intensity of the mood found in that specific text: "
        "- If the text content implies negative emotions (struggle, pain, worry), ZERO TOLERANCE for smiles. Reflect the specific depth of distress found in the words. "
        # ↑【解説】入力された文章が「悩み」系なら笑顔禁止。言葉の重みに表情を100%合わせるよ。

        "- If the text content implies positive emotions (joy, relief, success), reflect a joyful expression that scales directly with the energy and volume of those words. "
        # ↑【解説】入力された文章が「喜び」系なら、その言葉の勢いに合わせて表情を明るくさせるよ。

        "The subject must be the emotional heart of this framed composition."
    ),
    "マス目・タイル配置（均等に枠を分けて情報を整理する）": (
        "A systematic grid layout where 'Text Blocks' (units of text separated by empty entries in the list) are the fundamental units for each tile. "
        # ↑【変更点】「行」ではなく「空白で区切られた塊」を単位に指定！

        "CRITICAL UNIT RULE: Use empty entries in the list as the ONLY hard boundaries for new tiles. Every text unit located between blanks MUST be rendered in its own sovereign, independent tile. "
        # ↑【新ルール】空白を「絶対的なマスの区切り」として定義したよ。

        "DO NOT merge separate blocks (e.g., '喜びの舞をする' and 'わっしょいわっしょい') into one tile if a blank entry exists between them. Treat each block as a distinct data point. "
        # ↑【事故防止】空白があるなら、どんな短い言葉も絶対に統合させない！

        "The number of tiles must exactly match the total count of non-empty text blocks. Ensure structural unity."
        # ↑【整合性】マスの数をブロックの総数とピッタリ一致させる指示だよ。
    ),
"コラージュ型（雑誌風・空白行完全同期×ダーク背景×キャラ極小）": (
    "ELITE MAGAZINE COLLAGE WITH PURE EMPTY-LINE SEGMENTATION: "
    
    # 1. 【メインメッセージの巨大化とラベル化禁止】
    # タイトルを一番大きく描く。余計な「TITLE」などのラベル文字は絶対に入れない。
    "1. PRIMARY MESSAGE SUPREMACY: Render the 'title text' from the content list in a MASSIVE, bold, textured font. "
    "CRITICAL: DO NOT render the word 'TITLE' or 'Subject'. "

    # 2. 【空白行（空行）のみを分離のトリガーにする：最優先ルール】
    # ここが今回の修正の核心であり、あなたの要望を実現する部分です！
    # 前のコードにあった「箇条書き（1. 2. 3.）を守る」という指示は、この確定版では削除されています。
    # 代わりに、連続している行（空行がない行）は、どんな内容（箇条書きかどうか）に関わらず必ず「同じ1枚の紙」に描くこと。
    # 逆に、プロンプトに「明確な空白行」がある場合のみ、そこで紙を切り離して別の破片にすること。
    # 「1. 2. 3.」などの番号の有無は一切関係なく、空行の有無だけで判断してねっていうルール。
    "2. MANDATORY SEGMENTATION BY EMPTY LINES ONLY: "
    "MANDATORY: Render any sequence of text WITHOUT an empty line onto a SINGLE paper scrap. "
    "CRITICAL: The ONLY signal to separate text into different paper scraps is a CLEAR EMPTY LINE. "
    "If there is no empty line, keep the lines together. If there IS an empty line, you MUST terminate the current scrap and start a new one. "
    "Do not ignore empty lines, and do not create new scraps without an empty line. "

    # 3. 【意図的な「崩し」と角度のバラバラ化 ＆ 紙の質感】
    # 紙の破片をそれぞれバラバラのダイナミックな角度で配置。
    # 角度を揃えるのは禁止。手でちぎったような「ビリビリ感（繊維が見える縁）」と影をしっかりつけるよ。
    "3. ARTISTIC ANGLED LAYERING & TORN TEXTURE: PROHIBIT perfectly vertical or horizontal alignment. "
    "Each scrap MUST be tilted at a UNIQUE, DYNAMIC angle to ensure they look like scattered fragments. "
    "PROHIBIT synchronizing the angles of different scraps. Overlap them with deep Drop Shadows. "
    "EVERY scrap MUST have extreme rough-torn, fibrous edges for a tactile texture. "

    # 4. 【背景を「深みのあるネイビー」に固定 ＆ ヴィンテージの汚れ感】
    # ダークネイビーや黒系の背景に、ヴィンテージ風のシミや擦れを足す。
    # 文字が書いてある紙は「明るいオフホワイト」にして、読みやすさを最大にするよ。
    "4. DEEP DARK BASE LAYER & VINTAGE TEXTURE: The background base MUST be a textured paper in a DEEP, RICH color (e.g., Deep Navy, Dark Teal, or Charcoal Black). "
    "CRITICAL VINTAGE VIBE: Add subtle vintage distress (faint stains, scuffs). "
    "Text scraps MUST be bright off-white for maximum legibility. "

    # 5. 【キャラの極小サイズと視線誘導ロック】
    # キャラのサイズは画面の15%以下。視線とポーズはメインテキストを指し示すように固定。
    "5. MINIATURE SCALE & GAZE-LOCK: Render the character in a MINIATURE scale (less than 15% of the area). "
    "The character's gaze and posture MUST point DIRECTLY at the main text scrap. "

    # 6. 【装飾の厳選】
    # 装飾は控えめに。クリップ1個、ピン1個、スタンプ数枚だけを置くよ。
    "6. REFINED SYMBOLIC ACCENTS: Add exactly ONE clip, ONE pin, and a few unique stamps/leaves. PROHIBIT redundancy. "
    ),
   "スペクトル・グラデーション（0〜100%など段階的な変化を表現）": (
        "A full-background gradient infographic on textured paper, flowing smoothly from cool blue (representing low/0%) on the far left to hot red (representing high/100%) on the far right. " # 👈 「背景全体を青から赤へ」に修正！
        "The number of steps MUST EXACTLY MATCH the content list, arranged horizontally from left to right along this color spectrum. " # 👈 「横に並べる」と指示！
        "A central protagonist is integrated tightly with each step's corresponding text box. " # 👈 一体感を維持！
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
        "The main character should be interacting with the tree. NO REPEATING TEXT."
    ),
  "ステップ型（順序解説 × 視線誘導の徹底 × 障害物除去）": (
        "ELITE SEQUENTIAL STEP-FLOW WITH DYNAMIC QUANTITY & START-POINT FOCUS: "
        
        # 1. 【中央のアンカー：1番（左上）への強制誘導】
        "1. CENTRAL STARTING SIGNAL: The center element MUST act as a clear signpost pointing to Step 1 (Top-Left). "
        "CRITICAL: Render a prominent arrow emerging FROM the center title AND pointing DIRECTLY at the Top-Left block. This is the non-negotiable entry point. "

        # 2. 【数（N）に合わせた時計回り配置】
        # 「4個」という固定を捨て、3〜5個の数に合わせて等間隔に配置させる
        "2. DYNAMIC GEOGRAPHICAL LAYOUT: Distribute the provided number of detail blocks (3 to 5) evenly in a clockwise circular or curved path. "
        "Regardless of the count, Step 1 MUST be at the Top-Left. Subsequent blocks follow clockwise (e.g., for 3 blocks: TL, TR, Bottom-Center). "

        # 3. 【論理的なステップ矢印（最後から1への逆流を完全に封じる）】
        # 「最後のブロック」をターゲットにする指示に書き換え！
        "3. FORWARD-ONLY CONNECTORS: Connect blocks ONLY in numerical sequence (1->2, 2->3, etc., up to N). "
        "CRITICAL ERROR AVOIDANCE: ABSOLUTELY PROHIBIT any arrow pointing from the FINAL block in the sequence (the highest number) back to Step 1. "
        "The path MUST end definitively at the final block. Render a 'GOAL' icon (e.g., a flag or medal) next to the final block to signify the conclusion. "

        # 4. 【猫の「避難」配置（矢印の絶対保護）】
        "4. SAFE POSITIONING & LAYER PRIORITY: Arrows MUST be in the absolute foreground. "
        "Character guides MUST be positioned at the outer margins, completely avoiding the logical path of the arrows. No part of a character may obscure any arrow. "

        # 5. 【強弱と視認性】
        "5. CLEAR VISUAL HIERARCHY: Title is massive and bold. Detail text is medium size and weight for 100% legibility on mobile. "

        # 6. 【形状のバリエーション】
        "6. DYNAMIC SHAPE VARIETY: Use diverse silhouettes (bubbles, panels, arrows) to maintain rhythm. ONE high-quality icon per box. "
    ),
    "ルービックキューブ（立体ブロック）（複雑な要素の組み合わせを表現）": (
        "A 3D Rubik's cube structure composition where the individual block panels are SIGNIFICANTLY ENLARGED to maximize surface area. " # 👈 ブロックサイズを「大幅に拡大」する！
        "Prioritize text readability above all. Render all detail text (from the content list) in a VERY LARGE, BOLD, highly legible font (e.g., ゴシック体) within the enlarged panels. " # 👈 「文字の大きさ、太さ、読みやすさ」を最優先！
        "The Title is visually dominant at the top. Use a STRONG visual hierarchy, making the main 'title' significantly LARGER and BOLDER than the 'details' text. " # 👈 タイトルと詳細のメリハリを強化！
        "CRITICAL TEXT RULE: The content list is a STRICT SINGLE-USE INVENTORY. Absolutely zero word-for-word repetition across the entire image. Once an item is placed, it is EXHAUSTED. " # 👈 重複絶対禁止は維持！
        "ILLUSTRATIVE FILLING RULE: If a panel needs filling, add a theme-relevant small illustrative element (icon, prop, or decorative object), NEVER repeated text. Replace exhausted panels with fresh visuals like theme-relevant small icons, keeping the visuals fresh. " # 👈 小物の埋め草は維持！
        "INTEGRATION: The main characters should be actively interacting with the block panels. Ensure clean, instructional aesthetics with clear text hierarchy. "
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
        "The central character should be actively interacting with these giant numbers (e.g., sitting on a giant '90%', hugging a large '5', or leaning against them). "
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
  "タイポグラフィ主役（文字そのものをアートとして見せる）": (
        "An artful typography-first composition focusing purely on the title text as the main visual artwork. "
        "CRITICAL RULE: Render the main title in an EXTREMELY LARGE, BOLD, and highly decorative font style. "
        "The title text size must be at least 3X larger than any detail text, dominating the entire composition. "
        "Add expressive textures, glowing effects, or 3D depth to the title font, treating the letters as a physical object or stage set. "
        "Characters should be intimately integrated with the letters, perhaps resting on, hugging, or peaking from behind the massive typography."
    ),
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
    num_images = 1

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
            "details": [d.strip() for d in img_details.split('\n\n') if d.strip()]
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

    # 👇 289行目（placement_instructionの行）から最後まで全部上書き！
    placement_instruction = f"{char_placement}. CRITICAL RULE: This requested character placement has the HIGHEST absolute priority."

    data_for_gemini = {
        "role": "Exclusive AI Image Generation Expert",
        "format": "image_generation", 
        "objective": f"Generate 1 high-quality image for {use_case}",
        "design_concept": {
            "genre_worldview": genre,
            "style": style,
            "mood_tone": mood,
            "typography": {
                "font_style": font_choice,
                "alignment": text_align
            },
            "text_background": bg_instruction,
           "composition_structure": composition_dict[composition_ui],
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
            "Generate exactly 1 image file immediately. DO NOT output JSON.",
            "Render the provided text naturally on the image. Placement can be flexible.",
            # 👇 ここがポイント！「選んだ構図に合わせろ、勝手に枠を増やすな」という指示
            "Strictly follow the chosen 'composition_structure'. If the selected style is a single-frame composition (like Hinomaru), DO NOT add any grids, sub-panels, or collage elements.",
            "EMPTY SLOT PROTECTOR: If text is empty, do not draw any boxes or frames.",
            text_rule,
          "CRITICAL EMOTION-EXPRESSION SYNC RULE: The AI MUST analyze the SPECIFIC meaning of the text items and adapt the character's expression to match that mood. Avoid generic 'default smiles' UNLESS positive."
        ]
    }

    st.success("✨ 最強プロンプトが完成したよ！黒い枠の中身だけをコピーしてね！")
    st.code(json.dumps(data_for_gemini, indent=4, ensure_ascii=False), language='json')
    st.balloons()
