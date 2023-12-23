import requests
import pandas as pd
import streamlit as st
import datetime

key = "test_1c7f50637c55961a99c6ea04b154a42dd15f29e400fdba3541772fdf463bf19672748534a913f2e3b45cdd48215fc154"

def get_cube_history(api_key, date):
    date_str = date.strftime("%Y%m%d")
    header = {'x-nxopen-api-key': api_key}
    url = f"https://open.api.nexon.com/maplestory/v1/history/cube?count=1000&date_kst={date_str}"
    response = requests.get(url, headers=header).json()

    if "error" in response:
        st.header(response["error"]["message"])
        return None
    elif len(response["cube_history"]) != 0:
        return response["cube_history"]
    elif len(response["cube_history"]) == 0:
        st.header("큐브 사용 내역이 없습니다.")
        return None


def filter_by_character(df, selected_characters):
    if not selected_characters:
        return df
    return df[df["character_name"].isin(selected_characters)]


def display_cube_results(df):
    st.write("큐브 등업 결과")
    df0 = df["item_upgrade_result"].value_counts().reset_index()
    df0.columns = ["item_upgrade_result", "count"]

    df0_style = df0.style.apply(lambda x: ['background-color: tan' if x["item_upgrade_result"] == '성공' else '' for _ in df0.columns],
                                axis=1)
    st.dataframe(df0_style, use_container_width=True)


def display_character_info(df):
    st.markdown(f"# **사용 캐릭터:** {', '.join(df['character_name'].unique())}")
    selected_characters = []

    # 체크박스로 바꿔보기
    st.markdown("### **사용 캐릭터 필터링**")
    for character in df['character_name'].unique():
        selected = st.checkbox(character)
        if selected:
            selected_characters.append(character)

    if not selected_characters:
        st.warning("하나 이상의 캐릭터를 선택하세요.")

    cube_history_filtered = filter_by_character(df, selected_characters)
    
    df1 = cube_history_filtered[["character_name", "cube_type", "target_item", "date_create"]]
    st.dataframe(df1, use_container_width=True)
    return cube_history_filtered  # 선택된 캐릭터에 대한 데이터프레임 반환


def display_potential_options(selected_characters_df):
    #print(selected_characters_df[["character_name", "world_name", "cube_type", "target_item", "date_create","potential_option_grade"]])
    max_num_options = 3  # 잠재 옵션을 3개로 맞춥니다.
    df2 = pd.DataFrame([[entry["value"] for entry in cube] + [None] * (max_num_options - len(cube)) for cube in selected_characters_df["after_potential_option"]])
    df2.columns = [f"{i + 1}번째" for i in range(max_num_options)]
    df2["등급"] = ""
    
    abc = selected_characters_df["potential_option_grade"].tolist()
    for i in range(len(df2)):
        df2["등급"][i] = abc[i]
    
    grade_colors = {
        '레전드리': 'background-color: green',
        '유니크': 'background-color: yellow',
        '에픽': 'background-color: purple',
        '레어': 'background-color: blue',
    }
    df2_style = df2.style.apply(lambda x: [grade_colors[x["등급"]] for _ in df2.columns], axis=1)

    st.dataframe(df2_style, use_container_width=True)


def main():
    st.set_page_config(
        page_title="메이플 유저 조회 시스템",
        page_icon="🍞"
    )

    st.header("일단 openapi.nexon.com에 가서 Api 키를 발급 받아야 합니다.")

    key = st.text_input('api키 입력', '', type="password")

    if key == '':
        st.header("api키가 없으면 조회가 안됩니다.")
    else:
        date = st.date_input("확인하고 싶은 날짜를 선택하세요.", datetime.datetime.today(), format="YYYY/MM/DD")
        cube_history = get_cube_history(key, date)

        if cube_history:
            df = pd.DataFrame(cube_history)
            display_cube_results(df)
            selected_characters_df = display_character_info(df)
            display_potential_options(selected_characters_df)


if __name__ == "__main__":
    main()
