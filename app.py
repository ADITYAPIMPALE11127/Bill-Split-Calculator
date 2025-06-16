import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="💸 Bill Split Calculator", page_icon="💰", layout="centered")

# 🌈 Custom CSS Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
        }

        .main {
            animation: fadeIn 1.5s;
        }

        @keyframes fadeIn {
            0% {opacity: 0; transform: translateY(-10px);}
            100% {opacity: 1; transform: translateY(0);}
        }

        h1 {
            text-align: center;
            font-size: 2.8em;
            font-weight: bold;
            color: #00FFAB;
            text-shadow: 0 0 10px #00FFAB, 0 0 20px #00FFAB;
        }

        .stNumberInput label, .stSlider label {
            font-size: 1.1em;
        }

        footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0f2027;
            color: white;
            padding: 0.8em;
            font-size: "40px";
            text-align: center;
            padding-left: 1.5em;
            z-index: 100;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2.2em;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>💸 Bill Split Calculator</h1>", unsafe_allow_html=True)

with st.form("bill_form"):
    bill_amount = st.number_input("Enter the Bill Amount", min_value=0.0, format="%.2f")
    tip_percentage = st.slider("Tip Percentage", 0, 50, 10)
    count_person = st.number_input("How many people?", min_value=1, step=1)

    submitted = st.form_submit_button("✨ Calculate Split")

if submitted:
    with st.spinner("Crunching numbers..."):
        time.sleep(1.2)

    tip_amount = (tip_percentage / 100) * bill_amount
    total = bill_amount + tip_amount
    amount_per_person = total / count_person

    st.balloons()

    # 📊 Show Results in Table Format
    df = pd.DataFrame({
        "Description": ["Bill Amount", "Tip Amount", "Total Amount", "People", "Amount per Person"],
        "Value": [f"${bill_amount:.2f}", f"${tip_amount:.2f}", f"${total:.2f}", int(count_person), f"${amount_per_person:.2f}"]
    })

    st.success("✅ Calculation Complete!")
    st.table(df)

    # 🎉 Bonus Visual Feedback
    if amount_per_person > 100:
        st.snow()
    elif amount_per_person < 10:
        st.toast("💡 Such a deal!", icon="💸")
    else:
        st.toast("✅ Done splitting!", icon="🍰")

# 📝 Footer - now aligned left
st.markdown("""
    <footer>
         Made with ❤️ by <b>Aditya Pimpale</b>
    </footer>
""", unsafe_allow_html=True)
