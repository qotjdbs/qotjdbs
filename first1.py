import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")
if true:
    # 데이터 불러오기
    df = pd.read_csv("2025년 5월 기준 연령별 인구 현황 분석", encoding='EUC-KR')

    # 총인구수 컬럼 이름 변경
    df = df.rename(columns={'2025년05월_계_총인구수': '총인구수'})

    # 연령별 컬럼 필터링 및 이름 정리
    age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
    age_renamed = {col: col.replace('2025년05월_계_', '') for col in age_columns}
    df = df.rename(columns=age_renamed)

    # 총인구수 정수형 변환
    df['총인구수'] = df['총인구수'].str.replace(',', '').astype(int)

    # 총인구수 기준 상위 5개 행정구역 추출
    top5 = df.sort_values(by='총인구수', ascending=False).head(5)

    # 연령 데이터만 추출
    age_df = top5[['행정구역'] + list(age_renamed.values())]
    age_df.set_index('행정구역', inplace=True)

    # 문자열을 정수형으로 변환
    age_df = age_df.applymap(lambda x: int(str(x).replace(',', '')))

    # 전치하여 연령을 세로축으로 설정
    age_df = age_df.T
    age_df.index.name = '연령'

    # 시각화
    st.subheader("연령별 인구 현황 (상위 5개 행정구역)")
    st.line_chart(age_df)

    # 원본 데이터 표시
    st.subheader("원본 데이터")
    st.dataframe(df)

