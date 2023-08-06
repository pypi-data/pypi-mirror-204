from playwright.sync_api import Route


def a(route: Route):
    if "showre" in route.request.url and "POST" == route.request.method.upper():
        route.fulfill(
            body='{"status": 2222,"message": "操作成功", "data": {"key": "__LOGIN_ASSETS"}}',
            content_type="application/json;charset=utf-8"
        )


addons = [
    a
]
