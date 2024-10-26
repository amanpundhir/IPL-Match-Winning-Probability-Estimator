# Cricket Match Winning Probability Estimator

This project is a web application that estimates the winning probability of a cricket match based on historical match data and user input. The application allows users to input current match conditions and retrieves similar historical scenarios to provide insights.

## Features

- Select batting and bowling teams.
- Input target score, current score, overs completed, and wickets fallen.
- Display winning probabilities for both teams.
- List similar historical scenarios for reference.

## Technologies Used

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Handling**: Pandas, NumPy
- **Model Used**: Logistic Regression

## Prerequisites

To run this project, ensure you have Python installed on your system. You will also need to install the necessary libraries.

## Installation

1. **Clone the repository**:
   ```bash
   
   git clone https://github.com/amanpundhir/IPL-Match-Winning-Probability-Estimator.git
   
   cd IPL-Match-Winning-Probability-Estimator
   
   ```
2. Install required packages: You can install the necessary libraries using the requirements.txt file:
   ```bash
   
   pip install -r requirements.txt
   ```
3. Run the application: Start the Flask development server:
   ```bash
   
   python app.py
   ```
The application will be available at http://127.0.0.1:5000.
