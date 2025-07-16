import streamlit as st
import pandas as pd

# 앱 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로 (로컬 또는 스트림릿 클라우드에선 아래 경로 수정 필요)
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# CSV 파일 로딩
try:
    df = pd.read_csv(FILE_PATH, encoding="EUC-KR")
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 열 이름 정리: '2025년05월_계_' 제거
df = df.rename(columns={"2025년05월_계_총인구수": "총인구수"})
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_renamed = {col: col.replace("2025년05월_계_", "") for col in age_columns}
df = df.rename(columns=age_renamed)

# 총인구수 정수 변환
df["총인구수"] = df["총인구수"].str.replace(",", "").astype(int)

# 총인구수 기준 상위 5개 행정구역 추출
top5 = df.sort_values(by="총인구수", ascending=False).head(5)

# 연령별 데이터 추출 및 숫자 변환
age_df = top5[["행정구역"] + list(age_renamed.values())]
age_df.set_index("행정구역", inplace=True)
age_df = age_df.applymap(lambda x: int(str(x).replace(",", "")))

# 전치: 연령이 인덱스, 행정구역이 열이 되도록
age_df_transposed = age_df.T
age_df_transposed.index.name = "연령"

# 시각화 출력
st.subheader("상위 5개 행정구역의 연령별 인구 선 그래프")
st.line_chart(age_df_transposed)

# 원본 데이터 출력
st.subheader("원본 데이터 보기")
st.dataframe(df)

