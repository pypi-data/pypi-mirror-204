from playwright.sync_api import Route


def replace_resp(route: Route):
    if "http://example.com/" in route.request.url:
        response = route.fetch()
        body = response.text()
        body = body.replace("Example Domain", "gc")
        route.fulfill(
            body=body
        )


addons = [
    replace_resp
]
