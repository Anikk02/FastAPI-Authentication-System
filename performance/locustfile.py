import random
import string
from locust import HttpUser, task, between


PASSWORD = "strongpass123"


def random_email(prefix: str = "user") -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{suffix}@example.com"


def random_name() -> str:
    suffix = "".join(random.choices(string.ascii_letters, k=5))
    return f"User{suffix}"


class RegisterUser(HttpUser):
    """
    Simulates new users registering.
    Keep this user count LOW because registration is a write-heavy operation.
    """
    wait_time = between(2, 5)
    weight = 1

    @task
    def register(self):
        payload = {
            "name": random_name(),
            "email": random_email("register"),
            "password": PASSWORD
        }

        with self.client.post(
            "/auth/register",
            json=payload,
            name="POST /auth/register",
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Register failed | status={response.status_code} | body={response.text}"
                )


class LoginUser(HttpUser):
    """
    Simulates existing users logging in repeatedly.
    Each Locust user creates one account on start, then performs login requests.
    """
    wait_time = between(1, 3)
    weight = 2

    def on_start(self):
        self.email = random_email("login")
        self.name = random_name()

        register_payload = {
            "name": self.name,
            "email": self.email,
            "password": PASSWORD
        }

        register_response = self.client.post(
            "/auth/register",
            json=register_payload,
            name="SETUP /auth/register"
        )

        if register_response.status_code not in [200, 201]:
            print(
                f"[LoginUser Setup] Register failed | status={register_response.status_code} "
                f"| body={register_response.text}"
            )

    @task
    def login(self):
        payload = {
            "email": self.email,
            "password": PASSWORD
        }

        with self.client.post(
            "/auth/login",
            json=payload,
            name="POST /auth/login",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    response.success()
                else:
                    response.failure("Login succeeded but access_token missing")
            else:
                response.failure(
                    f"Login failed | status={response.status_code} | body={response.text}"
                )


class ProtectedUser(HttpUser):
    """
    Simulates authenticated users mostly accessing protected routes.
    This is usually the most realistic read-heavy traffic pattern.
    """
    wait_time = between(1, 2)
    weight = 5

    def on_start(self):
        self.email = random_email("protected")
        self.name = random_name()
        self.token = None

        register_payload = {
            "name": self.name,
            "email": self.email,
            "password": PASSWORD
        }

        register_response = self.client.post(
            "/auth/register",
            json=register_payload,
            name="SETUP /auth/register"
        )

        if register_response.status_code not in [200, 201]:
            print(
                f"[ProtectedUser Setup] Register failed | status={register_response.status_code} "
                f"| body={register_response.text}"
            )
            return

        login_payload = {
            "email": self.email,
            "password": PASSWORD
        }

        login_response = self.client.post(
            "/auth/login",
            json=login_payload,
            name="SETUP /auth/login"
        )

        if login_response.status_code == 200:
            data = login_response.json()
            self.token = data.get("access_token")
        else:
            print(
                f"[ProtectedUser Setup] Login failed | status={login_response.status_code} "
                f"| body={login_response.text}"
            )

    @task(4)
    def get_current_user(self):
        if not self.token:
            return

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        with self.client.get(
            "/auth/me",
            headers=headers,
            name="GET /auth/me",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"/auth/me failed | status={response.status_code} | body={response.text}"
                )

    @task(1)
    def relogin(self):
        """
        Simulate session refresh / repeated auth.
        """
        payload = {
            "email": self.email,
            "password": PASSWORD
        }

        with self.client.post(
            "/auth/login",
            json=payload,
            name="POST /auth/login (re-auth)",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    self.token = token
                    response.success()
                else:
                    response.failure("Re-login succeeded but token missing")
            else:
                response.failure(
                    f"Re-login failed | status={response.status_code} | body={response.text}"
                )