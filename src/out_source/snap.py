import time
from typing import Tuple, Optional
import uuid
import json
import base64
import requests
from nacl.public import PublicKey, SealedBox

class Snap:
    base_url = "https://snappfood.ir"
    


class SnapAnonymousAuth:
    base_url = "https://snappfood.ir"
    token_endpoint = "/oauth2/default/token"
    
    public_key_b64 = "eUhcujcdUs07+XAa6jPweavHMp26he6HCfowMUlaI08="

    client_id = "snappfood_pwa"
    client_secret = "snappfood_pwa_secret"
    scope = "mobile_v2 mobile_v1 webview"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expiry: int = 0

    def get_time_diff(self) -> int:
        try:
            r = requests.get(
                self.base_url + "/oauth2/default/status",
                headers=self.headers,
                timeout=3
            )
            r.raise_for_status()
            server_time = r.json()["data"]["time"]
            local_time = int(time.time())
            return server_time - local_time
        except Exception:
            return 0

    def payload(self, time_diff=0) -> dict:
        return {
            "time": int(time.time()) + time_diff,
            "device_uid": str(uuid.uuid4()),
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
            "grant_type": "client_credentials"
        }

    def seal_payload(self, payload: dict) -> str:
        public_key = PublicKey(base64.b64decode(self.public_key_b64))
        sealed_box = SealedBox(public_key)
        plaintext = json.dumps(payload).encode("utf-8")
        encrypted = sealed_box.encrypt(plaintext)
        return base64.b64encode(encrypted).decode("utf-8")

    def request_oauth_token(self, encrypted_data) -> Tuple[int, dict]:
        response = requests.post(
            self.base_url + self.token_endpoint,
            headers=self.headers,
            json={"data": encrypted_data},
            timeout=15
        )
        return response.status_code, response.json()

    def get_access_token(self) -> str:
        """
        Returns a valid access token.
        Reuses cached token if not expired.
        """
        now = int(time.time())

        if self._access_token and now < self._token_expiry:
            return self._access_token

        time_diff = self.get_time_diff()
        payload = self.payload(time_diff=time_diff)
        encrypted = self.seal_payload(payload)
        status, resp = self.request_oauth_token(encrypted)

        if status == 200 and "data" in resp:
            token_data = resp["data"]
            self._access_token = token_data["access_token"]
            # expires_in is in seconds
            self._token_expiry = now + token_data.get("expires_in", 0) - 10  # small buffer
            return self._access_token
        else:
            raise Exception(f"Failed to get access token: {resp}")

