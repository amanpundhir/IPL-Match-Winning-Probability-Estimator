from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# Load the model pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Load historical match data from CSV file
historical_data_path = 'all_matches.csv'  
all_matches_df = pd.read_csv(historical_data_path)


def find_closest_scenarios(all_matches_df, input_data, num_scenarios=5):
    runs_left, balls_left, wickets_left, crr, rrr = input_data

    # Calculate the distance metric for finding closest scenarios
    all_matches_df['distance'] = np.sqrt(
        (all_matches_df['runs_left'] - runs_left) ** 2 +
        (all_matches_df['balls_left'] - balls_left) ** 2 +
        (all_matches_df['wickets_left'] - wickets_left) ** 2 +
        (all_matches_df['crr'] - crr) ** 2 +
        (all_matches_df['rrr'] - rrr) ** 2
    )

    # Get the closest scenarios based on the smallest distance
    closest_scenarios_df = all_matches_df.nsmallest(num_scenarios * 2, 'distance')  

    output = []
    seen_scenarios = set()  # Set to track unique scenarios

    for _, row in closest_scenarios_df.iterrows():
        # Create a unique identifier for each scenario
        scenario_key = (row['batting_team'], row['bowling_team'], row['total_runs'], 
                         10 - row['wickets_left'], 20 - (row['balls_left'] // 6))

        # If the scenario is unique, add it to the output
        if scenario_key not in seen_scenarios:
            seen_scenarios.add(scenario_key)  
            
            scenario = {
                'batting_team': row.get('batting_team', 'N/A'),
                'bowling_team': row.get('bowling_team', 'N/A'),
                'total_runs': row.get('total_runs', 'N/A'),
                'wickets_fallen': 10 - row['wickets_left'],
                'overs_completed': 20 - (row['balls_left'] // 6),
                'runs_required': row['runs_left'],
                'winning_team': row.get('batting_team', 'N/A') if row['result'] == 1 else row.get('bowling_team', 'N/A')
            }
            output.append(scenario)

        # Stop if we have enough unique scenarios
        if len(output) >= num_scenarios:
            break

    # If we have fewer scenarios than required, return what we have
    return output if len(output) == num_scenarios else []


@app.route('/')
def home():
    return render_template('index.html')  
@app.route('/estimate', methods=['POST'])
def estimate():
    data = request.json

    batting_team = data['batting_team']
    bowling_team = data['bowling_team']
    target = data['target']
    score = data['score']
    overs = data['overs']
    wickets = data['wickets']

    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'target': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    closest_scenarios = find_closest_scenarios(all_matches_df, [runs_left, balls_left, wickets_left, crr, rrr])

    return jsonify({
        'batting_team_probability': round(win * 100),
        'bowling_team_probability': round(loss * 100),
        'closest_scenarios': closest_scenarios
    })

if __name__ == '__main__':
    app.run(debug=True)
