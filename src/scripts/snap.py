import time
import uuid
import json
import base64
import requests

from nacl.public import PublicKey, SealedBox

# =========================
# CONSTANTS
# =========================
BASE_URL = "https://snappfood.ir"
TOKEN_ENDPOINT = "/oauth2/default/token"
VENDORS_ENDPOINT = "/search/api/v4/restaurant/vendors-list"

PUBLIC_KEY_B64 = "eUhcujcdUs07+XAa6jPweavHMp26he6HCfowMUlaI08="

CLIENT_ID = "snappfood_pwa"
CLIENT_SECRET = "snappfood_pwa_secret"
SCOPE = "mobile_v2 mobile_v1 webview"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# =========================
# 1️⃣ SERVER TIME SYNC
# =========================
def get_time_diff():
    try:
        r = requests.get(BASE_URL + "/oauth2/default/status", headers=HEADERS, timeout=10)
        r.raise_for_status()
        server_time = r.json()["data"]["time"]
        local_time = int(time.time())
        return server_time - local_time
    except Exception:
        return 0

# =========================
# 2️⃣ BUILD PAYLOAD
# =========================
def build_payload(refresh_token=None, time_diff=0):
    payload = {
        "time": int(time.time()) + time_diff,
        "device_uid": str(uuid.uuid4()),
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
        "grant_type": "client_credentials"
    }
    if refresh_token:
        payload["grant_type"] = "refresh_token"
        payload["refresh_token"] = refresh_token
    return payload

# =========================
# 3️⃣ ENCRYPT PAYLOAD
# =========================
def seal_payload(payload: dict) -> str:
    public_key = PublicKey(base64.b64decode(PUBLIC_KEY_B64))
    sealed_box = SealedBox(public_key)
    plaintext = json.dumps(payload).encode("utf-8")
    encrypted = sealed_box.encrypt(plaintext)
    return base64.b64encode(encrypted).decode("utf-8")

# =========================
# 4️⃣ REQUEST OAUTH TOKEN
# =========================
def request_oauth_token(encrypted_data):
    response = requests.post(
        BASE_URL + TOKEN_ENDPOINT,
        headers=HEADERS,
        json={"data": encrypted_data},
        timeout=15
    )
    return response.status_code, response.json()

# =========================
# 5️⃣ GET VENDORS LIST
# =========================
def get_vendors_list(access_token):
    url = BASE_URL + VENDORS_ENDPOINT
    query_params = {
        "lat": "35.715",
        "long": "51.404",
        "optionalClient": "PWA",
        "client": "PWA",
        "deviceType": "PWA",
        "appVersion": "6.0.0",
        "UDID": str(uuid.uuid4()),
        "Bonyan": "true",
        "extra-filter": json.dumps({
            "vendor_collection": 0,
            "distance_sort": False,
            "vendor_count_respect": False,
            "vendor_collection_view_mode": "",
            "banner_collection": False,
            "new_home": True,
            "new_home_section": "SERVICES",
            "page_supertype": None,
            "user_base_list": False,
            "only_vendor_ids": None,
            "is_ads": False
        }),
        "filters": json.dumps({
            "superType": [2],
            "mode": "CURRENT",
            "item_position": "homePage"
        }),
        "page": "0",
        "page_size": "10",
        "X_ABT": json.dumps({
            "backend_delivery_fee_feature": False,
            "backend_commission_sort_feature": False,
            "backend_sort_home_carousel": False,
            "backend_sort_food_party": False,
            "backend_sort_vendor_search": False,
            "backend_best_offer_badge_on_vendor_card": False,
            "backend_modified_vps_in_product_search": False,
            "backend_active_pro_filter_as_default": False,
            "backend_service_fee_feature": True,
            "backend_food_vendor_list_default_sorting": 0,
            "backend_party_nonfood_feature": False,
            "backend_group_order": True,
            "backend_cpc_search_feature": False,
            "backend_m41_feature": False
        })
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {access_token}",
        "X-Is-Bonyan": "true"
    }

    response = requests.get(url, headers=headers, params=query_params)
    return response.status_code, response.json()

# =========================
# 6️⃣ MAIN FLOW
# =========================
def main():
    print("[*] Syncing server time...")
    time_diff = get_time_diff()
    print(f"[+] Time diff: {time_diff} seconds")

    print("[*] Building payload...")
    payload = build_payload(time_diff=time_diff)
    print(json.dumps(payload, indent=2))

    print("[*] Encrypting payload...")
    encrypted = seal_payload(payload)
    print(f"[+] Encrypted payload length: {len(encrypted)}")

    print("[*] Requesting OAuth token...")
    status, token_response = request_oauth_token(encrypted)
    print(status)
    print(token_response)

    # if status == 200 and "data" in token_response:
    #     access_token = token_response["data"]["access_token"]
    #     print("[+] Access token received!")

    #     print("[*] Fetching vendors list...")
    #     status, vendors_data = get_vendors_list(access_token)
    #     print("Status:", status)
    #     print(json.dumps(vendors_data, indent=2))

    #     # ✅ Write data to vendor.json
    #     with open("vendor.json", "w", encoding="utf-8") as f:
    #         json.dump(vendors_data, f, ensure_ascii=False, indent=2)
    #     print("[+] Data saved to vendor.json")
        
    # else:
    #     print("❌ Failed to get access token")
    #     print(token_response)


if __name__ == "__main__":
    main()
