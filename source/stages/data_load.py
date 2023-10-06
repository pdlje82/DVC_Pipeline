#!/usr/bin/env python
import argparse
import logging
import pathlib
import requests
import yaml
import os
import zipfile

# Determine the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to params.yaml which is 2 directories up from "here"
params_path = os.path.join(script_dir, "..", "..", "params.yaml")

# Load the parameters from params.yaml
with open(params_path, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

logging.basicConfig(
    level=config['base']['log_level'],
    format="%(asctime)-15s %(message)s"
)
logger = logging.getLogger()

# set where data is saved to
raw_save_path = os.path.join(script_dir, "..", "..", config['data_load']['dataset_raw_path'])
os.makedirs(raw_save_path, exist_ok=True)  # Ensure the directory exists


def download(args):
    try:
        # Derive the base name of the file from the URL
        basename = pathlib.Path(args.file_url).name.split("?")[0].split("#")[0]

        logger.info(f"Downloading {args.file_url} ...")

        raw_full_save_path = os.path.join(raw_save_path, basename)

        logger.info(f"Trying to save {raw_full_save_path}")

        # Download file streaming, so we can download files larger than the available memory.
        with open(raw_full_save_path, 'wb') as fp:
            with requests.get(args.file_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=8192):
                    fp.write(chunk)
            fp.flush()

            logger.info(f"Success downloading {basename} ")

        unzip(raw_full_save_path)

    except Exception as e:
        logger.warning(f"Error processing the URL or none given --> {args.file_url}: {e}")
        logger.info("Skipping the download")

    unzip('')


def unzip(raw_full_save_path):
    # Check file contents of data/raw directory
    try:
        file_name = os.path.basename(raw_full_save_path)
        if os.path.exists(raw_full_save_path) and \
                (zipfile.is_zipfile(raw_full_save_path) or config['data_load']['data_is_zip'] is True):

            logger.info(f"Found zip file, trying to extract {file_name}")

            with zipfile.ZipFile(raw_full_save_path, 'r') as zip_ref:
                zip_ref.extractall(raw_save_path)

            logger.info(f"Success")
        elif os.path.exists(raw_full_save_path) and not zipfile.is_zipfile(raw_full_save_path):
            logger.info(f"{file_name} is not a zip file")

    except Exception as e:
        logger.warning(f"{e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a file save it locally and unzip",
        fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--file_url",
        type=str,
        help="URL to the input file",
        default=config['data_load']['dataset_url'],
        required=False
    )

    parser.add_argument(
        "--artifact_name",
        type=str,
        help="Name for the artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_type",
        type=str,
        help="Type for the artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    download(args)
