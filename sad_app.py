import streamlit as st
import pandas as pd
from modules import normality, statistics, visualization, report, developer

st.set_page_config(page_title="SAD — Статистичний Аналіз Даних", page_icon="📊", layout="wide")
st.title("📊 SAD — Статистичний Аналіз Даних")
st.markdown("##### Розробник: Чаплоуцький А.М., кафедра плодівництва і виноградарства УНУ")

uploaded_file = st.file_uploader("📂 Завантажте Excel-файл з даними", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Дані успішно завантажено")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    factor_cols = df.select_dtypes(exclude='number').columns.tolist()

    selected_value = st.selectbox("🔢 Виберіть показник для аналізу", numeric_cols)
    selected_factor = st.selectbox("🧪 Виберіть фактор", factor_cols)

    if selected_value and selected_factor:
        st.subheader("🔍 Перевірка нормальності")
        normal = normality.check_normality(df[selected_value])

        if not normal["is_normal"]:
            st.error("❌ Дані не мають нормального розподілу")
            st.markdown(normal["recommendation"])
        else:
            st.success("✅ Дані мають нормальний розподіл")
            method = st.selectbox("📈 Виберіть метод аналізу", [
                "Однофакторний ANOVA",
                "Тест Тьюкі",
                "НІР (LSD)",
                "Тест Данкана",
                "Бонфероні"
            ])

            if st.button("🔬 Виконати аналіз"):
                result = statistics.run_analysis(df, selected_value, selected_factor, method)

                st.subheader("📊 Результати аналізу")
                st.dataframe(result["table"])

                st.subheader("📈 Графік")
                fig = visualization.plot_boxplot(df, selected_value, selected_factor)
                st.pyplot(fig)

                st.subheader("📐 Сила впливу факторів")
                st.dataframe(result["effect_size"])

                st.subheader("📥 Скачати звіт")
                doc_stream = report.generate_report(df, selected_value, selected_factor, result)
                st.download_button(
                    label="📥 Скачати звіт (.docx)",
                    data=doc_stream,
                    file_name="SAD_Звіт.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

developer.show_info()
