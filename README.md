# Subdomain Filter

A utility script (`subdomain_filter.py`) designed to parse asset discovery CSV files (specifically those from Project Discovery), clean the data, and extract a unique list of direct subdomains (first-level subdomains) for a specific target.

This tool prepares a clean target list for further auditing, such as checking for wildcard DNS records using [`wildcard_dns_auditor.py`](https://github.com/MagVeTs/Wildcard_DNS_Auditor).

## Features

- **CSV Parsing**: Automatically detects CSV dialects and identifies the correct column containing hostnames (supports `host`, `input`, `name`, `url`, `domain`).

- **Protocol Stripping**: Removes `http://` and `https://` prefixes.

- **Prefix Cleaning**: Removes `www.` if present at the start of the hostname.

- **Sub-subdomain Flattening**: Strips away deep subdomain levels to isolate the primary subdomain.

> Example: `job.runner.dev.example.com` becomes `dev.example.com`.

- **Root Domain Filtering**: Ignores the root domain itself (e.g., `example.com`) and excludes hostnames that do not match the target root domain.

- **Deduplication**: Produces a sorted list of unique entries.

## Prerequisites

- Python 3.x

No external dependencies are required (uses standard libraries: `csv`, `sys`, `os`, `argparse`).

## Usage

Run the script from the command line by providing the input CSV file and the target root domain.
```
Bash
python subdomain_filter.py <input_csv> <root_domain> [-o output_file]
```

## Arguments

|Argument|Type|Description|
|:----|:----|:----|
|`input_csv`|Required|The path to the source CSV file (e.g., `assets.csv`).|
|root_domain|Required|The target root domain (e.g., `example.com`) used to filter and clean the hostnames.|
|`-o`, `--output`|Optional|The filename for the output text file. Defaults to `clean_subdomains.txt` if not specified.|

## Examples

**Basic usage** (saves to default `clean_subdomains.txt`):
```
Bash
python subdomain_filter.py projectdiscovery_assets.csv example.com
```

**Specifying a custom output file**:
```
Bash
python subdomain_filter.py projectdiscovery_assets.csv example.com -o target_list.txt
```

## How It Works

1. **Input**: The script reads the provided CSV file. It attempts to "sniff" the CSV format to handle different delimiters automatically.

> Column Detection: It looks for a column header matching `host`, `input`, `name`, `url`, or `domain`.

2. **Processing**: For every row:

- It strips `http://` or `https://`.

- It removes `www.` if it exists at the beginning of the string.

- It verifies the hostname actually belongs to the root_domain provided.

- It calculates the "base" subdomain. If the input is `deep.nested.staging.example.com`, the script isolates `staging` and saves `staging.example.com`.

3. **Output**: A `.txt` file is generated containing only the unique, flattened subdomains, listed one per line.

## Workflow Integration

This script is part of a larger asset discovery workflow:

1. **Download Assets**: obtain a list of assets (CSV) from [Project Discovery](https://cloud.projectdiscovery.io/).
2. **Filter** (Using this script): Run `subdomain_filter.py` to normalize the data into a flat list of subdomains.
3. **Audit**: Use the resulting text file as input for [`wildcard_dns_auditor.py`](https://github.com/MagVeTs/Wildcard_DNS_Auditor) to check for wildcard DNS configurations.

## Contributors
- [MagVeTs](https://github.com/MagVeTs)
- [KfirDu](https://github.com/KfirDu)



