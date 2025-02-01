import streamlit as st
from huggingface_hub import InferenceClient

# Streamlit UI
st.title("🐳 Chat with DeepSeek 🐳")

with st.sidebar:
    # Input box for user to enter their Hugging Face API key
    api_key = st.text_input("Enter your Hugging Face API Key:", type="password")

if api_key:
    # Initialize the InferenceClient with the user-provided API key
    client = InferenceClient(api_key=api_key)

    # Input box for user to enter their question
    user_input = st.chat_input("Enter your question:")
    

    if user_input:
        # Prepare the messages for the model
        messages = [
            {
                "role": "user",
                "content": user_input
            }
        ]
        with st.chat_message("user"):
            st.write(user_input)

        # Get the completion from the model
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", 
            messages=messages, 
        )

        # Get the model's response
        response = completion.choices[0].message['content']

        # Check if the response contains <think> tags
        if "<think>" in response and "</think>" in response:
            # Extract content within <think> tags
            think_content = response.split("<think>")[1].split("</think>")[0].strip()
            # Display the thinking content in an expander
            with st.expander("Thinking..."):
                st.write(think_content)

            # Extract the rest of the response (outside <think> tags)
            rest_of_response = response.split("</think>")[1].strip()
            # Display the rest of the response with an AI icon
            with st.chat_message("ai"):
                st.write(rest_of_response)
        else:
            # If no <think> tags, display the entire response with an AI icon
            with st.chat_message("ai"):
                st.write(rest_of_response)
else:
    with st.sidebar:
        st.warning("Please enter your Hugging Face API Key to proceed.")