import os
import requests
from tqdm import tqdm

def download_pdfs(pdf_urls: list[str], output_dir: str) -> list[str]:
    """
    Downloads a list of PDF URLs into the specified output directory.

    Args:
        pdf_urls: List of direct PDF URLs.
        output_dir: The directory where PDFs should be saved.

    Returns:
        List of local file paths of successfully downloaded PDFs.
    """
    downloaded_paths = []
    print("\n--- Starting PDF Download ---")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for url in pdf_urls:
        # Extract the identifier from the URL for the filename
        # Example: https://arxiv.org/pdf/2501.12345 -> 2501.12345
        identifier = url.replace("https://arxiv.org/pdf/", "")
        local_filename = f"{identifier}.pdf"
        local_filepath = os.path.join(output_dir, local_filename)

        if os.path.exists(local_filepath):
            print(f"[SKIP] PDF already exists: {local_filename}")
            downloaded_paths.append(local_filepath)
            continue

        try:
            print(f"Downloading {identifier}...")
            # Using stream=True and tqdm for progress bar
            response = requests.get(url, stream=True, timeout=20)
            response.raise_for_status()

            with open(local_filepath, 'wb') as f:
                # Stream the content to handle large files
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