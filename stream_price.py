import streamlit as st
from serpapi import search as GoogleSearch
import pandas as pd

# Replace with your actual SerpAPI key
API_KEY = "748e1e99ab64c85919085820ec2b6a26c3b3173aedb3449120b0a8c6bb618246"

st.title("Google Shopping Price Comparison")

product_name = st.text_input("Enter the product you are looking for:", "Macbook M3")
search_button = st.button("Search")

def display_image(url):
    return f'<img src="{url}" width="50" height="50">'

if search_button:
    if product_name:
        params = {
            "engine": "google_shopping",
            "q": product_name,
            "api_key": API_KEY,
            "gl": "IN",  # Set geolocation to India
            "hl": "en",   # Set host language to English
            "location": "Bangalore, Karnataka, India"  # Set the specific city
        }

        search = GoogleSearch(params)
        results = search.as_dict()

        if "shopping_results" in results:
            shopping_results = results["shopping_results"]
            prices_data = []
            for item in shopping_results:
                if "price" in item and "title" in item and "source" in item and "thumbnail" in item:
                    prices_data.append({
                        "Product": item["title"],
                        "Store": item["source"],
                        "Price": item["price"],
                        "Image": item["thumbnail"]
                    })
                elif "price" in item and "source" in item and "thumbnail" in item:
                    prices_data.append({
                        "Product": product_name,  # Use the search query if title is missing
                        "Store": item["source"],
                        "Price": item["price"],
                        "Image": item["thumbnail"]
                    })

            if prices_data:
                df = pd.DataFrame(prices_data)
                st.subheader(f"Price comparison for '{product_name}' in Madurai, India:")
                df['Image'] = df['Image'].apply(display_image)
                st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.info(f"No shopping results found for '{product_name}' in Madurai, India.")
        else:
            st.error("Could not retrieve shopping results. Please check your API key or the product name.")
    else:
        st.warning("Please enter a product name to search.")