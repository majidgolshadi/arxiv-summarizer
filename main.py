import argparse
import os
import sys

import downloader
import extractor
import pdf_parser
import summarizer
from server import start_server
from utils import get_date_directory

import config


def main():
    parser = argparse.ArgumentParser(
        description="Download ArXiv PDFs and generate summaries.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--input", help="Path to the text file containing URLs.")
    parser.add_argument(
        "--summary-length",
        choices=["short", "medium"],
        help="Desired length for the summary: 'short' or 'medium'.",
    )
    parser.add_argument(
        "--web-server-only",
        action="store_true",
        help="Start the web server only, skipping download and summarization.",
    )
    args = parser.parse_args()

    date_dir = os.path.join(config.DATA_DIR, get_date_directory())
    summary_dir = os.path.join(date_dir, "summary")

    if args.web_server_only:
        start_server(summary_dir)
        return

    if not args.input or not args.summary_length:
        parser.error("--input and --summary-length are required when not using --serve-only")

    if not os.path.exists(args.input):
        print(f"Error: Input file not found at {args.input}")
        sys.exit(1)

    os.makedirs(date_dir, exist_ok=True)
    print(f"Output directory set to: {date_dir}")

    pdf_urls = extractor.extract_and_convert_urls(args.input)
    if not pdf_urls:
        print("Exiting workflow: No PDF URLs found or an error occurred during extraction.")
        return

    downloaded_paths = downloader.download_pdfs(pdf_urls, date_dir)
    if not downloaded_paths:
        print("Exiting workflow: No PDFs were successfully downloaded.")
        return

    print("\n--- Starting Summary Generation and Saving ---")
    os.makedirs(summary_dir, exist_ok=True)

    for pdf_path in downloaded_paths:
        title, text_content = pdf_parser.parse_pdf_metadata_and_text(pdf_path)

        if not title:
            print(f"[FAIL] Skipping summary for {os.path.basename(pdf_path)}: Could not determine a title.")
            continue

        summary_text = summarizer.generate_summary(pdf_path, text_content, title, args.summary_length)
        if summary_text:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            summary_filepath = os.path.join(summary_dir, f"{base_name}.txt")
            with open(summary_filepath, "w", encoding="utf-8") as f:
                f.write(f"{title}\n\n{summary_text}")
            print(f"[SUCCESS] Summary saved to: {summary_filepath}")

    print("\n--- Workflow Complete ---")
    start_server(summary_dir)


if __name__ == "__main__":
    main()
