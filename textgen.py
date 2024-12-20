import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can switch this to other models like "distilgpt2" or "gpt-neo"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Title of the app
st.title("Text Generation with GPT-2")

# User input for prompt
user_input = st.text_area("Enter your text prompt:", height=150)

# Slider to control text length
max_length = st.slider("Select Maximum Length", min_value=50, max_value=300, value=100)

# Slider to control creativity (temperature)
temperature = st.slider("Select Temperature", min_value=0.0, max_value=2.0, value=1.0)

# Text generation function
def generate_text(prompt, max_length=100, temperature=1.0):
    # Encode the input prompt to tensor
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Generate text
    outputs = model.generate(inputs,
                             max_length=max_length,
                             num_return_sequences=1,
                             no_repeat_ngram_size=2,
                             pad_token_id=tokenizer.eos_token_id,
                             temperature=temperature)

    # Decode and return the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Button to generate text
if st.button("Generate Text"):
    if user_input:
        with st.spinner("Generating..."):
            generated_text = generate_text(user_input, max_length, temperature)
            st.subheader("Generated Text:")
            st.write(generated_text)
    else:
        st.warning("Please enter a prompt first.")

