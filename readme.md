# 🚍 Onboard Stops Generator

>[!Note]
> **EDUCATIONAL PROJECT DISCLAIMER**
>
>This project is developed purely for **educational and demonstrative purposes**. While it aims to provide useful public transport information for Milan, it relies on data sources, including scraping information from `giromilano.atm.it`.
>
>**The terms of service for ATM (Azienda Trasporti Milanesi) regarding data usage are not explicitly clear, and this project may potentially violate them.**
>
>Therefore:
>- **Use at Your Own Risk:** We do not guarantee the accuracy or continued availability of the data, nor do we assume responsibility for any consequences arising from its use.
>- **Unscheduled Discontinuation:** This project, or parts of it, may be taken down or become non-functional unexpectedly if ATM's policies change or if the data sources become inaccessible.
>
>We advise caution and understanding of these limitations.

A simple command-line utility that downloads, processes, and combines public transport stop data for Milan, Italy, from the official ATM (Azienda Trasporti Milanesi) public data sources. This tool is a vital part of the [Onboard Project](https://github.com/onboard-project)'s data pipeline.

## ✨ Key Features

*   **Automated Data Fetching:** Automatically downloads `stops.txt` for surface transport and metro stop JSON from official ATM sources.
*   **Unified Data Output:** Processes and combines disparate data sources into a single, clean `onboard_stops.json` file.
*   **Data Validation & Cleaning:** Ensures data quality by standardizing names, filtering invalid entries, and transforming data into a consistent format.
*   **Validity Tracking:** Provides the expiry date for the dataset and remaining days, crucial for the [Onboard Project server](https://github.com/onboard-project/server)'s [Status endpoint](https://onboard-project-api.vercel.app/status).

## 🚀 Getting Started

### Installation

To use `onboard-stopgen` without setting up a Python environment, download the pre-compiled executable:

1.  **Download:** Visit the **Releases** page of this repository and download the `onboard-stopgen` executable for your operating system (e.g., `onboard-stopgen.exe` for Windows).
2.  **Place Executable:** Move the downloaded file to a dedicated folder (e.g., `C:\Tools\Onboard`).
3.  **Add to PATH:** To run the command from any location, add this folder to your system's PATH environment variable.
> [!TIP]
> **On Windows:**
> - Search for "Edit the system environment variables" and open it.
> - Click the "Environment Variables..." button.
> - Under "System variables" (or "User variables"), find and select the `Path` variable, then click "Edit...".
> - Click "New" and paste the path to the folder containing `onboard-stopgen.exe`.
> - Click OK on all windows to save. You may need to restart your terminal.

### Usage

Once installed and added to your PATH, using the tool is simple:

1.  Open your terminal or command prompt.
2.  Navigate to the folder where you want the `onboard_stops.json` file to be created.
3.  Run the command:
    ```bash
    onboard-stopgen
    ```
    This will generate or update the `onboard_stops.json` file in your current directory.

## 🛠️ Development Setup (Optional)

If you wish to contribute or modify the script:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/onboard-project/stopsgen.git
    cd stopsgen
    ```
2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Script:**
    ```bash
    python main.py
    ```

## 🤝 Contributing

We welcome contributions to improve the Onboard Stops Generator! Feel free to open issues for bug reports or feature requests, or submit pull requests with your enhancements.

## 📄 License

This project is licensed under the [GNU GPL v3.0 License](LICENSE).

