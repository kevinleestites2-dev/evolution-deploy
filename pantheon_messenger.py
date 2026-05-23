"""
PANTHEON MESSENGER — Evolution API Client
The messaging spine of the Pantheon.
All Primes use this to send WhatsApp messages.
"""

import requests
import json
import os

EVOLUTION_BASE_URL = os.getenv("EVOLUTION_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "pantheon_evolution_key_CHANGE_ME")
INSTANCE_NAME = os.getenv("EVOLUTION_INSTANCE", "pantheon")

HEADERS = {
    "apikey": EVOLUTION_API_KEY,
    "Content-Type": "application/json"
}


# ─── INSTANCE MANAGEMENT ────────────────────────────────────

def create_instance():
    """Create the Pantheon WhatsApp instance."""
    url = f"{EVOLUTION_BASE_URL}/instance/create"
    payload = {
        "instanceName": INSTANCE_NAME,
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS"
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


def get_qr():
    """Get QR code to connect WhatsApp number."""
    url = f"{EVOLUTION_BASE_URL}/instance/connect/{INSTANCE_NAME}"
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    if "base64" in data:
        print("[QR] Scan this with WhatsApp:")
        print(data["base64"])  # base64 image — save to file or display
    return data


def connection_status():
    """Check if WhatsApp is connected."""
    url = f"{EVOLUTION_BASE_URL}/instance/connectionState/{INSTANCE_NAME}"
    r = requests.get(url, headers=HEADERS)
    return r.json()


# ─── MESSAGING ───────────────────────────────────────────────

def send_text(number: str, message: str):
    """
    Send a WhatsApp text message.
    number: E.164 format, e.g. '19189007206'
    """
    url = f"{EVOLUTION_BASE_URL}/message/sendText/{INSTANCE_NAME}"
    payload = {
        "number": number,
        "text": message
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


def send_media(number: str, media_url: str, caption: str = "", media_type: str = "image"):
    """Send image/video/document."""
    url = f"{EVOLUTION_BASE_URL}/message/sendMedia/{INSTANCE_NAME}"
    payload = {
        "number": number,
        "mediatype": media_type,
        "media": media_url,
        "caption": caption
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


def send_buttons(number: str, title: str, body: str, buttons: list):
    """
    Send interactive button message.
    buttons: [{"buttonId": "1", "buttonText": {"displayText": "Yes"}}, ...]
    """
    url = f"{EVOLUTION_BASE_URL}/message/sendButtons/{INSTANCE_NAME}"
    payload = {
        "number": number,
        "title": title,
        "description": body,
        "buttons": buttons
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


def send_list(number: str, title: str, body: str, sections: list):
    """Send a WhatsApp list message."""
    url = f"{EVOLUTION_BASE_URL}/message/sendList/{INSTANCE_NAME}"
    payload = {
        "number": number,
        "title": title,
        "description": body,
        "sections": sections
    }
    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


# ─── PANTHEON ALERTS ─────────────────────────────────────────

FORGEMASTER_NUMBER = os.getenv("FORGEMASTER_NUMBER", "19189007206")

def alert_forgemaster(prime_name: str, message: str):
    """Any Prime can call this to alert the Forgemaster."""
    text = f"⚔️ *{prime_name}*\n\n{message}"
    return send_text(FORGEMASTER_NUMBER, text)


def scout_deal_alert(address: str, auction_price: float, market_value: float, spread: float, auction_date: str):
    """ScoutPrime deal alert template."""
    msg = (
        f"🏠 *DEAL ALERT — ScoutPrime*\n\n"
        f"📍 {address}\n"
        f"📅 Auction: {auction_date}\n"
        f"💰 Opening Bid: ${auction_price:,.0f}\n"
        f"📈 Market Value: ${market_value:,.0f}\n"
        f"🔥 Spread: *${spread:,.0f}*\n\n"
        f"React ✅ to flag for investigation."
    )
    return send_text(FORGEMASTER_NUMBER, msg)


def proppilot_lead_welcome(number: str, first_name: str):
    """Auto-fire when a lead hits the PropPilot landing page."""
    msg = (
        f"Hey {first_name} 👋\n\n"
        f"PropPilot AI here. You just signed up for distressed property alerts in Lee County FL.\n\n"
        f"We're tracking foreclosure auctions where properties sell 60-80% below market.\n\n"
        f"Want me to send you this week's top 5 deals? Reply *YES* and I'll fire them over."
    )
    return send_text(number, msg)


def war_chest_update(balance: float, delta: float, source: str):
    """MidasPrime calls this when revenue hits."""
    msg = (
        f"💎 *War Chest Update — MidasPrime*\n\n"
        f"Source: {source}\n"
        f"Added: +${delta:,.2f}\n"
        f"Balance: ${balance:,.2f}\n\n"
        f"Nexus Target: $3,000 | Citadel Target: $5,000"
    )
    return send_text(FORGEMASTER_NUMBER, msg)


# ─── CLI QUICK SEND ──────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pantheon_messenger.py [status|qr|send <number> <message>]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "status":
        print(json.dumps(connection_status(), indent=2))

    elif cmd == "qr":
        print(json.dumps(get_qr(), indent=2))

    elif cmd == "send" and len(sys.argv) >= 4:
        number = sys.argv[2]
        message = " ".join(sys.argv[3:])
        result = send_text(number, message)
        print(json.dumps(result, indent=2))

    elif cmd == "init":
        print("Creating Pantheon instance...")
        print(json.dumps(create_instance(), indent=2))

    else:
        print("Unknown command.")
