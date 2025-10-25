# 📊 CSV Upload Guide for NewAI Churn Model

## 🎯 **CSV Upload Functionality Successfully Added!**

The NewAI churn prediction model now includes comprehensive CSV file upload functionality with validation, processing, and analysis capabilities.

## 🚀 **New Features Added**

### **📁 CSV Upload Interface**
- **File Selection**: Choose CSV files with customer data
- **Progress Bar**: Visual upload progress indicator
- **Validation**: Automatic column validation and error handling
- **Status Messages**: Real-time feedback on upload status
- **Sample CSV**: Download sample data for testing

### **🔧 Upload Process**
1. **File Selection**: Click "Choose CSV File" to select your data
2. **Validation**: System checks for required columns (customerID)
3. **Processing**: CSV data is parsed and validated
4. **Storage**: Data is stored for churn prediction analysis
5. **Feedback**: Success/error messages displayed

### **📊 Data Processing**
- **Column Detection**: Automatic detection of data columns
- **Data Validation**: Checks for required fields
- **Error Handling**: Clear error messages for invalid data
- **Data Storage**: Uploaded data stored for analysis

## 🎨 **User Interface Updates**

### **Upload Section**
```
┌─────────────────────────────────────────────────────────┐
│  📊 Upload Customer Data                                │
├─────────────────────────────────────────────────────────┤
│  Upload a CSV file with customer data for churn        │
│  prediction analysis. Required columns: customerID     │
│                                                         │
│  [Choose CSV File] [Download Sample CSV]               │
│  Selected: customers.csv                               │
│                                                         │
│  ████████████████████████████████████████ 100%         │
│  Processing complete!                                   │
│                                                         │
│  ✅ Successfully uploaded 100 customer records         │
└─────────────────────────────────────────────────────────┘
```

### **Enhanced Results Table**
- **Additional Columns**: Contract, Internet Service
- **Data Integration**: Uses uploaded CSV data
- **Risk Analysis**: Based on actual customer attributes
- **Export Functionality**: Download predictions as CSV

## 🔧 **Technical Implementation**

### **JavaScript Functions Added**
- **`handleCSVUpload(event)`**: Handles file selection and upload
- **`processCSVFile(file)`**: Processes and validates CSV data
- **`generateChurnPredictionsFromData(data)`**: Creates predictions from uploaded data
- **`createSampleCSV()`**: Generates sample CSV for testing
- **`downloadNewAIPredictions()`**: Exports predictions as CSV

### **Data Validation**
```javascript
// Required columns validation
const requiredColumns = ['customerID'];
const missingColumns = requiredColumns.filter(col => !headers.includes(col));

if (missingColumns.length > 0) {
    // Show error message
    return;
}
```

### **Churn Prediction Logic**
```javascript
// Adjust probability based on customer data
if (customer.tenure && customer.tenure < 12) {
    probability += 0.2; // Higher churn risk for new customers
}
if (customer.MonthlyCharges && customer.MonthlyCharges > 70) {
    probability += 0.1; // Higher risk for expensive plans
}
if (customer.Contract && customer.Contract === 'Month-to-month') {
    probability += 0.15; // Higher risk for month-to-month
}
```

## 📊 **CSV File Requirements**

### **Required Columns**
- **`customerID`**: Unique customer identifier (required)

### **Optional Columns (for enhanced analysis)**
- **`tenure`**: Customer tenure in months
- **`MonthlyCharges`**: Monthly billing amount
- **`Contract`**: Contract type (Month-to-month, One year, Two year)
- **`InternetService`**: Internet service type (DSL, Fiber optic, No)
- **`gender`**: Customer gender
- **`SeniorCitizen`**: Senior citizen status
- **`Partner`**: Partner status
- **`Dependents`**: Dependents status
- **`PhoneService`**: Phone service status
- **`MultipleLines`**: Multiple lines status
- **`OnlineSecurity`**: Online security status
- **`OnlineBackup`**: Online backup status
- **`DeviceProtection`**: Device protection status
- **`TechSupport`**: Tech support status
- **`StreamingTV`**: Streaming TV status
- **`StreamingMovies`**: Streaming movies status
- **`PaperlessBilling`**: Paperless billing status
- **`PaymentMethod`**: Payment method
- **`TotalCharges`**: Total charges
- **`Churn`**: Churn status (Yes/No)

### **Sample CSV Format**
```csv
customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges,Churn
7590-VHVEG,Female,0,Yes,No,1,No,No phone service,DSL,No,Yes,No,No,No,No,Month-to-month,Yes,Electronic check,29.85,29.85,No
5575-GNVDE,Male,0,No,No,34,Yes,No,DSL,Yes,No,Yes,No,No,No,One year,No,Mailed check,56.95,1889.5,No
```

## 🎯 **Usage Instructions**

### **Step 1: Prepare Your Data**
1. Create a CSV file with customer data
2. Ensure `customerID` column is present
3. Include additional columns for better analysis

### **Step 2: Upload Data**
1. Navigate to the NewAI tab in the web interface
2. Click "Choose CSV File" to select your data
3. Wait for upload and validation to complete
4. Check status messages for any errors

### **Step 3: Run Analysis**
1. Click "Run Churn Prediction" to analyze the data
2. View results in the interactive table
3. Examine risk distribution charts
4. Analyze individual customers

### **Step 4: Export Results**
1. Click "Download Predictions" to export results
2. CSV file will include churn probabilities and risk levels
3. Use results for retention strategies

## 🔍 **Error Handling**

### **Common Issues and Solutions**

#### **Missing Required Columns**
```
❌ Missing required columns: customerID
```
**Solution**: Ensure your CSV file includes a `customerID` column

#### **Invalid File Format**
```
❌ Error processing CSV file: Invalid format
```
**Solution**: Ensure the file is a valid CSV with proper formatting

#### **Empty Data**
```
No customer data uploaded. Please upload a CSV file first.
```
**Solution**: Upload a CSV file before running predictions

## 📊 **Enhanced Analysis Features**

### **Risk Assessment**
- **Low Risk**: Probability < 30%
- **Medium Risk**: Probability 30-70%
- **High Risk**: Probability > 70%

### **Risk Factors**
- **New Customers**: Higher risk for tenure < 12 months
- **Expensive Plans**: Higher risk for MonthlyCharges > $70
- **Month-to-Month**: Higher risk for flexible contracts

### **Results Table Columns**
- **Customer ID**: Unique identifier
- **Churn Probability**: 0-100% risk score
- **Risk Level**: Low/Medium/High classification
- **Monthly Charges**: Billing amount
- **Tenure**: Months as customer
- **Contract**: Contract type
- **Internet Service**: Service type
- **Action**: Individual analysis button

## 🎉 **Ready to Use!**

The CSV upload functionality is now **fully operational** with:

✅ **File Upload**: Choose and upload CSV files
✅ **Data Validation**: Automatic column and format checking
✅ **Progress Tracking**: Visual upload progress
✅ **Error Handling**: Clear error messages and solutions
✅ **Sample Data**: Download sample CSV for testing
✅ **Enhanced Analysis**: Risk assessment based on uploaded data
✅ **Export Results**: Download predictions as CSV
✅ **Real-time Feedback**: Status messages and notifications

**Start uploading your customer data for advanced churn prediction analysis!** 🚀📊✨
