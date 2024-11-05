# -*- coding: utf-8 -*-
"""Copy of NAYANA_housePrice(Accuracy).py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zLbE9dgvVwWa3MHWIPUP8PmTu6bo-QYD
"""

import pandas as pd
df=pd.read_csv("https://raw.githubusercontent.com/Nayana940/Dataset/refs/heads/main/house-prices.csv")
df.head()

df.info()

df.columns

df.shape

df.isnull().sum()

import matplotlib.pyplot as plt
categorical_cols = df.select_dtypes(include=['object', 'category']).columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
data_type_counts = pd.Series({'Categorical': len(categorical_cols), 'Numerical': len(numerical_cols)})
print(data_type_counts)
plt.figure(figsize=(8, 5))
data_type_counts.plot(kind='bar', color='green')
plt.title('Count of Categorical and Numerical Columns')
plt.xlabel('Data Type')
plt.ylabel('Count of Columns')
plt.show()

#correlation matrix for numerical features
import seaborn as sns
import matplotlib.pyplot as plt
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
corr_matrix = df[numerical_columns + ['price']].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True,cmap='Greens', linewidths=0.5)
plt.title('Correlation Heatmap of Numerical Features')
plt.show()

#chi square for categorical feture selection
from sklearn.feature_selection import chi2
from sklearn.preprocessing import LabelEncoder
categorical_features = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
label_encoders = {}
for feature in categorical_features:
    le = LabelEncoder()
    df[feature] = le.fit_transform(df[feature])
    label_encoders[feature] = le
X_cat = df[categorical_features]
y = df['price']
chi2_scores, p_values = chi2(X_cat, y)
print("\nChi-Square test for categorical features:")
chi2_results = dict(zip(categorical_features, chi2_scores))
for feature, score in chi2_results.items():
    print(f"{feature}: {score:.2f}")
plt.figure(figsize=(10, 6))
sns.barplot(x=list(chi2_results.keys()), y=list(chi2_results.values()),color='green')
plt.title('Chi-Square Test Scores for Categorical Features', fontsize=16)
plt.xlabel('Categorical Features', fontsize=12)
plt.ylabel('Chi-Square Score', fontsize=12)
plt.tight_layout()
plt.show()

# List of all numerical features to normalize, including 'area'
numerical_features_to_normalize = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']

# Apply Min-Max normalization to bring values between 0 and 1
df[numerical_features_to_normalize] = (df[numerical_features_to_normalize] - df[numerical_features_to_normalize].min()) / (df[numerical_features_to_normalize].max() - df[numerical_features_to_normalize].min())

# Display the first few rows to check the normalized values
print(df[['area', 'bedrooms', 'bathrooms', 'stories', 'parking']].head())

df.columns

#label encoding
df.replace({"yes":1,"no":0},inplace=True)
df.replace({"unfurnished":0,"semi-furnished":1,"furnished":2},inplace=True)
df.head()

from sklearn.model_selection import train_test_split
x=df.drop(['price'],axis=1)
y=df['price']
# Change 'X' to 'x' in the train_test_split function call
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

from sklearn.svm import SVR
model = SVR(kernel='rbf')
model.fit(X_train, y_train)

from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Mean Squared Error:", mse)
accuracy = r2 * 100 #accuracy using r2 score
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 10
accuracy = 100 - mape
print("Mean Absolute Percentage Error:", mape)
print("Accuracy:", accuracy)

!pip install streamlit

import joblib
joblib.dump(model,'/content/model.joblib')

# Commented out IPython magic to ensure Python compatibility.
# %%writefile house_price_app.py
# import streamlit as st
# import pandas as pd
# import joblib
# import numpy as np
# 
# # Load the trained model
# model_path = 'model.joblib'  # Ensure this file exists by loading/saving it in `copy_of_pooja_houseprice.py`
# model = joblib.load(model_path)
# 
# # Define the Streamlit app
# def main():
#     st.title("House Price Prediction")
# 
#     # Collecting user inputs for features
#     st.subheader("Enter House Features")
# 
#     # Input fields based on dataset headers
#     area = st.number_input("Area (in square feet)", min_value=500, max_value=10000, step=10)
#     bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, step=1)
#     bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
#     stories = st.number_input("Number of Stories", min_value=1, max_value=5, step=1)
# 
#     # Binary features (yes/no) where 1 = Yes, 0 = No
#     mainroad = st.selectbox("Is it on the Main Road?", options=['No', 'Yes'])
#     guestroom = st.selectbox("Is there a Guest Room?", options=['No', 'Yes'])
#     basement = st.selectbox("Is there a Basement?", options=['No', 'Yes'])
#     hotwaterheating = st.selectbox("Is there Hot Water Heating?", options=['No', 'Yes'])
#     airconditioning = st.selectbox("Is there Air Conditioning?", options=['No', 'Yes'])
# 
#     parking = st.number_input("Number of Parking Spaces", min_value=0, max_value=5, step=1)
#     prefarea = st.selectbox("Preferred Area?", options=['No', 'Yes'])
# 
#     # Categorical feature for furnishing status
#     furnishingstatus = st.selectbox("Furnishing Status", options=['Unfurnished', 'Semi-furnished', 'Furnished'])
# 
#     # Convert categorical/binary inputs to numeric
#     input_data = pd.DataFrame({
#         'area': [area],
#         'bedrooms': [bedrooms],
#         'bathrooms': [bathrooms],
#         'stories': [stories],
#         'mainroad': [1 if mainroad == 'Yes' else 0],
#         'guestroom': [1 if guestroom == 'Yes' else 0],
#         'basement': [1 if basement == 'Yes' else 0],
#         'hotwaterheating': [1 if hotwaterheating == 'Yes' else 0],
#         'airconditioning': [1 if airconditioning == 'Yes' else 0],
#         'parking': [parking],
#         'prefarea': [1 if prefarea == 'Yes' else 0],
#         'furnishingstatus': [
#             0 if furnishingstatus == 'Unfurnished' else 1 if furnishingstatus == 'Semi-furnished' else 2
#         ]
#     })
# 
#     # Debugging: Display input data
#     st.write("Input Data for Prediction:")
#     st.write(input_data)
# 
#     # Predict and display the result
#     if st.button("Predict Price"):
#         try:
#             prediction = model.predict(input_data)
#             # Convert the prediction to a scalar value
#             predicted_price = float(prediction[0]) if isinstance(prediction, (np.ndarray, list)) else float(prediction)
#             st.write(f"Estimated House Price: ${predicted_price:,.2f}")
#         except Exception as e:
#             st.error(f"Error during prediction: {e}")
# 
# if __name__ == '__main__':
#     main()

!wget -q -O - ipv4.icanhazip.com

! streamlit run house_price_app.py & npx localtunnel --port 8501