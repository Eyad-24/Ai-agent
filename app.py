import streamlit as st
from agent import search_products, generate_ai_suggestion

st.set_page_config(page_title="🛍️ AI Shopping Assistant", layout="centered")

st.title("🛒 AI Shopping Assistant")
st.write("Enter what you're looking for, and let AI suggest the best product for you.")

query = st.text_input("What do you need? (e.g. wireless headphones under $100)", "")

if query:
    try:
        with st.spinner("🤖 Thinking..."):
            suggestion = generate_ai_suggestion(query)
            products = search_products(query)

        st.subheader("🧠 AI Suggestion")
        st.info(suggestion)

        st.subheader("🔍 Top Product Matches")
        for product in products:
            st.markdown(
                f'<a href="{product["link"]}" target="_blank" style="text-decoration:none">'
                f'<div style="background-color:#f0f4f8;padding:5px;border-radius:10px;margin-bottom:5px">'
                f'<b>{product["title"]}</b><br>'
                f'💲 {product["price"]} &nbsp;&nbsp; ⭐ {product["rating"]}/5'
                f'</div></a>',
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
