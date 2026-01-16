import streamlit as st
import pandas as pd
import json

# ---------------------------------------------------------
# 1. 환경 설정 & 데이터 로드
# ---------------------------------------------------------
st.set_page_config(page_title="Blox Fruits 거래 판독기", layout="wide", page_icon="⚖️")

# CSS 스타일링 (탭 디자인 및 전체 꾸미기)
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp { background-color: #0E1117; color: white; }
    
    /* 상단 헤더 숨기기 & 여백 최소화 */
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
    }

    /* 탭(Tab) 스타일 변경 */
    button[data-baseweb="tab"] {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: #888 !important;
        background-color: #1E1E1E !important;
        border-radius: 5px !important;
        margin: 0 5px !important;
        border: 1px solid #333 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0E1117 !important;
        background-color: #FFD700 !important; /* 선택된 탭: 금색 배경 */
        border: 1px solid #FFD700 !important;
    }

    /* Metric 스타일 */
    [data-testid="stMetricLabel"] { color: #dcdcdc !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }

    /* 카드 리스트 스타일 */
    .fruit-row {
        display: flex; align-items: center; 
        background-color: #1E1E1E; 
        margin-bottom: 8px; padding: 10px; 
        border-radius: 8px; border: 1px solid #333;
    }
    .fruit-img { width: 45px; height: 45px; object-fit: contain; margin-right: 15px; }
    .price-text { color: #FFD700; font-weight: bold; font-size: 1rem; }
    
    /* 선택된 아이템 스타일 */
    .selected-item-box {
        text-align: center; margin: 5px 0; background-color: #262730;
        border-radius: 8px; padding: 5px; border: 1px solid #444;
    }
    .selected-img { width: 40px; height: 40px; object-fit: contain; }
    .selected-name {
        font-size: 0.7em; color: #ddd; margin-top: 3px; 
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    
    /* 총 가치 스코어보드 스타일 */
    .total-box {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 10px; border-radius: 10px; text-align: center; margin-top: 10px;
        border: 2px solid #444;
    }
    .total-label { font-size: 0.8em; color: #aaa; margin-bottom: 2px; }
    .total-value { font-size: 1.5em; font-weight: bold; color: #FFD700; }
</style>
""", unsafe_allow_html=True)

# JSON 파일 로드
try:
    with open('fruits_data.json', 'r', encoding='utf-8') as f:
        FRUITS_DB = json.load(f)
except FileNotFoundError:
    st.error("🚨 데이터 파일을 찾을 수 없습니다.")
    FRUITS_DB = []

# 한글 이름 매핑
NAME_MAP = {
    "Kitsune": "키츠네", "West Dragon": "서쪽 용", "East Dragon": "동쪽 용", "Dragon": "용",
    "Leopard": "레오파드", "Dough": "도우(떡)", "T-Rex": "티렉스", "Spirit": "스피릿(영혼)",
    "Venom": "베놈(독)", "Control": "컨트롤", "Mammoth": "맘모스", "Shadow": "그림자",
    "Gravity": "중력", "Blizzard": "눈보라", "Pain": "페인", "Lightning": "번개",
    "Portal": "포탈", "Phoenix": "불사조", "Sound": "소리", "Spider": "거미",
    "Love": "러브", "Buddha": "부처(대불)", "Quake": "흔들", "Magma": "마그마",
    "Ghost": "유령", "Rubber": "고무", "Light": "빛", "Diamond": "다이아",
    "Dark": "어둠", "Sand": "모래", "Ice": "얼음", "Flame": "이글",
    "Spike": "가시", "Smoke": "연기", "Bomb": "폭탄", "Spring": "용수철",
    "Spin": "회전", "Rocket": "로켓", "Yeti": "예티", "Gas": "가스",
    "Tiger": "호랑이", "Fruit Notifier": "탐지기", "Dark Blade": "요루(닥블)",
    "Rumble": "럼블", "Barrier": "배리어", "Chop": "동강", "Falcon": "매"
}

# 데이터프레임 변환
df = pd.DataFrame(FRUITS_DB)
if not df.empty:
    df['value'] = df['value'].fillna(0).astype(int)
    
    def get_tier(value):
        if value >= 100000000: return "SS"
        elif value >= 20000000: return "S"
        elif value >= 5000000: return "A"
        elif value >= 1000000: return "B"
        else: return "C"
    
    def make_display_name(eng_name):
        kor = NAME_MAP.get(eng_name, "")
        if kor: return f"{eng_name} ({kor})"
        return eng_name

    df['tier'] = df['value'].apply(get_tier)
    df['display_name'] = df['name'].apply(make_display_name)

# ---------------------------------------------------------
# 2. 메인 화면 구성 (탭 방식)
# ---------------------------------------------------------
st.title("⚖️ Blox Fruits 거래 판독기")

# [핵심 변경] 사이드바 대신 상단 탭 사용
tab_calc, tab_tier = st.tabs(["🧮 거래 계산기", "💰 시세 등급표"])

# =========================================================
# 탭 1: 거래 계산기
# =========================================================
with tab_calc:
    st.markdown("##### 아이템을 선택하고 검은 배경을 터치하세요!")
    
    col1, col2 = st.columns([1, 1]) # 모바일에서는 1:1 비율이 더 보기 좋음

    # === [왼쪽] My Offer ===
    with col1:
        st.markdown("### 📤 나 (줌)")
        my_offer_names = st.multiselect("내 아이템", df['display_name'].tolist(), key="my_offer", label_visibility="collapsed", placeholder="내 아이템 선택")
        
        my_total = 0
        if my_offer_names:
            for d_name in my_offer_names:
                row = df[df['display_name'] == d_name].iloc[0]
                my_total += row['value']
                st.markdown(f"""
                <div class="selected-item-box">
                    <img src="{row['image']}" class="selected-img">
                    <div class="selected-name">{row['name']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown(f"""<div class="total-box"><div class="total-label">내 가치</div><div class="total-value">${my_total:,}</div></div>""", unsafe_allow_html=True)

    # === [오른쪽] Their Offer ===
    with col2:
        st.markdown("### 📥 상대 (받음)")
        their_offer_names = st.multiselect("상대 아이템", df['display_name'].tolist(), key="their_offer", label_visibility="collapsed", placeholder="상대 아이템 선택")
        
        their_total = 0
        if their_offer_names:
            for d_name in their_offer_names:
                row = df[df['display_name'] == d_name].iloc[0]
                their_total += row['value']
                st.markdown(f"""
                <div class="selected-item-box">
                    <img src="{row['image']}" class="selected-img">
                    <div class="selected-name">{row['name']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""<div class="total-box"><div class="total-label">상대 가치</div><div class="total-value">${their_total:,}</div></div>""", unsafe_allow_html=True)

    # === 분석 결과 ===
    st.markdown("---")
    
    diff = their_total - my_total
    
    # 결과 메시지 생성
    if diff > 0: 
        result_msg = f"🚀 대박 이득! (+${diff:,})"
        box_color = "rgba(0, 255, 0, 0.2)"
        border_color = "green"
        main_msg = f"✅ **대박! (+${diff:,}) 이득입니다.**"
    elif diff < 0: 
        result_msg = f"😭 손해 주의.. (-${abs(diff):,})"
        box_color = "rgba(255, 0, 0, 0.2)"
        border_color = "red"
        main_msg = f"🔻 **손해입니다! (-${abs(diff):,})**"
    else: 
        result_msg = "⚖️ 완벽한 공정 거래!"
        box_color = "rgba(100, 100, 100, 0.2)"
        border_color = "gray"
        main_msg = "⚖️ **가치가 동일합니다.**"

    if my_offer_names or their_offer_names:
        # 결과 박스 디자인 강화
        st.markdown(f"""
        <div style="background-color: {box_color}; padding: 15px; border-radius: 10px; border: 2px solid {border_color}; text-align: center; margin-bottom: 20px;">
            <h3 style="margin:0;">{main_msg}</h3>
        </div>
        """, unsafe_allow_html=True)

        # 공유 기능 (복사 박스)
        share_text = f"""[Blox Fruits 거래 결과]
📤 나: {', '.join(my_offer_names) if my_offer_names else '없음'}
📥 상대: {', '.join(their_offer_names) if their_offer_names else '없음'}
----------------
📊 {result_msg}
💰 나: ${my_total:,} vs 상대: ${their_total:,}
----------------
🔗 계산기 바로가기:
https://blox-fruits-calculator.streamlit.app"""
        
        with st.expander("📤 친구에게 결과 공유하기 (클릭)"):
            st.code(share_text, language="text")
    else:
        st.info("👆 위에서 아이템을 선택하면 결과를 분석해 드립니다.")

# =========================================================
# 탭 2: 시세 등급표
# =========================================================
with tab_tier:
    st.markdown("##### 🏆 현재 서버 시세 TOP 3")
    
    # TOP 3 로직
    sorted_df = df.sort_values(by='value', ascending=False)
    top3 = sorted_df.head(3)
    
    c1, c2, c3 = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
    
    for idx, (col, medal, color) in enumerate(zip([c1, c2, c3], medals, colors)):
        row = top3.iloc[idx]
        with col:
            st.markdown(f"""
            <div style="background-color: #262730; padding: 10px; border-radius: 10px; border: 2px solid {color}; text-align: center;">
                <div style="font-size: 1.5em;">{medal}</div>
                <img src="{row['image']}" style="width: 50px; height: 50px; object-fit: contain;">
                <div style="font-size: 0.8em; font-weight: bold; margin-top: 5px; color: {color};">{row['display_name'].split('(')[0]}</div>
                <div style="font-size: 0.9em; font-weight: bold;">${row['value']:,}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📊 전체 등급표")
    
    sub_tabs = st.tabs(["💎 SS", "🥇 S", "🥈 A", "🥉 B", "🧱 C"])
    tier_keys = ["SS", "S", "A", "B", "C"]

    for i, tier in enumerate(tier_keys):
        with sub_tabs[i]:
            items = df[df['tier'] == tier].sort_values(by='value', ascending=False)
            for _, row in items.iterrows():
                trend_icon = "🔥" if row['trend'] == "Overpaid" else "➖"
                st.markdown(f"""
                <div class='fruit-row'>
                    <img src="{row['image']}" class='fruit-img'>
                    <div style='flex-grow: 1;'>
                        <div style='font-weight: bold; font-size: 0.9rem;'>{row['display_name']}</div>
                    </div>
                    <div style='text-align: right;'>
                        <div class='price-text'>${row['value']:,}</div>
                        <div style='font-size: 0.7em; color: #aaa;'>{trend_icon}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 하단 푸터 (방문자 수 등)
# ---------------------------------------------------------
st.markdown("---")
st.caption("Updated: 2026.01.16 | Made in Fukuoka ✈️")
st.markdown("![Visitors](https://api.visitorbadge.io/api/visitors?path=blox-fruits-calculator.streamlit.app&label=VISITORS&countColor=%23FFD700&style=flat&labelStyle=upper)")
