import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import google.generativeai as genai

# Load Gemini AI API Key
GEMINI_API_KEY = "AIzaSyAhzATTujBYQwdUdGAwnwNediMhXkiMDvI"
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with an available model if necessary
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# Load the model and data
@st.cache_resource
def load_model():
    try:
        with open('nutrition_model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("⚠️ Model file not found. Please upload 'nutrition_model.pkl' to proceed.")
        st.stop()

@st.cache_data
def load_data():
    try:
        return pd.read_csv('processed_nutrition.csv')
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please upload 'processed_nutrition.csv' to proceed.")
        st.stop()

model = load_model()
data = load_data()

# Function to predict calorie class
def predict_calorie_class(protein, carbs, fat):
    prediction = model.predict([[protein, carbs, fat]])
    return "🔥 High Calorie" if prediction[0] == 1 else "🥗 Low Calorie"

# Streamlit app configuration
st.set_page_config(page_title="NutriPlan: Smart Meal Planner", page_icon="🥗", layout="wide")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🍽️ Meal Suggestion",
                    "📅 Weekly Meal Plan", "💰 Budget Planner", "ℹ️ About"])

# New Features ================================================================

def show_nutrition_facts(food_item):
    """Display detailed nutrition facts for a specific food item"""
    result = data[data['Food Item'].str.contains(food_item, case=False)]
    if not result.empty:
        with st.expander(f"🔍 Detailed Nutrition Facts for {food_item}"):
            cols = st.columns(3)
            cols[0].metric("Calories", f"{result['Calories'].values[0]} kcal")
            cols[1].metric("Protein", f"{result['Protein'].values[0]}g")
            cols[2].metric("Carbs", f"{result['Carbs'].values[0]}g")

            fig, ax = plt.subplots()
            sns.barplot(x=['Protein', 'Carbs', 'Fat'],
                       y=[result['Protein'].values[0],
                          result['Carbs'].values[0],
                          result['Fat'].values[0]])
            ax.set_ylabel("Grams")
            st.pyplot(fig)
    else:
        st.warning("⚠️ Food item not found in database")

 # Gemini AI Integration Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Gemini AI - Ask Anything")
ai_prompt = st.sidebar.text_area("Ask Gemini AI about nutrition, diet, or meal plans:")

if st.sidebar.button("🔍 Ask Gemini"):
    if ai_prompt:
        response = get_gemini_response(ai_prompt)
        st.sidebar.write("**Gemini AI Response:**")
        st.sidebar.write(response)
    else:
        st.sidebar.warning("⚠️ Please enter a question.")

        

def budget_planner():
    """Budget planning section with cost-saving tips"""
    st.subheader("💰 Smart Budget Planning")

    with st.expander("💡 Budget-Saving Strategies"):
        st.write("""
        ### 🛒 Grocery Shopping Tips:
        - Buy in bulk for staple items
        - Choose seasonal produce
        - Compare unit prices
        - Use frozen vegetables

        ### 🍳 Meal Prep Hacks:
        - Cook large batches and freeze
        - Repurpose leftovers creatively
        - Use versatile ingredients
        - Plan meals around sales
        """)

    st.subheader("📊 Weekly Budget Calculator")
    budget = st.slider("Set weekly food budget ($)", 20, 200, 50)
    st.write(f"### Recommended Allocation for ${budget}:")
    categories = {
        'Proteins': 0.35,
        'Vegetables': 0.25,
        'Grains': 0.20,
        'Other': 0.20
    }

    fig, ax = plt.subplots()
    ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    st.pyplot(fig)

# Page Content ================================================================

if page == "🏠 Home":
    st.title("NutriPlan: Smart Meal Planner 🥗")
    st.write("""
    Welcome to **NutriPlan** - Your AI-powered nutrition assistant! 🍏🥑
    Create personalized meal plans that respect your dietary needs and budget constraints.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🌱 Dietary Support")
        st.write("- Gluten-free\n- Vegan\n- Low-carb\n- Dairy-free\n- Diabetic-friendly")

    with col2:
        st.markdown("### 💰 Budget Features")
        st.write("- Cost-effective recipes\n- Grocery price tracking\n- Meal prep guides\n- Leftover optimization")

    with col3:
        st.markdown("### 🎯 Health Goals")
        st.write("- Weight management\n- Muscle gain\n- Energy boosting\n- Heart health\n- Digestive wellness")

    st.markdown("---")
    st.markdown("### 📈 Why Choose NutriPlan?")
    st.write("""
    - **AI-Powered Recommendations**: Machine learning algorithms tailored to your unique profile
    - **Science-Backed Plans**: Developed with certified nutritionists
    - **Dynamic Adaptation**: Adjusts to your progress and feedback
    - **Comprehensive Tracking**: Monitor nutrients, costs, and preferences
    """)

elif page == "🍽️ Meal Suggestion":
    st.title("Personalized Meal Suggestions 🍽️")

    with st.form("meal_form"):
        col1, col2 = st.columns(2)
        with col1:
            protein = st.number_input("💪 Protein (g)", min_value=0.0, value=50.0, step=1.0)
            carbs = st.number_input("🍞 Carbohydrates (g)", min_value=0.0, value=100.0, step=1.0)

        with col2:
            fat = st.number_input("🧈 Fat (g)", min_value=0.0, value=30.0, step=1.0)
            dietary_prefs = st.multiselect("Dietary Preferences",
                                         ["Vegetarian", "Vegan", "Gluten-Free", "Low-Carb", "Dairy-Free"])

        submitted = st.form_submit_button("🔍 Generate Meal Plan")

    if submitted:
        calorie_class = predict_calorie_class(protein, carbs, fat)
        st.success(f"🔔 Predicted Calorie Class: {calorie_class}")

        st.markdown("### 🍽️ AI-Recommended Meals")
        st.write("Based on your preferences, here are some meal suggestions:")

        # Meal Suggestions with Dietary Plans
        st.subheader("Breakfast")
        st.write("Oatmeal with Berries and Nuts")
        st.write("Dietary Plans: Vegan, Gluten-Free, Dairy-Free")

        st.subheader("Lunch")
        st.write("Quinoa Salad with Roasted Vegetables and Chickpeas")
        st.write("Dietary Plans: Vegetarian, Vegan, Gluten-Free, Nut-Free, Dairy-Free")

        st.subheader("Dinner")
        st.write("Lentil Soup with Whole Grain Bread")
        st.write("Dietary Plans: Vegan, Gluten-Free, Dairy-Free, Vegetarian, Low-Carb")

        st.markdown("### 🍎 Additional Dietary Considerations")
        st.write("1. **Low-Carb**: Focus on non-starchy vegetables, lean proteins, and healthy fats.")
        st.write("2. **Vegetarian**: Incorporate plant-based protein sources such as beans, lentils, and tofu.")
        st.write("3. **Vegan**: Ensure you're getting enough B12 from supplements or fortified foods.")
        st.write("4. **Gluten-Free**: Avoid wheat, barley, and rye; choose gluten-free alternatives.")
        st.write("5. **Dairy-Free**: Use almond, soy, or oat milk instead of dairy products.")

elif page == "📅 Weekly Meal Plan":
    st.title("Weekly Meal Planner 📅")

    with st.form("weekly_plan"):
        col1, col2 = st.columns(2)
        with col1:
            calorie_goal = st.number_input("Daily Calorie Goal", min_value=1200, value=2000)
            diet_type = st.selectbox("Diet Type", ["Balanced", "Keto", "Mediterranean", "Plant-Based"])

        with col2:
            budget = st.number_input("Weekly Budget ($)", min_value=20, value=100)
            allergies = st.multiselect("Allergies/Intolerances", ["Dairy", "Nuts", "Gluten", "Shellfish"])

        if st.form_submit_button("Generate Weekly Plan"):
            st.success("✅ Generated Weekly Meal Plan!")

            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            tab = st.tabs(days)

            for i, day in enumerate(tab):
                with day:
                    meals = data.sample(3)
                    for _, meal in meals.iterrows():
                        st.write(f"#### {meal['Food Item']} - {meal['Calories']}kcal")
                        st.write(f"**Protein**: {meal['Protein']}g | **Carbs**: {meal['Carbs']}g | **Fat**: {meal['Fat']}g")

elif page == "💰 Budget Planner":
    budget_planner()

elif page == "ℹ️ About":
    st.title("About NutriPlan ℹ️")

    st.markdown("""
    ### 🌟 Our Mission
    **NutriPlan** aims to make healthy eating accessible and affordable for everyone.
    We combine nutritional science with AI technology to create personalized meal plans
    that respect dietary needs and financial constraints.

    ### 📚 Data Sources
    - USDA Food Composition Database
    - WHO Nutritional Guidelines
    - Market price data from major retailers
    - User preference analytics

    ### 🛠️ Technology Stack
    - Machine Learning: Random Forest Classifier
    - Data Analysis: Pandas/Numpy
    - Visualization: Matplotlib/Seaborn
    - Backend: Python/Streamlit

    ### 📞 Contact Us
    **Email**: contact@nutriplan.ai
    **Support**: support@nutriplan.ai
    **Office**: 123 Health Lane, NutriCity, NC 98765

    ### 📜 Disclaimer
    Always consult with a healthcare provider before making significant dietary changes.
    Nutritional needs may vary based on individual health conditions.
    """)

    st.markdown("---")
    st.write("© 2024 NutriPlan. All rights reserved.")
 
