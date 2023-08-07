import requests

class BlockpipeClient:
    def __init__(self, project, options=None):
        if options is None:
            options = {}
        self.project = project
        self.environment = options.get("environment", "production")
        self.base_url = options.get("baseUrl", "https://app.blockpipe.io/endpoint")

    def get(self, endpoints):
        if isinstance(endpoints, str):
            endpoints = [endpoints]

        results = []
        for endpoint in endpoints:
            url = f"{self.base_url}/{self.project}/{self.environment}{endpoint}"
            response = requests.get(url)
            response.raise_for_status()
            results.append(response.json())

        if len(results) == 1:
            return results[0]
        return results

__all__ = ["BlockpipeClient"]
