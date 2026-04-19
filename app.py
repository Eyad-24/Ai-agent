import streamlit as st
from agent import search_products, generate_ai_suggestion
from services.recommendation_service import recommend_similar_products


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


        # Search Results
        st.subheader("🔍 Top Product Matches")
        for product in products:
                # Case 1: Product from SerpAPI (has link)
                if product.get("link"):
                    st.markdown(
                        f'<a href="{product["link"]}" target="_blank" style="text-decoration:none">'
                        f'<div style="background-color:#f0f4f8;padding:5px;border-radius:10px;margin-bottom:5px">'
                        f'<b>{product["title"]}</b><br>'
                        f'💲 {product["price"]} &nbsp;&nbsp; ⭐ {product["rating"]}/5'
                        f'</div></a>',
                        unsafe_allow_html=True
                    )
                # Case 2: Product from local database (no link)    
                else:
                    st.markdown(
                        f'''
                        <div style="
                            background-color: #ffffff;
                            color: #000000;
                            padding: 10px;
                            border-radius: 10px;
                            margin-bottom: 8px;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                        ">
                            <span style="color:#1f77b4; font-weight:bold; font-size:16px;">
                                {product["title"]}
                            </span><br>
                            <span style="color:green; font-weight:bold;">
                                💲 {product["price"]}
                            </span>
                            &nbsp;&nbsp;
                            <span style="color:black;">
                                ⭐ {product["rating"]}/5
                            </span><br>
                            <span style="color:#555555; font-style:italic;">
                                Product available in local database
                            </span>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

        # Recommendation Section   
        if products:
            base_product = products[0]["title"]
            recommendations = recommend_similar_products(base_product)

            if recommendations:
                st.subheader("⭐ Recommended Products")

                for rec in recommendations:
                    st.markdown(
                        f'''
                        <div style="
                            background-color:#ffffff;
                            color:#000000;
                            padding:8px;
                            border-radius:10px;
                            margin-bottom:6px;
                            box-shadow:0 1px 4px rgba(0,0,0,0.15);
                        ">
                            <b>{rec["title"]}</b><br>
                            💲 {rec["price"]} &nbsp;&nbsp; ⭐ {rec["rating"]}/5
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
        

    except Exception as e:
        st.error(f"Something went wrong: {e}")
