import pandas as pd
import streamlit as st
from joblib import load
from load_data import load_data, model_training_prediction

players = load_data()

x_scaled, y_scaled, x_train, x_test, y_train, y_test, y_pred, x_columns = model_training_prediction()

model = load('model/RFR.pkl')
scaler = load('model/scaler.pkl')

from matplotlib.pyplot import scatter, subplots, rcParams, plot
rcParams.update({
    'font.family': 'Times New Roman',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.facecolor': '#071330',
    'axes.facecolor': '#0c4160',
    'axes.edgecolor': '#000000',
    'axes.labelcolor': '#ffffff',
    'xtick.color': '#ffffff',
    'ytick.color': '#ffffff',
    'text.color': 'white',
    'grid.color': '#3ffcc9'
})

show = st.sidebar.checkbox('Show Scatter Plot', value=True)

if show:
    x_test_df = pd.DataFrame(scaler.inverse_transform(x_test), columns=x_columns)
    x_test_df['y_test'] = y_test
    x_test_df['y_pred'] = y_pred
    sorted = x_test_df.sort_values(by='reactions')
    from numpy import argsort
    indices = argsort(x_test_df['reactions'])
    fig, ax = subplots(figsize=(10,5))
    ax.scatter(sorted['reactions'], sorted['y_test'])
    ax.plot(sorted['reactions'], sorted['y_pred'])
    ax.set_title('Scatter Plot Of Model\'s Predictions')
    ax.set_xlabel('Reactions')
    ax.set_ylabel('Value')
    st.pyplot(fig)

#new

# Load scaler, model, and label encoder
scaler = load('model/scaler.pkl')
model = load('model/RFR.pkl')
label_encoder = load('model/encoder.pkl')  # make sure you saved this during training

# List of numeric features (excluding 'player', 'country', 'value')
numeric_features = [
    "height", "weight", "age",
    "ball_control", "dribbling", "slide_tackle", "stand_tackle",
    "aggression", "reactions", "att_position", "interceptions",
    "vision", "composure", "crossing",
    "short_pass", "long_pass",
    "acceleration", "stamina", "strength", "balance",
    "sprint_speed", "agility", "jumping", "heading",
    "shot_power", "finishing", "long_shots", "curve",
    "fk_acc", "penalties", "volleys",
    "gk_positioning", "gk_diving", "gk_handling",
    "gk_kicking", "gk_reflexes"
]

# Load clubs from the encoder's classes
club_options = list(label_encoder.classes_)

st.title("Player Value Prediction")

with st.form("player_input_form"):
    # Get all numeric inputs
    inputs = {}
    for feature in numeric_features:
        inputs[feature] = st.number_input(
            label=feature.replace("_", " ").title(),
            min_value=players[feature].min(),
            value=players[feature].min(),
            step=1
        )

    # Select club and encode
    selected_club = st.multiselect("Select Club", club_options)

    submitted = st.form_submit_button("Predict", use_container_width=True)

if submitted:
    # Encode club
    encoded_club = label_encoder.transform([selected_club])[0]

    # Combine all features into one DataFrame
    input_values = [inputs[f] for f in numeric_features]
    full_input = input_values + [encoded_club]

    # Ensure column order matches training
    full_input_df = pd.DataFrame([full_input], columns=numeric_features + ['club'])

    # Scale features
    scaled_input = scaler.transform(full_input_df)

    # Predict
    prediction = model.predict(scaled_input)

    st.success(f"Predicted Value: ${prediction[0] * 10000000:,.2f}")
