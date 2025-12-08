from src.auth.routes.v1.api import router as v1_auth_router

v1_prefix = "/v1"

v1_routers = (
    (v1_prefix, v1_auth_router)
)