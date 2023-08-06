import os
import pathlib
from datetime import datetime, timezone
from os import getcwd

import requests
import yaml

from prowler.lib.logger import logger

timestamp = datetime.today()
timestamp_utc = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
prowler_version = "3.4.0"
html_logo_url = "https://github.com/prowler-cloud/prowler/"
html_logo_img = "https://user-images.githubusercontent.com/3985464/113734260-7ba06900-96fb-11eb-82bc-d4f68a1e2710.png"

orange_color = "\033[38;5;208m"
banner_color = "\033[1;92m"

# Compliance
actual_directory = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
compliance_aws_dir = f"{actual_directory}/../compliance/aws"
available_compliance_frameworks = []
with os.scandir(compliance_aws_dir) as files:
    files = [
        file.name
        for file in files
        if file.is_file()
        and file.name.endswith(".json")
        and available_compliance_frameworks.append(file.name.removesuffix(".json"))
    ]

# AWS services-regions matrix json
aws_services_json_file = "aws_regions_by_service.json"

# gcp_zones_json_file = "gcp_zones.json"

default_output_directory = getcwd() + "/output"

output_file_timestamp = timestamp.strftime("%Y%m%d%H%M%S")
timestamp_iso = timestamp.isoformat(sep=" ", timespec="seconds")
csv_file_suffix = ".csv"
json_file_suffix = ".json"
json_asff_file_suffix = ".asff.json"
html_file_suffix = ".html"
config_yaml = f"{pathlib.Path(os.path.dirname(os.path.realpath(__file__)))}/config.yaml"


def check_current_version(prowler_version):
    try:
        release_response = requests.get(
            "https://api.github.com/repos/prowler-cloud/prowler/tags"
        )
        latest_version = release_response.json()[0]["name"]
        if latest_version != prowler_version:
            return f"(latest is {latest_version}, upgrade for the latest features)"
        else:
            return "(it is the latest version, yay!)"
    except Exception as e:
        print(e)
        return ""


def change_config_var(variable, value):
    try:
        with open(config_yaml) as f:
            doc = yaml.safe_load(f)

        doc[variable] = value

        with open(config_yaml, "w") as f:
            yaml.dump(doc, f)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}: {error}")


def get_config_var(variable):
    try:
        with open(config_yaml) as f:
            doc = yaml.safe_load(f)

        return doc[variable]
    except Exception as error:
        logger.error(f"{error.__class__.__name__}: {error}")
        return ""
