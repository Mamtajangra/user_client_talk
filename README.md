# user_client-talk

A Python project for managing chat conversations and extracting user information using Groq's Llama 3.1 model.

## Features

- **Conversation Manager:**  
   Summarizes chat history after every N turns using Llama 3.1.
- **User Info Extraction:**  
   Extracts personal details (name, email, phone, location, age) from chat text in JSON format.

## Setup

1. Clone the repository.
2. Install dependencies:
   ```sh
   pip install openai python-dotenv# user_client-talk
3. Add your Groq API key to a .env file:
   GROQ_API_KEY=your_groq_api_key  

##  Usage
Run the demo in talk.py:
python [talk.py](http://_vscodecontentref_/0)

## Files
talk.py — Main source code (talk.py)
.env — API key configuration
README.md — Project documentation

## Example

Conversation summary and user info extraction are demonstrated in talk.py