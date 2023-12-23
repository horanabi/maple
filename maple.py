import requests
import pandas as pd
import streamlit as st
import datetime
import random


api_key = "test_1c7f50637c55961a99c6ea04b154a42dd15f29e400fdba3541772fdf463bf19672748534a913f2e3b45cdd48215fc154"
header = {'x-nxopen-api-key': api_key}


def main():
    st.set_page_config(
        page_title="메이플스토리 유저 정보 조회 시스템",
        page_icon="🍞"
    )

    st.header("각종 메이플 정보 검색 공간입니다.")
    st.header("오늘의 종합랭킹")
    s_date = datetime.datetime.today() - datetime.timedelta(days=1)
    s_date = s_date.strftime("%Y-%m-%d") 
    

    url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={s_date}"
    res = requests.get(url, headers= header).json()
    res= res["ranking"]
    if len(res) == 0:
        st.write("종합랭킹이 조회되지 않습니다.")
    else:
        df =pd.DataFrame(res)
        df.drop("date", axis = 1, inplace= True)
        df= df.set_index("ranking")
        df = df.rename(columns={"character_name":"캐릭명", "character_level":"레벨","world_name":"서버", "character_popularity":"인기도", "character_guildname":"길드명"})
       
        
        ci = random.randint(1,200)
        st.session_state["char"] = df["캐릭명"][ci]
        st.dataframe(df,height=1000, use_container_width=True)

                  


if __name__ == "__main__":
    main()



