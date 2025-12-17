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
# Main Loop
# =========================
def main():
    print("🥗 Hello I'm Food Recommender Chatbot, How can I help you ?")
    while True:
        user_input = input("🟨YOU: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🥗 Food Recommender Chatbot: See you soon. \n Stay healthy ✨")
            break

        if not is_nutrition_related(user_input):
            print(
                "🥗 Food Recommender Chatbot: I can only help with ONLY nutrition, diet, "
                "diabetes-friendly and healthy lifestyle eating questions."
            )
            continue

        try:
            response = chat_with_nutrition_bot(user_input)
            print("🥗 Food Recommender Chatbot:", response)
        except Exception as e:
            print("🥗 Food Recommender Chatbot: Sorry, something went wrong. Please try again.")
            print("DEBUG:", e)

if __name__ == "__main__":
    main()
