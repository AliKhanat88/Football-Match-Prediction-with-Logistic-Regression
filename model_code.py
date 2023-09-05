import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

# Load your dataset
train_data = pd.read_csv('updated_data.csv')  # Replace with your training dataset filename

# Separate categorical and numerical columns
categorical_cols = ['home_club_name', 'away_club_name']
numerical_cols = ['away_goal_std', 'away_goal_mean', 'away_assist_std', 'away_assist_mean', 'home_goal_std', 'home_goal_mean', 'home_assist_std', 'home_assist_mean']

# One-hot encoding for categorical variables
encoder = OneHotEncoder(sparse=False, drop='first', handle_unknown='ignore')
encoded_categorical = encoder.fit_transform(train_data[categorical_cols])
encoded_categorical_df = pd.DataFrame(
    encoded_categorical,
    columns=encoder.get_feature_names_out(categorical_cols)
)

# Combine numerical and encoded categorical data
X_train = pd.concat([train_data[numerical_cols], encoded_categorical_df], axis=1)

# Separate target variables (y)
target_cols = ['WLD', 'BTTS', 'over_1.5', 'over_2.5', 'over_3.5']
y_train = train_data[target_cols]

# Train the models
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

models = {}
for col in target_cols:
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train[col])
    models[col] = model

# Load test data
test_data = pd.read_csv('new_ball_data.csv')  # Replace with your test dataset filename
test_data.fillna(0, inplace=True)

# Preprocess test data using the trained encoder
encoded_categorical_test = encoder.transform(test_data[categorical_cols])
encoded_categorical_test_df = pd.DataFrame(
    encoded_categorical_test,
    columns=encoder.get_feature_names_out(categorical_cols)
)
X_test = pd.concat([test_data[numerical_cols], encoded_categorical_test_df], axis=1)

# Feature scaling for test data
X_test_scaled = scaler.transform(X_test)
from collections import defaultdict
d=defaultdict(int)

# Make predictions using trained models
for i, row in enumerate(X_test_scaled):
    top_3_predictions = {}
    for col, model in models.items():
        y_pred_proba = model.predict_proba([row])  # Get probability estimates
        categories = model.classes_
        prob_categories = list(zip(categories, y_pred_proba[0]))
        sorted_probs = sorted(prob_categories, key=lambda x: x[1], reverse=True)
        top_3_categories = sorted_probs[:3]
        top_3_predictions[col] = top_3_categories


    for key in (top_3_predictions):
        d[i+1,key,top_3_predictions[key][0][0]] = top_3_predictions[key][0][1]
#sorted_keys = sorted(d, key=d.get)
sorted_data = sorted(d.items(), key=lambda x: x[1], reverse=True)
#print(d)


for i in range(min(len(sorted_data) * 3, 10)):
    
    if sorted_data[i][0][1] == "BTTS" and sorted_data[i][0][2] == 1:
        print(f"Match: {test_data.iloc[sorted_data[i][0][0]-1][0]} vs {test_data.iloc[sorted_data[i][0][0]-1][9]} ||||| Outcome: {sorted_data[i][0][1]} ||||| Probability: {sorted_data[i][1]}%")
    elif sorted_data[i][0][1] == "over_1.5":
        result = "over" if sorted_data[i][0][2] == 1 else "under"
        print(f"Match: {test_data.iloc[sorted_data[i][0][0]-1][0]} vs {test_data.iloc[sorted_data[i][0][0]-1][9]} ||||| Outcome: {result} 1.5 ||||| Probability: {round(sorted_data[i][1] * 100, 1)}%")
    elif sorted_data[i][0][1] == "over_2.5":
        result = "over" if sorted_data[i][0][2] == 1 else "under"
        print(f"Match: {test_data.iloc[sorted_data[i][0][0]-1][0]} vs {test_data.iloc[sorted_data[i][0][0]-1][9]} ||||| Outcome: {result} 2.5 ||||| Probability: {round(sorted_data[i][1] * 100, 1)}%")
    elif sorted_data[i][0][1] == "over_3.5":
        result = "over" if sorted_data[i][0][2] == 1 else "under"
        print(f"Match: {test_data.iloc[sorted_data[i][0][0]-1][0]} vs {test_data.iloc[sorted_data[i][0][0]-1][9]} ||||| Outcome: {result} 3.5 ||||| Probability: {round(sorted_data[i][1] * 100, 1)}%")
    elif sorted_data[i][0][1] == "WLD":
        if sorted_data[i][0][2] == "win":
            result = f"{test_data.iloc[sorted_data[i][0][0]-1][0]} Win"
        elif sorted_data[i][0][2] == "lose":
            result = f"{test_data.iloc[sorted_data[i][0][0]-1][0]} Lose"
        else:
            result = "Draw"
        print(f"Match: {test_data.iloc[sorted_data[i][0][0]-1][0]} vs {test_data.iloc[sorted_data[i][0][0]-1][9]} ||||| Outcome: {result} ||||| Probability: {round(sorted_data[i][1] * 100, 1)}%")

print()







