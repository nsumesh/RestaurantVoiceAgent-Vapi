"""
One-time setup script: creates or updates the Dishoom Vapi assistant.

Run once (or whenever you change the assistant configuration):
    python setup_assistant.py

Required environment variables in .env:
    VAPI_API_KEY            - Your Vapi private API key
    VAPI_PHONE_NUMBER_ID    - (optional) Vapi phone number ID to attach the assistant to
"""

import os
import sys

import requests
from dotenv import load_dotenv

from restaurant_data import format_hours, format_menu

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")
ASSISTANT_NAME = "Dishoom"
VAPI_BASE = "https://api.vapi.ai"

SYSTEM_PROMPT = f"""\
You are the friendly and warm voice assistant for Dishoom, a beloved Indian restaurant \
inspired by the Irani cafés of old Bombay. Speak in a warm, welcoming tone — think of \
yourself as a knowledgeable front-of-house host who genuinely loves the food.

You can help callers with two things:
1. Our opening hours
2. Our menu — answer questions about dishes, ingredients, or recommendations

Here is all the information you need:

--- OPENING HOURS ---
{format_hours()}

--- MENU ---
{format_menu()}
--- END OF MENU ---

IMPORTANT — Reservations:
Dishoom does not take reservations over the phone. If a caller asks to make, change, \
or cancel a reservation, decline politely and warmly. Explain that Dishoom operates \
predominantly on a walk-in basis, which is part of what makes it special. You may \
mention that a small number of bookings for larger groups (six or more) are available \
on the Dishoom website at dishoom.com. Do not offer to pass on reservation details or \
suggest the caller tries another way to book over the phone.

Keep responses concise and natural — remember, this is a phone call. Avoid bullet \
points or markdown formatting. Speak as you would to a caller, not as if writing an \
email.
"""

ASSISTANT_PAYLOAD = {
    "name": ASSISTANT_NAME,
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
        ],
    },
    "voice": {
        "provider": "11labs",
        "voiceId": "21m00Tcm4TlvDq8ikWAM",  # Rachel
    },
    "firstMessage": (
        "Thank you for calling Dishoom! How can I help you today? "
        "I can tell you about our menu or opening hours."
    ),
    "endCallMessage": "Thank you for calling Dishoom. We hope to see you soon — goodbye!",
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "en",
    },
}


def get_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json",
    }


def find_existing_assistant() -> str | None:
    """Return the ID of an existing assistant named ASSISTANT_NAME, or None."""
    resp = requests.get(f"{VAPI_BASE}/assistant", headers=get_headers(), timeout=15)
    resp.raise_for_status()
    for assistant in resp.json():
        if assistant.get("name") == ASSISTANT_NAME:
            return assistant["id"]
    return None


def _raise_with_body(resp: requests.Response) -> None:
    """Raise an HTTPError that includes the response body for easier debugging."""
    if not resp.ok:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise requests.exceptions.HTTPError(
            f"{resp.status_code} {resp.reason} — {detail}", response=resp
        )


def create_assistant() -> dict:
    resp = requests.post(
        f"{VAPI_BASE}/assistant",
        headers=get_headers(),
        json=ASSISTANT_PAYLOAD,
        timeout=15,
    )
    _raise_with_body(resp)
    return resp.json()


def update_assistant(assistant_id: str) -> dict:
    resp = requests.patch(
        f"{VAPI_BASE}/assistant/{assistant_id}",
        headers=get_headers(),
        json=ASSISTANT_PAYLOAD,
        timeout=15,
    )
    _raise_with_body(resp)
    return resp.json()


def attach_to_phone_number(assistant_id: str) -> None:
    """Associate the assistant with the provisioned inbound phone number."""
    if not PHONE_NUMBER_ID:
        print(
            "  Note: VAPI_PHONE_NUMBER_ID not set — skipping phone number attachment.\n"
            "  Set this in .env once you have provisioned a number in the Vapi dashboard."
        )
        return

    resp = requests.patch(
        f"{VAPI_BASE}/phone-number/{PHONE_NUMBER_ID}",
        headers=get_headers(),
        json={"assistantId": assistant_id},
        timeout=15,
    )
    _raise_with_body(resp)
    print(f"  Phone number {PHONE_NUMBER_ID} linked to assistant {assistant_id}.")


def main() -> None:
    if not VAPI_API_KEY:
        sys.exit("ERROR: VAPI_API_KEY is not set. Add it to your .env file.")

    print(f"Looking for existing assistant named '{ASSISTANT_NAME}'...")
    existing_id = find_existing_assistant()

    if existing_id:
        print(f"  Found existing assistant: {existing_id} — updating...")
        assistant = update_assistant(existing_id)
        action = "Updated"
    else:
        print("  No existing assistant found — creating a new one...")
        assistant = create_assistant()
        action = "Created"

    assistant_id: str = assistant["id"]
    print(f"  {action} assistant successfully.")
    print(f"\n  Assistant ID : {assistant_id}")
    print(f"  Name         : {assistant['name']}")
    print(f"  Model        : {assistant['model']['model']}")

    attach_to_phone_number(assistant_id)

    print("\n--- Next steps ---")
    print("1. Call your Vapi number and say hello to Dishoom!")
    print("   (Or test via the Vapi dashboard using the assistant ID above)\n")


if __name__ == "__main__":
    main()
