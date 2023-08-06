from playwright.sync_api import Route


def handler1(route: Route):
    if "__LOGIN_ASSETS" in route.request.url:
        route.fulfill(
            json={
                "status": 1,
                "message": "操作成功",
                "data": {
                    "json": """{\"logoWidth\":118,\"loginTitle\":\"高创\",\"tagTitle\":\"资源智能优化协同平台\",\"fontSize\":22,\"title\":\"资源智能优化协同平台\",\"fileName\":\"\",\"bgFileName\":\"\",\"tagFileName\":\"\"}""",
                    "key": "__LOGIN_ASSETS"
                }
            }
        )


addons = [
    handler1
]
