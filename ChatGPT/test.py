import openai

# Configure your OpenAI API key
openai.api_key = "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"


# Define the function for generating a ChatGPT response
def generate_chat_response(prompt):
    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract and return the generated response
    return response.choices[0].text.strip()


# Prompt for user input
user_input = input("You: ")

# Generate a ChatGPT response
response = generate_chat_response(user_input)

# Print the generated response
print("ChatGPT: " + response)
