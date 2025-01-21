import requests

# Replace these with your app's credentials
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"
SHORT_LIVED_TOKEN = "YOUR_SHORT_LIVED_TOKEN"  # Obtained earlier via the OAuth flow

def get_long_lived_token(app_id, app_secret, short_lived_token):
    """
    Exchange a short-lived access token for a long-lived token.
    """
    token_url = (
        f"https://graph.facebook.com/v17.0/oauth/access_token?"
        f"grant_type=fb_exchange_token&"
        f"client_id={app_id}&"
        f"client_secret={app_secret}&"
        f"fb_exchange_token={short_lived_token}"
    )
    response = requests.get(token_url)
    if response.status_code == 200:
        data = response.json()
        long_lived_token = data.get("access_token")
        expires_in = data.get("expires_in")
        print(f"Long-Lived Token: {long_lived_token}")
        print(f"Expires in: {expires_in} seconds")
        return long_lived_token
    else:
        print("Error:", response.json())
        return None

# Run the script
if __name__ == "__main__":
    get_long_lived_token(APP_ID, APP_SECRET, SHORT_LIVED_TOKEN)
