from copy import copy

from playwright.sync_api import Route


def aaa(route: Route):
    if "response" in route.request.url and "post" == route.request.method.lower():
        response = route.fetch()
        old_data = copy(response.json())
        data = route.replace_data(data=old_data["data"], _new={"gender": ("g", "c")})
        old_data["data"][::] = data
        route.fulfill(
            json=old_data
        )


addons = [
    aaa
]
