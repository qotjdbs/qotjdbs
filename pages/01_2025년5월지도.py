import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 행정구역 이름 → 위도, 경도 매핑 (예시용)
region_coords = {
    "서울특별시": (37.5665, 126.9780),
    "부산광역시": (35.1796, 129.0756),
    "경기도": (37.4138, 127.5183),
    "인천광역시": (37.4563, 126.7052),
    "대구광역시": (35.8714, 128.6014),
    # 필요시 추가 가능
}

# 앱 제목
st.title("2025년 5월 기준 상위 5개 행정구역 인구 현황 지도 시각화")

# CSV 파일 경로
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# CSV 로딩
try:
    df = pd.read_csv(FILE_PATH, encoding="EUC-KR")
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 열 이름 정리
df = df.rename(columns={"2025년05월_계_총인구수": "총인구수"})
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_renamed = {col: col.replace("2025년05월_계_", "") for col in age_columns}
df = df.rename(columns=age_renamed)

# 총인구수 수치형으로 변환
df["총인구수"] = df["총인구수"].str.replace(",", "").astype(int)

# 상위 5개 행정구역 추출
top5 = df.sort_values(by="총인구수", ascending=False).head(5)

# 지도 생성 (대한민국 중심)
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 마커 추가
for _, row in top5.iterrows():
    region = row["행정구역"]
    total_pop = row["총인구수"]
    coords = region_coords.get(region)

    if coords:
        folium.CircleMarker(
            location=coords,
            radius=10,
            popup=f"{region}<br>총인구수: {total_pop:,}명",
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.4
        ).add_to(m)
    else:
        st.warning(f"좌표 정보 없음: {region}")

# 지도 출력
st.subheader("총인구수 기준 상위 5개 행정구역 위치")
st_data = st_folium(m, width=700, height=500)

# 원본 데이터 보기
st.subheader("원본 데이터")
st.dataframe(df)
