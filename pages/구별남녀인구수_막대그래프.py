import streamlit as st
import pandas as pd

# 앱 제목
st.title("2025년 6월 기준 행정구역별 주민등록 인구 현황 분석")

# CSV 파일 경로 (이미 업로드된 파일 경로 사용)
FILE_PATH = "202506_202506_주민등록인구및세대현황_월간.csv"

# CSV 파일 불러오기
try:
    df = pd.read_csv(FILE_PATH, encoding='euc-kr')
except Exception as e:
    st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ✅ 필요한 열 추출
# '총인구수' 열 찾기
total_col = [col for col in df.columns if '총인구수' in col][0]

# '2025년05월_계_'로 시작하면서 '남자' 또는 '여자' 포함된 열 찾기
gender_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and ('남자' in col or '여자' in col)]

# 열 이름 정리: '2025년05월_계_남자' → '남자' 등
gender_rename = {col: col.split('_')[-1] for col in gender_cols}

# 필요한 열 선택 및 이름 바꾸기
df_filtered = df[['행정기관명', total_col] + gender_cols].copy()
df_filtered.rename(columns={total_col: '총인구수', **gender_rename}, inplace=True)

# 숫자형으로 변환
df_filtered['총인구수'] = df_filtered['총인구수'].astype(str).str.replace(',', '').astype(int)
df_filtered['남자'] = df_filtered['남자'].astype(str).str.replace(',', '').astype(int)
df_filtered['여자'] = df_filtered['여자'].astype(str).str.replace(',', '').astype(int)

# 총인구수 기준 상위 5개 지역 추출
top5 = df_filtered.sort_values(by='총인구수', ascending=False).head(5)

# ✅ 원본 데이터 출력
st.subheader("📄 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5)

# ✅ 남녀 인구수 시각화
st.subheader("👥 상위 5개 지역 남녀 인구수 비교 (단위: 명)")

# 그래프용 데이터: index → 행정기관명, 컬럼 → 남자/여자
chart_df = top5[['행정기관명', '남자', '여자']].set_index('행정기관명')

# Streamlit 기본 기능으로 선그래프 출력
st.line_chart(chart_df)
