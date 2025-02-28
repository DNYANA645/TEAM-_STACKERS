# 🍽️ AI-Powered Nutrition Planner

## 📌 Problem Statement
Creating a **meal-planning tool** for students that considers **dietary restrictions** and **budget constraints** using AI-powered recommendations.

---

## 📖 Description
The **AI-Powered Nutrition Planner** is designed to help students find **affordable and nutritious meals** that align with their dietary needs. This tool integrates **Machine Learning, AI, and an interactive Streamlit-based UI** to provide personalized meal recommendations. 

By leveraging **Random Forest Regressor** and **Gemini AI**, the system optimizes meal choices based on user input. It enables students to maintain a **healthy diet within their budget**, ensuring balanced nutrition without exceeding financial constraints.

This project is ideal for students, dieticians, and individuals looking for **AI-assisted meal planning** solutions. 

---

## 🚀 Solution Overview
This project leverages **Machine Learning** and **AI models** to provide optimized meal plans. The core components include:
1. **Data Collection & Preprocessing** 📊
2. **Machine Learning Module** 🤖
3. **Streamlit Web App** 🌐
4. **Gemini AI Integration** 🧠

---

## 📂 1️⃣ Data Collection & Preprocessing
**Steps Followed:**
- Collected a dataset containing **food items, calories, protein, carbs, fat, and cost.**
- Cleaned missing data and converted categorical features.
- Standardized numeric features using **StandardScaler**.
- Saved the preprocessed dataset for model training.

---

## 🤖 2️⃣ Machine Learning Module
**Model Used:**
- **Random Forest Regressor** for high accuracy predictions.
- Evaluated performance using **MAE, RMSE, and R² Score.**

**Process:**
1. Splitting dataset into **train & test sets**.
2. Training the model and saving it as a **.pkl file**.
3. Model predicts **nutritional values** based on food choices.
4. Reports generated to evaluate model accuracy.

---

## 🌐 3️⃣ Streamlit Web Application
The interactive **Streamlit-based UI** allows users to:
- Select **dietary preferences** & **budget**.
- View **AI-suggested meal plans**.
- Get **detailed nutrition analysis**.

To run the Streamlit app:
```bash
streamlit run app.py
```

---

## 🧠 4️⃣ Gemini AI for Enhanced Recommendations
- Used **Gemini AI** to improve food recommendations.
- AI refines the meal plan based on **health goals & constraints**.
- Provides **real-time feedback** on meal choices.

---

 

---

## 📜 Results & Reports
- **Model Accuracy Metrics:** Displayed in the Streamlit app.
- **ML Model Performance Reports:** Stored in `/reports/`.
- **AI Meal Plan Recommendations:** Based on user inputs.

📌 **Future Scope:** Expand dataset & add more AI-driven insights!

🔗 **Contributors:** [TEAM STACKERS] 🚀

