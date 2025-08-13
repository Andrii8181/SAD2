import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scikit_posthocs as sp
from scipy import stats

def run_analysis(df, value_col, factor_col, method):
    model = ols(f'{value_col} ~ C({factor_col})', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    if method == "Тест Тьюкі":
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        tukey = pairwise_tukeyhsd(df[value_col], df[factor_col])
        result_table = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    elif method == "НІР (LSD)":
        result_table = sp.posthoc_ttest(df, val_col=value_col, group_col=factor_col, p_adjust='holm')
    elif method == "Тест Данкана":
        result_table = sp.posthoc_duncan(df, val_col=value_col, group_col=factor_col)
    elif method == "Бонфероні":
        result_table = sp.posthoc_ttest(df, val_col=value_col, group_col=factor_col, p_adjust='bonferroni')
    else:
        result_table = anova_table

    # η²
    ss_between = anova_table["sum_sq"][0]
    ss_total = sum(anova_table["sum_sq"])
    eta_squared = ss_between / ss_total
    effect_size = pd.DataFrame([{
        "Фактор": factor_col,
        "η²": eta_squared
    }])

    return {
        "table": result_table,
        "effect_size": effect_size
    }
