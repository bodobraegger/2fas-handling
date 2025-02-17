import sys
import json
from uuid import uuid4

def convert_2fas_to_aegis(data_2fas):
    aegis_data = {
        "version": 1,
        "header": {
            "slots": None,
            "params": None
        },
        "db": {
            "version": 1,
            "entries": []
        }
    }

    for item in data_2fas:
        # Generate a unique UUID for each entry
        entry_uuid = str(uuid4())

        # Map 2FAS fields to Aegis fields
        aegis_entry = {
            "type": item["otp"]["tokenType"].lower(),  # Map tokenType to Aegis type (e.g., totp, hotp)
            "uuid": entry_uuid,
            "name": f"{item.get('name')}" + (' - ' + item.get("otp").get("account") if item.get("otp").get("account") else ''),  # Use the label as the name
            "issuer": item["otp"].get("issuer"),  # Use the issuer
            "note": "",  # 2FAS doesn't seem to have a note field
            "icon": None,  # Handle icons separately
            "info": {
                "secret": item["secret"],
                "algo": item["otp"].get("algorithm", 'SHA256'),  # Map algorithm (e.g., SHA1, SHA256)
                "digits": item["otp"].get("digits", 6),  # Map digits
                "period": item["otp"].get("period", 30) if item["otp"]["tokenType"].lower() == "totp" else None,  # Period for TOTP
                "counter": None if item["otp"]["tokenType"].lower() == "totp" else 0  # Counter for HOTP (default to 0)
            },
            "group": item.get("groupId", None),  # Preserve groupId if it exists
            "order": item["order"]["position"],  # Preserve order/position
            "icon_data": {
                "selected": item["icon"]["selected"],
                "iconCollection": item["icon"]["iconCollection"]
            } if "icon" in item else None  # Preserve icon data
        }

        # Add the entry to the Aegis database
        aegis_data["db"]["entries"].append(aegis_entry)

    return aegis_data

def main():
    # Load the 2FAS JSON file
    export_2fas = sys.argv[1]
    with open(export_2fas, "r") as f:
        data_2fas = json.load(f)

    # Convert to Aegis format
    aegis_data = convert_2fas_to_aegis(data_2fas)

    # Print the Aegis JSON to stdout, can be redirected to a file
    json.dump(aegis_data, sys.stdout, indent=4)

if __name__ == "__main__":
    main()
