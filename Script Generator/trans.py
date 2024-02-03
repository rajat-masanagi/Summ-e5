import g4f
import streamlit as st
g4f.debug.logging = True 
g4f.debug.version_check = False 
g4f.debug.logging = True 
g4f.debug.version_check = False 
st.title("Get your Script ")
user_input1 = st.text_input("Tell me about the topic :")
user_input2 = st.text_input("Whats the level of proficiency of your audience :")
user_input3 = st.text_input("Duration :")

#user_input = f"{user_input1} {user_input2} {user_input3} "
if st.button("Submit"):
    user_input = f"{user_input1} {user_input2} {user_input3} "
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    st.write(response)
