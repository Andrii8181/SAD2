import matplotlib.pyplot as plt

def plot_boxplot(df, value_col, factor_col):
    fig, ax = plt.subplots()
    df.boxplot(column=value_col, by=factor_col, ax=ax)
    plt.tight_layout()
    return fig
