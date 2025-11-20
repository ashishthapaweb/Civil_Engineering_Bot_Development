from rag.run import answer_query
import streamlit as st
# "Have I done any projects on semantic segmentation of cracks?"
st.title("My RAG App")
user_q = st.text_input("Ask Something Here:")
if user_q:
    answer = answer_query(user_q)
    st.write(answer)