import streamlit as st
import pandas as pd

import pickle
import matplotlib.pyplot as plt
import seaborn as sns


def load_model():
    
    #loading the saved model
    loaded_model=pickle.load(open('C:/Users/91807/OneDrive/Desktop/energy_consumption_prediction/trained_model.sav','rb')) 
    return loaded_model
    


   



def load_dataset():
    
    return pd.read_csv("C:/Users/91807/OneDrive/Desktop/energy_consumption_prediction/smart_home_energy_consumption_large.csv")


#def authenticate(username, password):
    #return username == "admin" and password == "password123"
USER_CREDENTIALS = {
    "admin": "password123",
    "vinay_kumar": "Vinay@2003",
    "Himaja": "Himaja",
    "Suraksha":"Suraksha",
    "Krithika":"Krithika"
}

def authenticate(username, password):
    return USER_CREDENTIALS.get(username) == password

# Login page
def login_page():
    st.title("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password")

# Prediction page
def prediction_page(model):
    st.title("🔮 Energy Consumption Prediction")

    def energy_consumption(input_data):
        #loading the saved model
        loaded_model=pickle.load(open('C:/Users/91807/OneDrive/Desktop/energy_consumption_prediction/trained_model.sav','rb')) 
        home_id, date, temperature, season, household_size = input_data

        # Generate input for all appliances over the day
        date_parsed = pd.to_datetime(date, format='%d:%m:%Y')
        prediction_data = pd.DataFrame({
            'home_id': [home_id] * 24,
            'appliance_type': ['all appliances'] * 24,  # Assuming aggregated data
            'season': [season] * 24,
            'household_size': [household_size] * 24,
            'outdoor_temperature': [temperature] * 24,
            'hour': list(range(24)),
            'day': [date_parsed.day] * 24,
            'month': [date_parsed.month] * 24
        })

        # Predict energy consumption for the entire day
        daily_predictions = loaded_model.predict(prediction_data)
        total_energy_consumption = daily_predictions.sum()

        return f"Predicted total energy consumption for {date}: {total_energy_consumption} kW"

    # Title of the app
    st.write("Input data for prediction:")

    # Home ID input
    home_id = st.number_input(
        "🏠 Home ID",
        min_value=1,
        max_value=500,
        value=1,
        step=1,
        help="Please enter values between 1 to 500"
    )

    # Date input
    date = st.text_input("📅 Date (DD:MM:YYYY)", "01:01:2025")

    # Temperature input
    temperature = st.number_input("🌡️ Temperature (°C)", value=25.0, step=0.1)

    # Season selection
    season = st.selectbox("🗓️ Season", ["Winter", "Summer", "Fall", "Spring"])

    # Household size input
    household_size = st.number_input(
        "👨‍👩‍👧‍👦 Occupancy",
        min_value=1,
        value=1,
        step=1,
        help="Enter the number of people in the household"
    )

    # Predict button
    if st.button("Predict"):
        # Call the prediction function
        prediction = energy_consumption((home_id, date, temperature, season, household_size))

        # Display the prediction
        st.success(f"{prediction}")

# Visualization page
def visualization_page(dataset):
    st.title("📊 Dataset and Visualizations")

    st.write("### 📋 Dataset")
    st.dataframe(dataset)

    st.write("### 📈 Visualizations")

    # Energy Consumption Distribution
    if st.checkbox("Show Energy Consumption Distribution"):
        st.subheader("Energy Consumption Distribution")
        fig, ax = plt.subplots()
        dataset['Energy Consumption (kWh)'].hist(ax=ax, bins=20, color='skyblue')
        ax.set_xlabel("Energy Consumption (kW)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    # Household Size vs. Energy Consumption
    if st.checkbox("Show Household Size vs. Energy Consumption"):
        st.subheader("Household Size vs. Energy Consumption")
        fig, ax = plt.subplots()
        ax.scatter(dataset['Household Size'], dataset['Energy Consumption (kWh)'], color='green')
        ax.set_xlabel("Household Size")
        ax.set_ylabel("Energy Consumption (kW)")
        st.pyplot(fig)

    # Average Energy Consumption by Appliance Type
    if st.checkbox("Show Average Energy Consumption by Appliance Type"):
        st.subheader("Average Energy Consumption by Appliance Type")
        avg_consumption = dataset.groupby('Appliance Type')['Energy Consumption (kWh)'].mean()
        fig, ax = plt.subplots()
        avg_consumption.plot(kind='bar', ax=ax, color='orange')
        ax.set_ylabel("Average Energy Consumption (kW)")
        st.pyplot(fig)
        
    if st.checkbox("Show Energy Consumption Share by Appliance"):
        st.subheader("Energy Consumption Share by Appliance")
        appliance_share = dataset.groupby('Appliance Type')['Energy Consumption (kWh)'].sum()
        fig, ax = plt.subplots()
        appliance_share.plot.pie(ax=ax, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3"))
        ax.set_ylabel('')
        st.pyplot(fig)
        
    
        

        
   

        
 


    

    

# Logout function
def logout():
    st.session_state["authenticated"] = False

# Main application
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Load resources
model = load_model()
dataset = load_dataset()

if not st.session_state["authenticated"]:
    login_page()
else:
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Go to", ["Prediction", "Visualization"])
    if st.sidebar.button("🔓 Logout"):
        logout()

    if page == "Prediction":
        prediction_page(model)
    elif page == "Visualization":
        visualization_page(dataset)

    
    
    
