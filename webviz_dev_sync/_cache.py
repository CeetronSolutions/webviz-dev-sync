from pathlib import Path
import json
import time

from ._user_data_dir import user_data_dir


class Cache:
    def __init__(self) -> None:
        self._cache_file_path = Path.joinpath(user_data_dir(), ".cache.json")
        self._cache = None
        if not self._cache_file_path.exists():
            Path.mkdir(user_data_dir(), exist_ok=True)
            self.make_default_file()
        else:
            self.read()

    def make_default_file(self) -> None:
        self._cache = {
            "config-last-modified": 0,
            "packages-last-modified": {},
        }
        self.save()

    def read(self) -> None:
        with open(self._cache_file_path, mode="r") as cache_file:
            self._cache = json.load(cache_file)

    def save(self) -> None:
        with open(self._cache_file_path, mode="w") as cache_file:
            json.dump(self._cache, cache_file)

    def store_config_modified_date(self) -> None:
        if self._cache:
            self._cache["config-last-modified"] = time.time()
            self.save()

    def get_config_modified_date(self) -> float:
        if self._cache:
            return self._cache["config-last-modified"]
        return 0

    def store_package_modified_date(self, package_name: str, local: bool) -> None:
        if self._cache:
            if not package_name in self._cache["packages-last-modified"]:
                self._cache["packages-last-modified"][package_name] = {
                    "local": 0,
                    "remote": 0,
                }
            self._cache["packages-last-modified"][package_name]["local" if local else "remote"] = time.time()
            self.save()

    def get_package_modified_date(self, package_name: str, local: bool) -> float:
        if self._cache:
            if not package_name in self._cache["packages-last-modified"]:
                return 0
            return self._cache["packages-last-modified"][package_name]["local" if local else "remote"]
        return 0
