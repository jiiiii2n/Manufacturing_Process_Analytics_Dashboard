import plotly.express as px


def make_line_chart(df, x_col, y_col):
    return px.line(df, x=x_col, y=y_col, markers=True, title=f"{y_col} Trend")


def make_histogram(df, col):
    return px.histogram(df, x=col, title=f"{col} Histogram")


def make_box_plot(df, col):
    return px.box(df, y=col, title=f"{col} Box Plot")


def make_scatter_plot(df, x_col, y_col):
    return px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")


def make_corr_heatmap(df, numeric_cols):
    corr = df[numeric_cols].corr()
    return px.imshow(corr, text_auto=True, title="Correlation Heatmap")