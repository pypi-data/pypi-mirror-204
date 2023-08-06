import asyncio
from playwright._impl._impl_to_api_mapping import ImplToApiMapping
from playwright.sync_api import Page, Route
from .function import *

mapping = ImplToApiMapping()


def stop_(self):
    async def stop():
        async def inner():
            while True:
                await asyncio.sleep(1)

        await asyncio.gather(inner())

    return mapping.from_maybe_impl(self._sync(stop()))


setattr(Page, "stop", stop_)
for func in function.__all__:  # noqa: F405
    setattr(Route, func, getattr(function, func))  # noqa: F405
