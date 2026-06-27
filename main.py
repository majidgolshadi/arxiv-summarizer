import argparse
import sys
from pathlib import Path

from src import config
from src import downloader
from src import extractor
from src import pdf_parser
from src import summarizer
from src.utils import get_date_directory, get_latest_directory
from web.server import start_server


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
        help="Start the web server using the most recent output directory.",
    )
    args = parser.parse_args()

    data_dir = Path(config.DATA_DIR)

    if args.web_server_only:
        latest = get_latest_directory(data_dir)
        date_dir = data_dir / (latest or get_date_directory())
        start_server(date_dir / "summary")
        return

    if not args.input or not args.summary_length:
        parser.error("--input and --summary-length are required")

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    date_dir = data_dir / get_date_directory()
    summary_dir = date_dir / "summary"
    date_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {date_dir}")

    pdf_urls = extractor.extract_and_convert_urls(str(input_path))
    if not pdf_urls:
        print("No PDF URLs found — exiting.")
        return

    downloaded = downloader.download_pdfs(pdf_urls, str(date_dir))
    if not downloaded:
        print("No PDFs downloaded — exiting.")
        return

    print("\n--- Generating summaries ---")
    summary_dir.mkdir(exist_ok=True)

    for pdf_path in downloaded:
        title, text = pdf_parser.parse_pdf_metadata_and_text(pdf_path)
        if not title:
            print(f"[SKIP] {Path(pdf_path).name}: could not determine title")
            continue
        summary = summarizer.generate_summary(pdf_path, text, title, args.summary_length)
        if summary:
            out = summary_dir / f"{Path(pdf_path).stem}.txt"
            out.write_text(f"{title}\n\n{summary}", encoding="utf-8")
            print(f"[OK] {out}")

    print("\n--- Done ---")
    start_server(summary_dir)


if __name__ == "__main__":
    main()
