#!/usr/bin/env python3

import argparse
import configparser
import pandas as pd
import requests
import numpy as np
from tabulate import tabulate
import sys
import json
import time

from ncclient import manager
from ncclient.transport.errors import SSHError
from ncclient.operations.rpc import RPCError

import concurrent.futures
import traceback

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('ncclient').setLevel(logging.WARNING)

# Global settings and cache for site details
settings = {}
site_details_cache = {}

def load_settings(file_path):
    """
    Load settings from a JSON file.

    :param file_path: Path to the settings file.
    :return: Dictionary containing the settings.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Error: The settings file '{file_path}' was not found.")
        logging.error("Please ensure the settings file is present and try again.")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(f"Error: The settings file '{file_path}' contains invalid JSON.")
        sys.exit(1)

def cache_site_details(settings, api_url_template):
    """
    Cache site details for each organization.

    :param settings: Dictionary containing settings.
    :param api_url_template: URL template for fetching site details.
    """
    for org_name, details in settings['org'].items():
        if ' ' in details['id']:  # Skip organization IDs with spaces
            continue

        api_url = api_url_template.format(org_id=details['id'])
        headers = {
            "Authorization": f"Token {details['token']}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            site_details_cache[details['id']] = {site['name']: site['id'] for site in response.json()}
        else:
            logging.error(f"Failed to fetch sites for '{org_name}': Status Code '{response.status_code}' - '{response.text}'")

def initialize_sites_cache(settings):
    """
    Initialize the site details cache.

    :param settings: Dictionary containing settings.
    """
    default_cloud = settings['api']['default']
    api_url_template = settings['api']['server'][default_cloud]['url'] + "/orgs/{org_id}/sites"
    cache_site_details(settings, api_url_template)

def get_site_id_by_name(org_id, site_name):
    """
    Get site ID by site name.

    :param org_id: Organization ID.
    :param site_name: Site name.
    :return: Site ID.
    """
    try:
        return site_details_cache[org_id][site_name]
    except KeyError:
        raise ValueError(f"Site '{site_name}' not found for organization ID '{org_id}'")

def dump_excel_file(file_name):
    """
    Dump the contents of an Excel file.

    :param file_name: Path to the Excel file.
    """
    try:
        df = pd.read_excel(file_name)

        # Mask password fields with asterisks
        for col in df.columns:
            if 'password' in col.lower():
                df[col] = df[col].apply(lambda x: len(str(x)) * '*')

        # Replace empty cells with "Empty"
        df.replace(np.nan, 'Empty', inplace=True)

        # Log the data in a table format
        logging.info('Device Excel file dump!!!')
        logging.info("\n" + tabulate(df, headers='keys', tablefmt='psql'))

    except FileNotFoundError:
        logging.error(f"Error: The file {file_name} was not found.")
        sys.exit(1)

def read_excel(file_name):
    """
    Read and process the Excel file.

    :param file_name: Path to the Excel file.
    :return: Processed DataFrame.
    """
    df = pd.read_excel(file_name, engine="openpyxl")
    unique_df = df.drop_duplicates(subset=['address', 'port'], keep="last")
    
    return unique_df

def fetch_jcloud_config(base_url, api_token, org_id, site_id=None, remove_phone_home=True):
    """
    Fetch configuration commands from the JCloud API.

    :param base_url: Base URL for the API.
    :param api_token: API token.
    :param org_id: Organization ID.
    :param site_id: Site ID (optional).
    :param remove_phone_home: Whether to remove the 'delete system phone-home' command.
    :return: List of configuration commands or error message.
    """
    url = f"{base_url}/orgs/{org_id}/ocdevices/outbound_ssh_cmd"

    if site_id and not pd.isna(site_id):
        url += f"?site_id={site_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {api_token}"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        cmd = response.json()["cmd"]
        if remove_phone_home:
            cmd = "\n".join(line for line in cmd.split("\n") if "delete system phone-home" not in line)
        return cmd.split("\n")
    else:
        return f"Failed to fetch adoption command from jcloud API: {response.text}"

def push_config(device_info, config_commands, max_retries=3, retry_delay=30):
    """
    Push configuration commands to a device.

    :param device_info: Tuple containing device information (address, port, username, password).
    :param config_commands: List of configuration commands.
    :param max_retries: Maximum number of retries.
    :param retry_delay: Delay between retries in seconds.
    :return: Result message.
    """
    address, port, username, password = device_info
    retries = 0

    while retries < max_retries:
        try:
            conn = manager.connect(
                host=address,
                port=port,
                username=username,
                password=password,
                timeout=60,
                hostkey_verify=False,
                device_params={"name": "junos"},
                allow_agent=False,
                look_for_keys=False
            )
            
            result = conn.get_system_information()
            hardware_model = result.xpath('//system-information/hardware-model/text()')[0]
            os_name = result.xpath('//system-information/os-name/text()')[0]
            os_version = result.xpath('//system-information/os-version/text()')[0]
            serial_number = result.xpath('//system-information/serial-number/text()')[0]
            host_name = result.xpath('//system-information/host-name/text()')[0]

            conn.load_configuration(action='set', config=config_commands)
            commit_result = conn.commit()

            if commit_result.find(".//ok") is not None:
                logging.info(f'{address}:{port}, {hardware_model}, {os_name}, {os_version}, {serial_number}, {host_name} => Configuration pushed successfully.')
                return [f'{address}:{port}, {hardware_model}, {os_name}, {os_version}, {serial_number}, {host_name}', 'OK']
            else:
                logging.error(f'{address}:{port} => Error: Commit failed.')
                return 'Error: Commit failed'

        except (ConnectionResetError, SSHError, RPCError) as e:
            if isinstance(e, RPCError) and "configuration database locked" in str(e):
                retries += 1
                if retries < max_retries:
                    logging.warning(f'{address}:{port} => Configuration database locked. Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})')
                    time.sleep(retry_delay)
                else:
                    logging.error(f'{address}:{port} => Error: Unable to push configuration after {max_retries} attempts due to locked configuration database.')
                    return f"Error: Unable to push configuration to {address} after {max_retries} attempts due to locked configuration database."
            else:
                retries += 1
                if retries < max_retries:
                    logging.warning(f'{address}:{port} => Connection reset by peer. Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})')
                    time.sleep(retry_delay)
                else:
                    logging.error(f'{address}:{port} => Error: Unable to establish NETCONF connection after {max_retries} attempts.')
                    logging.error(f"Details: {str(e)}")
                    traceback.print_exc()
                    return f"Error: Unable to establish NETCONF connection with {address} after {max_retries} attempts. Reason: {str(e)}"

        except Exception as e:
            logging.error(f'{address}:{port} => Error: Unable to establish NETCONF connection.')
            logging.error(f"Details: {str(e)}")
            traceback.print_exc()
            return f"Error: Unable to establish NETCONF connection with {address}. Reason: {str(e)}"

def worker(device_info, remove_phone_home):
    """
    Worker function for processing a single device.

    :param device_info: Dictionary containing device information.
    :param remove_phone_home: Whether to remove the 'delete system phone-home' command.
    :return: Tuple containing address and result message.
    """
    org_name = device_info['organization']
    site_name = device_info['site']
    address = device_info['address']
    port = device_info['port']
    username = device_info['username']
    password = device_info['password']

    # Retrieve organization ID and token from the settings using org_name
    try:
        org_id = settings['org'][org_name]['id']
        token = settings['org'][org_name]['token']
        default_cloud = settings['api']['default']
        base_url = settings['api']['server'][default_cloud]['url']
    except KeyError:
        return address, port, f"Organization or token not found for {org_name}"

    # Retrieve site ID using cached site details
    try:
        site_id = get_site_id_by_name(org_id, site_name)
    except ValueError as e:
        return address, str(e)

    # Fetch configuration commands
    config_commands = fetch_jcloud_config(base_url, token, org_id, site_id, remove_phone_home=remove_phone_home)
    if isinstance(config_commands, str):  # If an error message is returned
        return address, config_commands

    # Push configuration to the device
    result = push_config((address, port, username, password), config_commands)
    return result

def main():
    parser = argparse.ArgumentParser(description="Juniper device configuration script")
    parser.add_argument("excel_file", help="Excel file containing device information (org_id, site_id, ip, user_id, password)")
    parser.add_argument("-k", "--keep-phone-home", action="store_true", help="Keep 'delete system phone-home' command in the configuration")
    parser.add_argument("-t", "--max-threads", type=int, default=10, help="Maximum number of concurrent threads (default: 10)")

    args = parser.parse_args()

    # Load settings and initialize site cache
    global settings
    settings = load_settings("settings.json")
    initialize_sites_cache(settings)

    # Load and process the Excel file
    dump_excel_file(args.excel_file)
    try:
        device_data = read_excel(args.excel_file)
    except FileNotFoundError:
        logging.error(f"Cannot open the file '{args.excel_file}'. Please check the file path.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error processing the Excel file: {str(e)}")
        sys.exit(1)

    required_fields = {"organization", "site", "address", "port", "username", "password"}
    if not required_fields.issubset(device_data.columns):
        logging.error(f"Invalid Excel file format. Required fields: {', '.join(required_fields)}")
        sys.exit(1)

    logging.info(f'address:port, hardware model, os name, os version, serial number, host name')

    # Concurrent device processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_threads) as executor:
        futures = [executor.submit(worker, row.to_dict(), not args.keep_phone_home) for _, row in device_data.iterrows()]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Output results
    for result in results:
        if isinstance(result, list) and len(result) == 2:
            pass
            # device_id, message = result
            # logging.info(f"Device {device_id}: {message}")
        else:
            logging.error(f"Unexpected result format: {result}")

if __name__ == "__main__":
    main()
