# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the Random Forest Classifier model
try:
    filename = 'first-innings-score-lr-model.pkl'
    with open(filename, 'rb') as model_file:
        regressor = pickle.load(model_file)
except FileNotFoundError:
    print(f"Model file {filename} not found. Please check the file path.")
    regressor = None
except Exception as e:
    print(f"Error loading the model: {e}")
    regressor = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if regressor is None:
        return "Model is not loaded. Please contact the administrator."

    temp_array = []

    if request.method == 'POST':
        
        # Get the Batting Team
        batting_team = request.form.get('batting-team', '')
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]

        # Get the Bowling Team
        bowling_team = request.form.get('bowling-team', '')
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]

        # Get other match data (overs, runs, wickets, etc.)
        try:
            overs = float(request.form['overs'])
            runs = int(request.form['runs'])
            wickets = int(request.form['wickets'])
            runs_in_prev_5 = int(request.form['runs_in_prev_5'])
            wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        except ValueError:
            return "Invalid input. Please enter correct numerical values."

        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        # Convert list to numpy array and make prediction
        data = np.array([temp_array])
        try:
            my_prediction = int(regressor.predict(data)[0])
        except Exception as e:
            return f"Error during prediction: {e}"

        return render_template('result.html', lower_limit=my_prediction-10, upper_limit=my_prediction+5)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
