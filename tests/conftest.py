import json

import pytest


class Helpers:
    def read_json(self, filename: str) -> dict:
        with open(filename, "r") as f:
            data = json.load(f)
        return data

    def cookie_msg(self):
        return (
            "laravel_session=eyJpdiI6InB1UHF1N1pEUFU3R0xxZU1rNzVMVkE9PSIsIn"
            "ZhbHVlIjoiTVBZXC9aSHkreWhUbEhIM1E2NnlUVG0xSFdER2MzRDk0RWtcLzM2"
            "SHdCN05ZRUFQSmd1XC95XC9DalVPelJYRTQra2ciLCJtYWMiOiI5OTQ4MGYyNz"
            "cxYzc4M2RjYWQ0NTg5Y2IzZWY5ODg1NWU3ZjdlMjIyNGNlOTI3ZjQzMDNmOGQz"
            "ZjQ2ODQxY2ZlIn0%3D; expires=Fri, 01-Jan-2021 12:31:22 GMT; "
            "Max-Age=7200; path=/; httponly"
        )

    def pattern_msg(self):
        return r"^(.+)?\;version:\1"

    def headers_msg(self):
        return {
            "Set-Cookie": self.cookie_msg(),
            "Connection": "keep-alive",
            "Content-Length": "50426",
            "Server": "nginx",
            "Content-Type": "text/html; charset=utf-8",
            "X-Frame-Options": "DENY",
            "Via": "1.1 vegur, 1.1 varnish, 1.1 varnish",
            "Accept-Ranges": "bytes",
            "Date": "Sat, 02 Jan 2021 13:00:54 GMT",
            "Age": "1610",
            "X-Served-By": "cache-bwi5146-BWI, cache-hhn4038-HHN",
            "X-Cache": "HIT, HIT",
            "X-Cache-Hits": "1, 7",
            "X-Timer": "S1609592455.808592,VS0,VE0",
            "Vary": "Cookie",
            "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
        }

    def read_txt(self, filename: str, *, as_bytes: bool = False):
        with open(filename, "r") as f:
            if as_bytes:
                return f.read().encode()
            return f.read()

    def analyze_headers_msg(self):
        return {
            "Web frameworks": ["Laravel"],
            "Web servers": ["Nginx"],
            "Reverse proxies": ["Nginx"],
            "Caching": ["Varnish"],
        }

    def sort_dict_lists(self, value):
        result = {}
        for key, val in value.items():
            result[key] = sorted(val)

        return result

    def result_analyze_msg(self):
        return {
            "Web frameworks": ["Laravel"],
            "Web servers": ["Nginx"],
            "Reverse proxies": ["Nginx"],
            "Caching": ["Varnish"],
            "Analytics": ["Google Analytics"],
            "JavaScript libraries": ["jQuery", "jQuery UI", "Modernizr"],
        }


@pytest.fixture
def helpers():
    return Helpers()
