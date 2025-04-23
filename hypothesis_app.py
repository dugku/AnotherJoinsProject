import streamlit as st
import pandas as pd
import bambi as bmb
import arviz as az
from pathlib import Path


DATA_PATH = Path("car_data.csv")  # put your CSV here

st.set_page_config(page_title="Bayesian Regression (fixed data)", layout="centered")
st.title("Bayesian Regression")
st.button("Back to Home")

if not DATA_PATH.exists():
    st.error(f"CSV not found at {DATA_PATH.resolve()}. Please place your file there.")
    st.stop()

@st.cache_data(show_spinner="Reading CSV …", experimental_allow_widgets=True)
def load_data(path: Path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)
st.write("### Data preview", df.head())
st.write("Rows:", df.shape[0], "• Columns:", df.shape[1])


cols = df.columns.tolist()

target = st.selectbox("Target (dependent variable)", cols)
predictors = st.multiselect("Predictor(s)", [c for c in cols if c != target])
chains = st.number_input("Number of MCMC chains", 1, 8, 4, 1)

draws = st.slider("Draws per chain", 500, 5000, 2000, 500)

if st.button("Run Bayesian regression"):
    if predictors:
        formula = f"{target} ~ {' + '.join(predictors)}"
    else:
        formula = f"{target} ~ 1"  # intercept‑only model

    st.code(f"Formula: {formula}")

    with st.spinner("Sampling …"):
        model = bmb.Model(formula, df)
        idata = model.fit(draws=draws, chains=chains, target_accept=0.9)

    st.success("Sampling finished!")

    summary = az.summary(idata, round_to=2)
    st.subheader("Chain statistics")
    st.dataframe(summary)
    st.write("**Max R‑hat:**", float(summary["r_hat"].max()))
    st.write("**Min ESS (bulk):**", int(summary["ess_bulk"].min()))
