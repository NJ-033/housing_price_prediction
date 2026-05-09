# Filipino Housing Price Predictor

## System Overview
The Filipino Housing Price Predictor is a modern Python Desktop Application built using `customtkinter` for an elegant graphical user interface. It utilizes a pre-trained Random Forest Machine Learning model (via `scikit-learn`) to accurately estimate property prices in the Philippines based on specific features like bedrooms, bathrooms, floor area, land size, and subdivision. The system also features a secure login system and a database integration to save and manage historical predictions.

## Key Features
- **Modern GUI:** Clean, dark/light mode responsive interface built with `customtkinter`.
- **Machine Learning Integration:** Uses `scikit-learn`'s Random Forest Regressor to predict prices based on housing parameters.
- **Database Management:** Uses local SQLite (with MySQL compatibility in mind) to securely store users and prediction history.
- **Real-Time Validation:** Input fields actively block non-numerical characters to prevent crashes.
- **History Tracking:** View and delete past predictions from an intuitive data table.

## Prerequisites
- Python 3.8 or higher
- Windows/macOS/Linux

## Installation Guide
1. Clone or extract the project folder to your local machine.
2. Open your terminal or command prompt and navigate to the project directory.
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python main.py
   ```
*(Note: The system will automatically create the required database files and tables upon its first launch.)*

## Usage
1. **Login:** Use the default credentials to access the system:
   - **Username:** `admin`
   - **Password:** `admin123`
2. **Predict Price:** Enter the property details into the form. Ensure that numbers are used for all fields. Click "Predict" to generate an estimated housing price.
3. **Save Prediction:** Once a prediction is made, click "Save Prediction" to store it in the database.
4. **My History:** Navigate to the History tab on the sidebar to view, manage, and delete your saved predictions.
