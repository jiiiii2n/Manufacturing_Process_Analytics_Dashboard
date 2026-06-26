import plotly.express as px

def line_chart(df, x_col, y_col):
    return px.line(df, x=x_col, y=y_col, markers=True)
