import streamlit as st
import joblib
import numpy as np

# Load the trained decision tree model
try:
    model = joblib.load('cvd_classifier.joblib')  # Adjust the path if necessary
except Exception as e:
    st.error(f"Error: Unable to load the model. Please check the path. Error details: {e}")
    model = None  # Ensure model is None to prevent further errors

# Function to calculate the waist-to-hip ratio
def calculate_whr(waist_circumference, hip_circumference):
    if hip_circumference == 0:
        return 0  # Avoid division by zero
    return waist_circumference / hip_circumference

# Function to predict CVD risk
def predict_cvd_risk(whr, model):
    """ Predicts cardiovascular risk based on WHR and the trained model.

    Args:
        whr (float): Waist-to-hip ratio.
        model: Trained machine learning model.

    Returns:
        str: "Low Risk", "Medium Risk", or "High Risk".
             Returns "Model not available" if the model failed to load.
    """
    if model is None:
        return "Model not available. Please check the application setup."
    # Prepare the input data for the model
    input_data = np.array([[whr]])  # Ensure the input is a 2D array
    try:
        prediction = model.predict(input_data)
        # Assuming the model predicts 0, 1, or 2 for low, medium, and high risk, respectively
        if prediction[] == "LOW":
            return "Low Risk"
        elif prediction[0] == MODERATE:
            return "Medium Risk"
        else:
            return "High Risk"
    except Exception as e:
        return f"Error during prediction: {e}"

# Streamlit app
def main():
    st.title("Cardiovascular Risk Prediction App")

    # User inputs
    WAIST = st.number_input("Waist Circumference (cm)", min_value=50.0, max_value=150.0, step=1.0)
    HIP = st.number_input("Hip Circumference (cm)", min_value=70.0, max_value=150.0, step=1.0)

    # Calculate waist-to-hip ratio
    WHR = calculate_whr(WAIST, HIP)
    st.write(f"Waist-to-Hip Ratio: {WHR:.2f}")

    # Predict CVD risk
    if st.button("Predict CVD Risk"):
        risk_level = predict_cvd_risk(WHR, model)
        st.write(f"Predicted Cardiovascular Risk: {risk_level}")
        if model is None:
            st.warning("The model was not loaded correctly.  Please ensure the model file is available and the path is correct.")

if __name__ == "__main__":
    main()
