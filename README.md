# 🥗 Food Recommender Chatbot
---

This project is a **Food Recommender Chatbot** that provides short, personalized meal and nutrition recommendations based on the user’s profile (Age, Sex, Diabetes status, Activity level, Personal goal)  
The chatbot is built using:
- Large Language Models (LLMs) via **OpenRouter API**
- **Python**
- **Streamlit** (UI)

The project is divided into **two main parts**:
1. Terminal-based chatbot (logic & API)
2. Web UI with Streamlit

## 📌 PART 1 - Terminal-Based Nutrition Chatbot
- Instead of training a model from scratch, we use an API-based approach.
- We use OpenRouter, a platform that provides access to multiple LLMs.
- We selected a free model: `gpt-oss-120b`.

### 📦 Installation

```bash
pip install openai
``` 

### API client setup
- We initialize the OpenRouter client using an **API key** and a **base URL**.  
- This allows the chatbot to communicate with Large Language Models hosted on OpenRouter.
```python
client = OpenAI(
    api_key="PUT YOU API KEY HERE",
    base_url="https://openrouter.ai/api/v1"
)
```

### We define some chatbot instructions 
- Answers only nutrition-related questions  
- Adapts responses based on user profile  
- Refuses questions outside the nutrition domain  
- Provides short, practical, and safe advice  

### Domain filtering
To ensure the chatbot responds only to nutrition questions, we implemented this key-words filter.  
```python
NUTRITION_KEYWORDS = [
    "nutrition", "diet", "food", "meal", "eat", "calorie",
    "protein", "carbohydrate", "fat", "fiber",
    "diabetes", "blood sugar", "workout", "exercise"
]
```
-> If a question does not contain nutrition-related keywords, the chatbot politely refuses.

### Dedfine some key parameters
`temperature=0.3` → stable, less random answers  
`max_tokens=500` → controlled response length  
-> This phase is used to test and validate logic before creating a UI.

## 📌 PART 2 — Streamlit Web Interface
Create a modern web UI for the chatbot.

📦 Installation
```bash
pip install streamlit
```

**Streamlit:**  
⦁ Simple and fast UI creation    
⦁ Built-in chat components    


**UI:**  
⦁ Displays previous messages  
⦁ Accepts user input  
⦁ Handle greetings ("hello")    
⦁ Exit messages ("bye")    
⦁ Non-nutrition questions    
⦁ Valid nutrition questions via the API    
⦁ Displays chatbot responses in real time  





  

