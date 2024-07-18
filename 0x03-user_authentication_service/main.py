#!/usr/bin/env python3
"""Testing all the routes in my Web App"""
import requests


def register_user(email: str, password: str) -> None:
    """test register a user route"""
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/users", data=data)
    assert response.json() == {"email": email, "message": "user created"}
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with a wrong password"""
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with a correct credentials"""
    data = {"email": email, "password": password}
    response = requests.post("http://127.0.0.1:5000/sessions", data=data)
    email = response.json().get("email")
    assert response.json() == {"email": email, "message": "logged in"}
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test profile unlogged"""
    response = requests.get("http://127.0.0.1:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile logged"""
    cookies = {"session_id": session_id}
    response = requests.get("http://127.0.0.1:5000/profile", cookies=cookies)
    email = response.json().get("email")
    assert response.json() == {"email": email}
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Test logout route"""
    cookies = {"session_id": session_id}
    response = requests.delete(
        "http://127.0.0.1:5000/sessions", cookies=cookies)
    assert response.json() == {"message": "Bienvenue"}
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Test reset_password_token route"""
    data = {"email": email}
    response = requests.post("http://127.0.0.1:5000/reset_password", data=data)
    token = response.json().get("reset_token")
    assert response.json() == {"email": email, "reset_token": token}
    assert response.status_code == 200
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test the update password route"""
    data = {
        "email": email, "new_password": new_password,
        "reset_token": reset_token
    }
    response = requests.put("http://127.0.0.1:5000/reset_password", data=data)
    assert response.json() == {"email": email, "message": "Password updated"}
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    """Testing"""
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
