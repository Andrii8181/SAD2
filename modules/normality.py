from scipy import stats

def check_normality(series):
    stat, p = stats.shapiro(series.dropna())
    return {
        "is_normal": p > 0.05,
        "p_value": p,
        "recommendation": "Рекомендується використовувати непараметричні методи." if p <= 0.05 else "Можна використовувати параметричні методи."
    }
