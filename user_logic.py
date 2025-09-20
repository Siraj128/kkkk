import pandas as pd
from datetime import datetime
import jwt

def handle_user_login(token, users_file='users.csv'):
    """Decodes token, manages user registration, and returns user's full record."""
    try:
        decoded_token = jwt.decode(token['id_token'], options={"verify_signature": False})
    except Exception:
        return None

    try:
        users_df = pd.read_csv(users_file)
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=['email', 'name', 'last_login', 'profile_complete'])

    user_email = decoded_token.get('email')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if user_email in users_df['email'].values:
        users_df.loc[users_df['email'] == user_email, 'last_login'] = timestamp
        users_df.to_csv(users_file, index=False)
        return users_df[users_df['email'] == user_email].iloc[0]
    else:
        new_user = pd.DataFrame({
            'email': [user_email],
            'name': [decoded_token.get('name', 'N/A')],
            'last_login': [timestamp],
            'profile_complete': [False]
        })
        updated_users_df = pd.concat([users_df, new_user], ignore_index=True)
        updated_users_df.to_csv(users_file, index=False)
        return updated_users_df[updated_users_df['email'] == user_email].iloc[0]

def complete_profile_setup(email, new_username, users_file='users.csv'):
    """Updates the user's name and sets their profile to complete."""
    try:
        users_df = pd.read_csv(users_file)
        # Find the user and update their name and profile status
        users_df.loc[users_df['email'] == email, 'name'] = new_username
        users_df.loc[users_df['email'] == email, 'profile_complete'] = True
        users_df.to_csv(users_file, index=False)
        return True
    except Exception as e:
        print(f"Error updating profile: {e}")
        return False