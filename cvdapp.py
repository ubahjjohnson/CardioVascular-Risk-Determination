import streamlit as st
import joblib
import numpy as np

# Try to load the model
try:
    model = joblib.load('cvd_classifier.pkl')
except Exception as e:
    model = None
    st.error(f"Failed to load model: {e}")

# Function to calculate the waist-to-hip ratio
def calculate_whr(WAIST, HIP):
    if HIP == 0:
        return 0  # Avoid division by zero
    return WAIST / HIP

# Function to predict CVD risk
def predict_cvd_risk(WAIST, HIP, WHR, model):
    """ Predicts cardiovascular risk based on WAIST, HIP, WHR and the trained model. """
    if model is None:
        return "Model not available. Please check the application setup."

    input_data = np.array([[WAIST, HIP, WHR]])  # All three features in correct order
    try:
        prediction = model.predict(input_data)
        result = prediction[0]

        # Handle both string and numeric model outputs
        if isinstance(result, str):
            if result.upper() == "LOW":
                return "Low Risk"
            elif result.upper() == "MODERATE":
                return "Medium Risk"
            else:
                return "High Risk"
        elif isinstance(result, (int, float)):
            if result == 0:
                return "Low Risk"
            elif result == 1:
                return "Medium Risk"
            else:
                return "High Risk"
        else:
            return f"Unexpected model output: {result}"
    except Exception as e:
        return f"Error during prediction: {e}"

# Streamlit app
def main():
    st.title("Cardiovascular Risk Prediction App")

    # User inputs
    WAIST = st.number_input("Waist Circumference (cm)", min_value=0.0, max_value=150.0, step=1.0)
    HIP = st.number_input("Hip Circumference (cm)", min_value=0.0, max_value=150.0, step=1.0)

    # Calculate waist-to-hip ratio
    WHR = calculate_whr(WAIST, HIP)
    st.write(f"Waist-to-Hip Ratio: {WHR:.2f}")

    # Predict CVD risk
    if st.button("Predict CVD Risk"):
        risk_level = predict_cvd_risk(WAIST, HIP, WHR, model)
        st.success(f"Predicted Cardiovascular Risk: {risk_level}")

if __name__ == "__main__":
    main()
