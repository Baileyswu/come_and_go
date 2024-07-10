import pandas as pd
import streamlit_echarts as ets


def bar_stack(df: pd.DataFrame, x: str, y: str, hue: str):
    x_list = df[x].drop_duplicates().to_list()
    hue_list = df[hue].drop_duplicates().to_list()
    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {
            "data": hue_list,
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": x_list,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": hue_value,
                "type": "bar",
                "stack": "total",
                "label": {"show": True},
                "emphasis": {"focus": "series"},
                "data": df[df[hue] == hue_value][y].tolist(),
            } for hue_value in hue_list
        ],
    }
    ets.st_echarts(options=options, height="500px")
