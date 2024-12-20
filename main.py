import flet as ft
import msal
import requests

CLIENT_ID = open("client_id.txt").read()
TENANT_ID = open("tenant_id.txt").read()
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"] 

def authenticate_user():
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY
    )
    
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        
    if not result or "access_token" not in result:
        result = app.acquire_token_interactive(
            scopes=SCOPES,
            port=8080,
            prompt="login"
        )

    
    return result

def get_user_profile(access_token):
    graph_endpoint = "https://graph.microsoft.com/v1.0/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(graph_endpoint, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("displayName", ""), data.get("mail", "")

def main(page: ft.Page):
    page.title = "Single Sign On (SSO)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    welcome_text = ft.Text(value="Welcome, please authenticate!", size=20)
    sign_in_button = ft.ElevatedButton(text="Sign In with Microsoft", on_click=lambda e: sign_in_clicked(e, page, welcome_text))

    page.add(welcome_text, sign_in_button)

def sign_in_clicked(e, page, welcome_text):
    try:
        print("Sign-in button clicked")
        page.show_snack_bar(ft.SnackBar(ft.Text("Signing in..."), open=True))
        print("Before authenticate_user")
        result = authenticate_user()
        print("After authenticate_user, result =", result)
        if result and "access_token" in result:
            name, email = get_user_profile(result["access_token"])
            print("Fetched profile:", name, email)
            welcome_text.value = f"Hello {name}, your email is {email}"
            page.update()
        else:
            print("No access_token in result:", result)
            welcome_text.value = "Authentication failed."
            page.update()
    except Exception as ex:
        welcome_text.value = f"Error: {str(ex)}"
        print("Exception occurred:", ex)
        page.update()


if __name__ == "__main__":
    ft.app(target=main)
