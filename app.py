import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Customer Retention Intelligence", layout="centered")

# --- 2. LOAD THE SAVED MODEL ---
@st.cache_resource
def load_data():
    model = joblib.load('churn_model.pkl')
    features = joblib.load('model_columns.pkl')
    return model, features

try:
    model, features = load_data()
except FileNotFoundError:
    st.error("⚠️ Error: Please place 'churn_model.pkl' and 'model_columns.pkl' in the same directory as this file.")
    st.stop()

# --- 3. UI DESIGN ---
st.title(" Customer Retention Intelligence System")
st.markdown("###  Decision Support Tool for Managers")
st.write("Enter customer details below to predict churn risk and generate a retention strategy.")
st.divider()

# --- 4. INPUT FORM (Sidebar) ---
st.sidebar.header("Customer Profile")

# Numerical Inputs
tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Monthly Charges ($)", 0.0, 150.0, 70.0)


# Categorical Inputs
# Note: I fixed the spelling "Electeronic" -> "Electronic"
contract = st.sidebar.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet_service = st.sidebar.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
payment_method = st.sidebar.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
tech_support = st.sidebar.selectbox("Has Tech Support?", ["Yes", "No", "No internet service"])
paperless = st.sidebar.selectbox("Paperless Billing?", ["Yes", "No"])

# --- 5. PREDICTION LOGIC ---
if st.button("Analyze Risk ", type="primary"):
    
    # A. Create a "Template" DataFrame with all columns set to 0
    input_df = pd.DataFrame(columns=features)
    input_df.loc[0] = 0  # Initialize with zeros
    
    # B. Fill in the Numerical Values (LOWERCASE to match your model)
    input_df['tenure'] = tenure
    input_df['monthlycharges'] = monthly_charges
    input_df['totalcharges'] = tenure * monthly_charges 
    
    # C. Manually Map the One-Hot Encoded Features
    # I added checks for both Capital and Lowercase to be 100% safe
    
    # Contract
    if contract == "One year":
        if 'contract_One year' in input_df.columns: input_df['contract_One year'] = 1
        elif 'Contract_One year' in input_df.columns: input_df['Contract_One year'] = 1
    elif contract == "Two year":
        if 'contract_Two year' in input_df.columns: input_df['contract_Two year'] = 1
        elif 'Contract_Two year' in input_df.columns: input_df['Contract_Two year'] = 1

    # Internet Service
    if internet_service == "Fiber optic":
        if 'internetservice_Fiber optic' in input_df.columns: input_df['internetservice_Fiber optic'] = 1
        elif 'InternetService_Fiber optic' in input_df.columns: input_df['InternetService_Fiber optic'] = 1
    elif internet_service == "No":
        if 'internetservice_No' in input_df.columns: input_df['internetservice_No'] = 1
        elif 'InternetService_No' in input_df.columns: input_df['InternetService_No'] = 1
        
    # Payment Method
    if payment_method == "Electronic check":
        if 'paymentmethod_Electronic check' in input_df.columns: input_df['paymentmethod_Electronic check'] = 1
        elif 'PaymentMethod_Electronic check' in input_df.columns: input_df['PaymentMethod_Electronic check'] = 1
    elif payment_method == "Mailed check":
        if 'paymentmethod_Mailed check' in input_df.columns: input_df['paymentmethod_Mailed check'] = 1
        elif 'PaymentMethod_Mailed check' in input_df.columns: input_df['PaymentMethod_Mailed check'] = 1
    elif payment_method == "Credit card":
        if 'paymentmethod_Credit card (automatic)' in input_df.columns: input_df['paymentmethod_Credit card (automatic)'] = 1
        elif 'PaymentMethod_Credit card (automatic)' in input_df.columns: input_df['PaymentMethod_Credit card (automatic)'] = 1
        
    # Others
    if tech_support == "No":
        if 'techsupport_No' in input_df.columns: input_df['techsupport_No'] = 1
        elif 'TechSupport_No' in input_df.columns: input_df['TechSupport_No'] = 1
    if paperless == "Yes":
        if 'paperlessbilling_Yes' in input_df.columns: input_df['paperlessbilling_Yes'] = 1
        elif 'PaperlessBilling_Yes' in input_df.columns: input_df['PaperlessBilling_Yes'] = 1

    # --- 6. GET PREDICTION ---
    prediction_prob = model.predict_proba(input_df)[0][1]
    prediction = (prediction_prob > 0.3)  # Using your optimized 30% Threshold
    
    # --- 7. DISPLAY RESULTS ---
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prediction Score")
        st.metric(label="Churn Probability", value=f"{prediction_prob:.1%}")
    
    with col2:
        st.subheader("Risk Assessment")
        
        # --- LOGIC FOR TIERS ---
        if prediction_prob < 0.3:
            st.success("✅ LOW RISK")
            st.write("Loyal customer. No action needed.")
            risk_tier = "Low"
            
        elif prediction_prob >= 0.3 and prediction_prob < 0.6:
            st.warning("⚠️ MODERATE RISK")
            st.write("Showing signs of churn. Monitor closely.")
            risk_tier = "Moderate"
            
        else:
            st.error("🚨 HIGH RISK")
            st.write("Immediate action required!")
            risk_tier = "High"

    # --- 8. STRATEGIC RECOMMENDATION ---
    st.divider()
    st.subheader("💡 AI Recommendation Strategy")
    
    if risk_tier == "High":
        st.error(f"⚠️ **Action Required: Intervention**")
        st.markdown(f"""
        **Target:** Prevent revenue loss of **${monthly_charges*24:,.2f}** (Est. 2-Year LTV).
        
        **Strategy:**
        > *"Hi, I noticed you've been a valued customer. 
        > To thank you for your loyalty, I can apply a **15% discount** to your bill if we switch you to a 1-Year plan today."*
        """)
        
    elif risk_tier == "Moderate":
        st.warning(f"👀 **Action Required: Soft Retention**")
        st.markdown(f"""
        **Target:** Improve satisfaction before risk increases.
        
        **Strategy:**
        > *"Hi, just checking in to ensure your **{internet_service}** service is working perfectly. 
        > We also have a complimentary tech support check-up available if you'd like to use it."*
        """)
        
    else: # Low Risk
        st.info("No immediate action required. Maintain standard service quality.")