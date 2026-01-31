#  Customer Retention Intelligence System (CRIS)

### **Executive Summary**
A full-stack Data Science solution designed to predict customer churn and recommend retention strategies. This project utilizes a **Random Forest Classifier (SMOTE-enhanced)** to identify high-risk customers with **79% Recall** and deploys the model via an interactive **Streamlit Dashboard** for real-time decision-making.

---

###  Business Impact
* **Problem:** Telecom provider facing high customer attrition (26.5% churn rate).
* **Solution:** Predictive model to flag at-risk customers before they leave.
* **ROI Analysis:**
    * **Target:** 635 high-risk customers identified.
    * **Projected Revenue Saved:** ~$61,300 (Conservative Case @ 50% acceptance).
    * **Potential Revenue Saved:** ~$135,800 (Best Case @ 100% acceptance).

---

###  Tech Stack
* **Python** (Data Processing & Modeling)
* **Scikit-Learn** (Machine Learning: Random Forest)
* **SMOTE** (Handling Class Imbalance)
* **Streamlit** (Interactive Web Application)
* **Pandas & NumPy** (Data Manipulation)

---

###  Key Features
1.  **Real-Time Prediction:** Instantly calculates Churn Probability (0-100%).
2.  **Risk Segmentation:** Classifies users as "Safe" or "High Risk" based on a 30% threshold.
3.  **Automated Strategy:** Generates a tailored script for managers to offer discounts to high-risk users.
4.  **Interactive Dashboard:** Allows non-technical stakeholders to adjust tenure, contract type, and monthly charges to simulate scenarios.

---

###  Strategic Insights (From Model)
* **Contract Type** is the #1 predictor of churn. Moving a user from "Month-to-Month" to "One Year" reduces risk significantly.
* **Fiber Optic** users are the most volatile segment.
* **Electronic Check** payers have the highest churn rate; migrating them to Auto-Pay reduces attrition.

---

### 📸 Project Screenshots

**1. High Risk Scenario (The Problem)**
![High Risk](screenshot/High%20Churn%20.png)

**2. Moderate Risk Scenario (Soft Retention)**
![Moderate Risk](screenshot/Moderate%20Churn%20.png)

**3. Safe Scenario (The Solution)**
![Low Risk](screenshot/Low%20Churn%20.png)

---

###  Author
**Aswin Panengal**
*Connect with me on LinkedIn!*
