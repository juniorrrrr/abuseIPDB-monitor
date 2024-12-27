# AbuseIPDB Monitor Script

This script monitors specified IP blocks for abuse reports using the AbuseIPDB API and sends notifications via Pushover when an IP is listed with a new or higher score.

## Prerequisites

1. **Python 3.7 or later**
2. **Dependencies:**
   - `requests`
   - `ipaddress`
3. **API Keys:**
   - AbuseIPDB API Key
   - Pushover User Key
   - Pushover App Token

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/abuseipdb-monitor.git
   cd abuseipdb-monitor
   ```

2. **Set up a Python Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Script:**
   - Open the script file `monitor_ips_abuseipdb.py`.
   - Replace the placeholders with your actual API keys:
     ```python
     ABUSEIPDB_API_KEY = "your_abuseipdb_api_key"
     PUSHOVER_USER_KEY = "your_pushover_user_key"
     PUSHOVER_API_TOKEN = "your_pushover_app_token"
     ```

5. **Specify IP Blocks to Monitor:**
   - Update the `BLOCKS` variable in the script with the IP ranges you want to monitor:
     ```python
     BLOCKS = [
         "192.168.0.0/24",
         "10.0.0.0/24"
     ]
     ```

## Running the Script

1. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the Script:**
   ```bash
   python monitor_ips_abuseipdb.py
   ```

## Automating with Cron (Optional)

1. **Edit Cron Jobs:**
   ```bash
   crontab -e
   ```

2. **Add the Following Entry:**
   ```bash
   0 13 * * * /path/to/venv/bin/python /path/to/monitor_ips_abuseipdb.py >> /path/to/monitor.log 2>&1
   ```

   - This example runs the script daily at 1 PM.

## Logs

Logs will be saved in the specified log file (e.g., `monitor.log`) if configured in the cron job.

## Notes

- Ensure the `notified_ips.json` file is writable by the script. This file stores previously notified IPs to avoid duplicate notifications.
- Be mindful of AbuseIPDB API rate limits when monitoring large blocks of IPs.

## License


