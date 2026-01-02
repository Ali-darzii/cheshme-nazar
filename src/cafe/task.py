import json
import uuid
import requests
import logging

from src.core import celery_app
from src.out_source.snap import SnapAnonymousAuth

logger = logging.getLogger("cheshme-nazar")
snap_auth = SnapAnonymousAuth()

@celery_app.task(queue="scrape_snap_cafe")
def scrape_snap_cafe():
    access_token = snap_auth.get_access_token()

    BASE_URL = "https://snappfood.ir"
    VENDOR_ENDPOINT = "/search/api/v4/restaurant/vendors-list"
    
    url = BASE_URL + VENDOR_ENDPOINT
    query_params = {
        "lat": "35.72809",
        "long": "51.4845",
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
    logger.info(f"status: {response.status_code} snap's cafes")

