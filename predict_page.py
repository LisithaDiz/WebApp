import streamlit as st
import pickle
import numpy as np
import sklearn


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


df = load_model()

model = df['model']
le_country = df['le_country']
le_education = df['le_education']


def show_predication():
    st.title('Software Developer Salary Prediction')
    st.write("""### We need some info to predict thhe salary""")

    contries = (
        'United States of America',
        'Germany',
        'United Kingdom of Great Britain and Northern Ireland',
        'India',
        'Canada',
        'France',
        'Brazil',
        'Spain',
        'Netherlands',
        'Australia',
        'Italy',
        'Poland',
        'Sweden',
        'Russian Federation',
        'Switzerland',
    )

    education = ('Master’s degree',
                 'Less than a bachelors',
                 'Bachelor’s degree',
                 'Post grad')

    country = st.selectbox('Country', contries)
    edu = st.selectbox('Education Level', education)
    exp_Y = st.slider('Years of Experience', 0, 50, 3)

    ok = st.button('Calucalte Salary')
    if ok:
        new = np.array([[country, edu, exp_Y]])
        new_data_encoded = new.copy()
        new_data_encoded[:, 0] = le_country.transform(new[:, 0])
        new_data_encoded[:, 1] = le_education.transform(new[:, 1])
        new_data_encoded = new_data_encoded.astype(float)

        salary = model.predict(new_data_encoded)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")


