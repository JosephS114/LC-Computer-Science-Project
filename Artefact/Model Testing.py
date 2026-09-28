# Import model to use its functions
import ProjectModel as model

# Function to test drought model
def droughtModelTest():
    # Test input data for different enviromental conditions
    lightLevel = [0, 255, 20, 100, 150]
    temp = [0, 20, -2, 10, 15]
    rainfall = [0, 0.1, 0.8, 0.6, 0.4]
    moisture = [500, 500, 1023, 800, 700]
    
    # Expected results from tests
    results = ['Severe', 'Severe', 'Normal', 'Watch', 'Warning']
    
    # Track number of tests passed
    passedTests = 0
    
    # Print header for table
    print('\nTemperature : Light Level : Rain(mm) : Soil : Evapotranspiration : Index : Status : Expected : Pass/Fail')
    
    # Loop for each test
    for i in range(len(results)):
        # Retrieve expected result for this test
        expectedStatus = results[i]
        
        # Retrieve temperature and light level
        temperature = temp[i]
        lightIntensity = lightLevel[i]
        
        #Calculate evapotranspiration from light and temperature data
        evapotranspiration = model.calculateET(temperature, lightIntensity)
        
        # Retrieve rainfall and soil moisture values
        precipitation  = rainfall[i]
        soilMoisture = moisture[i]
        
        # Calculating drought index and status from model functions
        droughtIndex = model.calculateDroughtIndex(precipitation, soilMoisture, evapotranspiration)
        actualStatus = model.getDroughtStatus(droughtIndex)
        
        # Compare actual result with expected result
        if actualStatus == expectedStatus:
            test = 'Pass'
            passedTests += 1
        else:
            test = 'Fail'
        
        # Print results for this test
        print(temperature, ':', lightIntensity, ':', precipitation, ':', soilMoisture,':', evapotranspiration, ':', droughtIndex, ':', actualStatus, ':', expectedStatus, ':', test)
    
    # Print umber of tests passed
    print("\nPassed:", passedTests, "out of", len(results))

# Run test
droughtModelTest()