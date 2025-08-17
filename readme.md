# Onboard Stops Generator

A simple command-line utility that downloads, processes, and combines public transport stop data for Milan, Italy, from the official ATM (Azienda Trasporti Milanesi) public data sources.

## What It Does

This tool automates the process of fetching stop information for both surface-level transport (buses, trams) and metro lines.

1.  **Downloads Surface Stops**: Fetches a GTFS-like zip file containing `stops.txt` for all surface-level stops.
2.  **Downloads Metro Stops**: Queries a specific API endpoint to get a JSON file with all metro line stops.
3.  **Processes & Cleans Data**: It parses both data sources, cleans up the data (e.g., standardizes names, filters invalid entries), and transforms it into a unified format.
4.  **Generates a Single File**: The final output is a clean, combined, and ready-to-use `onboard_stops.json` file.

## Installation

To use the tool without needing to set up a Python environment, you can download the pre-compiled executable.

1.  **Download**: Go to the **Releases** page of this repository and download the `onboard-stopgen` executable for windows.
2.  **Place the Executable**: Move the downloaded file to a dedicated folder on your computer (e.g., `C:\Tools`).
3.  **Add to PATH**: To run the command from any location, add the folder from the previous step to your system's PATH environment variable.
>[!TIP]
> **On Windows:**
> - Search for "Edit the system environment variables" and open it.
> - Click the "Environment Variables..." button.
> - Under "System variables" (or "User variables"), find and select the `Path` variable, then click "Edit...".
> - Click "New" and paste the path to the folder containing `onboard-stopgen.exe`.
> - Click OK on all windows to save. You may need to restart your terminal.

## Usage

Once installed and added to your PATH, using the tool is simple.

1.  Open your terminal or command prompt.
2.  Navigate to any folder where you want the final JSON file to be created.
3.  Run the command: 
    ```bash
    onboard-stopgen
    ```