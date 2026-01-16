import streamlit as st
import pandas as pd
import json

# ---------------------------------------------------------
# 1. 환경 설정 & 데이터 로드
# ---------------------------------------------------------
st.set_page_config(page_title="Blox Fruits 거래 판독기", layout="wide", page_icon="⚖️")

# JSON 파일 로드 (같은 폴더에 fruits_data.json이 있어야 함)
try:
    with open('fruits_data.json', 'r', encoding='utf-8') as f:
        FRUITS_DB = json.load(f)
except FileNotFoundError:
    st.error("🚨 'fruits_data.json' 파일을 찾을 수 없습니다! 데이터 파일을 확인해주세요.")
    FRUITS_DB = []

# [한글 패치] 이름 매핑 사전 (주요 열매 및 아이템)
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

# 데이터프레임 변환 및 전처리
df = pd.DataFrame(FRUITS_DB)

if not df.empty:
    df['value'] = df['value'].fillna(0).astype(int)
    
    # 1. 등급 자동 판정 함수
    def get_tier(value):
        if value >= 100000000: return "SS"
        elif value >= 20000000: return "S"
        elif value >= 5000000: return "A"
        elif value >= 1000000: return "B"
        else: return "C"
    
    # 2. 표시용 이름(한글 포함) 생성 함수
    def make_display_name(eng_name):
        kor = NAME_MAP.get(eng_name, "")
        if kor:
            return f"{eng_name} ({kor})"
        return eng_name

    df['tier'] = df['value'].apply(get_tier)
    df['display_name'] = df['name'].apply(make_display_name)

# ---------------------------------------------------------
# 2. CSS 스타일링 (디자인 최종 수정)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp { background-color: #0E1117; color: white; }
    
    /* [상단 공란 제거] 헤더 숨기기 & 여백 최소화 */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* [분석 결과 가독성] Metric 글자색 강제 변경 */
    [data-testid="stMetricLabel"] {
        color: #dcdcdc !important; /* 라벨: 밝은 회색 */
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important; /* 값: 완전 흰색 */
    }

    /* [사이드바 디자인] 배경 및 글자색 변경 */
    [data-testid="stSidebar"] {
        background-color: #262730; /* 어두운 배경 */
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFD700 !important; /* 제목: 금색 */
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important; /* 본문: 흰색 */
        font-size: 1.05em;
    }

    /* 카드 리스트 스타일 */
    .fruit-row {
        display: flex; align-items: center; 
        background-color: #1E1E1E; 
        margin-bottom: 8px; padding: 10px; 
        border-radius: 8px; border: 1px solid #333;
    }
    .fruit-row:hover { border: 1px solid #FFD700; transition: 0.3s; transform: scale(1.01); }
    .fruit-img { width: 50px; height: 50px; object-fit: contain; margin-right: 15px; }
    .price-text { color: #FFD700; font-weight: bold; }
    
    /* 선택된 아이템 스타일 */
    .selected-item-box {
        text-align: center; margin: 5px 0; background-color: #262730;
        border-radius: 8px; padding: 8px; border: 1px solid #444;
    }
    .selected-img { width: 50px; height: 50px; object-fit: contain; }
    .selected-name {
        font-size: 0.75em; color: #ddd; margin-top: 5px; 
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    
    /* 총 가치 스코어보드 스타일 */
    .total-box {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 15px; border-radius: 12px; text-align: center; margin-top: 15px;
        border: 2px solid #444; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .total-label { font-size: 0.9em; color: #aaa; margin-bottom: 5px; }
    .total-value { font-size: 1.8em; font-weight: bold; color: #FFD700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. 사이드바 메뉴 구성
# ---------------------------------------------------------
with st.sidebar:
    st.header("메뉴 (Menu)")
    menu = st.radio("이동할 페이지:", ["🧮 거래 계산기", "💰 시세 등급표"])
    st.markdown("---")
    st.caption("Updated: 2026.01.16")
    # ... (사이드바의 기존 코드들: 메뉴, 업데이트 날짜 등) ...
    st.caption("Made in Fukuoka ✈️")
    
    # [NEW] 방문자 수 배지 (여기에 붙여넣으세요!)
    st.markdown("---")
    st.markdown("![Visitors](https://api.visitorbadge.io/api/visitors?path=blox-fruits-calculator.streamlit.app&label=VISITORS&countColor=%23FFD700&style=flat&labelStyle=upper)")

# ---------------------------------------------------------
# 4. 페이지 1: 거래 계산기
# ---------------------------------------------------------
if menu == "🧮 거래 계산기":
    st.title("⚖️ Blox Fruits 거래 가격 판독기")
    st.markdown("##### 내 거래가 이득일까? 아이템을 선택하고 바로 확인하세요!", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([4, 1, 4])

    # === [왼쪽] My Offer ===
    with col1:
        st.markdown("### 📤 My Offer (줌)")
        my_offer_names = st.multiselect("내 아이템 검색", df['display_name'].tolist(), key="my_offer", placeholder="아이템 선택...")
        
        my_total = 0
        if my_offer_names:
            img_cols = st.columns(3) # 모바일 최적화 (3열)
            for idx, d_name in enumerate(my_offer_names):
                row = df[df['display_name'] == d_name].iloc[0]
                my_total += row['value']
                with img_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="selected-item-box">
                        <img src="{row['image']}" class="selected-img">
                        <div class="selected-name">{row['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown(f"""<div class="total-box"><div class="total-label">내 총 가치</div><div class="total-value">${my_total:,}</div></div>""", unsafe_allow_html=True)

    # === [가운데] VS ===
    with col2:
        st.write(""); st.write(""); st.write("") 
        st.markdown("<h2 style='text-align: center; color: #888;'>VS</h2>", unsafe_allow_html=True)

    # === [오른쪽] Their Offer ===
    with col3:
        st.markdown("### 📥 Their Offer (받음)")
        their_offer_names = st.multiselect("상대 아이템 검색", df['display_name'].tolist(), key="their_offer", placeholder="아이템 선택...")
        
        their_total = 0
        if their_offer_names:
            img_cols = st.columns(3)
            for idx, d_name in enumerate(their_offer_names):
                row = df[df['display_name'] == d_name].iloc[0]
                their_total += row['value']
                with img_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="selected-item-box">
                        <img src="{row['image']}" class="selected-img">
                        <div class="selected-name">{row['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown(f"""<div class="total-box"><div class="total-label">상대 총 가치</div><div class="total-value">${their_total:,}</div></div>""", unsafe_allow_html=True)

    # === 결과 분석 ===
    st.markdown("---")
    st.subheader("📊 분석 결과")
    
    diff = their_total - my_total

    if my_offer_names or their_offer_names:
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("내 가치 합계", f"${my_total:,}")
        with m2: st.metric("차익 (이득/손해)", f"${diff:,}", delta=diff)
        with m3: st.metric("상대 가치 합계", f"${their_total:,}")

        st.write("")
        result_msg = "" # 공유용 텍스트 변수
        
        if diff > 0: 
            st.success(f"✅ **대박! (+${diff:,}) 이득입니다.** 교환을 추천합니다.")
            result_msg = f"🚀 대박 이득! (+${diff:,}) 나만 믿고 거래해!"
        elif diff < 0: 
            st.error(f"🔻 **손해입니다! (-${abs(diff):,})** 교환을 다시 생각해보세요.")
            result_msg = f"😭 으악 손해다.. (-${abs(diff):,}) 말려줘서 고마워.."
        else: 
            st.info("⚖️ **가치가 동일합니다.** 공정한 거래입니다.")
            result_msg = "⚖️ 완벽하게 공정한 엄대엄 거래!"

        # ---------------------------------------------------------
        # [NEW] 친구에게 자랑하기 (텍스트 복사 기능)
        # ---------------------------------------------------------
        st.write("")
        st.write("")
        st.markdown("##### 📤 친구에게 결과 공유하기")
        
        # 복사할 텍스트 만들기
        share_text = f"""[Blox Fruits 거래 판독기 결과]
📤 나: {', '.join(my_offer_names) if my_offer_names else '없음'}
📥 상대: {', '.join(their_offer_names) if their_offer_names else '없음'}
--------------------------------
📊 결과: {result_msg}
💰 내 가치: ${my_total:,} vs 상대 가치: ${their_total:,}
--------------------------------
🔗 나도 계산하러 가기:
https://blox-fruits-calculator.streamlit.app"""
        
        # 1. 캡처 유도 멘트
        st.caption("📸 화면을 캡처해서 친구에게 보내거나, 아래 텍스트를 복사하세요!")
        
        # 2. 복사하기 쉬운 코드 블록 (우측 상단에 복사 버튼이 자동으로 생김)
        st.code(share_text, language="text")

    else:
        st.info("👆 위에서 아이템을 선택하면 결과를 분석해 드립니다.")
# ---------------------------------------------------------
# 5. 페이지 2: 시세 등급표
# ---------------------------------------------------------
elif menu == "💰 시세 등급표":
    st.header("💰 시장 가치 티어표 (Market Value)")
    st.caption("※ 실제 거래되는 시세를 기준으로 한 순위입니다.")
    st.markdown("---")

    tabs = st.tabs(["💎 SS급", "🥇 S급", "🥈 A급", "🥉 B급", "🧱 C급"])
    tier_keys = ["SS", "S", "A", "B", "C"]

    for i, tier in enumerate(tier_keys):
        with tabs[i]:
            items = df[df['tier'] == tier].sort_values(by='value', ascending=False)
            st.markdown(f"**총 {len(items)}개 아이템**")
            
            for _, row in items.iterrows():
                trend_icon = "🔥" if row['trend'] == "Overpaid" else "➖"
                
                st.markdown(f"""
                <div class='fruit-row'>
                    <img src="{row['image']}" class='fruit-img'>
                    <div style='flex-grow: 1;'>
                        <div style='font-weight: bold;'>{row['display_name']}</div>
                        <div style='font-size: 0.8em; color: #aaa;'>{row['category']}</div>
                    </div>
                    <div style='text-align: right;'>
                        <div class='price-text'>${row['value']:,}</div>
                        <div style='font-size: 0.8em; color: #aaa;'>{trend_icon} {row['trend']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
