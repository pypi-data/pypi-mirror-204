import os
import copy
from functools import lru_cache
import requests
import pathlib
import json
from tabulate import tabulate
import warnings
from pathlib import Path
from polly.errors import (
    paramException,
    extract_error_message_details,
    UnauthorizedException,
    EmptyPayloadException,
    InvalidSchemaJsonException,
    InvalidSyntaxForRequestException,
)

import pandas as pd
import polly.constants as const
from cryptography.fernet import Fernet
from polly.errors import error_handler, ValidationError
import polly.helpers as helpers
import polly.http_response_codes as http_codes
from polly import application_error_info as app_err_info

dataset_level_metadata_files_not_uploaded = []
data_files_whose_metadata_failed_validation = []


def reset_global_variables_with_validation_results():
    """
    Reset Global variables storing value to default after
    add and update datasets are complete
    """
    global dataset_level_metadata_files_not_uploaded
    dataset_level_metadata_files_not_uploaded = []

    global data_files_whose_metadata_failed_validation
    data_files_whose_metadata_failed_validation = []


def parameter_check_for_repo_id(repo_id):
    """Checking for validity of repo id
    Args:
        repo_id (): Repository Id of omixatlas

    Raises:
        paramException: Error if repo id is empty or is not str or int
    """
    if not repo_id:
        raise paramException(
            title="Param Error",
            detail="repo_id should not be empty",
        )
    elif type(repo_id) != str and type(repo_id) != int:
        raise paramException(
            title="Param Error",
            detail=f"repo_id, {repo_id} should be str or int",
        )


def make_repo_id_string(repo_id: int) -> str:
    """If repo id is int, change to string

    Args:
        repo_id (int/str): repo_id of the omixatlas

    Returns:
        str: return repo_id as string
    """
    if isinstance(repo_id, int):
        repo_id = str(repo_id)
    return repo_id


def schema_param_check(repo_key: str, body: dict):
    """Do sanity checks for the parameters passed in schema functions

    Args:
        repo_key (str): _description_
        body (dict): _description_
    Raises:
        paramError: In case of any issue with the parameter
    """
    try:
        if not body or not isinstance(body, dict):
            raise paramException(
                title="Param Error",
                detail="body should not be empty and it should be of type dict",
            )
        parameter_check_for_repo_id(repo_key)
    except Exception as err:
        raise err


def create_move_data_payload(
    payload_datasets: list, src_repo_key: str, dest_repo_key: str, priority: str
) -> dict:
    """_summary_

    Args:
        payload_datasets (list): _description_
        src_repo_key (str): _description_
        dest_repo_key (str): _description_
        priority (str): _description_
    Returns:
        Dict : Dictionary of the move data payload
    """
    move_data_payload = {}
    move_data_payload["data"] = {}
    move_data_payload["data"]["type"] = "ingestion-transaction"
    move_data_payload["data"]["attributes"] = {}
    move_data_payload["data"]["attributes"]["datasets"] = payload_datasets
    move_data_payload["data"]["attributes"]["source_repo_id"] = src_repo_key
    move_data_payload["data"]["attributes"]["destination_repo_id"] = dest_repo_key
    move_data_payload["data"]["attributes"]["priority"] = priority
    move_data_payload["data"]["attributes"]["flags"] = {}
    move_data_payload["data"]["attributes"]["flags"]["file_metadata"] = "true"
    move_data_payload["data"]["attributes"]["flags"]["col_metadata"] = "true"
    move_data_payload["data"]["attributes"]["flags"]["row_metadata"] = "true"
    move_data_payload["data"]["attributes"]["flags"]["data_required"] = "true"
    return move_data_payload


def update_dataset_parameter_check(source_folder_path: dict):
    """Check update dataset parameter check

    Args:
        source_folder_path (dict): _description_

    Raise:
        Param Exception: In case parameters not as per requirement
    """
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
                    detail=f"{key} path passed is not found. "
                    + "Please pass the correct path and call the function again",
                )


# TODO: Make it Similar to update_dataset_parameter_check
# where there is loop on source_folder_path.keys()
# In this way, keys to pick from source_folder_path will be picked
# from the looping variable
# Use the set substraction functionality to figure out which data or metadata path is missing
# or is there additional key present in source_folder_path
# Ex - https://github.com/ElucidataInc/polly-python-code/pull/257/files#r1048116264
# check the above link
def add_dataset_parameter_check(source_folder_path: dict):
    """Check update dataset parameter check

    Args:
        source_folder_path (dict): _description_

    Raise:
        Param Exception: In case parameters not as per requirement
    """
    # check that both data and metadata keys are present or not
    # as the keys in the dict are unique. Converting it into set will not
    # delete any keys
    # doing set comparison to check for equality
    if set(source_folder_path.keys()) == set(const.INGESTION_FILES_PATH_DIR_NAMES):
        # checking if data path passed exists or not
        data_directory = os.fsencode(source_folder_path["data"])
        if not os.path.exists(data_directory):
            raise paramException(
                title="Param Error",
                detail="`data` path passed is not found. "
                + "Please pass the correct path and call the function again",
            )
        # checking if metadata passed path exists or not
        metadadata_directory = os.fsencode(source_folder_path["metadata"])
        if not os.path.exists(metadadata_directory):
            raise paramException(
                title="Param Error",
                detail="`metadata` path passed is not found. Please pass the correct path and call the function again",
            )
    else:
        # if any of the metadata or data keys or both keys are not present
        if "data" not in source_folder_path:
            raise paramException(
                title="Param Error",
                detail=f"{source_folder_path} does not have `data` path."
                + f" Format the source_folder_path_dict like this  {const.FILES_PATH_FORMAT}",
            )
        if "metadata" not in source_folder_path:
            raise paramException(
                title="Param Error",
                detail=f"{source_folder_path} does not have `metadata` path. "
                + f"Format the source_folder_path_dict like this  {const.FILES_PATH_FORMAT}",
            )


def data_metadata_parameter_check(source_folder_path: dict, update=False):
    """
    Sanity check for data and metadata path parameters.
    This is done for both add and update functions
    In Update
    => No need to have both data and metadata file paths. Only 1 is sufficient.
    => This is because either data or metadata files can also be updated.
    In Add
    => Both file paths, data and metadata are required.
    => As file is getting ingested for the first time, both files are needed.
    """
    try:
        if not source_folder_path or not isinstance(source_folder_path, dict):
            raise paramException(
                title="Param Error",
                detail="source_folder_path should be a dict with valid data and"
                + f" metadata path values in the format {const.FILES_PATH_FORMAT} ",
            )
        if update:
            update_dataset_parameter_check(source_folder_path)
        else:
            add_dataset_parameter_check(source_folder_path)
    except Exception as err:
        raise err


def check_for_single_word_multi_word_extension(
    data_file_list: list, data_file_format_constants: list
):
    """iterate the data directory and check for different types of extensions
    in data files

    Args:
        data_directory (list): dataset files directory
        data_file_format_constants (list): List of approved formats
    """
    for file in data_file_list:
        file_ext = pathlib.Path(file).suffixes
        if len(file_ext) == 0:
            # file without extension
            raise paramException(
                title="Param Error",
                detail=f"File format for file {file} is not available"
                + f"It can be => {data_file_format_constants}",
            )
        elif len(file_ext) == 1:
            # file with single word extension
            file_ext_single_word = file_ext[-1]
            if file_ext_single_word not in data_file_format_constants:
                raise paramException(
                    title="Param Error",
                    detail=f"File format for file {file} is invalid."
                    + f"It can be => {data_file_format_constants}",
                )
        elif len(file_ext) > 1:
            # file with multi word extension
            # or `.`'s present in file name
            # check for multiword extensions
            compression_type_check = file_ext[-1]

            # compression types
            compression_types = copy.deepcopy(const.COMPRESSION_TYPES)
            # concatenating 2nd last and last word together to check
            # for multiword extension
            # pathlib.Path('my/library.tar.gar').suffixes
            # ['.tar', '.gz']
            file_type_multi_word = file_ext[-2] + file_ext[-1]
            if (compression_type_check in compression_types) and (
                file_type_multi_word in data_file_format_constants
            ):
                # multi word extension
                continue
            elif file_ext[-1] in data_file_format_constants:
                # single word extension with `.`'s in file which is accepted
                continue
            elif file_ext[-1] not in data_file_format_constants:
                raise paramException(
                    title="Param Error",
                    detail=f"File format for file {file} is invalid."
                    + f"It can be => {data_file_format_constants}",
                )


def data_files_for_upload(data_source_folder_path: str) -> list:
    """Gives the list of data files for upload

    Args:
        data_source_path (str): folder path containing all the data files

    Returns:
        list: List of data files for upload
    """
    data_directory = os.fsencode(data_source_folder_path)
    data_files_list = []
    for file in os.listdir(data_directory):
        file = file.decode("utf-8")
        # skip hidden files
        if not file.startswith("."):
            data_files_list.append(file)
    return data_files_list


def get_file_format_constants() -> dict:
    """
    Returns file format info from public assests url
    """
    response = copy.deepcopy(const.FILE_FORMAT_CONSTANTS)
    return response


def data_metadata_file_ext_check(source_folder_path: dict):
    """
    Check extension for data and metadata file names
    """
    format_constants = get_file_format_constants()
    data_file_format_constants = format_constants.get("data")
    data_source_folder_path = source_folder_path.get("data", "")

    if data_source_folder_path:
        data_file_list = data_files_for_upload(data_source_folder_path)
        try:
            check_for_single_word_multi_word_extension(
                data_file_list, data_file_format_constants
            )
        except Exception as err:
            raise err

    metadata_file_format_constants = format_constants["metadata"]
    metadata_source_folder_path = source_folder_path.get("metadata", "")
    if metadata_source_folder_path:
        metadata_file_list = metadata_files_for_upload(metadata_source_folder_path)
        for file in metadata_file_list:
            file_ext = pathlib.Path(file).suffixes
            file_ext_single_word = file_ext[-1]
            if file_ext_single_word not in metadata_file_format_constants:
                raise paramException(
                    title="Param Error",
                    detail=f"File format for file {file} is invalid."
                    + f"It can be => {metadata_file_format_constants}",
                )


def get_data_path_from_source_folder_path(source_folder_path: dict):
    """Get data path from source_folder_path
    Args : source_folder_path: (dict)
    """
    data_source_folder_path = source_folder_path.get("data", "")
    return data_source_folder_path


def get_metadata_path_from_source_folder_path(source_folder_path: dict):
    """Get metadata path from source_folder_path

    Args:
        source_folder_path (dict): _description_
    """
    metadata_source_folder_path = source_folder_path.get("metadata", "")
    return metadata_source_folder_path


def check_data_metadata_file_path(source_folder_path: dict):
    """
    Check Metadata and Data files folders to test for empty case.
    in case of update, data/metadata folders are optional.
    Only if present in the source_folder_path dict and is a directory, empty case checked.
    """
    data_source_folder_path = source_folder_path.get("data", "")
    metadata_source_folder_path = source_folder_path.get("metadata", "")

    if data_source_folder_path:
        if not os.path.isdir(data_source_folder_path):
            raise paramException(
                title="Param Error",
                detail=f"{data_source_folder_path} is not a folder path. "
                + "Please pass a folder path containing data files. ",
            )

        data_directory = os.fsencode(data_source_folder_path)

        if not os.listdir(data_directory):
            raise paramException(
                title="Param Error",
                detail=f"{data_source_folder_path} does not contain any datafiles. "
                + "Please add the relevant data files and try again",
            )
    if metadata_source_folder_path:
        if not os.path.isdir(metadata_source_folder_path):
            raise paramException(
                title="Param Error",
                detail=f"{data_source_folder_path} is not a folder path. "
                + "Please pass a folder path containing metadata files. ",
            )

        metadata_directory = os.fsencode(metadata_source_folder_path)

        if not os.listdir(metadata_directory):
            raise paramException(
                title="Param Error",
                detail=f"{metadata_source_folder_path} does not contain any metadatafiles. "
                + "Please add the relevant metadata files and try again",
            )


def group_passed_and_failed_validation(validation_dataset_lvl: dict) -> dict:
    """Group Dataset Level Metadata Files who have passed and who have failed validation

    Args:
        validation_dataset_lvl (dict): validation status of metadata file
    Returns:
        Dict -> containing two sets of files
        validation_passed_metadata_files: Metadata Files Passed Validation
        validation_failed_metadata_files: Metadata Files failed Validation
    """
    validation_dataset_lvl_grouped = {}
    validation_dataset_lvl_grouped["passed"] = []
    validation_dataset_lvl_grouped["failed"] = []
    for dataset_id, status_val_dict in validation_dataset_lvl.items():
        if status_val_dict["status"]:
            validation_dataset_lvl_grouped["passed"].append(
                status_val_dict["file_name"]
            )
        else:
            validation_dataset_lvl_grouped["failed"].append(
                status_val_dict["file_name"]
            )

    if validation_dataset_lvl_grouped["failed"]:
        print("\n")
        failed_validation_files = validation_dataset_lvl_grouped["failed"]
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
        warnings.warn(
            f"These {failed_validation_files} file have failed validation. "
            + "These files will only be ingested if force_ingest key in metadata is set to True"
        )
    return validation_dataset_lvl_grouped


def apply_validation_on_metadata_files(
    metadata_file_list: list,
    metadata_path: str,
    validation_dataset_lvl_grouped: dict,
) -> list:
    """Apply Validation on Metadata Files
    Rules
    => The Files which have passed validation would included in final list
    => Files which have failed validation, if `force_ingest` flag for them is true
    Then they will be included in the final list

    Args:
        metadata_file_list (list): List of all the metadata Files

    Returns:
        list: Returns the list metadata files which will be uploaded
    """
    final_metadata_file_list = []
    for file in metadata_file_list:
        file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            # checking if validate key is true or not in metadata
            # if validate key is true then the file name
            # should be in valid_dataset_level_files
            # If the file name is not in valid_dataset_level_files
            # then it should be have `force_ingest` set to true
            # if the both the conditions are False
            # Then the file will not be ingested
            validate_param = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("validate", "")
            )
            force_ingest = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("force_ingest", "")
            )
            if (
                validate_param
                and file in validation_dataset_lvl_grouped["failed"]
                and not force_ingest
            ):
                # skip this file for ingesting
                # if force ingest not true then file will be skipped
                continue
            else:
                # if validate_param == true and file not in valid_dataset_id and force_ingest == True
                # if validate_param == true and file in valid_dataset_id
                # if validate_param == false
                # In all these cases continue the ingestion process

                # pop out the file from invalid_dataset_level_files
                if file in validation_dataset_lvl_grouped["failed"] and force_ingest:
                    # this file has has not passed validation
                    # but it is force ingested by the user
                    validation_dataset_lvl_grouped["failed"].remove(file)

                # append the files which will be uploaded
                final_metadata_file_list.append(file)

    global dataset_level_metadata_files_not_uploaded

    dataset_level_metadata_files_not_uploaded = validation_dataset_lvl_grouped["failed"]
    return final_metadata_file_list


def filter_data_files_whose_metadata_not_uploaded(
    data_files_list: list, data_metadata_mapping: dict
) -> list:
    """Filter Data Files whose metadata Not Valid

    Args:
        data_files_list (list): all the data files

    Returns:
        list: list of data files which can be uploaded
    """

    # this means no metadata files were given by user
    # no mapping dict generated
    if not data_metadata_mapping:
        return data_files_list

    # used to filter data files as metadata and data file names same
    not_uploaded_metadata_file_names = []

    # construct a list with metadata file names without extension
    for metadata_file in dataset_level_metadata_files_not_uploaded:
        metadata_file_name = pathlib.Path(metadata_file).stem
        not_uploaded_metadata_file_names.append(metadata_file_name)

    dataset_whose_metadata_not_valid = []

    # construct list of dataset files whose metadata is not valid
    for metadata_file_name in not_uploaded_metadata_file_names:
        data_file_name = data_metadata_mapping[metadata_file_name]
        dataset_whose_metadata_not_valid.append(data_file_name)

    global data_files_whose_metadata_failed_validation
    data_files_whose_metadata_failed_validation = dataset_whose_metadata_not_valid
    final_data_files_list = []

    for file in data_files_list:
        if file not in dataset_whose_metadata_not_valid:
            final_data_files_list.append(file)

    return final_data_files_list


def create_file_name_with_extension_list(file_names: list, file_ext_req=True) -> list:
    """Decode the file name in bytes to str

    Args:
        data_file_names (list): data file name in bytes
    Returns:
        list: data file names in str
    """
    file_names_str = []
    # convert file names from bytes to strings
    # file name is kept with extension here
    for file in file_names:
        file = file.decode("utf-8")
        if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
            if not file_ext_req:
                file = pathlib.Path(file).stem
            file_names_str.append(file)
    return file_names_str


def data_metadata_file_dict(
    metadata_file_names_str: list, data_file_names_str: list
) -> list:
    """Construct data metadata file name dict and also return list of files which are unmapped
    Convention Followed in naming -> Metadata and Data File Name -> Will always be same
    Extension will be different -> Name always same

    Args:
        metadata_file_names_str (list): List of all metadata file names
        data_file_names_str (list): list of all data file names with extensions

    Returns:
        list: Returns list of mapped and unmapped files
    """
    # metadata file name -> key, data file name with extension -> value
    data_metadata_mapping_dict = {}
    unmapped_file_names = []
    for data_file in data_file_names_str:
        data_file_name = get_file_name_without_suffixes(data_file)
        # check for matching data and metadata file name
        # convention for the system to know data and metadata mapping
        # also removing the metadata file from the list
        # which maps to data file
        # so as to return the unmapped metadata files at last if any
        if data_file_name in metadata_file_names_str:
            data_metadata_mapping_dict[data_file_name] = data_file
            metadata_file_names_str.remove(data_file_name)
        else:
            unmapped_file_names.append(data_file_name)
    return data_metadata_mapping_dict, unmapped_file_names, metadata_file_names_str


def data_metadata_file_mapping_conditions(
    unmapped_data_file_names: list,
    unmapped_metadata_file_names: list,
    data_metadata_mapping_dict: dict,
) -> dict:
    """Different conditions to check for data metadata mapping

    Args:
        unmapped_file_names (list): data file names which are not mapped
        metadata_file_names_str (list): metadata file names list
        data_metadata_mapping_dict (dict): dict of data metadata mapping

    Returns:
        dict: data_metadata mapping dict if conditions succeed
    """
    # data and metadata file names are unmapped
    if len(unmapped_data_file_names) > 0 and len(unmapped_metadata_file_names) > 0:
        raise paramException(
            title="Missing files",
            detail=f" No metadata for these data files {unmapped_data_file_names}. "
            + f"No data for these metadata files {unmapped_metadata_file_names}. "
            + "Please add the relevant files or remove them.",
        )
    elif len(unmapped_data_file_names) > 0:
        raise paramException(
            title="Missing files",
            detail=f" No metadata for these data files {unmapped_data_file_names}"
            + ". Please add the relevant files or remove them.",
        )
    elif len(unmapped_metadata_file_names) > 0:
        raise paramException(
            title="Missing files",
            detail=f"No data for these metadata files {unmapped_metadata_file_names}"
            + ". Please add the relevant files or remove them.",
        )
    else:
        return data_metadata_mapping_dict


def get_file_name_without_suffixes(data_file: str) -> str:
    """
    Returns just the file name without the suffixes.
    This functionality is written according to the rules of data file naming
    i) Data Files can have single extension
    ii) Data Files can have multiple extension
        => Multiword Extensions only possible if
        => Data file name has one main extension and one compressed extension
        => Examples are -> `.gct.bz`, `.h5ad.zip`
    iii) Data Files can have `.`'s in the names
    """
    file_format = get_file_format_constants()
    file_format_data = file_format.get("data", [])
    file_ext = pathlib.Path(data_file).suffixes
    if len(file_ext) == 1:
        # single word extension
        data_file_name = pathlib.Path(data_file).stem
    elif len(file_ext) > 1:
        # Either file with multi word extension
        # or `.`'s present in file name
        # check for multiword extensions
        compression_type_check = file_ext[-1]

        # compression types
        compression_types = copy.deepcopy(const.COMPRESSION_TYPES)
        # concatenating 2nd last and last word together to check
        # for multiword extension
        # pathlib.Path('my/library.tar.gz').suffixes
        # ['.tar', '.gz']

        if compression_type_check in compression_types:
            # multi word extension case
            # data_file -> file name with extension and compression format
            # file name with extension attached with `.`
            file_name_with_extension = pathlib.Path(data_file).stem

            # check if file_name_with_extension has an extension or is it a name
            # for ex
            # Case 1 => abc.gct.bz => after compression ext split
            # abc.gct => .gct => valid supported extension
            # Case 2 => abc.tar.gz => after compression ext split
            # abc.tar => .tar => valid compression type
            # Case 3 => abc.bcd.gz => Only zip as extension, no other extension

            file_main_ext = pathlib.Path(file_name_with_extension).suffix
            if file_main_ext in file_format_data:
                # file name
                data_file_name = pathlib.Path(file_name_with_extension).stem
            elif file_main_ext in compression_types:
                # second compression type
                data_file_name = pathlib.Path(file_name_with_extension).stem
            else:
                data_file_name = file_name_with_extension
        else:
            # single word extension with `.`'s in file which is accepted
            data_file_name = pathlib.Path(data_file).stem
    elif len(file_ext) == 0:
        # this case will never arise when we are passing files from add or
        # update function i.e. data and metadata files
        # Because this check is applied in the parameter check

        # this case will arise if somebody has ingested a file without extension
        # through quilt. In that case while we are updating either data or
        # metadata files in the repo, we are fetching all the files of that repo
        # there a file can exist which does not have extension, for that edgecase
        # this check is helpful
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
        warnings.warn(
            f"{data_file}"
            + " does not have an extension. "
            + "This file is invalid. Please delete this file. "
            + "For any questions, please reach out to polly.support@elucidata.io."
        )
        data_file_name = ""
    return data_file_name


def parameter_check_for_priority(priority: str):
    if not isinstance(priority, str) or priority not in ["low", "medium", "high"]:
        raise paramException(
            title="Param Error",
            detail="`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`",
        )


def move_data_params_check(
    src_repo_key: str, dest_repo_key: str, dataset_ids: list, priority: str
):
    """Check move data params

    Args:
        src_repo_key (str/int): source repo id
        dest_repo_key (str/int): destination repo id
        dataset_ids (list): List of dataset ids
        priority (str): priority of the operation
    """
    try:
        parameter_check_for_repo_id(src_repo_key)
        parameter_check_for_repo_id(dest_repo_key)
        parameter_check_for_priority(priority)
        if not dataset_ids or not isinstance(dataset_ids, list):
            raise paramException(
                title="param error",
                detail="dataset_ids should not be empty and dataset_ids should be in list format.",
            )
    except Exception as err:
        raise err


def metadata_files_for_upload(source_metadata_path: str) -> list:
    """Find List of all the metadata files to be uploaded

    Args:
        repo_id (str): Repo Id of the OmixAtlas
        source_metadata_path (str): metadata path for the files
        data_metadata_mapping (dict): dictionary containing the data metadata mapping

    Returns:
        list: List of metadata files to be uploaded
    """
    metadata_directory = os.fsencode(source_metadata_path)
    metadata_file_list = []
    for file in os.listdir(metadata_directory):
        file = file.decode("utf-8")
        # skip hidden files
        # skip the validation_status.json
        if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
            metadata_file_list.append(file)
    return metadata_file_list


def check_all_files_validated(
    metadata_file_list: str, decrypted_status_data_dict: dict, metadata_folder_path
):
    """
        Check if the files which have `validate: True` are validated or not
        Check the files which are to be validated, have entry in decrypted_status_data_dict
    Args:
        metadata_file_list(list): list of metadata files to be checked
        metadata_folder_path (str): Folder path for metadata file
        decrypted_status_data_dict (dict): status dict containing status of all validated files
    """
    for file in metadata_file_list:
        file_path = str(Path(metadata_folder_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            validate_param = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("validate", "")
            )

            # dataset id represents metadata file entry in status dict
            # if validate is true
            # the dataset id of res_dict
            # should exist in status dict
            # if dataset_id does not exist in status dict
            # that means the file has not been validated
            dataset_id = res_dict.get("dataset_id", "")
            if not dataset_id:
                raise Exception(f"Dataset Id not present in metadata file {file}")
            if validate_param and dataset_id not in decrypted_status_data_dict:
                raise Exception(
                    f"This {file} has validate set to True but not validated"
                )


def check_validation_false_in_all_files(
    metadata_file_list: list, metadata_folder_path: str
) -> dict:
    """Check if all the files have validation status False

    Args:
        metadata_file_list (list): List of all metadata files to be checked
    """

    # first check if all the `validate:False` or not
    # if every file has `validate:False` then every file has bypassed validation
    # in that case `validation_status` file is not needed
    # But if any file has `validate:True` and validation status is not there
    # This means the files have not gone through validation step

    for file in metadata_file_list:
        file_path = str(Path(metadata_folder_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            validate_param = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("validate", "")
            )

            if validate_param:
                # for this file `validate:True`
                # this means file has not gone through validation
                # raise error
                raise ValidationError(
                    f"Metadata File {file} have not been validated and `validate` is set to True. "
                    + "Please run the validation step first."
                )

    # return empty dictionary
    # no status data present
    # no error is raised
    return {}


def initialize_fernet_encryption():
    """Initialize Fernet Encryption"""
    # fetch key
    response = requests.get(const.ENCRYPTION_KEY_URL)
    error_handler(response)
    encryption_key = response.text
    # initialize decryption
    f = Fernet(encryption_key)
    return f


def check_status_file(source_folder_path: dict):
    """Check if status file is present or not
    If Present
    => Return Status Dict If files that have validation True are Validated
    => If all files that have validation true are not validated then raise error

    If not present
    => Check if all files have validation false
    => IF not then raise error
    Args:
        source_folder_path (dict): Source Folder Path containing data & metadata paths
    """
    metadata_folder_path = source_folder_path.get("metadata", "")
    encrypted_status_data = ""

    status_file_path = f"{metadata_folder_path}/{const.VALIDATION_STATUS_FILE_NAME}"
    # check if this path exists
    # if path exists then save the status data in encrypted_status_data
    if os.path.isfile(status_file_path):
        status_file_path = str(
            Path(metadata_folder_path)
            / Path(os.fsdecode(const.VALIDATION_STATUS_FILE_NAME))
        )
        with open(status_file_path, "rb") as encrypted_file:
            encrypted_status_data = encrypted_file.read()

    try:
        metadata_file_list = metadata_files_for_upload(metadata_folder_path)
        # if status file not present
        if not encrypted_status_data:
            empty_status_dict = check_validation_false_in_all_files(
                metadata_file_list, metadata_folder_path
            )
            return empty_status_dict
        elif encrypted_status_data:
            # decrypt status file
            f = initialize_fernet_encryption()
            decrypted_status_data = f.decrypt(encrypted_status_data)
            decrypted_status_data_dict = json.loads(decrypted_status_data)

            # check if all the files which have `validate:True` is validated or not
            # i.e. their entry is present in status dict or not
            check_all_files_validated(
                metadata_file_list, decrypted_status_data_dict, metadata_folder_path
            )
            return decrypted_status_data_dict
    except Exception as err:
        raise err


def check_create_omixatlas_parameters(
    display_name: str,
    description: str,
    repo_name: str,
    image_url: str,
    components: list,
    category: str,
    data_type: str,
    org_id: str,
):
    """Sanity check for Parameters passed in Create Method
    Args:
        display_name (str): Display name of the Omixatlas
        description (str): Description of the Omixatlas
        repo_name (str): proposed repo name for the omixatlas
        image_url (str): image url provided for the icon for the omixatlas
        components (list): components to be added in the omixatlas
        category (str): category definition of the omixatlas
        data_type(str): datatype of the omixatlas. By default it is None
        org_id(str): org id of the Organisation. By default it is empty
    """
    try:
        str_params = [display_name, description, repo_name, image_url]
        for param in str_params:
            if not isinstance(param, str):
                raise paramException(
                    title="Param Error", detail=f"{param} should be a string"
                )
        check_components_parameter(components)

        if not isinstance(category, str) or (
            category not in const.OMIXATLAS_CATEGORY_VALS
        ):
            raise paramException(
                title="Param Error",
                detail=f"category should be a string and its value must be one of {const.OMIXATLAS_CATEGORY_VALS}",
            )
        check_org_id(org_id)
        check_data_type_parameter(data_type)
    except Exception as err:
        raise err


def check_org_id(org_id: str):
    """Sanity check for org id

    Args:
        org_id (str): org id of the Organisation. By default it is empty
    """
    if org_id:
        if not isinstance(org_id, str):
            raise paramException(
                title="Param Error",
                detail="org id should be a string.",
            )


def check_data_type_parameter(data_type: str):
    """Check for data type parameter

    Args:
        data_type (str): datatype of the omixatlas. By default it is None
    """
    if data_type:
        if not isinstance(data_type, str) or (
            data_type not in const.OMIXATLAS_DATA_TYPE_VALS
        ):
            raise paramException(
                title="Param Error",
                detail=(
                    "data_type should be a string and its value must be one of "
                    + f"{const.OMIXATLAS_DATA_TYPE_VALS}"
                ),
            )


def check_components_parameter(components: list):
    """Check components parameter

    Args:
        components (list): components to be added in the omixatlas
    """
    if not isinstance(components, list):
        raise paramException(
            title="Param Error", detail=f"{components} should be a list"
        )


def check_update_omixatlas_parameters(
    display_name: str,
    description: str,
    repo_key: str,
    image_url: str,
    components: list,
    workspace_id: str,
):
    """Sanity check for Parameters passed in Update Method
    Args:
        display_name (str): Display name of the Omixatlas
        description (str): Description of the Omixatlas
        repo_name (str): proposed repo name for the omixatlas
        image_url (str): image url provided for the icon for the omixatlas
        components (list): components to be added in the omixatlas
        workspace_id (str): ID of the Workspace to be linked to the Omixatlas.
        data_type(str): datatype of the omixatlas. By default it is None
    """
    try:
        parameter_check_for_repo_id(repo_key)
        # this can be refactored using args -> just passing **args into the function
        # have a discussion on this
        if (
            not display_name
            and not description
            and not image_url
            and not components
            and not workspace_id
        ):
            raise paramException(
                title="Param Error",
                detail=(
                    "No parameters passed to update, please pass at least one of the following"
                    + " params [display_name, description, image_url, components, workspace_id, data_type]."
                ),
            )

        str_params = [display_name, description, image_url, workspace_id]
        for param in str_params:
            if not isinstance(param, str):
                raise paramException(
                    title="Param Error", detail=f"{param} should be a string"
                )
        check_components_parameter(components)
    except Exception as err:
        raise err


def verify_repo_identifier(repo_identifier: str):
    """Verify if the repository_idenfier is repo_id for a repo

    Args:
        repo_identifier (str): Identifier of a repo
    """
    if not repo_identifier.isdigit():
        raise paramException(
            title="Param Error",
            detail="Value of repo_id key in the schema payload dict is not valid repo_id. "
            + "repo_id should contain digits only. Please correct it.",
        )


def compare_repo_id_and_id(repo_id: str, id: str):
    """Repo id in the schema payload and the payload identifier(id) should be same
    id is the payload identifier as per JSON schema spec conventions.

    Args:
        repo_id (str): repo_id of the repo
        id (str): payload identifier of the schema payload
    """
    if repo_id != id:
        raise paramException(
            title="Param Error",
            detail="Value of repo_id key and id key is not same in the payload. "
            + "Please correct it. ",
        )


def extract_error_message(error_msg) -> str:
    """
    Extract error message from the error
    """
    error_msg = json.loads(error_msg)
    error = error_msg.get("error")
    if error is None:
        error = error_msg.get("errors")[0]
    if "detail" in error:
        detail = error.get("detail")

    return detail


def dataset_id_type_check_in_delete_datasets(dataset_ids: list):
    """Dataset Id type check in delete datasets

    Args:
        dataset_id (list): dataset ids list
    """
    if not (dataset_ids and isinstance(dataset_ids, list)):
        raise paramException(
            title="Param Error",
            detail="dataset_ids should be list of strings",
        )


def dataset_file_path_dict_type_check_in_delete_datasets(dataset_file_path_dict: dict):
    """dataset_file_path_dict type check in delete datasets

    Args:
        dataset_file_path_dict (dict): dict of dataset_file_path_dict
    """
    if not isinstance(dataset_file_path_dict, dict):
        raise paramException(
            title="Param Error",
            detail=(
                "dataset_file_path_dict should be dict -> {<dataset_id>:<list_of_paths>}",
            ),
        )

    for key, val in dataset_file_path_dict.items():
        if not isinstance(val, list):
            raise paramException(
                title="File paths datatype is incorrect",
                detail=(
                    "File paths should be in the format of list of strings in the "
                    + "dataset_file_path_dict. Correct format -> {<dataset_id>:<list_of_paths>}"
                ),
            )
        if not isinstance(key, str):
            raise paramException(
                title="dataset_id datatype is incorrect",
                detail=(
                    "dataset_id should be in the format of string in the "
                    + "dataset_file_path_dict. Correct format -> {<dataset_id>:<list_of_paths>}"
                ),
            )


def parameter_check_for_delete_dataset(
    repo_id: int, dataset_ids: list, dataset_file_path_dict: dict
):
    """
    Sanity check for all the parameters of delete datasets
    """
    try:
        parameter_check_for_repo_id(repo_id)
        dataset_id_type_check_in_delete_datasets(dataset_ids)
        dataset_file_path_dict_type_check_in_delete_datasets(dataset_file_path_dict)
    except Exception as err:
        raise err


def dataset_file_path_is_subset_dataset_id(
    dataset_ids: list, dataset_file_path_dict: dict
):
    """Check if all the keys of dataset_file_path_dict which represents dataset id
    are present in dataset_ids list or not
    Ideally all the dataset id present as key in dataset_file_path_dict should be mandatorily
    present in the dataset_ids list
    i.e. All the keys of dataset_file_path_dict should be a subset of dataset_ids list
    The function is to check the subset validity

    Args:
        dataset_ids (list): List of dataset ids
        dataset_file_path_dict (dict): Dictionary containing dataset ids and file paths
        corresponding to it

    Raises:
        paramError: If Params are not passed in the desired format or value not valid.

    """
    dataset_file_path_dict_keys = dataset_file_path_dict.keys()

    # converting both the lists and checking for the error case
    # Error Case -> dataset_file_path_dict_keys list not a subset of dataset_ids list
    # in that case raise warnings for those dataset_ids
    # which are a part of dataset_file_path_dict but not dataset_ids
    # For Example
    # a = [1, 3, 5]
    # b = [1, 3, 5, 8]
    # set(a) <= set(b)
    # ANS -> TRUE
    if not set(dataset_file_path_dict_keys) <= set(dataset_ids):
        # find the difference of elements present in dataset_file_path_dict_keys list
        # that are not present in dataset_ids list
        # Example ->
        # list_1 = ['a', 'b', 'c']
        # list_2 = ['a', 'd', 'e']
        # result_1 = list(set(list_2).difference(list_1))
        # print(result_1)  # 👉️ ['e', 'd']
        invalid_dataset_ids = list(
            set(dataset_file_path_dict_keys).difference(dataset_ids)
        )
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
        warnings.warn(
            f"Unable to delete these dataset_ids {invalid_dataset_ids} because "
            + "these are not present in dataset_ids list. "
            + "For any questions, please reach out to polly.support@elucidata.io. "
        )
        # break line added -> for better UX
        print("\n")


# cached for the cases when this function is called internally when same
# result is needed multiple times
@lru_cache(maxsize=None)
def list_files(
    self: dict, repo_id: str, metadata="true", data="true", version="current"
) -> list:
    """helper function to integrate list files API response

    Args:
        self (dict): dictionary storing session vara
        repo_id (str): repo id of the omixatlas
    Returns:
        list_files_resp -> list of objects with requests type
    """
    # page_size -> for paginating the API
    files_api_endpoint = f"{self.discover_url}/repositories/{repo_id}/files"
    # initialising an empty value of next link
    next_link = ""
    responses_list = []
    # once the pages will end -> next_link will be
    # set to None by the API
    while next_link is not None:
        if next_link:
            next_endpoint = f"{self.discover_url}{next_link}"
            response = self.session.get(next_endpoint)
        else:
            # getting the response for the first 1000 pages initially
            query_params = {
                "page[size]": 1000,
                "page[after]": 0,
                "include_metadata": f"{metadata}",
                "data": f"{data}",
                "version": f"{version}",
            }
            response = self.session.get(files_api_endpoint, params=query_params)
        response.raise_for_status()
        response_json = response.json()
        # list of request objects
        # request object having both status and data of the response
        responses_list.append(response)
        # seeing after 1000 pages whose response is already fetched
        # if there are more pages
        next_link = response_json.get("links").get("next")

    return responses_list


def normalize_file_paths(dataset_file_path_dict: dict):
    """Normalise all the file paths in the dataset_file_path_dict

    Args:
        dataset_file_path_dict (dict): key is dataset id and value is the file_path
    """
    # iterating over the dictionary containing dataset_id and list of file paths
    # format: {<dataset_id>:[<file_path_1>, ........., <file_path_n>]}
    for dataset_id, file_path_list in dataset_file_path_dict.items():
        # iterating over the list of file paths and
        # normalising each file path and storing in
        # normalised_file_path_list which will be mapped to
        # dataset_id
        normalised_file_path_list = []
        for file_path in file_path_list:
            normalised_file_path = os.path.normpath(file_path)
            normalised_file_path_list.append(normalised_file_path)
        dataset_file_path_dict[dataset_id] = normalised_file_path_list
    return dataset_file_path_dict


# TODO -> @shilpa to make a ticket for this to make this generic enough
def check_res_dict_has_file_deleted_entries(result_dict: dict) -> bool:
    """Check if result_dict has entries for deleted files
    If res_dict has entries of deleted files, then only commit API will be
    called else commit API will not be called
    This will ensure that commit API is only called when actually there is an
    entry in the DF where files are deleted

    Args:
        result_dict (dict): DF containing messages from the API corresponding to
        deletion request

    Returns:
        bool: Flag to show if any dataset_id from the result_dict have deleted message
    """
    # valid_deletion_entry is initalized to false -> if no deletion entry is valid
    # then False flag will be returned -> commit API will not be hit
    valid_deletion_entry = False
    # Example result_dict
    # {'GSE140509_GPL16791':
    # {'Message': 'Request Accepted. Dataset will be deleted in the next version of OmixAtlas',
    # 'Folder Path': 'transcriptomics_213/GSE140509_GPL16791.gct'}}

    # if message string has `Request Accepted` substring then deletion for that dataset_id
    # has been accepted
    # if in any of the other entries -> the deletion request is accepted -> means
    # at least one dataset_id has valid deletion entry -> commit will be hit then
    # for deletion request -> break the loop there

    # TODO ->
    # i. Make this more generic enough
    # ii. ( any(any('Request Accepted' in deletion_res["Message"])
    # for deletion_res in result_dict.values()) )

    for dataset_id, deletion_res_list in result_dict.items():
        for deletion_res in deletion_res_list:
            message = deletion_res["Message"]
            if "Request Accepted" in message:
                valid_deletion_entry = True
                break

    return valid_deletion_entry


def user_file_path_incorrect(user_file_path: str, datasetid_key: str):
    """If user_file_path not equal to file_path passed by the user

    Args:
        user_file_path (str): file_path passed by the user in dataset_file_path_dict
        datasetid_key (str): dataset_id for which file_path passed
    """
    # passed file path by the user is does not contain the file
    # raise a warning and store an error message corresponding to
    # dataset_id and return
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        "Unable to delete file from the file_path "
        + f"{user_file_path} because the file corresponding to the "
        + f"dataset id {datasetid_key} is not present in this file_path. "
        + "This dataset_id file is present only in 1 path so passing path "
        + "using optional parameter not required here. "
        + "For any questions, please reach out to polly.support@elucidata.io. "
    )
    # break line added -> for better UX
    print("\n")
    res = {
        "Message": "Dataset not deleted because file_path for the dataset_id is incorrect",
        "Folder Path": f"{user_file_path}",
    }
    return res


def convert_delete_datasets_res_dict_to_df(result_dict: dict):
    """Convert result dict of delete datasets to df
    Key -> dataset_id
    Value -> Message from deleted files in a list
    DF
    Col 1 -> DatasetId
    Col 2 -> Message
    Col 3 -> File Path


    Args:
        result_dict (dict): Dict of delete datasets result
    """
    # res dict format -> {"<dataset_id>":[{"<Folder_Path>":<val>, "Message":<val>}]}
    # result dict format -> example
    # {'GSE101942_GPL11154': [{'Message': 'Dataset not deleted because file_path for
    #  the dataset_id is incorrect', 'Folder Path': 'transcriptomics_906s/GSE76311_GPL17586.gct'},
    # {'Message': 'Dataset not deleted because file_path for the dataset_id is incorrect',
    # 'Folder Path': 'transcriptomics_907s/GSE76311_GPL17586.gct'}]}
    df_list = []
    for key, val_list in result_dict.items():
        for val in val_list:
            df_1 = pd.DataFrame(
                val,
                index=[
                    "0",
                ],
            )
            # print(df_1)
            df_1.insert(0, "DatasetId", key)
            # df_1["Dataset Id"] = key
            df_list.append(df_1)

    data_delete_df = pd.concat(df_list, axis=0, ignore_index=True)
    print(
        tabulate(
            data_delete_df,
            headers="keys",
            tablefmt="fancy_grid",
            maxcolwidths=[None, 10, None],
        )
    )


def warning_invalid_path_delete_dataset_multiple_paths(
    invalid_path: str, datasetid_key: str
):
    """Function to raise warning for invalid path for dataset_ids present in
    multiple paths
    Args:
        invalid_path: str
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        "Unable to delete file from these file paths "
        + f"{invalid_path}"
        + " because in these file paths, file corresponding to the dataset id "
        + datasetid_key
        + " is not present. "
        + "Please run <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>) to get all "
        + "valid paths for this dataset_id. For any questions, please reach out to polly.support@elucidata.io. "
    )
    # break line added -> for better UX
    print("\n")
    res = {
        "Message": "Dataset not deleted because file_path is incorrect.",
        "Folder Path": f"{invalid_path}",
    }
    return res


def get_all_file_paths_param_check(repo_id: int, dataset_id: str):
    """Function to do sanity checks on arguments of
    get_all_file_paths_param functions

    Args:
        repo_id (int): repo_id of the repo of the Omixatlas
        dataset_id (str): dataset id passed by the user
    """
    try:
        parameter_check_for_repo_id(repo_id)
        if not (dataset_id and isinstance(dataset_id, str)):
            raise paramException(
                title="Param Error",
                detail="dataset_ids should be a string",
            )
    except Exception as err:
        raise err


def warning_message_for_wrong_destination_folder(
    corresponding_data_file_names: list,
    required_file_name: str,
    destination_folder_path: str,
):
    """Method to raise warning in case destination folder passed by the user is incorrect

    Args:
        corresponding_data_file_names (list): list of full absolute file paths of files
        required_file_name (str): required file name that is being updated with update_datasets functionality
        destination_folder_path (str): folder path to which the files are to be updated
    """
    valid_folder_list = helpers.get_folder_list_from_list_of_filepaths(
        corresponding_data_file_names
    )
    warnings.simplefilter("always", UserWarning)
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        "Unable to update the data/metadata for  "
        + required_file_name
        + " because original data file not present in the provided destination folder path: \n "
        + destination_folder_path
        + " in the omixatlas. "
        + "Please choose the required destination folder path from the following: \n "
        + str(valid_folder_list)
        + ".\n For any questions, please reach out to polly.support@elucidata.io. "
        + " \n Please use add_datasets to upload the files if no destination folder"
        + " paths in the Omixatlas contain the data being updated by you."
    )


def get_possible_file_from_matching_filename_list_from_oa(
    corresponding_data_file_names: list,
    required_file_name: str,
    destination_folder_path: str,
) -> str:
    """
    The functions selects and returns file from a list of filepaths provided.
    The selection is based on the the fact that the file's folder path should match
    the destination folder path provided.


    Arguments:
        corresponding_data_file_names -- list of full absolute file paths of files
        required_file_name -- required file name that is being updated with update_datasets functionality
        destination_folder_path -- folder path to which the files are to be updated

    Returns:
        file name : absolute file path or empty string if no match found
    """

    possible_data_file = ""
    if corresponding_data_file_names:
        for data_file in corresponding_data_file_names:
            # loop
            # comparing dir path of the file in OA to the provided destination folder path.
            # if the destination folder matches the dir of any one of the corresoponding files
            # then all good.
            # step 3: if there are files present in the OA corresponding to the metadta file then
            # looping to find if any of the file's folder path match the destination folder path provided
            # by the user.
            # normpath is to normalise the folder path
            # empty str -> "."
            # "/" -> "/"
            # "a/b//c" -> "a/b/c"
            if os.path.normpath(os.path.dirname(data_file)) == os.path.normpath(
                destination_folder_path
            ):
                possible_data_file = data_file
        if not possible_data_file:
            # none of the matching files names in the OA are in the same dir as the
            # provided destination folder, warning thrown
            warning_message_for_wrong_destination_folder(
                corresponding_data_file_names,
                required_file_name,
                destination_folder_path,
            )
            # valid_folder_list = helpers.get_folder_list_from_list_of_filepaths(
            #     corresponding_data_file_names
            # )
            # warnings.simplefilter("always", UserWarning)
            # warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
            # warnings.warn(
            #     "Unable to update the data/metadata for  "
            #     + required_file_name
            #     + " because original data file not present in the provided destination folder path: "
            #     + destination_folder_path
            #     + " in the omixatlas. "
            #     + "Please choose the required destination folder path from the following: \n "
            #     + str(valid_folder_list)
            #     + ".\n For any questions, please reach out to polly.support@elucidata.io. "
            # )
    return possible_data_file


def check_if_destination_folder_correct(
    corresponding_data_file_names: list,
    required_file_name: str,
    destination_folder_path: str,
) -> bool:
    """Check for the metadata file is getting updated in correct destination folder or not

    Args:
        corresponding_data_file_names (list): list of full absolute file paths of files
        required_file_name (str): required file name corresponding to which destination folder is matched
        destination_folder_path (str): destination folder passed by the user

    Returns:
        bool: Return the boolean flag depicting destination folder passed by the user is correct or not
    """
    # by default initialising the flag to False
    is_dest_folder_correct = False

    # if the passed destination folder matches one of the destination
    # folder in the corresponding_data_file_names paired to required_file_name
    # then the destination folder passed by the user is ok -> change the
    # is_dest_folder_correct flag to True
    # Else if no destination folder matches one of the destination folder in the
    # corresponding_data_file_names paired to the required_file_name
    # then raise warning

    for data_file in corresponding_data_file_names:
        # Looping in the corresponding_data_file_names i.e. <destination_folder>/<file_name>
        # fetch the destination folder and check if it matches the passed destination folder
        # if use then make the is_dest_folder_correct to TRUE and break the loop
        # Use of normpath
        # normpath is to normalise the folder path
        # empty str -> "."
        # "/" -> "/"
        # "a/b//c" -> "a/b/c"
        if os.path.normpath(os.path.dirname(data_file)) == os.path.normpath(
            destination_folder_path
        ):
            is_dest_folder_correct = True
            break
    if not is_dest_folder_correct:
        # none of the matching files names in the OA are in the same dir as the
        # provided destination folder, warning thrown
        warning_message_for_wrong_destination_folder(
            corresponding_data_file_names, required_file_name, destination_folder_path
        )
    return is_dest_folder_correct


def check_params_for_get_metadata(repo_key, dataset_id, table_name):
    """
    Args:
        repo_key(str): repo_name/repo_id of the repository.
        dataset_id(str): dataset_id of the dataset.
        table_name(str): table name for the desired metadata, 'samples' supported for now.
    """
    if not (repo_key and (isinstance(repo_key, str) or isinstance(repo_key, int))):
        raise paramException(
            title="Param Error",
            detail="Argument 'repo_key' is either empty or invalid. \
It should either be a string or an integer. Please try again.",
        )
    if not (dataset_id and isinstance(dataset_id, str)):
        raise paramException(
            title="Param Error",
            detail="Argument 'dataset_id' is either empty or invalid. It should be a string. Please try again.",
        )
    if not (table_name and isinstance(table_name, str)):
        raise paramException(
            title="Param Error",
            detail="Argument 'table_name' is either empty or invalid. It should be a string. Please try again.",
        )
    if table_name.lower() not in const.TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP:
        raise paramException(
            title="Param Error",
            detail=const.ERROR_MSG_GET_METADATA,
        )


def param_check_download_dataset(
    repo_key: str, dataset_ids: list, folder_path: str
) -> None:
    if not (repo_key and isinstance(repo_key, str)):
        raise paramException(
            title="Param Error",
            detail="repo_key (either id or name) is required and should be a string",
        )
    if not (dataset_ids and isinstance(dataset_ids, list)):
        raise paramException(
            title="Param Error",
            detail="dataset_ids is required and should be a list of dataset_ids as strings",
        )
    if (not isinstance(folder_path, str)) or (not os.path.isdir(folder_path)):
        raise paramException(
            title="Param Error",
            detail="folder_path if provided should be a string and a valid folder path.",
        )


def handle_elastic_discover_api_error(response):
    if response.status_code == http_codes.UNAUTHORIZED:
        raise UnauthorizedException("User is unauthorized to access this")
    elif response.status_code == http_codes.BAD_REQUEST:
        title, details = extract_error_message_details(response)
        if title == app_err_info.EMPTY_PAYLOAD_CODE:
            raise EmptyPayloadException()
        elif app_err_info.INVALID_MODEL_NAME_TITLE in title:
            raise InvalidSyntaxForRequestException()
    elif response.status_code == http_codes.INTERNAL_SERVER_ERROR:
        raise InvalidSchemaJsonException()
    else:
        (
            title,
            details,
        ) = extract_error_message_details(response)
        raise Exception("Exception Occurred :" + str(details))
