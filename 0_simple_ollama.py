from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'What is Pocari Sweat and how much does it cost?',
  },
])
print(response['message']['content'])