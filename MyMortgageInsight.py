import numpy as np
import pandas as pd
import streamlit as st

def monthly_payment(PV,interest,years):
    for payment in range(60,800,1):
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

def years_months_text(yr):
    years_, months_ = divmod((yr)*12, 12)
    years_text, months_text = "",""
    if years_ > 0: 
        years_text = f"{round(years_)} year"
        if years_ > 1: years_text += "s" 
    if months_ > 0: 
        months_text = f"{round(months_)} month"
        if months_ > 1: months_text += "s"
    if (months_ > 0) and (years_ > 0): years_text += " and "
    return years_text + months_text

st.title("My Mortgage Insight")

st.header("Tell us about your current Mortgage:")

current_monthly_payment = st.slider('How much are you paying every month?', 300, 6000, 2020,10, format="£%d")
years = st.slider('How many years do you have left on your mortgage?', 7, 35, 21, format="%d years")
current_interest = st.slider('What interest rate are you on now?', 0.5, 9.0, 1.9,0.1, format="%f%%")

Remaining = PV_implicit(current_monthly_payment, current_interest,years)
repayment = 0

st.subheader(f"You are currently paying £{round(current_monthly_payment):,} at {current_interest}% interest over {years} years.")
st.subheader(f"Based on what you have said, you still have £{round(Remaining):,} to pay over {years} years.")

st.header("My Future Mortgage")

new_interest = st.slider('What new interest rate are you considering?', 0.1, 9.0, current_interest,0.1, format="%f%%")

extension = st.slider('Are you thinking of extending the term at all?', 0, 15, 0, format="%d years")
extension_text = ""
if extension > 0: extension_text = f" and extending the term by {years_months_text(extension)},"

new_term = years+extension   
new_monthly_payment = monthly_payment(Remaining, new_interest,years+extension)

st.subheader(f"With a new interest rate of {new_interest}%,{extension_text} your new monthly payment will be £{round(new_monthly_payment):,} over {years_months_text(new_term)}.")

if (new_interest > current_interest) or (extension > 0):
    if new_monthly_payment > current_monthly_payment: 
        increase_decrease = f"This is an increase of £{round(new_monthly_payment - current_monthly_payment):,} every month."
    elif new_monthly_payment < current_monthly_payment: 
        increase_decrease = f"This is a decrease of £{round(-new_monthly_payment + current_monthly_payment):,} every month."
    else: increase_decrease = "There is no change in your monthly payment."
    st.subheader(increase_decrease)

st.header("Value of My One-off Early Repayment")

repayment = st.slider('How much extra are you willing to pay today?', 0,round(Remaining*0.2),0,100, format="£%d")

# value of repayment if reducing terms
value = early_repayment_value(Remaining,repayment, new_monthly_payment,new_interest)
new_term = number_years(Remaining-repayment,new_monthly_payment,new_interest)

# value of repayment if reducing monthly payment
updated_monthly_payment = monthly_payment(Remaining - repayment, new_interest,years+extension)
value2 = (new_monthly_payment- updated_monthly_payment)*12*(years+extension)

if repayment > 0:
    st.subheader(f'If you repay an extra £{round(repayment):,} now, you can either shorten the term by {years_months_text(years+extension-new_term)} and pay £{round(value):,} less over {years_months_text(new_term)} at {new_interest}% interest; or reduce monthly payment by £{round(new_monthly_payment- updated_monthly_payment)} and pay £{round(value2):,} less over {years_months_text(years+extension)} at {new_interest}% interest.')
    
st.write("Copyright © 2023 Joseph Bae")
