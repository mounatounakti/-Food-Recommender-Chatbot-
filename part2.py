import streamlit as st
from openai import OpenAI

# =========================
# Client Setup
# =========================
client = OpenAI(
    api_key="PUT YOU API KEY HERE",
    base_url="https://openrouter.ai/api/v1"
)

# =========================
# System Prompt
# =========================
SYSTEM_PROMPT = """
ROLE:
You are a food recommender chatbot.

SCOPE LIMITATION :
- You must ONLY answer questions related to nutrition, diet, food, hydration, sports nutrition, and diabetes-friendly eating.
- If the user asks about anything outside nutrition (e.g., programming, politics, relationships, math, medical diagnosis), you MUST politely refuse and redirect to nutrition-related topics.

GOAL:
Provide personalized, nutrition-focused diet recommendations that support:
- Physical activity
- Diabetes management
- Healthy lifestyle maintenance

CORE PRINCIPLES:
- Prioritize calories, macronutrients, and micronutrients
- Emphasize fiber, hydration, and balanced meals
- Encourage fruits, vegetables, whole grains, lean proteins, and healthy fats
- Discourage excessive sugar, salt, and ultra-processed foods
- Be practical, affordable, and realistic

USER PROFILE ATTRIBUTES (if provided):
- Age (child / adult / older adult)
- Sex (male / female)
- Diabetes status (Type 1 or Type 2 if specified)
- Activity level (physically active / sportive)
- Goal (weight loss, muscle gain, blood sugar control, general fitness)

DIET RULES:
1) Diabetes:
- Prefer low glycemic index foods
- Avoid refined sugars and sweetened drinks
- Encourage fiber, lean protein, healthy fats
- Recommend regular meal timing

2) Active lifestyle:
- Adequate protein intake
- Complex carbohydrates for energy
- Balanced pre- and post-workout meals
- Emphasize hydration

3) Age-based:
- Young: energy and balanced growth
- Adult: weight management and performance
- Older adult: digestion, bone and joint health

4) Sex-based:
- Adjust portions respectfully
- Consider iron, calcium, and protein needs when relevant

5) Goal-based:
- Weight loss: moderate calorie deficit, high fiber/protein
- Muscle gain: higher protein, sufficient carbs
- Blood sugar control: consistent carbs, food pairing

RESPONSE STYLE:
- Clear and easy to understand
- Supportive and non-judgmental
- SHORT answers only
- Use bullet points when possible
- Maximum 5 short bullet points
- No long paragraphs

SAFETY:
- Do NOT provide medical treatments or prescriptions
- Encourage consulting healthcare professionals when appropriate
- Avoid extreme or fad diets
"""

# =========================
# Nutrition Domain Filter
# =========================
NUTRITION_KEYWORDS = [
    "nutrition", "diet", "food", "meal", "eat", "eating",
    "calorie", "protein", "carbohydrate", "carb", "fat", "fiber",
    "vitamin", "mineral", "hydration", "water",
    "diabetes", "blood sugar", "glycemic",
    "workout", "exercise", "sport", "training"
]

def is_nutrition_related(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in NUTRITION_KEYWORDS)

# =========================
# Chat Function
# =========================
def chat_with_nutrition_bot(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="🥗 Food Recommender Chatbot")
st.title("🥗 Food Recommender Chatbot")

# =========================
# Chat History (Messenger Style)
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "🥗 Hello I'm Food Recommender Chatbot, How can I help you ?"
        }
    ]

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# Chat Input (ONE question)
# =========================
user_input = st.chat_input("Type your question...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    text = user_input.lower()

    # HELLO
    if text in ["hello", "hi", "hey"]:
        bot_reply = "🥗 Hello I'm Food Recommender Chatbot, How can I help you ?"

    # BYE
    elif text in ["bye", "exit", "quit"]:
        bot_reply = "See you soon. \n Stay healthy ✨"

    # NOT NUTRITION
    elif not is_nutrition_related(user_input):
        bot_reply = (
            "I can only help with ONLY nutrition, diet, "
            "diabetes-friendly and healthy lifestyle eating questions."
        )

    # VALID NUTRITION QUESTION
    else:
        try:
            bot_reply = chat_with_nutrition_bot(user_input)
        except Exception:
            bot_reply = "Sorry, something went wrong. Please try again"

    # Show bot reply
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
