import runpy
import sys
import types
from abc import abstractmethod
from pathlib import Path
from typing import Literal
from playwright.sync_api import sync_playwright, Browser, Page, Route, Error
from importlib import reload


class Base:
    _page = None

    @classmethod
    @abstractmethod
    def run(cls, script: str | Path, url, browser: Literal["chromium", "firefox", "webkit"], channel=None):
        driver = sync_playwright().start()
        br: Browser = getattr(driver, browser).launch(headless=False, args=["--start-maximized"], channel=channel)
        page: Page = br.new_page(no_viewport=True)
        page.route("**/*", cls.handler)
        if url:
            page.goto(url)
        page.stop()

        return page

    @classmethod
    @abstractmethod
    def handler(cls, route: Route):
        pass


class Run(Base):
    path = None

    @classmethod
    def run(cls, script: str | Path, url=None, browser="chromium", channel="chrome"):
        path = Path(script) if isinstance(script, str) else script
        if not path.exists():
            raise FileNotFoundError(f"{str(path)!r} 文件不存在")
        cls.path = path
        page = super().run(path, url, browser, channel)
        return page

    @classmethod
    def handler(cls, route: Route):
        code = runpy.run_path(cls.path)
        addons = code["addons"]
        runner = types.ModuleType("runner")
        runner.__dict__["addons"] = addons
        sys.modules["runner"] = runner

        try:
            while True:
                for _ in runner.__dict__["addons"]:
                    _(route)
                route.continue_()
                try:
                    reload(runner)
                except ModuleNotFoundError:
                    ...
                except ImportError:
                    ...
        except Error:
            ...


if __name__ == "__main__":
    # Run.run("../../test/test_2.py", url="http://172.16.4.3")

    # page = Run.run("../../test/test_3.py", url="http://example.com/")
    page = Run.run("../../test/test_4.py", url="http://127.0.0.1:5000/response/")
    ...
