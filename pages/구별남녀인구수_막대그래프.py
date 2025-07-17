import streamlit as st
import pandas as pd

st.title("2025년 6월 기준 주민등록 인구 및 세대 현황 분석")

# CSV 파일 경로
FILE_PATH = "202506_202506_주민등록인구및세대현황_월간.csv"

# CSV 파일 로딩
try:
    df = pd.read_csv(FILE_PATH, encoding='EUC-KR')
except Exception as e:
    st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 데이터 표시
st.subheader("📄 원본 데이터")
st.dataframe(df)

# 총인구수 열 이름 찾기
total_col = [col for col in df.columns if '총인구수' in col][0]

# '2025년05월_계_'로 시작하는 열 필터링
gender_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '계' not in col]

# 열 이름 간소화: '2025년05월_계_남자' → '남자', '여자'
gender_rename = {col: col.split('_')[-1] for col in gender_cols}

# 필요한 컬럼 선택 및 이름 변경
selected_cols = ['행정기관코드', '행정기관명', total_col] + gender_cols
df_selected = df[selected_cols].rename(columns=gender_rename)
df_selected = df_selected.rename(columns={total_col: '총인구수'})

# 상위 5개 행정기관 추출 (총인구수 기준)
df_top5 = df_selected.sort_values(by='총인구수', ascending=False).head(5)

# 시각화를 위한 정리
df_chart = df_top5[['행정기관명', '남자', '여자']].set_index('행정기관명')

# Streamlit 기본 차트로 시각화
st.subheader("👥 상위 5개 지역 남녀 인구수 비교")
st.line_chart(df_chart)

# 데이터 요약
st.subheader("📌 상위 5개 지역 요약 데이터")
st.dataframe(df_top5)
