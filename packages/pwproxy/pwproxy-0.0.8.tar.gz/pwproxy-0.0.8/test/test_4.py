from playwright.sync_api import Route


def aaa(route: Route):
    if "response" in route.request.url and "post" == route.request.method.lower():
        response = route.fetch()
        data = route.delete_col(data=response.json()["data"], cols=["gander"])
        route.fulfill(
            json=data
        )


addons = [
    aaa
]
