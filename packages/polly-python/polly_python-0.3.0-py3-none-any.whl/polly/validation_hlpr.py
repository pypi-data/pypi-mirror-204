import os
import copy
import requests
import json
from pathlib import Path
from polly.errors import paramException, error_handler
from tqdm import tqdm

# import pandas as pd
import polly.constants as const
from cryptography.fernet import Fernet
import polly.omixatlas_hlpr as omix_hlpr


def create_status_file(status_dict: dict, metadata_path: str):
    """Creates an encrypted status dict and places it inside
        metadata folder and mark the file hidden
    Args:
        status_dict (dict): Status of the files validated
        metadata_path: Metadata folder path
    """

    # fetch key
    response = requests.get(const.ENCRYPTION_KEY_URL)
    error_handler(response)
    encryption_key = response.text

    # initialize encryption
    f = Fernet(encryption_key)

    modified_status_dict = modify_status_dataset(status_dict, metadata_path)

    # convert dict to string
    status_dict_str = json.dumps(modified_status_dict)

    # string with encoding 'utf-8'
    status_dict_str_bytes = bytes(status_dict_str, "utf-8")

    # encrypt the string
    encrypted_status_str = f.encrypt(status_dict_str_bytes)

    validation_status_file_path = str(
        metadata_path / Path(os.fsdecode(const.VALIDATION_STATUS_FILE_NAME))
    )

    if os.path.isfile(validation_status_file_path):
        # read the file and update -> `r+` mode
        with open(validation_status_file_path, "rb+") as validation_status_file:
            validation_status_file.write(encrypted_status_str)
    else:
        # opening file with `with` block closes the file at the end of with block
        # opening the file in w+ mode allows to both read and write files
        with open(validation_status_file_path, "wb+") as validation_status_file:
            validation_status_file.write(encrypted_status_str)


def modify_status_dataset(status_dataset: dict, metadata_path: str) -> dict:
    """Modify the status dataset to also add the validation level
    Status Dataset Dict contains File Name and Validation Status Right now
    Args:
        status_dataset (dict):status dict of files
        validation_level (str):validation level passed by the user
    Returns
    """
    modified_status_dataset = {}
    metadata_file_list = omix_hlpr.metadata_files_for_upload(metadata_path)
    # metadata_directory = os.fsencode(metadata_path)

    for file in tqdm(metadata_file_list, desc="Generating Status File of Validation"):
        # file = file.decode("utf-8")
        # # skip hidden files and validation status file
        # if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
        file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            dataset_id = res_dict.get("dataset_id")
            if dataset_id in status_dataset:
                modified_status_dataset[dataset_id] = {}
                modified_status_dataset[dataset_id]["file_name"] = file
                # status dataset => {`dataset_id`: `status`}
                modified_status_dataset[dataset_id]["status"] = status_dataset[
                    dataset_id
                ]
    return modified_status_dataset


def construct_combined_metadata_for_validation(source_folder_path: dict) -> dict:
    """Construct Combined Metadata DataStructure
    List of metadata dictionaries grouped together on the basis of validation level
    Validation Lib Takes List of Metadata Dicts and validation level param
    That is the reason the grouping is created
    Args:
        source_folder_path (dict): Source folder path of data and metadata files.
    Returns:
        dict: {
            <validation_level> : [{..metadata dict 1...}, {{..metadata dict 1...},......]
        }
    """
    metadata_path = source_folder_path["metadata"]
    metadata_file_list = omix_hlpr.metadata_files_for_upload(metadata_path)
    combined_metadata_dict_list = {}
    try:
        for file in tqdm(
            metadata_file_list,
            desc="Combined Metadata Files for Validation",
        ):
            # file = file.decode("utf-8")
            # skip hidden files and validation status file
            # if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
            file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
            with open(file_path, "r") as file_to_upload:
                res_dict = json.load(file_to_upload)
                # only put a file for validation
                # if validate is True in the metadata dict
                if (
                    res_dict.get("__index__", {})
                    .get("validation_check", {})
                    .get("dataset", {})
                    .get("validate", "")
                ):
                    # validation level needed for grouping
                    # metadata dicts with same validation level
                    validation_level_val = (
                        res_dict.get("__index__", {})
                        .get("validation_check", {})
                        .get("dataset", {})
                        .get("scope", "")
                    )
                    validate_on_val = compute_validate_on_param(validation_level_val)
                    if validate_on_val in combined_metadata_dict_list:
                        combined_metadata_dict_list.get(validate_on_val).append(
                            res_dict
                        )
                    else:
                        combined_metadata_dict_list[validate_on_val] = []
                        combined_metadata_dict_list.get(validate_on_val).append(
                            res_dict
                        )

        return combined_metadata_dict_list
    except Exception as err:
        raise err


def compute_validate_on_param(validation_level: str) -> str:
    """Compute validate_on param based on validation level
    Args:
        validation_level (str): Passed by the user
    Returns:
        str: returns validation_on parameter
    """
    validation_level_const = copy.deepcopy(const.VALIDATION_LEVEL_CONSTANTS)
    validation_on_val = validation_level_const.get(validation_level, "")
    if not validation_on_val:
        keys = [key for key, val in validation_level_const.items()]
        raise paramException(
            detail=f"Incorrect value of validation_level param. It can be one of {keys}"
        )
    return validation_on_val


def data_metadata_parameter_check(source_folder_path: dict):
    """Sanity Check for Data and Metadata path parameters in source folder path
    Both the data and metadata keys need not be present.
    The data that has to be validated must be present.
    As this function is common for both dataset level and sample level validation
    Passing both data and metadata keys are optional. It is on user to pass
    the relevant data and metadata paths for validation
    Args:
        source_folder_path (dict): dictionary containing data and metadata paths
    """
    if not isinstance(source_folder_path, dict):
        raise paramException(
            title="Param Error", detail="source_folder_paths needs to a dict"
        )

    for key in source_folder_path.keys():
        if key not in const.INGESTION_FILES_PATH_DIR_NAMES:
            raise paramException(
                title="Param Error",
                detail="source_folder_path should be a dict with valid data and"
                + f"metadata path values in the format {const.FILES_PATH_FORMAT} ",
            )
        else:
            data_directory = os.fsencode(source_folder_path[key])
            if not os.path.exists(data_directory):
                raise paramException(
                    title="Param Error",
                    detail="`key` path passed is not found. "
                    + "Please pass the correct path and call the function again",
                )
