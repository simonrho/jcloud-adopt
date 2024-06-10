# Adopt Devices to Juniper Cloud Services 
This script automates the adoption of Juniper devices to the JCloud platform. It reads device information from an Excel file, fetches the adoption configuration from the JCloud API, and pushes the configuration to the devices using NETCONF.
## Requirements
* Python 3
* Libraries: `pandas`, `openpyxl`, `requests`, `ncclient`, `numpy`, and `tabulate`
* Excel file with device information
* JCloud Org API key
## Installation
1. Make sure you have Python 3 installed.
2. Install the required libraries using pip:
```bash
pip install pandas openpyxl requests ncclient numpy tabulate

or

pip install -r requirements.txt
```
## Usage
```bash
python jcloud-adopt.py <excel_file> [-k] [--keep-phone-home] [-t] [--max-threads]
```
### Arguments
* `<excel_file>`: Path to the Excel file containing device information (organization, site, address, port, username, password).
* `-k`, `--keep-phone-home`: Keep the 'delete system phone-home' command in the configuration (optional).
* `-t`, `--max-threads`: Maximum number of concurrent threads (default: 10) (optional).
### Excel file format
The Excel file should contain the following columns:
* `organization`: Organization name.
* `site`: Site name.
* `address`: Device IP address.
* `port`: Device port.
* `username`: Device username.
* `password`: Device password.
### Example Excel file
```
+----+-------------------------+---------+-----------+--------+------------+------------+
|    | organization            | site    | address   |   port | username   | password   |
|----+-------------------------+---------+-----------+--------+------------+------------|
|  0 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5901 | poc        | ******     |
|  1 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5902 | poc        | ******     |
|  2 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5903 | poc        | ******     |
|  3 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5904 | poc        | ******     |
|  4 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5905 | poc        | ******     |
|  5 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5906 | poc        | ******     |
|  6 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5907 | poc        | ******     |
|  7 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5908 | poc        | ******     |
|  8 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5909 | poc        | ******     |
|  9 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5910 | poc        | ******     |
| 10 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5911 | poc        | ******     |
| 11 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5912 | poc        | ******     |
| 12 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5913 | poc        | ******     |
| 13 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5914 | poc        | ******     |
| 14 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5915 | poc        | ******     |
| 15 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5916 | poc        | ******     |
| 16 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5917 | poc        | ******     |
| 17 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5918 | poc        | ******     |
| 18 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5919 | poc        | ******     |
| 19 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5920 | poc        | ******     |
| 20 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5921 | poc        | ******     |
| 21 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5922 | poc        | ******     |
| 22 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5923 | poc        | ******     |
| 23 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5924 | poc        | ******     |
| 24 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5925 | poc        | ******     |
| 25 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5926 | poc        | ******     |
| 26 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5927 | poc        | ******     |
| 27 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5928 | poc        | ******     |
| 28 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5929 | poc        | ******     |
| 29 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5930 | poc        | ******     |
| 30 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5931 | poc        | ******     |
| 31 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5932 | poc        | ******     |
+----+-------------------------+---------+-----------+--------+------------+------------+
```

### Example usage
```bash
python jcloud-adopt.py devices.xlsx
```
## Settings
The `settings.json` file should contain the API server URLs and organization details. Example `settings.json`:
```json
{
    "api": {
        "server": {
            "mist1": { "url": "https://api.mist.com/api/v1", "name": "Global 01" },
            "mist2": { "url": "https://api.gc1.mist.com/api/v1", "name": "Global 02" },
            "mist3": { "url": "https://api.ac2.mist.com/api/v1", "name": "Global 03" },
            "mist4": { "url": "https://api.gc2.mist.com/api/v1", "name": "Global 04" },
            "mist5": { "url": "https://api.ac99.mist.com/api/v1", "name": "Global 99" },
            "mist6": { "url": "https://api.eu.mist.com/api/v1", "name": "EMEA 01" },
            "mist7": { "url": "https://api.gc3.mist.com/api/v1", "name": "EMEA 02" },
            "mist8": { "url": "https://api.ac5.mist.com/api/v1", "name": "APAC 01" },
            "jsi1": { "url": "https://jsi.ai.juniper.net/api/v1", "name": "Global 01" },
            "ra1": { "url": "https://routing.ai.juniper.net/api/v1", "name": "Global 01" }
        },
        "default": "jsi1"
    },
    "org": {
        "your org name1": {
            "id": "your org id1",
            "token": "your org1's api token"
        },
        "your org name2": {
            "id": "your org id2",
            "token": "your org2's api token"
        }
    }
}
```
### Example settings file
Save the above JSON structure as `settings.json` in the same directory as your script.
## Notes
- Ensure the settings file (`settings.json`) and the Excel file containing device details are properly formatted.
- The script will log detailed information and errors to help diagnose issues.
- If the `--keep-phone-home` option is not specified, the script will remove the 'delete system phone-home' command from the configuration before pushing it to the devices.
## Example Usage
```bash
python jcloud-adopt.py devices.xlsx
```
This command will run the script using the `devices.xlsx` file and process up to 5 devices concurrently.
Remember to update your `settings.json` file with the correct API URLs and organization details before running the script.


### Script Logging Details ###
```bash
% ./jcloud-adopt.py devices.xlsx
2024-06-10 01:06:11,109 - INFO - Device Excel file dump!!!
2024-06-10 01:06:11,110 - INFO -
+----+-------------------------+---------+-----------+--------+------------+------------+
|    | organization            | site    | address   |   port | username   | password   |
|----+-------------------------+---------+-----------+--------+------------+------------|
|  0 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5901 | poc        | ******     |
|  1 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5902 | poc        | ******     |
|  2 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5903 | poc        | ******     |
|  3 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5904 | poc        | ******     |
|  4 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5905 | poc        | ******     |
|  5 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5906 | poc        | ******     |
|  6 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5907 | poc        | ******     |
|  7 | JSI Demo Company - ACME | Site-01 | 10.6.3.55 |   5908 | poc        | ******     |
|  8 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5909 | poc        | ******     |
|  9 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5910 | poc        | ******     |
| 10 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5911 | poc        | ******     |
| 11 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5912 | poc        | ******     |
| 12 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5913 | poc        | ******     |
| 13 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5914 | poc        | ******     |
| 14 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5915 | poc        | ******     |
| 15 | JSI Demo Company - ACME | Site-02 | 10.6.3.55 |   5916 | poc        | ******     |
| 16 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5917 | poc        | ******     |
| 17 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5918 | poc        | ******     |
| 18 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5919 | poc        | ******     |
| 19 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5920 | poc        | ******     |
| 20 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5921 | poc        | ******     |
| 21 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5922 | poc        | ******     |
| 22 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5923 | poc        | ******     |
| 23 | JSI Demo Company - ACME | Site-03 | 10.6.3.55 |   5924 | poc        | ******     |
| 24 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5925 | poc        | ******     |
| 25 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5926 | poc        | ******     |
| 26 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5927 | poc        | ******     |
| 27 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5928 | poc        | ******     |
| 28 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5929 | poc        | ******     |
| 29 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5930 | poc        | ******     |
| 30 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5931 | poc        | ******     |
| 31 | JSI Demo Company - ACME | Site-04 | 10.6.3.55 |   5932 | poc        | ******     |
+----+-------------------------+---------+-----------+--------+------------+------------+
2024-06-10 01:06:11,113 - INFO - address:port, hardware model, os name, os version, serial number, host name
2024-06-10 01:06:14,859 - WARNING - 10.6.3.55:5908 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,105 - WARNING - 10.6.3.55:5910 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,271 - WARNING - 10.6.3.55:5906 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,529 - INFO - 10.6.3.55:5905, ex9214, junos, 23.2R2.21, VM666622442A, vmx05-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,540 - WARNING - 10.6.3.55:5909 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,645 - INFO - 10.6.3.55:5901, ex9214, junos, 23.2R2.21, VM6666222DEE, vmx01-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,695 - INFO - 10.6.3.55:5904, ex9214, junos, 23.2R2.21, VM6666221CE8, vmx04-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,818 - INFO - 10.6.3.55:5903, ex9214, junos, 23.2R2.21, VM6666221B74, vmx03-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,891 - INFO - 10.6.3.55:5907, ex9214, junos, 23.2R2.21, VM6666229F26, vmx07-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,907 - INFO - 10.6.3.55:5902, ex9214, junos, 23.2R2.21, VM6666221CF6, vmx02-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,102 - INFO - 10.6.3.55:5912, ex9214, junos, 23.2R2.21, VM666622A078, vmx12-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,159 - INFO - 10.6.3.55:5911, ex9214, junos, 23.2R2.21, VM6666228936, vmx11-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,215 - INFO - 10.6.3.55:5914, ex9214, junos, 23.2R2.21, VM666622A8E7, vmx14-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,298 - INFO - 10.6.3.55:5915, ex9214, junos, 23.2R2.21, VM6666229C5F, vmx15-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,316 - INFO - 10.6.3.55:5916, ex9214, junos, 23.2R2.21, VM666622BDB6, vmx16-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,384 - INFO - 10.6.3.55:5913, ex9214, junos, 23.2R2.21, VM666622887A, vmx13-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:22,324 - WARNING - 10.6.3.55:5919 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:22,356 - WARNING - 10.6.3.55:5917 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:22,442 - WARNING - 10.6.3.55:5918 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:24,735 - INFO - 10.6.3.55:5920, ex9214, junos, 23.2R2.21, VM666622EC99, vmx20-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:24,805 - INFO - 10.6.3.55:5922, ex9214, junos, 23.2R2.21, VM666622EEB3, vmx22-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:25,243 - INFO - 10.6.3.55:5921, ex9214, junos, 23.2R2.21, VM666622ED93, vmx21-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:29,271 - INFO - 10.6.3.55:5924, ex9214, junos, 23.2R2.21, VM6666231E50, vmx24-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:29,414 - INFO - 10.6.3.55:5923, ex9214, junos, 23.2R2.21, VM6666231CB0, vmx23-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:29,724 - INFO - 10.6.3.55:5925, ex9214, junos, 23.2R2.21, VM66662346E8, vmx25-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:33,612 - INFO - 10.6.3.55:5927, ex9214, junos, 23.2R2.21, VM66662361B4, vmx27-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:33,699 - INFO - 10.6.3.55:5926, ex9214, junos, 23.2R2.21, VM666623535C, vmx26-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:33,980 - INFO - 10.6.3.55:5928, ex9214, junos, 23.2R2.21, VM6666236FDD, vmx28-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:37,782 - INFO - 10.6.3.55:5929, ex9214, junos, 23.2R2.21, VM66662377CD, vmx29-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:37,950 - INFO - 10.6.3.55:5930, ex9214, junos, 23.2R2.21, VM6666237F48, vmx30-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:38,256 - INFO - 10.6.3.55:5931, ex9214, junos, 23.2R2.21, VM66662382E9, vmx31-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:42,024 - INFO - 10.6.3.55:5932, ex9214, junos, 23.2R2.21, VM666623873A, vmx32-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:48,571 - INFO - 10.6.3.55:5908, ex9214, junos, 23.2R2.21, VM66662281C7, vmx08-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:48,892 - INFO - 10.6.3.55:5910, ex9214, junos, 23.2R2.21, VM666622A0EF, vmx10-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:48,997 - INFO - 10.6.3.55:5906, ex9214, junos, 23.2R2.21, VM6666221E95, vmx06-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:49,188 - INFO - 10.6.3.55:5909, ex9214, junos, 23.2R2.21, VM6666227B07, vmx09-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:56,025 - INFO - 10.6.3.55:5919, ex9214, junos, 23.2R2.21, VM66662301D8, vmx19-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:56,046 - INFO - 10.6.3.55:5917, ex9214, junos, 23.2R2.21, VM666622EDB6, vmx17-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:56,174 - INFO - 10.6.3.55:5918, ex9214, junos, 23.2R2.21, VM666622BEBD, vmx18-EX9214 => Configuration pushed successfully.

```



