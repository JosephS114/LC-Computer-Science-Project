#Importing Module
import pandas as pd


# Function to calculate Evapotranspiration using simplified Hargreaves method
def calculateET(temp, light):
    
    normLight = light/255   # Normalize light intensity (sensor reads 0-255)
    ET = round(0.0135*(temp+17.78)*normLight, 2)   # Rounded to 2 decimal places
    
    return ET

# Function to calculate drought severity score based on rainfall, soil moisture, and evapotranspiration
def calculateDroughtIndex(rainfall, moisture, ET):
    
    normRain = (rainfall - minRain)/(maxRain - minRain) # Normalize rainfall so its inbetween 0–1 range
    normMoisture = (moisture - drySoil)/(wetSoil - drySoil) # Normalize soil moisture so its inbetween 0–1 range
    # Normalize ET so its inbetween 0–1 range and invert it as higher ET = more drought stress
    normET = 1 - (ET - minET)/(maxET - minET)   
    # Calculating Drought Score using weights based on how important each variable is to drought severity
    # Weights: rainfall 0.2, soil moisture 0.6, ET 0.2
    DroughtIndex = round((normRain * 0.2) + (normMoisture * 0.6) + (normET * 0.2), 2)   # Rounded to 2 decimal places
    
    return DroughtIndex.clip(0, 1)

# Function to assign drought status based on drought score
def getDroughtStatus(DroughtIndex):
    
    if DroughtIndex >= 0.75:
        status = "Normal"
    elif DroughtIndex >= 0.5:
        status = "Watch"
    elif DroughtIndex >= 0.25:
        status = "Warning"
    else:
        status = "Severe"
        
    return status


# Open CSV File
df = pd.read_csv("Logged Data.csv")


# Calculate Evapotranspiration for each row
df['Evapotranspiration'] = calculateET(df['Temperature(°C)'], df['Light Intensity(0-255)'])


# Soil moisture constants (0-1023 scale from micro:bit sensor)
wetSoil = 1023  # Wet soil moisture reading
drySoil = 500   # Dry soil moisture reading

# Rainfall constants (in mm) per half hour
maxRain = df['Precipitation(mm) - Open-Source  data'].max()
minRain = 0

# Evapotranspiration constants per half hour
maxET = df['Evapotranspiration'].max()
minET = 0

#------------------------------------
#Scenario 2 - Decreased Soil Moisture 
#------------------------------------

#Creating copy of data
df_DecreasedSoilMoisture = df.copy()

#Making lowering all soil moisture values to 600
df_DecreasedSoilMoisture['Soil Moisture(0-1023)'] = 600

# Calculate drought score and assign drought status
df_DecreasedSoilMoisture['Drought Score'] = calculateDroughtIndex(df_DecreasedSoilMoisture['Precipitation(mm) - Open-Source  data'], df_DecreasedSoilMoisture['Soil Moisture(0-1023)'], df_DecreasedSoilMoisture['Evapotranspiration'])
df_DecreasedSoilMoisture['Drought Status'] = df_DecreasedSoilMoisture['Drought Score'].apply(getDroughtStatus)


# Display Table and Results of scenario
print(df_DecreasedSoilMoisture)
print("\n---------- What-if Scenario 2 - Results ----------")
print(f"Average Drought Score: {df_DecreasedSoilMoisture['Drought Score'].mean():.2f}")
print("Number of Normal Conditions:", df_DecreasedSoilMoisture[df_DecreasedSoilMoisture['Drought Status'] == "Normal"].shape[0])
print("Number of Watch Conditions:", df_DecreasedSoilMoisture[df_DecreasedSoilMoisture['Drought Status'] == "Watch"].shape[0])
print("Number of Warning Conditions:", df_DecreasedSoilMoisture[df_DecreasedSoilMoisture['Drought Status'] == "Warning"].shape[0])
print("Number of Severe Conditions:", df_DecreasedSoilMoisture[df_DecreasedSoilMoisture['Drought Status'] == "Severe"].shape[0])
