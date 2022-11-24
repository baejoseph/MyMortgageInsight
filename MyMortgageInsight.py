import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interactive, HBox, Label
from IPython.display import display
import streamlit as st


def monthly_payment(PV,interest,years):
    for payment in range(100,800,1):
        ePV = 1e5
        for month in range(years*12):
            ePV *= (1+interest/1200)
            ePV -= payment
        FV = ePV
        if FV< 0: break
    return payment*PV/1e5

def PV_implicit(current_monthly_payment,interest,years):
    minPV = int(current_monthly_payment*years//1e3*1e3)
    maxPV = int(300*minPV)
    for PV in range(minPV,maxPV,int(1e3)):
        ePV = PV
        for month in range(years*12):
            ePV *= (1 + interest/1200)
            ePV -= current_monthly_payment
        FV = ePV
        if FV>0: break
    return  PV

def number_years(PV,current_monthly_payment,interest):
    nPV = 1e5
    current_monthly_payment *= nPV/PV
    for months in range(24,10000):
        ePV = nPV
        for month in range(months):
            ePV *= (1+interest/1200)
            ePV -= current_monthly_payment
        FV = ePV
        if FV < 0: break
    return round(months/12,2)

def implicit_interest(PV,current_monthly_payment,years):
    nPV = 1e5
    current_monthly_payment *= nPV/PV
    for interest in range(1,100):
        interest *= 0.1
        ePV = nPV
        for month in range(years*12):
            ePV *= (1 + interest/1200)
            ePV -= current_monthly_payment
        FV = ePV
        if FV > 0: break
    return max(0,interest-0.1)

def early_repayment_value(PV,ER, current_monthly_payment,interest):
    y1 = number_years(PV,current_monthly_payment,interest)
    y2 = number_years(PV-ER,current_monthly_payment,interest)
        
    return (y1-y2)*12*current_monthly_payment



st.title("My Mortgage Insight")


st.header("My Current Mortgage")

st.write("Tell us about your current Mortgage:")


current_monthly_payment = st.slider('How much are you paying every month?', 100, 3000, 1257, format="£%d")
years = st.slider('How many years do you have left on your mortgage?', 5, 35, 25, format="%d years")
current_interest = st.slider('What interest rate are you on now?', 0.1, 9.0, 1.9, format="%f%%")

Remaining = PV_implicit(current_monthly_payment, current_interest,years)

st.subheader(f"You are currently paying: £{round(current_monthly_payment):,} at {current_interest}% interest over {years} years.")
st.subheader(f"Based on what you have told us, you still have £{round(Remaining):,} to pay over {years} years.")


st.header("My Future Mortgage")

new_interest = st.slider('What new interest rate are you considering?', 0.1, 9.0, current_interest, format="%f%%")


new_monthly_payment = monthly_payment(Remaining, new_interest,years)

st.subheader(f"With a new interest rate of {new_interest}%, your new monthly payment will be: £{round(new_monthly_payment):,}.")

if new_interest > current_interest:
    st.subheader(f"This is an increase of: £{round(new_monthly_payment - current_monthly_payment):,}.")


st.header("Value of My Early Repayments")

repayment = st.slider('How much extra are you willing to pay today?', 0,3000,0, format="£%d")

value = early_repayment_value(Remaining,repayment, new_monthly_payment,new_interest)
new_term = number_years(Remaining-repayment,new_monthly_payment,new_interest)

if repayment > 0:
    st.subheader(f'If you repay extra £{round(repayment):,} now, you will pay £{round(value):,} less over {new_term} years at {new_interest}% interest.')
