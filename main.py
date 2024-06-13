import os
from time import sleep
from dotenv import load_dotenv
import requests
import CloudFlare

# Environment init
load_dotenv(".env")

# Load env vars and init CF library
CF_TOKEN = os.getenv("CF_TOKEN")
CF_ZONE = os.getenv("CF_ZONE")
CF_DNSNAMES = os.getenv("CF_DNSNAMES").split(',')
CF_PROXIED = os.getenv("CF_PROXIED")
DDNS_CHECKDELAY = os.getenv("DELAY")

cf = CloudFlare.CloudFlare(token=CF_TOKEN)


def error(msg):
    """Pseudo-error handler, just so I don't need to keep writing "Error:" and exit(1) over and over."""
    print(f"Error: {msg}. Exiting.")
    exit(1)


# Verify env vars
for i in [CF_TOKEN, CF_ZONE, CF_DNSNAMES]:
    if i is None:
        error("Missing one or more env vars")

if DDNS_CHECKDELAY is None:
    DDNS_CHECKDELAY = 300

if CF_PROXIED is None:
    CF_PROXIED = False
else:
    CF_PROXIED = True

del i

# Verify token
try:
    cf.user.tokens.verify()
except CloudFlare.exceptions.CloudFlareAPIError as e:
    error("Invalid token")

# Verify zone name and get zone id

zones = cf.zones.get(params={"name": CF_ZONE})
if len(zones) == 0:
    error("Invalid zone name")

zoneid = zones[0]["id"]

# All clear from here, define functions and run.

def get_ip() -> str:
    """
    Get public IP address of running machine.
    Returns the public IP address as a string if successful, otherwise raises an exception.
    """
    try:
        r = requests.get("https://api.ipify.org", timeout=30)
        r.raise_for_status()
        return r.text
    except (requests.RequestException, requests.HTTPError) as e:
        error(f"Could not get public IP address: {e}")


def update_dns(lastip) -> None:
    """
    Update DNS records with current public IP address.
    Returns nothing if successful, otherwise raises an exception.
    """
    ip = get_ip()
    if ip == lastip:
        print("IP unchanged. No changes made.")
        return None
    else:
        for i in CF_DNSNAMES:
            # Setup record info to update or add.
            recordinfo = {
                "type": "A",
                "name": i,
                "content": ip,
                "proxied": CF_PROXIED,
                "ttl": 1,
                "comment": "Automatically updated by cloudflareddns.",
            }

            # Check if record already exists
            record = cf.zones.dns_records.get(zoneid, data={"name": i})

            # If record doesn't exist, create it.
            if len(record) == 0:
                try:
                    cf.zones.dns_records.post(zoneid, json=recordinfo)
                    print(f"Created DNS record for {i}. IP address is {ip}.")
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    error(f"Could not create DNS record for {i}: {e}")

            # If record exists, update it.
            else:
                try:
                    cf.zones.dns_records.patch(
                        zoneid, record[0]["id"], data=recordinfo
                    )
                    print(f"Updated DNS record for {i}.dorkd.net. IP address is {ip}.")
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    error(f"Could not update DNS record for {i}: {e}")

        return ip


def main() -> None:
    """Main function."""
    lastip = None
    while True:
        ip = update_dns(lastip)
        if ip is not None:
            lastip = ip
        print(f"Checking again in {DDNS_CHECKDELAY} seconds.")
        sleep(DDNS_CHECKDELAY)


if __name__ == "__main__":
    main()
