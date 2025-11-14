import datetime
import urllib.request
import zipfile
import csv
import shutil
import gzip
import json
import os
import re

# Headers for HTTP requests to mimic a browser
REQUEST_HEADERS =  {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "_ga=GA1.1.589408982.1745526590; _ga_MRH8B7W6P2=GS2.1.s1750439719$o1$g1$t1750439945$j60$l0$h0; _ga_K11B0NGD33=GS2.1.s1761755720$o1$g0$t1761755720$j60$l0$h0; _ga=GA1.1.589408982.1745526590; _ga_5W1ZB23GRH=GS2.1.s1761776886$o16$g0$t1761776886$j60$l0$h0; dtCookie9205gfup=v_4_srv_3_sn_812370C1F8BEE6083A5EE30B95AA1086_perc_100000_ol_0_mul_1_app-3A55a23a6474838c57_1; rxVisitor9205gfup=1763117742187K548LSI5AVUIBLUKB3MPI26ORHN1G5TT; dtSa9205gfup=-; _gid=GA1.1.356836040.1763117743; TS01ac3475=0199b2c74a7f97edea4d7a630df2db81421a69fa59475491ad91da5e47ac1873889c90b474ab9e43effa0cc1400d71b1cadc45ff0d08b29556b0764c48553535e7ade8020e; _gat=1; rxvt9205gfup=1763120682256|1763117742189; dtPC9205gfup=3$317742178_943h-vBMMEKKANGHPQMICHMWTKFTBGHKMQLURH-0e0; _ga_RD7BG8RLV0=GS2.1.s1763117742$o44$g1$t1763118890$j60$l0$h0",
    "dnt": "1",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

# Define filenames for raw data
GTFS_ZIP = "surface_gtfs.zip"
NET_GTFS_ZIP = "NET_gtfs.zip"
STOPS_TXT = "stops.txt"
NET_STOPS_TXT = "NET_stops.txt"
METRO_STOPS_JSON = "metro_stops.json"

def fetch_file(url: str, filename: str, headers: dict = None) -> None:
    """Fetches a file from a URL, handling gzip decompression if necessary."""
    print(f"Fetching {filename} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req) as response:
            if response.info().get('Content-Encoding') == 'gzip':
                with gzip.GzipFile(fileobj=response) as decompressed_response, open(filename, 'wb') as out_file:
                    shutil.copyfileobj(decompressed_response, out_file)
            else:
                with open(filename, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
        print(f"Successfully fetched {filename}.")
    except urllib.error.URLError as e:
        print(f"Error fetching {filename}: {e.reason}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while fetching {filename}: {e}")
        raise

def get_surface_stops_data() -> None:
    """Downloads and extracts surface stops data from a ZIP file."""
    zip_url = "https://dati.comune.milano.it/gtfs.zip"
    urllib.request.urlretrieve(zip_url, GTFS_ZIP)
    print(f"Downloaded {GTFS_ZIP}. Extracting {STOPS_TXT}...")
    with zipfile.ZipFile(GTFS_ZIP, 'r') as zip_ref:
        zip_ref.extract(STOPS_TXT)
    print(f"Extracted {STOPS_TXT}.")

def get_metro_stops_data() -> None:
    """Downloads metro stops data from an API endpoint."""
    metro_url = "https://giromilano.atm.it/proxy.tpportal/api/tpPortal/tpl/journeyPatterns/metromap"
    fetch_file(metro_url, METRO_STOPS_JSON, REQUEST_HEADERS)

def get_net_stops_data() -> None:
    """Downloads and extracts surface stops data from a ZIP file."""
    zip_url = str(input("Inserisci manualmente l'indirizzo dei dati GTFS di NET\nVisita https://www.agenziatpl.it/open-data/gtfs#:~:text=NET%20Nord%20Est%20Trasporti%20S.r.l.%3A, clicca su \"link al file\" e copia il link dal pulsante \"scarica\""))
    urllib.request.urlretrieve(zip_url, NET_GTFS_ZIP)
    print(f"Downloaded {NET_GTFS_ZIP}. Extracting {NET_STOPS_TXT}...")
    with zipfile.ZipFile(NET_GTFS_ZIP, 'r') as zip_ref:
        with zip_ref.open(STOPS_TXT) as origin:
            with open(NET_STOPS_TXT, "xb") as target:
                shutil.copyfileobj(origin, target)

    print(f"Extracted {NET_STOPS_TXT}.")

def process_surface_stops() -> list[dict]:
    """Reads and transforms surface stop data from stops.txt."""
    print("Processing surface stops...")
    stops = []
    try:
        with open(STOPS_TXT, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('stop_id') or not row['stop_id'].isdigit() or \
                   not row.get('stop_lat') or not row.get('stop_lon'):
                    continue  # Skip invalid entries

                stops.append({
                    "info": {"id": row['stop_id']},
                    "details": {"name": row['stop_name'].title(), "type": "surface"},
                    "location": {"X": str(float(row['stop_lon'])), "Y": str(float(row['stop_lat']))}
                })
        print(f"Processed {len(stops)} surface stops.")
        return stops
    except FileNotFoundError:
        print(f"{STOPS_TXT} not found. Please ensure it's downloaded.")
        return []
    except Exception as e:
        print(f"Error processing surface stops: {e}")
        return []

def process_net_stops() -> list[dict]:
    """Reads and transforms surface stop data from stops.txt."""
    print("Processing NET stops...")
    stops = []
    try:
        with open(NET_STOPS_TXT, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('stop_id') or not row['stop_id'].isdigit() or \
                   not row.get('stop_lat') or not row.get('stop_lon'):
                    continue  # Skip invalid entries

                stops.append({
                    "info": {"id": "1"+row['stop_id']},
                    "details": {"name": row['stop_name'].title(), "type": "surface"},
                    "location": {"X": str(float(row['stop_lon'])), "Y": str(float(row['stop_lat']))}
                })
        print(f"Processed {len(stops)} net stops.")
        return stops
    except FileNotFoundError:
        print(f"{NET_STOPS_TXT} not found. Please ensure it's downloaded.")
        return []
    except Exception as e:
        print(f"Error processing net stops: {e}")
        return []

def process_metro_stops() -> list[dict]:
    """Reads and transforms metro stop data from metro_stops.json."""
    print("Processing metro stops...")
    stops = []
    try:
        with open(METRO_STOPS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for stop in data.get('Stops', []):
                s_type = "metro" if stop.get('Code') not in ["-2000", "-2001"] else "mela"
                stops.append({
                    "info": {"id": stop.get('Code')},
                    "details": {"name": stop.get('Description'), "type": s_type},
                    "location": {"X": str(stop.get('Location', {}).get('X')), "Y": str(stop.get('Location', {}).get('Y'))}
                })
        print(f"Processed {len(stops)} metro stops.")
        return stops
    except FileNotFoundError:
        print(f"{METRO_STOPS_JSON} not found. Please ensure it's downloaded.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {METRO_STOPS_JSON}. File might be corrupt.")
        return []
    except Exception as e:
        print(f"Error processing metro stops: {e}")
        return []

def consolidate_and_save_stops(output_filename: str) -> None:
    """Combines processed surface and metro stops and saves to a JSON file."""
    print("\nConsolidating and saving all stops...")
    all_stops = process_metro_stops() + process_surface_stops() + process_net_stops()

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(all_stops, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {len(all_stops)} stops to {output_filename}.")
    except Exception as e:
        print(f"Error saving consolidated stops: {e}")

def cleanup_files(*filenames: str) -> None:
    """Deletes specified files if they exist."""
    print("\nCleaning up temporary files...")
    for filename in filenames:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Deleted {filename}.")
        except OSError as e:
            print(f"Error deleting {filename}: {e}")


def get_dataset_validity_date() -> datetime.date | None:
    """
    Scrapes the dataset page to find its validity end date and returns it as a date object.
    """
    print("Checking dataset validity date...")
    url = "https://dati.comune.milano.it/dataset/ds929-orari-del-trasporto-pubblico-locale-nel-comune-di-milano-in-formato-gtfs"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"! Warning: Could not fetch dataset info page (status: {response.status}).")
                return None

            html_content = response.read().decode('utf-8')
            pattern = re.compile(r"Estensione temporale.*?A:.*?<span>(.*?)</span>", re.DOTALL)
            match = pattern.search(html_content)

            if match:
                date_str = match.group(1).strip()
                try:
                    # Parse the date string 'dd-mm-yyyy' into a date object
                    return datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
                except ValueError:
                    print(f"! Warning: Found a date string '{date_str}' but could not parse it.")
                    return None
            else:
                print("! Warning: Could not find the validity date pattern on the page.")
                return None

    except Exception as e:
        print(f"! Warning: An error occurred while scraping for validity date: {e}")
        return None

if __name__ == "__main__":
    get_surface_stops_data()
    get_net_stops_data()
    get_metro_stops_data()

    # Ask the user for the output filename
    output_file_name = input("Enter the desired name for the output JSON file (e.g., my_stops.json): ")
    if not output_file_name.strip():
        output_file_name = "onboard_stops.json" # Default if user enters nothing
        print(f"No filename entered. Defaulting to '{output_file_name}'.")

    # Ensure it has a .json extension
    if not output_file_name.lower().endswith(".json"):
        output_file_name += ".json"
        print(f"Appended '.json' extension. Output file will be '{output_file_name}'.")

    consolidate_and_save_stops(output_file_name)

    # Clean up the downloaded raw data files
    cleanup_files(GTFS_ZIP, STOPS_TXT, METRO_STOPS_JSON, NET_GTFS_ZIP, NET_STOPS_TXT)

    # Get and display dataset validity information
    print("\n--- ⚠️IMPORTANT: DATASET VALIDITY ⚠️---")
    expiry_date = get_dataset_validity_date()

    if expiry_date:
        today = datetime.date.today()
        days_remaining = (expiry_date - today).days

        # Format the date for display as dd/mm/yyyy
        formatted_expiry_date = expiry_date.strftime("%d/%m/%Y")

        print(f"Dataset is valid until: {formatted_expiry_date}")

        if days_remaining >= 0:
            print(f"There are {days_remaining} days of validity remaining.")
        else:
            # Use abs() or unary minus to show a positive number of days
            print(f"This dataset expired {-days_remaining} days ago.")
    else:
        print("Could not determine the dataset's validity period.")