from typing import Optional
from pathlib import Path
import json
import time

from ._user_data_dir import user_data_dir


class Cache:
    _cache: Optional[dict] = None
    def __init__(self) -> None:
        self._cache_file_path = Path.joinpath(user_data_dir(), ".cache.json")
        if not self._cache_file_path.exists():
            Path.mkdir(user_data_dir(), exist_ok=True)
            self.make_default_file()
        elif not self._cache:
            self.read()

    def make_default_file(self) -> None:
        Cache._cache = {
            "config-last-modified": 0,
            "packages-last-modified": {},
            "packages-last-built": {},
        }
        self.save()

    def read(self) -> None:
        with open(self._cache_file_path, mode="r") as cache_file:
            Cache._cache = json.load(cache_file)

    def save(self) -> None:
        with open(self._cache_file_path, mode="w") as cache_file:
            json.dump(Cache._cache, cache_file)

    def store_config_modified_timestamp(self) -> None:
        if Cache._cache:
            Cache._cache["config-last-modified"] = time.time()
            self.save()

    def get_config_modified_timestamp(self) -> float:
        if Cache._cache:
            return float(str(Cache._cache["config-last-modified"]))
        return 0

    def store_package_modified_timestamp(self, package_name: str, local: bool) -> None:
        if Cache._cache:
            if not package_name in Cache._cache["packages-last-modified"]:
                Cache._cache["packages-last-modified"][package_name] = {
                    "local": 0,
                    "remote": 0,
                }
            Cache._cache["packages-last-modified"][package_name]["local" if local else "remote"] = time.time()
            self.save()

    def get_package_modified_timestamp(self, package_name: str, local: bool) -> float:
        if Cache._cache:
            if not package_name in Cache._cache["packages-last-modified"]:
                return 0
            return Cache._cache["packages-last-modified"][package_name]["local" if local else "remote"]
        return 0

    def get_package_build_timestamp(self, package_name: str, local: bool) -> float:
        if Cache._cache:
            if not package_name in Cache._cache["packages-last-built"]:
                return 0
            return Cache._cache["packages-last-built"][package_name]["local" if local else "remote"]
        return 0

    def store_package_built_timestamp(self, package_name: str, local: bool) -> None:
        if Cache._cache:
            if not package_name in Cache._cache["packages-last-built"]:
                Cache._cache["packages-last-built"][package_name] = {
                    "local": 0,
                    "remote": 0,
                }
            Cache._cache["packages-last-built"][package_name]["local" if local else "remote"] = time.time()
            self.save()
