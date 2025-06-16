import streamlit as st
import pandas as pd
import time
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Unicode font
font_path = "fonts/DejaVuSans.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
else:
    st.error("Font file not found! Please place 'DejaVuSans.ttf' in the 'fonts' folder.")

st.set_page_config(page_title="💸 Bill Split Calculator", page_icon="💰", layout="centered")

# 🌈 CSS Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
        }
        h1 {
            text-align: center;
            font-size: 2.8em;
            font-weight: bold;
            color: #00FFAB;
            text-shadow: 0 0 10px #00FFAB, 0 0 20px #00FFAB;
        }
        footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0f2027;
            color: white;
            padding: 0.8em;
            font-size: 0.9em;
            text-align: left;
            padding-left: 1.5em;
            z-index: 100;
        }
        @media (max-width: 768px) {
            h1 { font-size: 2.2em; }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>💸 Bill Split Calculator</h1>", unsafe_allow_html=True)

# 🔢 Input Form
with st.form("bill_form"):
    bill_amount = st.number_input("Enter the Bill Amount", min_value=0.0, format="%.2f")
    tip_percentage = st.slider("Tip Percentage", 0, 50, 10)
    count_person = st.number_input("How many people?", min_value=1, step=1)
    submitted = st.form_submit_button("✨ Calculate Split")

# 📄 PDF Generation Function
def generate_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("DejaVuSans", 16)
    c.drawString(200, height - 30, "Pay Karde Mittr 😂")

    c.setFont("DejaVuSans", 12)
    y = height - 80
    for index, row in df.iterrows():
        c.drawString(80, y, f"{row['Description']}: {row['Value']}")
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer

# ✅ Form Submission Logic
if submitted:
    with st.spinner("Crunching numbers..."):
        time.sleep(1.2)

    tip_amount = (tip_percentage / 100) * bill_amount
    total = bill_amount + tip_amount
    amount_per_person = total / count_person

    st.balloons()

    df = pd.DataFrame({
        "Description": ["Bill Amount", "Tip Amount", "Total Amount", "People", "Amount per Person"],
        "Value": [f"₹{bill_amount:.2f}", f"₹{tip_amount:.2f}", f"₹{total:.2f}", int(count_person), f"₹{amount_per_person:.2f}"]
    })

    st.success("✅ Calculation Complete!")
    st.table(df)

    pdf_buffer = generate_pdf(df)

    # 📥 Download Button
    downloaded = st.download_button(
        label="📄 Download Result as PDF",
        data=pdf_buffer.getvalue(),
        file_name="bill_details.pdf",
        mime="application/pdf"
    )

    # ✅ Toast on Download Click
    if downloaded:
        st.toast("📥 PDF has been downloaded!", icon="✅")

    # 🎉 Reactions based on amount per person
    if amount_per_person > 100:
        st.snow()
    elif amount_per_person < 10:
        st.toast("💡 Such a deal!", icon="💸")
    else:
        st.toast("✅ Done splitting!", icon="🍰")

# 📜 Footer
st.markdown("""
    <footer>
        🚀 Made with ❤️ by <b>Aditya Pimpale</b>
    </footer>
""", unsafe_allow_html=True)
