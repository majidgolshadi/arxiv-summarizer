import argparse
import sys
import os
import extractor
import downloader
import pdf_parser
import summarizer
from utils import get_date_directory

def main():
    """
    Main entry point for the ArXiv Downloader and Farsi Summarizer.
    Parses arguments and orchestrates the entire workflow.
    """
    parser = argparse.ArgumentParser(
        description="Download ArXiv PDFs and generate Farsi summaries.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the text file containing URLs."
    )
    parser.add_argument(
        "--summary-length",
        required=True,
        choices=['short', 'medium'],
        help="Desired length for the summary: 'short' (150-250 words) or 'medium' (400-700 words)."
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found at {args.input}")
        sys.exit(1)

    # 1. Determine output directory
    date_dir = get_date_directory()
    os.makedirs(date_dir, exist_ok=True)
    print(f"Output directory set to: {date_dir}")

    # --- 2. Extract ArXiv URLs and convert to PDF links ---
    pdf_urls = extractor.extract_and_convert_urls(args.input)
    
    if not pdf_urls:
        print("Exiting workflow: No PDF URLs found or an error occurred during extraction.")
        return

    # --- 3. Download PDFs ---
    downloaded_paths = downloader.download_pdfs(pdf_urls, date_dir)

    if not downloaded_paths:
        print("Exiting workflow: No PDFs were successfully downloaded.")
        return

    # --- 4. Summarize and save summaries ---
    print("\n--- Starting Summary Generation and Saving ---")
    summary_dir = os.path.join(date_dir, "summary")
    os.makedirs(summary_dir, exist_ok=True)

    for pdf_path in downloaded_paths:
        # Extract title and text content
        title, _ = pdf_parser.parse_pdf_metadata_and_text(pdf_path)
        
        if title:
            # Generate the summary (uses pdf_path again internally)
            summary_text = summarizer.generate_farsi_summary(pdf_path, title, args.summary_length)
            
            if summary_text:
                # Get the base filename (e.g., 2501.12345.pdf -> 2501.12345)
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                summary_filepath = os.path.join(summary_dir, f"{base_name}.txt")
                
                # Write content: Title + two blank lines + Summary
                full_content = f"{title}\n\n{summary_text}"
                
                with open(summary_filepath, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                print(f"[SUCCESS] Summary saved to: {summary_filepath}")
        else:
            print(f"[FAIL] Skipping summary for {os.path.basename(pdf_path)}: Could not determine a title.")

    print("\n--- Workflow Complete ---")
    print("All required PDFs were processed, and summaries have been saved to the 'summary' subdirectory.")

    # --- 2. Extract ArXiv URLs and convert to PDF links ---
    pdf_urls = extractor.extract_and_convert_urls(args.input)
    
    if not pdf_urls:
        print("Exiting workflow: No PDF URLs found or an error occurred during extraction.")
        return

    # --- 3. Download PDFs ---
    downloaded_paths = downloader.download_pdfs(pdf_urls, date_dir)

    if not downloaded_paths:
        print("Exiting workflow: No PDFs were successfully downloaded.")
        return

    # --- 4. Summarize and save summaries ---
    print("\n--- Starting Summary Generation and Saving ---")
    summary_dir = os.path.join(date_dir, "summary")
    os.makedirs(summary_dir, exist_ok=True)

    for pdf_path in downloaded_paths:
        # Extract title and text content
        title, _ = pdf_parser.parse_pdf_metadata_and_text(pdf_path)
        
        if title:
            # Generate the summary (uses pdf_path again internally)
            summary_text = summarizer.generate_farsi_summary(pdf_path, title, args.summary_length)
            
            if summary_text:
                # Get the base filename (e.g., 2501.12345.pdf -> 2501.12345)
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                summary_filepath = os.path.join(summary_dir, f"{base_name}.txt")
                
                # Write content: Title + two blank lines + Summary
                full_content = f"{title}\n\n{summary_text}"
                
                with open(summary_filepath, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                print(f"[SUCCESS] Summary saved to: {summary_filepath}")
        else:
            print(f"[FAIL] Skipping summary for {os.path.basename(pdf_path)}: Could not determine a title.")

    print("\n--- Workflow Complete ---")
    print("All required PDFs were processed, and summaries have been saved to the 'summary' subdirectory.")


if __name__ == "__main__":
    main()