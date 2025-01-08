# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:01:26 2025

@author: 91807
"""

import pandas as pd
import pickle 
import streamlit as st 
import datetime
import pandas as pd


#loading the saved model
loaded_model=pickle.load(open('C:/Users/91807/OneDrive/Desktop/energy_consumption_prediction/trained_model.sav','rb')) 


def energy_consumption(input_data):
    
    # Prediction for new input data
    #input_data = (94, 'Fridge', '21:12:00', '06-08-2023', 31.1, 'Winter', 3)

    # Preprocess the input data
    datetime_input = pd.to_datetime(input_data[3] + ' ' + input_data[2])
    hour = datetime_input.hour
    day = datetime_input.day
    month = datetime_input.month

    processed_input = pd.DataFrame({
        'home_id': [input_data[0]],
        'appliance_type': [input_data[1]],
        'household_size': [input_data[6]],
        'outdoor_temperature': [input_data[4]],
        'season': [input_data[5]],
        'hour': [hour],
        'day': [day],
        'month': [month]
    })

    # Load the trained model
    #loaded_model = joblib.load('energy_consumption_model.pkl')

    # Predict energy consumption
    predicted_consumption = loaded_model.predict(processed_input)
    
    return f"{predicted_consumption[0]} kW"


def main():
    
    
    # Title of the app
    st.title("Energy Consumption Prediction for Smart Buildings")
    
    
    
    # Home ID input
    home_id = st.number_input(
    "Home ID",
    min_value=1,
    max_value=500,
    value=1,
    step=1,
    help="Please enter values between 1 to 500"
    )
    
    # Appliance type input
    appliance_type = st.selectbox(
    "Appliance Type",
    ["Washing Machine", "Oven", "Fridge", "Microwave", "Computer", "Heater", "Air Conditioning", "Dishwasher", "TV", "Lights"]
    )
    
    # Time input
    time = st.text_input("Time (HH:MM:SS)", "12:00:00")
    
    # Date input
    date = st.text_input("Date (DD:MM:YYYY)", "01:01:2025")

    # Temperature input
    temperature = st.number_input("Temperature (°C)", value=25.0, step=0.1)
    
    
    # Season selection
    season = st.selectbox("Season", ["Winter", "Summer", "Fall", "Spring"])

# Household size

    # Household size input
    household_size = st.number_input(
    "Household Size",
    min_value=1,
    value=1,
    step=1,
    help="Enter the number of people in the household"
    )
    
    # Predict button
    if st.button("Predict"):
    # Validate date and time input
        try:
            datetime.datetime.strptime(time, "%H:%M:%S")
            datetime.datetime.strptime(date, "%d:%m:%Y")
        
            # Call the prediction function
            prediction = energy_consumption([home_id, appliance_type, time, date, temperature,season, household_size])
        
            # Display the prediction
            st.success(f"Predicted Energy Consumption: {prediction} ")
        except ValueError:
                st.error("Please enter valid date and time in the specified format.") 



if __name__== "__main__":
     main()



    
    
    
    
    
    
    
    
    
    
    
    
    