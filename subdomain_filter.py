import csv
import sys
import os
import argparse

def clean_subdomains(input_csv, output_txt, root_domain):
    """
    Reads a CSV, extracts hostnames, strips protocols, strips them to the 
    first subdomain level, and writes unique entries to a TXT file.
    """
    
    # Potential column names PD uses for the hostname
    host_headers = ['host', 'input', 'name', 'url', 'domain']
    
    unique_subdomains = set()
    root_domain = root_domain.lower().strip()
    
    print(f"--- Processing {input_csv} ---")
    print(f"Target Root Domain: {root_domain}")
    
    try:
        with open(input_csv, mode='r', encoding='utf-8', errors='ignore') as f:
            # Attempt to handle potential CSV variations (delimiters)
            try:
                dialect = csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
                reader = csv.DictReader(f, dialect=dialect)
            except:
                # Fallback if sniffer fails
                f.seek(0)
                reader = csv.DictReader(f)

            # Find which column holds the hostname
            header_row = reader.fieldnames
            target_col = None
            if header_row:
                for h in header_row:
                    if h.lower() in host_headers:
                        target_col = h
                        break
            
            if not target_col:
                print(f"Error: Could not find a 'Host' or 'Input' column in CSV headers: {header_row}")
                return

            print(f"Found hostname column: '{target_col}'")

            for row in reader:
                full_host = row.get(target_col, '').strip().lower()
                
                # --- CHANGE 1: Remove http/s prefixes ---
                if full_host.startswith("http://"):
                    full_host = full_host[7:]
                elif full_host.startswith("https://"):
                    full_host = full_host[8:]
                
                # Optional: Remove www. if it exists after stripping protocol
                if full_host.startswith("www."):
                    full_host = full_host[4:]

                # Basic validation
                if not full_host or root_domain not in full_host:
                    continue
                
                # Logic to strip sub-sub-domains
                # Example: job.runner.dev.momentick.app -> dev.momentick.app
                
                # 1. Remove the root domain from the end
                if full_host == root_domain:
                    continue # Skip the root domain itself
                
                if full_host.endswith("." + root_domain):
                    # Extract the prefix (e.g., "job.runner.dev")
                    prefix = full_host[:-len(root_domain)-1]
                    
                    # Split by dot and take the last part (e.g., "dev")
                    parts = prefix.split('.')
                    base_sub = parts[-1]
                    
                    # Reconstruct the clean subdomain
                    clean_host = f"{base_sub}.{root_domain}"
                    unique_subdomains.add(clean_host)

    except FileNotFoundError:
        print(f"Error: File {input_csv} not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Write to output file
    try:
        with open(output_txt, 'w') as f:
            for sub in sorted(unique_subdomains):
                f.write(sub + '\n')

        print(f"\nSuccess! Extracted {len(unique_subdomains)} unique parent subdomains.")
        print(f"Saved to: {output_txt}")
    except IOError as e:
        print(f"Error writing to file {output_txt}: {e}")

if __name__ == "__main__":
    # --- CHANGE 2: Using argparse for better flag handling ---
    parser = argparse.ArgumentParser(description="Extract and clean subdomains from a CSV file.")
    
    # Positional arguments
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("root_domain", help="The root domain to filter by (e.g., example.com)")
    
    # Optional argument for output
    parser.add_argument("-o", "--output", 
                        help="Name of the output text file (default: clean_subdomains.txt)", 
                        default="clean_subdomains.txt")

    args = parser.parse_args()

    clean_subdomains(args.input_csv, args.output, args.root_domain)
