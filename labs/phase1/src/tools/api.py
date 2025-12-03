import requests
from typing import Dict, Any
from utils.config import config


class LogisticsTools:
    def __init__(self):
        self.base_url = config.API_BASE_URL

    def fetch_spot_prices(self, chip_type: str = "H100") -> Dict[str, Any]:
        """
        Checks the spot market price for a specific chip.
        Endpoint: GET /v1/market/spot?chip=H100 [cite: 97]
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/market/spot", params={"chip": chip_type}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Market API unreachable: {str(e)}"}

    def estimate_shipping(self, origin: str, destination: str = "US") -> Dict[str, Any]:
        """
        Gets shipping estimates.
        Endpoint: GET /v1/shipping/estimate?origin=TW&dest=US [cite: 99]
        """
        try:
            response = requests.get(
                f"{self.base_url}/v1/shipping/estimate",
                params={"origin": origin, "dest": destination},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Shipping API unreachable: {str(e)}"}
