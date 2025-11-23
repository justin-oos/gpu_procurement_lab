from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(title="Global GPU Spot Market API", version="1.0.0")


@app.get("/")
def health_check():
    return {"status": "online", "service": "Mock Vendor API"}


@app.get("/v1/market/spot")
def get_spot_price(chip: str):
    """
    Returns current spot market pricing.
    Design Doc Requirement: Price 10x normal, Limited Availability.
    """
    chip_key = chip.upper()

    if "H100" in chip_key:
        return {
            "chip": "H100",
            "price": 32000,  # $32k/unit (High price to discourage full buy)
            "currency": "USD",
            "availability": 250,  # Only 250 available (Forces use of Internal Stock)
            "vendor": "FastChips_Reseller_LLC",
        }
    elif "A100" in chip_key:
        return {
            "chip": "A100",
            "price": 15000,
            "availability": 50,
            "vendor": "Legacy_Systems_Inc",
        }
    else:
        # Simulate market scarcity for unknown chips
        return {
            "chip": chip,
            "price": 0,
            "availability": 0,
            "note": "No stock found in global spot market.",
        }


@app.get("/v1/shipping/estimate")
def get_shipping_estimate(origin: str, dest: str):
    """
    Returns shipping timeframes.
    """
    # Logic to simulate different shipping routes
    if origin.upper() == "TW" and dest.upper() == "US":
        return {
            "route": "TW-US",
            "days": 14,
            "method": "AIR_FREIGHT_RUSH",
            "cost_per_unit": 150,
        }
    else:
        return {
            "route": f"{origin}-{dest}",
            "days": 45,
            "method": "STANDARD_SEA",
            "cost_per_unit": 50,
        }
