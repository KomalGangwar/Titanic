import streamlit as st
import requests
from io import BytesIO

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f9f8fa;
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 36px;
        color: #4a90e2;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .query-box {
        border: 2px solid #4a90e2;
        border-radius: 8px;
        padding: 10px;
    }
    .response-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title with styling
st.markdown('<h1 class="title">🚢 Titanic Dataset Query</h1>', unsafe_allow_html=True)

# Sidebar for information
st.sidebar.title("ℹ️ About the App")
st.sidebar.write(
    "This app allows you to ask questions about the Titanic dataset. "
    "Simply enter a query in the text box, and the model will respond with insights."
)

st.sidebar.markdown("---")
st.sidebar.write("🔹 Try queries like:")
st.sidebar.write("• How many passengers survived?")
st.sidebar.write("• What was the average fare?")

# Query input with custom styling
query = st.text_input("Ask a question:", placeholder="E.g., How many people survived?", key="query_input")

# Send query to FastAPI server and display response
if query:
    response = requests.get("http://127.0.0.1:8000/query", params={"q": query})

    # Get the content type from the response headers
    content_type = response.headers.get("content-type", "")

    st.markdown("### Response:")

    if "image" in content_type:
        # Display the image in Streamlit
        st.image(BytesIO(response.content))
    else:
        try:
            result = response.json()["response"]
            st.markdown(f'<div class="response-box">{result}</div>', unsafe_allow_html=True)
        except requests.exceptions.JSONDecodeError:
            st.error("Unexpected response format. Please check the API.")
            st.write(response.text)  # Debugging: Print raw response
