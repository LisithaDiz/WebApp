import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_category(categorties, cutoff):
    categorty_new = {}
    for i in range(len(categorties)):
        if categorties.values[i] >= cutoff:
            categorty_new[categorties.index[i]] = categorties.index[i]
        else:
            categorty_new[categorties.index[i]] = "Other"
    return categorty_new


def clean_exp(x):
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post grad'
    return 'Less than a bachelors'


@st.cache_data
def load_data():
    data = pd.read_csv('survey_results_public.csv')
    data = data[['Country', "EdLevel", 'Employment', 'ConvertedCompYearly', 'YearsCodePro']]
    data = data[data['ConvertedCompYearly'].notnull()]
    data = data.dropna()
    data = data[data['Employment'] == 'Employed, full-time']
    data = data.drop('Employment', axis=1)

    contries = shorten_category(data.Country.value_counts(), 400)
    data['Country'] = data['Country'].map(contries)
    data = data[data['ConvertedCompYearly'] <= 25000]
    data = data[data['ConvertedCompYearly'] >= 10000]
    data = data[data['ConvertedCompYearly'] != "Other"]

    data['YearsCodePro'] = data['YearsCodePro'].apply(clean_exp)
    data['EdLevel'] = data['EdLevel'].apply(clean_education)
    data = data.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    return data


data = load_data()


def show_explore():
    st.title("Explore Software Engineer Salaries")

    st.write("""
    ### Stack Overflow Developer Salaries
    """)

    df = data["Country"].value_counts()

    fig, ax1 = plt.subplots()
    ax1.pie(df, labels=df.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis('equal')

    st.write("""#### Number of data from different countries""")
    st.pyplot(fig)

    st.write("""
    ### Mean Salary On Country
    """)

    df = data.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(df)

    st.write("""
    ### Mean Salary On Experience
    """)
    df = data.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(df)
