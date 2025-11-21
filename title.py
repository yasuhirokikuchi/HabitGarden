import streamlit as st

def title():
    image_title = "image/title/unnamed.png"

    # テキスト(マークダウンで書けます。)
    st.write("# Habit Gardenへようこそ")

    # 注釈
    st.caption("注釈")

    # 画像
    st.image(image_title)

    # テーブル
    import pandas as pd
    df = pd.DataFrame(
            {
                "first column": [1, 2, 3, 4],
                "second column": [10, 20, 30, 40],
            }
        )
    st.write(df)

    # チャート
    st.line_chart(df)