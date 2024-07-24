# Adopt Devices to Juniper Cloud Services 
This script automates the adoption of Juniper devices into Juniper cloud services such as MIST, RA, and JSI. It reads device information from an Excel file, fetches the adoption configuration from the relevant API server, and pushes the configuration to the devices using NETCONF.

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
python bulk-adopt.py [-h] [-k] [-t MAX_THREADS] [-s SETTINGS] [-j] excel_file
```
### Arguments
* `<excel_file>`: Path to the Excel file containing device information (organization, site, address, port, username, password).
* `-k`, `--keep-phone-home`: Keep the 'delete system phone-home' command in the configuration (optional).
* `-t`, `--max-threads`: Maximum number of concurrent threads (default: 10) (optional).
* `-s`, `--settings`: Path to the settings file (default: settings.json)
* `-j`, `--jsi`: Use the jsi-term service instead of oc-term to terminate the outbound SSH connection

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
+----+-------------------------+---------+---------------+--------+------------+------------+
|    | organization            | site    | address       |   port | username   | password   |
|----+-------------------------+---------+---------------+--------+------------+------------|
|  0 | JSI Demo Company - ACME | Site-01 | 192.168.1.101 |   22   | poc        | ******     |
|  1 | JSI Demo Company - ACME | Site-01 | 192.168.1.102 |   22   | poc        | ******     |
|  2 | JSI Demo Company - ACME | Site-01 | 192.168.1.103 |   22   | poc        | ******     |
|  3 | JSI Demo Company - ACME | Site-01 | 192.168.1.104 |   22   | poc        | ******     |
|  4 | JSI Demo Company - ACME | Site-01 | 192.168.1.105 |   22   | poc        | ******     |
|  5 | JSI Demo Company - ACME | Site-01 | 192.168.1.106 |   22   | poc        | ******     |
|  6 | JSI Demo Company - ACME | Site-01 | 192.168.1.107 |   22   | poc        | ******     |
|  7 | JSI Demo Company - ACME | Site-01 | 192.168.1.108 |   22   | poc        | ******     |
|  8 | JSI Demo Company - ACME | Site-02 | 192.168.1.109 |   22   | poc        | ******     |
|  9 | JSI Demo Company - ACME | Site-02 | 192.168.1.110 |   22   | poc        | ******     |
| 10 | JSI Demo Company - ACME | Site-02 | 192.168.1.111 |   22   | poc        | ******     |
| 11 | JSI Demo Company - ACME | Site-02 | 192.168.1.112 |   22   | poc        | ******     |
| 12 | JSI Demo Company - ACME | Site-02 | 192.168.1.113 |   22   | poc        | ******     |
| 13 | JSI Demo Company - ACME | Site-02 | 192.168.1.114 |   22   | poc        | ******     |
| 14 | JSI Demo Company - ACME | Site-02 | 192.168.1.115 |   22   | poc        | ******     |
| 15 | JSI Demo Company - ACME | Site-02 | 192.168.1.116 |   22   | poc        | ******     |
| 16 | JSI Demo Company - ACME | Site-03 | 192.168.1.117 |   22   | poc        | ******     |
| 17 | JSI Demo Company - ACME | Site-03 | 192.168.1.118 |   22   | poc        | ******     |
| 18 | JSI Demo Company - ACME | Site-03 | 192.168.1.119 |   22   | poc        | ******     |
| 19 | JSI Demo Company - ACME | Site-03 | 192.168.1.120 |   22   | poc        | ******     |
| 20 | JSI Demo Company - ACME | Site-03 | 192.168.1.121 |   22   | poc        | ******     |
| 21 | JSI Demo Company - ACME | Site-03 | 192.168.1.122 |   22   | poc        | ******     |
| 22 | JSI Demo Company - ACME | Site-03 | 192.168.1.123 |   22   | poc        | ******     |
| 23 | JSI Demo Company - ACME | Site-03 | 192.168.1.124 |   22   | poc        | ******     |
| 24 | JSI Demo Company - ACME | Site-04 | 192.168.1.125 |   22   | poc        | ******     |
| 25 | JSI Demo Company - ACME | Site-04 | 192.168.1.126 |   22   | poc        | ******     |
| 26 | JSI Demo Company - ACME | Site-04 | 192.168.1.127 |   22   | poc        | ******     |
| 27 | JSI Demo Company - ACME | Site-04 | 192.168.1.128 |   22   | poc        | ******     |
| 28 | JSI Demo Company - ACME | Site-04 | 192.168.1.129 |   22   | poc        | ******     |
| 29 | JSI Demo Company - ACME | Site-04 | 192.168.1.130 |   22   | poc        | ******     |
| 30 | JSI Demo Company - ACME | Site-04 | 192.168.1.131 |   22   | poc        | ******     |
| 31 | JSI Demo Company - ACME | Site-04 | 192.168.1.132 |   22   | poc        | ******     |
+----+-------------------------+---------+---------------+--------+------------+------------+
```

### Example usage
```bash
python bulk-adopt.py devices.xlsx
```
## Settings
The `settings.json` file should contain the API server URLs and organization details. Please add your organization information (organization ID, name(names must be unique) and API token). Additionally, make sure that `api.server.default` is configured to your target service and region.
If only the JSI dedicated service is required, please set `using_jsi_term` to `true`.

Example `settings.json`:


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
    "using_jsi_term": false,
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
python bulk-adopt.py devices.xlsx
```
This command will run the script using the `devices.xlsx` file and process up to 10 (default value) devices concurrently.
Remember to update your `settings.json` file with the correct API URLs, the default cloud, and organization details before running the script.

```bash
python bulk-adopt.py -s ./site1/my-settings.json -j ./my_devices.xlsx
```
This command runs the script using the `my_devices.xlsx` file and processes up to 10 devices concurrently (default value), using the `./site1/my-settings.json` settings file. It also uses the `jsi-term` service to terminate the outbound SSH connection from devices.


### Script Logging Details ###
```bash
% ./bulk-adopt.py devices.xlsx
2024-06-10 01:06:11,109 - INFO - Device Excel file dump!!!
2024-06-10 01:06:11,110 - INFO -
+----+-------------------------+---------+---------------+--------+------------+------------+
|    | organization            | site    | address       |   port | username   | password   |
|----+-------------------------+---------+---------------+--------+------------+------------|
|  0 | JSI Demo Company - ACME | Site-01 | 192.168.1.101 |   22   | poc        | ******     |
|  1 | JSI Demo Company - ACME | Site-01 | 192.168.1.102 |   22   | poc        | ******     |
|  2 | JSI Demo Company - ACME | Site-01 | 192.168.1.103 |   22   | poc        | ******     |
|  3 | JSI Demo Company - ACME | Site-01 | 192.168.1.104 |   22   | poc        | ******     |
|  4 | JSI Demo Company - ACME | Site-01 | 192.168.1.105 |   22   | poc        | ******     |
|  5 | JSI Demo Company - ACME | Site-01 | 192.168.1.106 |   22   | poc        | ******     |
|  6 | JSI Demo Company - ACME | Site-01 | 192.168.1.107 |   22   | poc        | ******     |
|  7 | JSI Demo Company - ACME | Site-01 | 192.168.1.108 |   22   | poc        | ******     |
|  8 | JSI Demo Company - ACME | Site-02 | 192.168.1.109 |   22   | poc        | ******     |
|  9 | JSI Demo Company - ACME | Site-02 | 192.168.1.110 |   22   | poc        | ******     |
| 10 | JSI Demo Company - ACME | Site-02 | 192.168.1.111 |   22   | poc        | ******     |
| 11 | JSI Demo Company - ACME | Site-02 | 192.168.1.112 |   22   | poc        | ******     |
| 12 | JSI Demo Company - ACME | Site-02 | 192.168.1.113 |   22   | poc        | ******     |
| 13 | JSI Demo Company - ACME | Site-02 | 192.168.1.114 |   22   | poc        | ******     |
| 14 | JSI Demo Company - ACME | Site-02 | 192.168.1.115 |   22   | poc        | ******     |
| 15 | JSI Demo Company - ACME | Site-02 | 192.168.1.116 |   22   | poc        | ******     |
| 16 | JSI Demo Company - ACME | Site-03 | 192.168.1.117 |   22   | poc        | ******     |
| 17 | JSI Demo Company - ACME | Site-03 | 192.168.1.118 |   22   | poc        | ******     |
| 18 | JSI Demo Company - ACME | Site-03 | 192.168.1.119 |   22   | poc        | ******     |
| 19 | JSI Demo Company - ACME | Site-03 | 192.168.1.120 |   22   | poc        | ******     |
| 20 | JSI Demo Company - ACME | Site-03 | 192.168.1.121 |   22   | poc        | ******     |
| 21 | JSI Demo Company - ACME | Site-03 | 192.168.1.122 |   22   | poc        | ******     |
| 22 | JSI Demo Company - ACME | Site-03 | 192.168.1.123 |   22   | poc        | ******     |
| 23 | JSI Demo Company - ACME | Site-03 | 192.168.1.124 |   22   | poc        | ******     |
| 24 | JSI Demo Company - ACME | Site-04 | 192.168.1.125 |   22   | poc        | ******     |
| 25 | JSI Demo Company - ACME | Site-04 | 192.168.1.126 |   22   | poc        | ******     |
| 26 | JSI Demo Company - ACME | Site-04 | 192.168.1.127 |   22   | poc        | ******     |
| 27 | JSI Demo Company - ACME | Site-04 | 192.168.1.128 |   22   | poc        | ******     |
| 28 | JSI Demo Company - ACME | Site-04 | 192.168.1.129 |   22   | poc        | ******     |
| 29 | JSI Demo Company - ACME | Site-04 | 192.168.1.130 |   22   | poc        | ******     |
| 30 | JSI Demo Company - ACME | Site-04 | 192.168.1.131 |   22   | poc        | ******     |
| 31 | JSI Demo Company - ACME | Site-04 | 192.168.1.132 |   22   | poc        | ******     |
+----+-------------------------+---------+---------------+--------+------------+------------+
2024-06-10 01:06:11,113 - INFO - address:port, hardware model, os name, os version, serial number, host name
2024-06-10 01:06:14,859 - WARNING - 192.168.1.108:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,105 - WARNING - 192.168.1.110:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,271 - WARNING - 192.168.1.106:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,529 - INFO - 192.168.1.105:22, ex9214, junos, 23.2R2.21, VM666622442A, vmx05-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,540 - WARNING - 192.168.1.109:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:15,645 - INFO - 192.168.1.101:22, ex9214, junos, 23.2R2.21, VM6666222DEE, vmx01-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,695 - INFO - 192.168.1.104:22, ex9214, junos, 23.2R2.21, VM6666221CE8, vmx04-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,818 - INFO - 192.168.1.103:22, ex9214, junos, 23.2R2.21, VM6666221B74, vmx03-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,891 - INFO - 192.168.1.107:22, ex9214, junos, 23.2R2.21, VM6666229F26, vmx07-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:15,907 - INFO - 192.168.1.102:22, ex9214, junos, 23.2R2.21, VM6666221CF6, vmx02-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,102 - INFO - 192.168.1.112:22, ex9214, junos, 23.2R2.21, VM666622A078, vmx12-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,159 - INFO - 192.168.1.111:22, ex9214, junos, 23.2R2.21, VM6666228936, vmx11-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,215 - INFO - 192.168.1.114:22, ex9214, junos, 23.2R2.21, VM666622A8E7, vmx14-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,298 - INFO - 192.168.1.115:22, ex9214, junos, 23.2R2.21, VM6666229C5F, vmx15-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,316 - INFO - 192.168.1.116:22, ex9214, junos, 23.2R2.21, VM666622BDB6, vmx16-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:20,384 - INFO - 192.168.1.113:22, ex9214, junos, 23.2R2.21, VM666622887A, vmx13-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:22,324 - WARNING - 192.168.1.119:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:22,356 - WARNING - 192.168.1.117:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:22,442 - WARNING - 192.168.1.118:22 => Configuration database locked. Retrying in 30 seconds... (Attempt 1/3)
2024-06-10 01:06:24,735 - INFO - 192.168.1.120:22, ex9214, junos, 23.2R2.21, VM666622EC99, vmx20-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:24,805 - INFO - 192.168.1.122:22, ex9214, junos, 23.2R2.21, VM666622EEB3, vmx22-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:25,243 - INFO - 192.168.1.121:22, ex9214, junos, 23.2R2.21, VM666622ED93, vmx21-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:29,271 - INFO - 192.168.1.124:22, ex9214, junos, 23.2R2.21, VM6666231E50, vmx24-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:29,414 - INFO - 192.168.1.123:22, ex9214, junos, 23.2R2.21, VM6666231CB0, vmx23-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:29,724 - INFO - 192.168.1.125:22, ex9214, junos, 23.2R2.21, VM66662346E8, vmx25-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:33,612 - INFO - 192.168.1.127:22, ex9214, junos, 23.2R2.21, VM66662361B4, vmx27-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:33,699 - INFO - 192.168.1.126:22, ex9214, junos, 23.2R2.21, VM666623535C, vmx26-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:33,980 - INFO - 192.168.1.128:22, ex9214, junos, 23.2R2.21, VM6666236FDD, vmx28-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:37,782 - INFO - 192.168.1.129:22, ex9214, junos, 23.2R2.21, VM66662377CD, vmx29-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:37,950 - INFO - 192.168.1.130:22, ex9214, junos, 23.2R2.21, VM6666237F48, vmx30-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:38,256 - INFO - 192.168.1.131:22, ex9214, junos, 23.2R2.21, VM66662382E9, vmx31-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:42,024 - INFO - 192.168.1.132:22, ex9214, junos, 23.2R2.21, VM666623873A, vmx32-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:48,571 - INFO - 192.168.1.108:22, ex9214, junos, 23.2R2.21, VM66662281C7, vmx08-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:48,892 - INFO - 192.168.1.110:22, ex9214, junos, 23.2R2.21, VM666622A0EF, vmx10-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:48,997 - INFO - 192.168.1.106:22, ex9214, junos, 23.2R2.21, VM6666221E95, vmx06-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:49,188 - INFO - 192.168.1.109:22, ex9214, junos, 23.2R2.21, VM6666227B07, vmx09-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:56,025 - INFO - 192.168.1.119:22, ex9214, junos, 23.2R2.21, VM66662301D8, vmx19-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:56,046 - INFO - 192.168.1.117:22, ex9214, junos, 23.2R2.21, VM666622EDB6, vmx17-EX9214 => Configuration pushed successfully.
2024-06-10 01:06:56,174 - INFO - 192.168.1.118:22, ex9214, junos, 23.2R2.21, VM666622BEBD, vmx18-EX9214 => Configuration pushed successfully.

```



