"""Dashboard:  streamlit run app.py"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import fund_model as fm

st.set_page_config(page_title="Can the fund survive a bad year?", layout="wide")
st.title("Can a credit guarantee fund survive a bad year?")
st.caption("1,000 guaranteed loans, the fund pays $20,000 per default. Synthetic data, 10,000 simulated years.")

with st.sidebar:
    st.header("Move these")
    capital_m = st.slider("Fund capital ($M)", 1.0, 6.0, 2.5, 0.25)
    p_rec = st.slider("Share of years that are recessions", 0.0, 0.5, 0.15, 0.05)
    pd_rec = st.slider("Default rate in a recession", 0.04, 0.25, 0.12, 0.01)
    pd_norm = st.slider("Default rate in a normal year", 0.01, 0.10, 0.04, 0.005)

capital = capital_m * 1e6
claims, is_rec = fm.simulate_with_recessions(pd_normal=pd_norm, pd_recession=pd_rec, p_recession=p_rec)
ruin = fm.prob_of_ruin(claims, capital)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Leverage (promises / capital)", f"{fm.GUARANTEES / capital:.1f}x")
c2.metric("Average claims per year", f"${claims.mean()/1e6:.2f}M")
c3.metric("Worst simulated year", f"${claims.max()/1e6:.2f}M")
c4.metric("Chance the fund is wiped out", f"{100*ruin:.1f}%")

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(claims[~is_rec], bins=60, color="#2a78d6", alpha=0.75, label="Normal years")
if is_rec.any():
    ax.hist(claims[is_rec], bins=60, color="#eb6834", alpha=0.7, label="Recession years")
ax.axvline(capital, color="black", ls="--", lw=1.5)
ax.set_xlabel("Total claims in one year ($)")
ax.set_ylabel("Simulated years")
ax.legend(frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
st.pyplot(fig)
st.caption("Dashed line = fund capital. Any year to the right of it, the fund cannot pay all its claims.")
