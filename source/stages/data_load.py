#!/usr/bin/env python
import argparse
import logging
import pathlib
import requests
import yaml
import os
import zipfile
import glob

# Determine the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to params.yaml which is 2 directories up from "here"
params_path = os.path.normpath(
    os.path.join(
        script_dir,
        "..",
        "..",
        "params.yaml"
    )
)

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
raw_save_path = os.path.normpath(
    os.path.join(
        script_dir,
        "..",
        "..",
        config['data_load']['dataset_raw_path']
    )
)
os.makedirs(raw_save_path, exist_ok=True)  # Ensure the directory exists


def download(args):
    # if a download link exists
    if config['data_load']['dataset_url'] or args.file_url:
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
            logger.warning(f"Error processing the URL --> {args.file_url}: {e}")
            logger.error("No dataset file downloaded, stopping the pipeline.")
    else:
        # if no file had to be downloaded, try to unzip an existing file
        if config['data_load']['file_name']:
            try:
                search_pattern = os.path.join(raw_save_path, config['data_load']['file_name'] + ".zip")
                matching_files = glob.glob(search_pattern)
                if len(matching_files) > 1:
                    logger.error((f"found more than 1 file with name {config['data_load']['file_name']}"))
                    raise Exception()
                else:
                    matching_files = matching_files[0] if isinstance(matching_files, list) else matching_files
                    logger.info(f"Found zip file --> {matching_files}")
                unzip(matching_files)

            except Exception as e:
                logger.error(f"Error processing the file --> {args.file_url}: {e} Stopping the pipeline.")
                raise Exception()


def unzip(raw_full_save_path):
    # Check file contents of data/raw directory
    processed_save_path = os.path.join(script_dir, "..", "..", config['data_process']['dataset_proc_path'])
    os.makedirs(processed_save_path, exist_ok=True)  # Ensure the directory exists
    try:
        logger.info(f"Trying to extract.")
        with zipfile.ZipFile(raw_full_save_path, 'r') as zip_ref:
            zip_ref.extractall(processed_save_path)
            logger.info(f"Success")

    except Exception as e:
        logger.error(f"Could not extract the zip file --> {e}")





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
