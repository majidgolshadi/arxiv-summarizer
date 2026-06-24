import os

import requests


def download_pdfs(pdf_urls: list[str], output_dir: str) -> list[str]:
    downloaded_paths = []
    print("\n--- Starting PDF Download ---")

    os.makedirs(output_dir, exist_ok=True)

    for url in pdf_urls:
        identifier = url.rsplit("/", 1)[-1]
        local_filename = f"{identifier}.pdf"
        local_filepath = os.path.join(output_dir, local_filename)

        if os.path.exists(local_filepath):
            print(f"[SKIP] PDF already exists: {local_filename}")
            downloaded_paths.append(local_filepath)
            continue

        try:
            print(f"Downloading {identifier}...")
            response = requests.get(url, stream=True, timeout=20)
            response.raise_for_status()

            with open(local_filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"[SUCCESS] Downloaded and saved: {local_filename}")
            downloaded_paths.append(local_filepath)

        except requests.exceptions.RequestException as e:
            print(f"[FAIL] Failed to download {identifier} from {url}: {e}")
        except Exception as e:
            print(f"[FAIL] An unexpected error occurred while processing {identifier}: {e}")

    print("--- PDF Download Complete ---")
    return downloaded_paths
