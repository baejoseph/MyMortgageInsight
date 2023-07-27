import numpy as np
import streamlit as st
from MortgageProduct import MortgageProduct
from typing import Literal
from streamlit.components.v1 import html

def add_vertical_space(num_lines: int = 1):
    """Add vertical space to your Streamlit app."""
    for _ in range(num_lines):
        st.write("")

Font = Literal['Cookie', 'Lato', 'Arial', 'Comic', 'Inter', 'Bree', 'Poppins']
        
def button(
    username: str,
    floating: bool = True,
    text: str = "Buy me a coffee",
    emoji: str = "",
    bg_color: str = "#FFDD00",
    font: Font = "Cookie",
    font_color: str = "#000000",
    coffee_color: str = "#000000",
    width: int = 220,
):
    button = f"""
        <script type="text/javascript"
            src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js"
            data-name="bmc-button"
            data-slug="{username}"
            data-color="{bg_color}"
            data-emoji="{emoji}"
            data-font="{font}"
            data-text="{text}"
            data-outline-color="#000000"
            data-font-color="{font_color}"
            data-coffee-color="{coffee_color}" >
        </script>
    """

    html(button, height=70, width=width)

    if floating:
        st.markdown(
            f"""
            <style>
                iframe[width="{width}"] {{
                    position: fixed;
                    bottom: 60px;
                    right: 40px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

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

st.header("My Current Mortgage")

current_pmt = st.slider('How much are you paying every month?', 700, 6000, 2020,10, format="£%d")
current_term = st.slider('How many years do you have left on your mortgage?', 13, 35, 21, format="%d years")
current_rate = st.slider('What interest rate are you on now?', 0.5, 9.0, 1.9,0.1, format="%f%%")

params = {'pmt': current_pmt,
          'term': current_term,
          'rate': current_rate }

mp1 = MortgageProduct(**params)

st.subheader(f"You are currently paying £{round(current_pmt):,} at {current_rate}% interest over {current_term} years.")
st.subheader(f"Based on what you have said, you still have £{round(mp1.get_loan()):,} to pay over {current_term} years.")

add_vertical_space(5)

st.header("My Future Mortgage")

new_rate = st.slider('What new interest rate are you considering?', 0.1, 9.0, current_rate,0.1, format="%f%%")

extension = st.slider('Are you thinking of extending the term at all?', 0, 15, 0, format="%d years")
extension_text = ""
if extension > 0: extension_text = f" and extending the term by {years_months_text(extension)},"

new_term = current_term + extension

params2 = {'loan': mp1.get_loan(),
           'term': new_term,
           'rate': new_rate}

mp2 = MortgageProduct(**params2)

new_pmt = mp2.get_pmt()

st.subheader(f"With a new interest rate of {new_rate}%,{extension_text} your new monthly payment will be £{round(new_pmt):,} over {years_months_text(new_term)}.")

if (new_rate > current_rate) or (extension > 0):
    if new_pmt > current_pmt: 
        increase_decrease = f"This is an increase of £{round(new_pmt - current_pmt):,} every month."
    elif new_pmt < current_pmt: 
        increase_decrease = f"This is a decrease of £{round(-new_pmt + current_pmt):,} every month."
    else: increase_decrease = "There is no change in your monthly payment."
    st.subheader(increase_decrease)

add_vertical_space(5)

st.header("Value of My One-off Early Repayment")

repayment = st.slider('How much extra are you willing to pay today?', 0,round(mp1.get_loan()*0.2),0,100, format="£%d")

# value of repayment if reducing terms
params3 = {'loan': mp2.get_loan() - repayment,
           'pmt': mp2.get_pmt(),
           'rate': new_rate}

mp3 = MortgageProduct(**params3)
value = (mp2.get_term() - mp3.get_term())*12*new_pmt

# value of repayment if reducing monthly payment
params4 = {'loan': mp2.get_loan() - repayment,
           'term': new_term,
           'rate': new_rate}

mp4 = MortgageProduct(**params4)
value2 = (new_pmt - mp4.get_pmt())*12*new_term

if repayment > 0:
    st.subheader(f'If you repay an extra £{round(repayment):,} now, you can either shorten the term by {years_months_text(new_term - mp3.get_term())} and pay £{round(value):,} less over {years_months_text(new_term)} at {new_rate}% interest; or reduce monthly payment by £{round(new_pmt - mp4.get_pmt())} and pay £{round(value2):,} less over {years_months_text(new_term)} at {new_rate}% interest.')

add_vertical_space(10)

st.write("Copyright © 2023 Joseph Bae")

button(username="baejoseph", floating=False, width=221)
