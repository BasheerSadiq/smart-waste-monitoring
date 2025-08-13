"""
Download a dataset version from Roboflow via API.
Set ROBOFLOW_API_KEY env var.
"""
import os, requests, zipfile, io, argparse
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Roboflow download URL")
    args = ap.parse_args()
    headers = {"Authorization": f"Bearer {os.getenv('ROBOFLOW_API_KEY','')}"}
    r = requests.get(args.url, headers=headers)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("data")
    print("[roboflow] extracted to data/")
if __name__ == "__main__":
    main()
