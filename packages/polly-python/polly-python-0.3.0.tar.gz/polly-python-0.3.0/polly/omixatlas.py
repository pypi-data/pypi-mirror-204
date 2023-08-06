from functools import lru_cache
import gzip
import json
import warnings
import ssl
import copy
import pathlib
import logging
import os
import platform
import tempfile
import boto3
from boto3.s3.transfer import TransferConfig
from boto3.exceptions import S3UploadFailedError
from tempfile import TemporaryDirectory as TempDir
from pathlib import Path
from typing import Union, Dict
from collections import namedtuple
import xml.etree.ElementTree as ET
import pandas as pd
import time
from joblib import Parallel, delayed
import requests
from retrying import retry
from polly.help import example
from polly import constants as const
from polly import helpers
from polly.auth import Polly
from tqdm import tqdm
from tabulate import tabulate
from urllib.parse import urlparse, quote
from polly.constants import (
    DATA_TYPES,
    REPORT_GENERATION_SUPPORTED_REPOS,
    ERROR_MSG_GET_METADATA,
    TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP,
)
from polly.errors import (
    QueryFailedException,
    UnfinishedQueryException,
    InvalidParameterException,
    error_handler,
    is_unfinished_query_error,
    paramException,
    wrongParamException,
    invalidApiResponseException,
    invalidDataException,
    UnsupportedRepositoryException,
    InvalidPathException,
    InvalidDirectoryPathException,
    AccessDeniedError,
    RequestFailureException,
)
from datetime import datetime

import numpy as np
import datapane as dp
import plotly.express as px
from polly.index_schema_level_conversion_const import (
    schema_levels,
    schema_table_names,
)

import polly.omixatlas_hlpr as omix_hlpr

import polly.http_response_codes as http_codes
from polly.schema import check_schema_for_errors
from polly.tracking import Track

QUERY_API_V1 = "v1"
QUERY_API_V2 = "v2"


class OmixAtlas:
    """
    OmixAtlas class enables users to interact with functional properties of the omixatlas such as \
    create and update an Omixatlas, get summary of it's contents, add, insert, update the schema, \
    add, update or delete datasets, query metadata, download data, save data to workspace etc.\

    Args:
        token (str): token copy from polly.
    Usage:
        from polly.OmixAtlas import OmixAtlas

        omixatlas = OmixAtlas(token)
    """

    example = classmethod(example)

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.discover_url = f"https://api.discover.{self.session.env}.elucidata.io"
        self.elastic_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )
        self.resource_url = f"{self.base_url}/v1/omixatlases"

    @Track.track_decorator
    def get_all_omixatlas(
        self, query_api_version="v2", count_by_source=True, count_by_data_type=True
    ):
        """
        This function will return the summary of all the Omixatlas on Polly which the user has access to.\
        Please use this function with default values for the paramters.
        Args:
            query_api_version (str): query api version
            count_by_source (bool): count by source
            count_by_data_type (bool): count by data type

        Returns:
            It will return a list of JSON objects. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """

        url = self.resource_url
        if query_api_version == "v2":
            if count_by_source and count_by_data_type:
                params = {
                    "summarize": "true",
                    "v2": "true",
                    "count_by_source": "true",
                    "count_by_data_type": "true",
                }
            elif count_by_source:
                params = {"summarize": "true", "v2": "true", "count_by_source": "true"}
            elif count_by_data_type:
                params = {
                    "summarize": "true",
                    "v2": "true",
                    "count_by_data_type": "true",
                }
            else:
                params = {
                    "summarize": "true",
                    "v2": "true",
                }
        elif query_api_version == "v1":
            params = {"summarize": "true"}
        else:
            raise wrongParamException("Incorrect query param version passed")
        response = self.session.get(url, params=params)
        error_handler(response)
        return response.json()

    @Track.track_decorator
    def omixatlas_summary(
        self,
        repo_key: str,
        query_api_version="v2",
        count_by_source=True,
        count_by_data_type=True,
    ):
        """
        This function will return you a object that contain summary of a given Omixatlas.\
        Please use the function with the default values for optional parameters.
        Args:
            repo_key (str): repo_id or repo_name.
            query_api_version (str, optional): query api version
            count_by_source (bool, optional): count by source
            count_by_data_type (bool, optional): count by data_type
        Returns:
            It will return a JSON object. (see examples)

        Raises:
            wrongParamException: invalid paramter passed.
        """

        url = f"{self.resource_url}/{repo_key}"
        if query_api_version == "v2":
            if count_by_source and count_by_data_type:
                params = {
                    "summarize": "true",
                    "v2": "true",
                    "count_by_source": "true",
                    "count_by_data_type": "true",
                }
            elif count_by_source:
                params = {"summarize": "true", "v2": "true", "count_by_source": "true"}
            elif count_by_data_type:
                params = {
                    "summarize": "true",
                    "v2": "true",
                    "count_by_data_type": "true",
                }
            else:
                params = {
                    "summarize": "true",
                    "v2": "true",
                }
        elif query_api_version == "v1":
            params = {"summarize": "true"}
        else:
            raise wrongParamException("Incorrect query param version passed")
        if params:
            response = self.session.get(url, params=params)
        error_handler(response)
        return response.json()

    # TODO -> Make this function private while refactoring
    def _get_omixatlas(self, key: str):
        """
        This function will return a omixatlas repository in polly.

        ``Args:``
            |  ``key:`` repo name or repo id.

        ``Returns:``
            It will return a objects like this.

            .. code::


                    {
                    'repo_name': 'repo',
                    'repo_id': '1646',
                    'indexes': {
                    'gct_metadata': 'repo_gct_metadata',
                        'h5ad_metadata': 'repo_h5ad_metadata',
                        'csv': 'repo_csv',
                        'files': 'repo_files',
                        'json': 'repo_json',
                        'ipynb': 'repo_ipynb',
                        'gct_data': 'repo_gct_data',
                        'h5ad_data': 'repo_h5ad_data'
                        },
                    'diseases': [],
                    'organisms': [],
                    'sources': [],
                    'datatypes': [],
                    'dataset_count': 0,
                    'disease_count': 0,
                    'tissue_count': 0,
                    'organism_count': 0,
                    'cell_line_count': 0,
                    'cell_type_count': 0,
                    'drug_count': 0,
                    'data_type_count': 0,
                    'data_source_count': 0,
                    'sample_count': 0,
                    'normal_sample_count': 0
                    }

        | To use this function import Omixatlas class and make a object.


        .. code::


                from polly.omixatlas import OmixAtlas
                omixatlas = OmixAtlas(token)
                # to use OmixAtlas class functions
                omixatlas.get_omixatlas('9')

        """
        if key and isinstance(key, str):
            url = f"{self.resource_url}/{key}"
            response = self.session.get(url)
            error_handler(response)
            return response.json()
        else:
            raise paramException(
                title="param error", detail="repo_id is either empty or not string"
            )

    @Track.track_decorator
    def query_metadata(
        self,
        query: str,
        experimental_features=None,
        query_api_version=QUERY_API_V2,
        page_size=None,  # Note: do not increase page size more than 999
    ):
        """
        This function will return a dataframe containing the SQL response.

        Args:
           query (str) : sql query  on  omixatlas.
           experimental_features : this section includes in querying metadata <target>.
           query_api_version (str) : v1 or v2.
           page_size (int): page size for query.

        Returns:
            It will return a dataframe that contains the query response.

        Raises:
            UnfinishedQueryException: when query has not finised the execution.
            QueryFailedException: when query failed to execute.
        """

        max_page_size = 999
        if page_size is not None and page_size > max_page_size:
            raise ValueError(
                f"The maximum permitted value for page_size is {max_page_size}"
            )
        elif page_size is None and query_api_version != QUERY_API_V2:
            page_size = 500

        queries_url = f"{self.resource_url}/queries"
        queries_payload = {
            "data": {
                "type": "queries",
                "attributes": {
                    "query": query,
                    "query_api_version": query_api_version,
                    "query_results_format": "JSON",
                },
            }
        }
        if experimental_features is not None:
            queries_payload.update({"experimental_features": experimental_features})

        response = self.session.post(queries_url, json=queries_payload)
        error_handler(response)

        query_data = response.json().get("data")
        query_id = query_data.get("id")
        return self._process_query_to_completion(query_id, query_api_version, page_size)

    @retry(
        retry_on_exception=is_unfinished_query_error,
        wait_exponential_multiplier=500,  # Exponential back-off starting 500ms
        wait_exponential_max=10000,  # After 10s, retry every 10s
        stop_max_delay=900000,  # Stop retrying after 900s (15m)
    )
    def _process_query_to_completion(
        self, query_id: str, query_api_version: str, page_size: Union[int, None]
    ):
        queries_url = f"{self.resource_url}/queries/{query_id}"
        response = self.session.get(queries_url)
        error_handler(response)

        query_data = response.json().get("data")
        query_status = query_data.get("attributes", {}).get("status")
        if query_status == "succeeded":
            return self._handle_query_success(query_data, query_api_version, page_size)
        elif query_status == "failed":
            self._handle_query_failure(query_data)
        else:
            raise UnfinishedQueryException(query_id)

    def _handle_query_failure(self, query_data: dict):
        fail_msg = query_data.get("attributes").get("failure_reason")
        raise QueryFailedException(fail_msg)

    def _handle_query_success(
        self, query_data: dict, query_api_version: str, page_size: Union[int, None]
    ) -> pd.DataFrame:
        query_id = query_data.get("id")

        details = []
        time_taken_in_ms = query_data.get("attributes").get("exec_time_ms")
        if isinstance(time_taken_in_ms, int):
            details.append("time taken: {:.2f} seconds".format(time_taken_in_ms / 1000))
        data_scanned_in_bytes = query_data.get("attributes").get("data_scanned_bytes")
        if isinstance(data_scanned_in_bytes, int):
            details.append(
                "data scanned: {:.3f} MB".format(data_scanned_in_bytes / (1024**2))
            )

        if details:
            detail_str = ", ".join(details)
            print("Query execution succeeded " f"({detail_str})")
        else:
            print("Query execution succeeded")

        if query_api_version != QUERY_API_V2 or page_size is not None:
            return self._fetch_results_as_pages(query_id, page_size)
        else:
            return self._fetch_results_as_file(query_id)

    def _fetch_results_as_pages(self, query_id, page_size):
        first_page_url = (
            f"{self.resource_url}/queries/{query_id}" f"/results?page[size]={page_size}"
        )
        response = self.session.get(first_page_url)
        error_handler(response)
        result_data = response.json()
        rows = [row_data.get("attributes") for row_data in result_data.get("data")]

        all_rows = rows

        message = "Fetched {} rows"
        print(message.format(len(all_rows)), end="\r")

        while (
            result_data.get("links") is not None
            and result_data.get("links").get("next") is not None
            and result_data.get("links").get("next") != "null"
        ):
            next_page_url = self.base_url + result_data.get("links").get("next")
            response = self.session.get(next_page_url)
            error_handler(response)
            result_data = response.json()
            if result_data.get("data"):
                rows = [
                    row_data.get("attributes") for row_data in result_data.get("data")
                ]
            else:
                rows = []
            all_rows.extend(rows)
            print(message.format(len(all_rows)), end="\r")

        # Blank line resets console line start position
        print()
        return self._get_sorted_col_df(pd.DataFrame(all_rows))

    def _get_root_loc_from_url(self, url) -> str:
        # Function to parse the root location from URL & return it.
        pos = url.rfind("?")
        s = ""
        for i in range(0, pos):
            s += url[i]
        return s.split("/")[-1]

    def _local_temp_file_path(self, filename):
        # Function to check presence of file based upon system platform
        temp_dir = Path(
            "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
        ).absolute()

        temp_file_path = os.path.join(temp_dir, filename)
        if Path(temp_file_path).exists():
            os.remove(temp_file_path)

        return temp_file_path

    def _extract_results_from_download_urls(self, download_urls):
        # Function to pull out & combine results from the list of Download URLS
        results = []
        for url in download_urls:
            r = requests.get(url, allow_redirects=True)
            name = self._get_root_loc_from_url(url)
            filename = self._local_temp_file_path(name)
            with open(filename, "wb") as f:
                f.write(r.content)
            with gzip.open(filename, "rt", encoding="utf-8") as fgz:
                for line in fgz:
                    results.append(json.loads(line))

        df = pd.DataFrame.from_records(results)
        print(f"Fetched {len(df.index)} rows")
        return df

    def _fetch_results_as_file(self, query_id):
        results_file_req_url = (
            f"{self.resource_url}/queries/{query_id}/results?action=download"
        )
        response = self.session.get(results_file_req_url)
        error_handler(response)
        result_data = response.json()

        results_file_download_url = result_data.get("data", {}).get("download_url")
        if (
            results_file_download_url is None
            or results_file_download_url == "Not available"
        ):
            # The user is probably executing SHOW TABLES or DESCRIBE query
            return self._fetch_results_as_pages(query_id, 100)
        else:
            pd.set_option("display.max_columns", None)
            df = self._extract_results_from_download_urls(results_file_download_url)
            return self._get_sorted_col_df(df)

    def _get_sorted_col_df(self, results_dataframe):
        """
        Function to sort a dataframe columnwise. Primarily being used before returning the
        query_metadata result dataframe.

        ``Args:``
            |  ``results_dataframe :`` dataframe containing the query_metadata results

        ``Returns:``
            |  coloumn-wise sorted dataframe where the order will be dataset_id , src_dataset_id, alphabetically ordered
            |  rest of the columns.
        """

        # checking presence of either of the dataset_id related cols in the df
        id_cols_present = set.intersection(
            set(["dataset_id", "src_dataset_id"]), set(results_dataframe.columns)
        )
        if len(id_cols_present) == 0:
            # none of the dataset id related cols are present - sorting cols alphabetically
            results_dataframe = self._get_alphabetically_sorted_col_df(
                results_dataframe
            )
        elif len(id_cols_present) == 1:
            col_data = results_dataframe.pop(id_cols_present.pop())
            results_dataframe = self._get_alphabetically_sorted_col_df(
                results_dataframe
            )
            results_dataframe.insert(0, col_data.name, col_data)
        else:
            dataset_id_data = results_dataframe.pop("dataset_id")
            src_dataset_id_data = results_dataframe.pop("src_dataset_id")
            results_dataframe = self._get_alphabetically_sorted_col_df(
                results_dataframe
            )
            results_dataframe.insert(0, src_dataset_id_data.name, src_dataset_id_data)
            results_dataframe.insert(0, dataset_id_data.name, dataset_id_data)

        return results_dataframe

    def _get_alphabetically_sorted_col_df(self, results_dataframe):
        """
        Function to alphabetically column-wise sort a dataframe.

        ``Args:``
            |  ``dataframe :`` dataframe containing the query_metadata results

        ``Returns:``
            |  coloumn-wise sorted dataframe where the order will be alphabetical.

        """
        return results_dataframe.sort_index(axis=1)

    def _get_schema_from_api(
        self, repo_key: str, schema_type_dict: dict, source: str, data_type: str
    ) -> dict:
        """
        Gets the schema of a repo id for the given repo_key and
        schema_type definition at the top level

        ``Args:``
            |  ``repo_key (str) :`` repo id or repo name
            |  ``schema_type_dict (dictionary) :`` {schema_level:schema_type}
            |  example {'dataset': 'files', 'sample': 'gct_metadata'}

        ``Returns:``

            .. code::


                    {
                        "data": {
                            "id": "<REPO_ID>",
                            "type": "schema",
                            "attributes": {
                                "schema_type": "files | gct_metadata | h5ad_metadata",
                                "schema": {
                                    ... field definitions
                                }
                            }
                        }
                    }

        :meta private:
        """
        resp_dict = {}
        schema_base_url = f"{self.discover_url}/repositories"
        summary_query_param = "?response_format=summary"
        filter_query_params = ""
        if source:
            if data_type:
                filter_query_params = f"&source={source}&datatype={data_type}"
            else:
                filter_query_params = f"&source={source}"
        if repo_key and schema_type_dict and isinstance(schema_type_dict, Dict):
            for schema_table_key, val in schema_type_dict.items():
                schema_type = val
                if filter_query_params:
                    dataset_url = (
                        f"{schema_base_url}/{repo_key}/"
                        + f"schemas/{schema_type}"
                        + f"{summary_query_param}{filter_query_params}"
                    )
                else:
                    dataset_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}{summary_query_param}"
                resp = self.session.get(dataset_url)
                error_handler(resp)
                resp_dict[schema_table_key] = resp.json()
        else:
            raise paramException(
                title="Param Error",
                detail="repo_key and schema_type_dict are either empty or its datatype is not correct",
            )
        return resp_dict

    def _get_full_schema_payload_from_api(self, repo_key: str, schema_type_dict: str):
        """
        Get full schema payload from the API
        """
        resp_dict = {}
        schema_base_url = f"{self.discover_url}/repositories"
        if repo_key and schema_type_dict and isinstance(schema_type_dict, Dict):
            for schema_table_key, val in schema_type_dict.items():
                schema_type = val
                dataset_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}"
                resp = self.session.get(dataset_url)
                error_handler(resp)
                resp_dict[schema_table_key] = resp.json()
        else:
            raise paramException(
                title="Param Error",
                detail="repo_key and schema_type_dict are either empty or its datatype is not correct",
            )
        return resp_dict

    def _return_type_param_check(self, return_type: str):
        """
        get_schema parameters sanity check
        """
        if not isinstance(return_type, str):
            raise paramException(
                title="Param Error",
                detail="return_type should be a string",
            )

        return_type_vals = copy.deepcopy(const.GET_SCHEMA_RETURN_TYPE_VALS)

        if return_type not in return_type_vals:
            raise paramException(
                title="Param Error",
                detail=f"return_type take only two vals : {return_type_vals}",
            )

    @Track.track_decorator
    def get_schema(
        self,
        repo_key: str,
        schema_level=[],
        source="",
        data_type="",
        return_type="dataframe",
    ) -> dict:
        """
        Function to get the Schema of all the tables in an OmixAtlas.
        User need to have Data Admin at the resource level to get the schema of an OmixAtlas.
        Please contact polly@support.com if you get Access Denied error message.
        Args:
            repo_key (str): repo_id OR repo_name. This is a mandatory field.
            schema_level (list, optional): Table name for which users want to get the schema. \
            Users can get the table names by querying `SHOW TABLES IN <repo_name>` using query_metadata function.\
            The default value is all the table names for the repo.
            source (str, optional): Source for which user wants to fetch the schema. \
            The default value is all the sources in the schema.
            data_type (str, optional): Datatype for which user wants to fetch the schema. \
            The default value is all the datatypes in the schema.
            return_type (str, optional): For users who intend to query should use "dataframe" output. \
            For users, who want to perform schema management, they should get the output in "dict" format. \
            Dataframe format doesn't give the complete schema, it only shows the information \
            which aids users for writing queryies. Default value is "dataframe".
        Raises:
            paramException: When Function Parameter passed are not in the right format.
            RequestException: There is some issue in fetching the Schema.
            invalidApiResponseException: The Data returned is not in appropriate format.
        """

        # get schema_type_dict
        schema_type_dict = self._get_schema_type_info(repo_key, schema_level, data_type)
        try:
            self._return_type_param_check(return_type)
        except Exception as err:
            raise err

        # schema from API calls
        if repo_key and schema_type_dict and isinstance(schema_type_dict, Dict):
            if return_type == "dict":
                schema_payload_dict = self._get_full_schema_payload_from_api(
                    repo_key, schema_type_dict
                )
                schema_payload_dict = self._remove_links_key_in_schema_payload(
                    schema_payload_dict
                )
                return self.return_schema_data(schema_payload_dict)
            else:
                schema = self._get_schema_from_api(
                    repo_key, schema_type_dict, source, data_type
                )
        if schema and isinstance(schema, Dict):
            for key, val in schema.items():
                if schema[key]["data"]["attributes"]["schema"]:
                    schema[key] = schema[key]["data"]["attributes"]["schema"]
        df_map = {}
        for key, val in schema.items():
            flatten_dict = self._flatten_nested_schema_dict(schema[key])
            df_map[key] = self._nested_dict_to_df(flatten_dict)

        return self.return_schema_data(df_map)

    def _remove_links_key_in_schema_payload(self, schema_payload_dict: dict) -> dict:
        """
        Remove links key from the schema response
        """
        for schema_level_key, schema_level_value in schema_payload_dict.items():
            if "data" in schema_level_value:
                val_data_dict = schema_level_value.get("data", {})
                if "links" in val_data_dict:
                    val_data_dict.pop("links", None)

        return schema_payload_dict

    def return_schema_data(self, df_map: dict) -> tuple:
        """
        Return schema data as named tuple

        :meta private:
        """
        Schema = namedtuple("Schema", (key for key, value in df_map.items()))
        return Schema(**df_map)

    def _get_schema_type_info(
        self, repo_key: str, schema_level: list, data_type: str
    ) -> dict:
        """
        Return schema type dict for valid schema level and table name values
        """

        # if schema level passed then return schema type accordingly
        if schema_level:
            schema_levels_const = copy.deepcopy(schema_levels)
            schema_table_name_const = copy.deepcopy(schema_table_names)

            # check if schema level parameter is a subset of schema_levels_const
            # a.issubset(b) => schema_level.issubset(schema_level_const)
            schema_levels_const_set = set(schema_levels_const)
            schema_table_name_const_set = set(schema_table_name_const)
            schema_level_set = set(schema_level)
            if schema_level_set.issubset(schema_levels_const_set):
                schema_type_dict = self._get_schema_type(schema_level, data_type)
            elif schema_level_set.issubset(schema_table_name_const_set):
                schema_type_dict = self._schema_table_name_schema_type_mapping(
                    repo_key, schema_level
                )
            else:
                raise paramException(
                    title="Param Error",
                    detail="schema_level input is incorrect. Use the query SHOW TABLES IN <repo_name>"
                    + "to fetch valid table names for schema_level input",
                )
            # else if check schema level is subset of schema table names
            # else raise errors
        else:
            # return all the schema types, in the default condition
            # default condition is no schema level or table name passed by user
            schema_type_dict = self._schema_table_name_schema_type_mapping(
                repo_key, schema_level
            )

        return schema_type_dict

    def _get_schema_type(self, schema_level: list, data_type: str) -> dict:
        """
        Compute schema_type based on data_type and schema_level
        Old Schema Level Value Mapping and New Schema Level Value Mapping
        Backward compatible

        Old Schema Level Value Mapping
        |  schema_level   --------    schema_type
        |  dataset       --------     file
        |  sample    --------      gct_metadata
        |  sample and  ------       h5ad_metadata
        |  single cell

        :meta private:
        """
        if schema_level and isinstance(schema_level, list):
            if "dataset" in schema_level and "sample" in schema_level:
                if data_type != "single_cell" or data_type == "":
                    schema_type_dict = {"dataset": "files", "sample": "gct_metadata"}
                elif data_type == "single_cell":
                    schema_type_dict = {"dataset": "files", "sample": "h5ad_metadata"}
                else:
                    raise wrongParamException(
                        title="Incorrect Param Error",
                        detail="Incorrect value of param passed data_type ",
                    )
            elif "dataset" in schema_level or "sample" in schema_level:
                if "dataset" in schema_level:
                    schema_type_dict = {"dataset": "files"}
                elif "sample" in schema_level:
                    if data_type != "single_cell" or data_type == "":
                        schema_type_dict = {"sample": "gct_metadata"}
                    elif data_type == "single_cell":
                        schema_type_dict = {"sample": "h5ad_metadata"}
                    else:
                        raise wrongParamException(
                            title="Incorrect Param Error",
                            detail="Incorrect value of param passed data_type ",
                        )
            else:
                raise wrongParamException(
                    title="Incorrect Param Error",
                    detail="Incorrect value of param passed schema_level ",
                )
        else:
            raise paramException(
                title="Param Error",
                detail="schema_level is either empty or its datatype is not correct",
            )
        return schema_type_dict

    def _schema_table_name_schema_type_mapping(
        self, repo_key: str, schema_table_names: list
    ) -> dict:
        """
        New Schema Level Value mapping
        |   Table Name  Schema Type
        |   datasets ----- file
        |   samples ----- gct_metadata
        |   features ---- gct_row_metadata
        |   samples_singlecell ---- h5ad_metadata
        """
        # all the table and index name mapping present
        # for the repo is fetched
        schema_base_url = f"{self.discover_url}/repositories"
        schema_url = f"{schema_base_url}/{repo_key}/schemas"
        meta_true_query_param = "?meta=true"
        schema_mapping_url = f"{schema_url}{meta_true_query_param}"
        schema_mapping_info = self.session.get(schema_mapping_url)
        error_handler(schema_mapping_info)
        schema_mapping_info = schema_mapping_info.json()
        # schema mapping info structure
        # table name, index name mapping dict fetched from it
        # {"data":{"type":"<type>", "repository_id":"<repo_id>", "attributes":{"schemas":{<schema-mapping>}}}}
        schema_mapping = (
            schema_mapping_info.get("data").get("attributes").get("schemas")
        )

        # if user has passed table names
        # then only those are filtered
        # from the table and index name mapping dict
        # else the whole mapping dict returnedß

        if schema_table_names:
            schema_mapping_res = {
                schema_table: schema_mapping[schema_table]
                for schema_table in schema_table_names
            }
        else:
            schema_mapping_res = schema_mapping

        return schema_mapping_res

    def _flatten_nested_schema_dict(self, nested_schema_dict: dict) -> dict:
        """
        Flatten the nested dict

        ``Args:``
            |  schema:{
            |         "<SOURCE>": {
            |             "<DATATYPE>": {
            |                 "<FIELD_NAME>": {
            |                 "type": "text | integer | object",
            |                 "description": "string", (Min=1, Max=100)
            |                 },
            |                 ... other fields
            |             }
            |             ... other Data types
            |         }
            |         ... other Sources
            |     }

        ``Returns:``
            |  {
            |      'Source':source_list,
            |      'Datatype': datatype_list,
            |      'Field Name':field_name_list,
            |      'Field Description':field_desc_list,
            |      'Field Type': field_type_list
            |  }


        :meta private:
        """
        reformed_dict = {}
        source_list = []
        data_type_list = []
        field_name_list = []
        field_description_list = []
        field_type_list = []
        is_curated_list = []
        is_array_list = []
        for outer_key, inner_dict_datatype in nested_schema_dict.items():
            for middle_key, inner_dict_fields in inner_dict_datatype.items():
                for inner_key, field_values in inner_dict_fields.items():
                    source_list.append(outer_key)
                    data_type_list.append(middle_key)
                    field_name_list.append(inner_key)
                    for key, value in field_values.items():
                        if key == "description":
                            field_description_list.append(field_values[key])
                        if key == "type":
                            field_type_list.append(field_values[key])
                        if key == "is_curated":
                            is_curated_list.append(field_values[key])
                        if key == "is_array":
                            is_array_list.append(field_values[key])

        reformed_dict["Source"] = source_list
        reformed_dict["Datatype"] = data_type_list
        reformed_dict["Field Name"] = field_name_list
        reformed_dict["Field Description"] = field_description_list
        reformed_dict["Field Type"] = field_type_list
        if is_curated_list:
            reformed_dict["Is Curated"] = is_curated_list
        reformed_dict["Is Array"] = is_array_list

        return reformed_dict

    def _nested_dict_to_df(self, schema_dict: dict) -> pd.DataFrame:
        """
        Convert flatten dict into df and print it

        ``Args:``
            |  {
            |      'Source':source_list,
            |      'Datatype': datatype_list,
            |      'Field Name':field_name_list,
            |      'Field Description':field_desc_list,
            |      'Field Type': field_type_list
            |  }

        ``Returns:``
            DataFrame

        :meta private:
        """
        pd.options.display.max_columns = None
        pd.options.display.width = None
        multiIndex_df = pd.DataFrame.from_dict(schema_dict, orient="columns")
        # sort Field Name in an ascending order
        multiIndex_df.sort_values(by=["Field Name"], inplace=True, ignore_index=True)
        return multiIndex_df

    def _format_type(self, data: dict) -> dict:
        """
        Format the dict data

        :meta private:
        """
        if data and isinstance(data, Dict):
            return json.dumps(data, indent=4)

    @Track.track_decorator
    def validate_schema(self, body: dict) -> dict:
        """Validate the payload of the schema.
        If there are errors schema in schema, then table of errors are printed
        If there are no errors in the schema, success message is printed
        Payload Format
        {
            "data":{
                "type": <type_val>,
                "id": <id_val>,
                "attributes":{
                    "repo_id":<repo_id_val>,
                    "schema_type":<schema_type_val>,
                    "schema":{
                        <schema_val>
                    }
                }
            }
        }

        Args:
            body (dict): payload of the schema

        Raises:
            paramException: if payload is not in correct format

        Returns:
            dict: Dataframe having all the errors in the schema
        """
        try:
            # validate repo key
            if "data" not in body:
                raise paramException(
                    title="Param Error",
                    detail="schema_dict not in correct format, data key not present."
                    + "Please recheck the schema dict format and values.",
                )
            if "attributes" not in body["data"]:
                raise paramException(
                    title="Param Error",
                    detail="schema_dict not in correct format, attributes key not present."
                    + "Please recheck the schema dict format and values.",
                )
            if "repo_id" not in body["data"]["attributes"]:
                raise paramException(
                    title="Param Error",
                    detail="schema_dict not in correct format, repo_id key not present."
                    + "Please recheck the schema dict format and values.",
                )
            repo_identifier = body.get("data", "").get("attributes", "").get("repo_id")

            # only repo_id allowed in payload, repo_name not allowed in payload
            omix_hlpr.verify_repo_identifier(repo_identifier)

            id = body.get("data", "").get("id", "")

            # check for similarity in id and repo_identifier passed in payload
            omix_hlpr.compare_repo_id_and_id(repo_identifier, id)

            # to check if repo_identifier is a valid repo_id
            # if an atlas is present for the repo_identifier then only
            # it is a valid repo_id
            self._get_omixatlas(repo_identifier)

            # validate schema attributes
            # there can be multiple sources and datatypes in an Omixatlas schema
            # schema will have multiple fields and each field
            # will have attributes
            if "schema" not in body["data"]["attributes"]:
                raise paramException(
                    title="Param Error",
                    detail="schema_dict not in correct format, schema key not present."
                    + "Please recheck the schema dict format and values.",
                )
            schema_dict = body.get("data", "").get("attributes", "").get("schema", "")
            errors_res_list = []
            # {"<src_1>":
            #       {"<dp1>":
            #           {"<field1>":{"<attribiutes>"}
            #           ...multiple fields
            #           }
            #           ...multiple dps
            #       }
            #       ...multiple sources
            # }
            for source, datatype in schema_dict.items():
                for datatype_key, datatype_val in datatype.items():
                    error_res = check_schema_for_errors(
                        datatype_val, source, datatype_key
                    )
                    errors_res_list.append(error_res)

            error_res_combined = helpers.merge_dataframes_from_list(errors_res_list)
            if error_res_combined.empty:
                print("Schema has no errors")
            else:
                print(
                    "Schema update didn’t go through because there’s a mistake in the schema. "
                    + "That mistake is summarised in the table below: "
                )
                print(
                    tabulate(error_res_combined, headers="keys", tablefmt="fancy_grid")
                )
            return error_res_combined
        except Exception as err:
            raise err

    def _compare_repo_key_and_repo_id(self, repo_key: str, id: str):
        """Compare repo_key in params and repo_id in the payload
        if repo_key is repo_id => check the equality of repo_key and repo_id
        if repo_key is repo_name => fetch repo_id for the repo and then check equality

        Args:
            repo_key (str): repo_id/repo_name for the repository
            repo_id (str): repo_id in the payload
        """
        repo_id = ""
        if repo_key.isdigit():
            # repo_key is repo_id
            repo_id = repo_key
        else:
            # repo key is repo name
            # fetch the repo id
            repo_data = self._get_omixatlas(repo_key)
            repo_id = repo_data["data"]["attributes"]["repo_id"]

        if repo_id != id:
            raise paramException(
                title="Param Error",
                detail="repo_key passed in the param and repo_id in the payload does not match. ",
            )

    @Track.track_decorator
    def insert_schema(self, repo_key, body: dict):
        """
        This function is used to insert the Schema in a newly created OmixAtlas.
        In order to insert schema the user must be a Data Admin at the resource level.
        Please contact polly@support.com if you get Access Denied error message.
        Args:
            repo_key (str/int, Optional): repo_id OR repo_name of the OmixAtlas. Users can  \
            get this by running `get_all_omixatlas` function. If not passed, taken from payload.
            body (dict):  The payload should be a JSON file for a specific table as per the structure defined for \
            schema.
        Raises:
            RequestException: Some Issue in Inserting the Schema for the OmixAtlas.
        """
        try:
            omix_hlpr.schema_param_check(repo_key, body)
            # validate payload
            error_df = self.validate_schema(body)
            # if there are no errors in the schema payload
            # which means error df is empty then only proceed
            # with schema insert/update/replace operation
            if error_df.empty:
                repo_id = body.get("data").get("attributes").get("repo_id")
                repo_key = omix_hlpr.make_repo_id_string(repo_key)
                self._compare_repo_key_and_repo_id(repo_key, repo_id)
                schema_base_url = f"{self.discover_url}/repositories"
                schema_url = f"{schema_base_url}/{repo_key}/schemas"
                body = json.dumps(body)
                resp = self.session.post(schema_url, data=body)
                error_handler(resp)
                if resp.status_code == http_codes.CREATED:
                    print(const.SCHEMA_INSERT_SUCCESS)
        except Exception as err:
            raise err

    @Track.track_decorator
    def update_schema(self, repo_key, body: dict):
        """
        This function is used to update the schema of an existing OmixAtlas.
        If the user wants to edit a field or its attribute in existing schema or if they want to
        add or delete new fields or if they want add a new source or datatype then they should use
        update schema function.\
        Using update_schema, users can:\
            ADD new source or datatypes in the schema\
            ADD a new field to a source+data_type combination\
            UPDATE attributes of an existing field\
            However, using update_schema, users can't perform DELETE operations on any field, source or datatype.\
        A message will be displayed on the status of the operation.\
        In order to update schema the user must be a Data Admin at the resource level.\
        Please contact polly@support.com if you get Access Denied error message.\
        For more information, see
        https://docs.elucidata.io/polly-python/OmixAtlas/Schema Management.html#change-schema-in-an-existing-atlas
        Args:
            repo_key (str/int, Optional): repo_id OR repo_name of the OmixAtlas. Users can  \
            get this by running get_all_omixatlas function. If not passed, taken from payload.
            body (dict): The payload should be a JSON file for a specific table as per the structure defined for \
            schema.
        Raises:
            RequestException: Some Issue in Updating the Schema for the OmixAtlas.
            paramException: Parameter Functions are not passed correctly.
        """

        try:
            omix_hlpr.schema_param_check(repo_key, body)
            # validate payload
            error_df = self.validate_schema(body)
            # if there are no errors in the schema payload
            # which means error df is empty then only proceed
            # with schema insert/update/replace operation
            if error_df.empty:
                repo_id = body.get("data").get("attributes").get("repo_id")
                repo_key = omix_hlpr.make_repo_id_string(repo_key)
                self._compare_repo_key_and_repo_id(repo_key, repo_id)

                schema_type = body.get("data").get("attributes").get("schema_type")
                schema_base_url = f"{self.discover_url}/repositories"
                schema_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}"
                body = json.dumps(body)
                resp = self.session.patch(schema_url, data=body)
                error_handler(resp)
                # converting requests output to JSON
                resp = resp.json()
                schema_update_verdict = (
                    resp.get("data", {})
                    .get("attributes", {})
                    .get("schema_update_verdict", "")
                )
                # There are 3 cases for schema updation
                # In case 1 -> if user changes attributes in the field
                # other than `original_name`, `type`, `is_array`, `is_keyword`
                # `is_searchable`
                # In those cases -> schema update is performed instantly
                # In the schema_update_verdict key -> value is none

                # In case 2 -> If user renames a field or drops a field
                # from the schema -> then schema updation job happens
                # In the schema_update_verdict key -> value is schema_update

                # In case 3 -> if for any field 1 of
                # `is_searchable`
                # `original_name`, `type`, `is_array`, `is_keyword` is changed
                # or a source or datatype is added or renamed or dropped
                # schema reingestion job takes place
                # In the schema_update_verdict key -> value is reingestion

                # SCHEMA_VERDICT_DICT
                # {"schema_update": SCHEMA_UPDATE_SUCCESS, "no_change": SCHEMA_NO_CHANGE_SUCCESS,
                # "reingeston": SCHEMA_REINGEST_SUCCESS}
                # if schema_update_verdict from API matches any of the keys in the dict then
                # its corresponding value will be printed

                schema_update_verdict_val = const.SCHEMA_VERDICT_DICT.get(
                    schema_update_verdict, ""
                )
                if schema_update_verdict_val:
                    print(schema_update_verdict_val)
                else:
                    print(const.SCHEMA_UPDATE_GENERIC_MSG)
        except Exception as err:
            raise err

    @Track.track_decorator
    def replace_schema(self, repo_key, body: dict):
        """
        The function will completely replace existing schema with the new schema passed in the body.\
        A message will be displayed on the status of the operation.\
        Completely REPLACE the existing schema with the one provided, so it can do all the \
        ops (including deletion of fields if they are no longer present in the new incoming schema).\
        In order to replace schema the user must be a Data Admin at the resource level.\
        Please contact polly@support.com if you get Access Denied error message.\
        For more information, see
        https://docs.elucidata.io/polly-python/OmixAtlas/Schema Management.html#change-schema-in-an-existing-atlas
        Args:
            repo_key (str/int, optional): repo_id OR repo_name of the OmixAtlas. Users can  \
            get this by running get_all_omixatlas function. If not passed, taken from payload.
            body (dict): The payload should be a JSON file for a specific table as per the structure defined for schema.
        Raises:
            RequestException: Some Issue in Replacing the Schema for the OmixAtlas.
            paramException: Parameter Functions are not passed correctly.
        """
        try:
            omix_hlpr.schema_param_check(repo_key, body)
            # validate payload
            error_df = self.validate_schema(body)
            # if there are no errors in the schema payload
            # which means error df is empty then only proceed
            # with schema insert/update/replace operation
            if error_df.empty:
                repo_id = body.get("data").get("attributes").get("repo_id")
                repo_key = omix_hlpr.make_repo_id_string(repo_key)
                self._compare_repo_key_and_repo_id(repo_key, repo_id)

                schema_type = (
                    body.get("data", "").get("attributes", "").get("schema_type", "")
                )
                body = json.dumps(body)
                schema_base_url = f"{self.discover_url}/repositories"
                schema_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}"
                resp = self.session.put(schema_url, data=body)
                error_handler(resp)
                # converting requests output to JSON
                resp = resp.json()
                schema_update_verdict = (
                    resp.get("data", {})
                    .get("attributes", {})
                    .get("schema_update_verdict", "")
                )
                # There are 3 cases for schema updation
                # In case 1 -> if user changes attributes in the field
                # other than `original_name`, `type`, `is_array`, `is_keyword`
                # `is_searchable`
                # In those cases -> schema update is performed instantly
                # In the schema_update_verdict key -> value is none

                # In case 2 -> If user renames a field or drops a field
                # from the schema -> then schema updation job happens
                # In the schema_update_verdict key -> value is schema_update

                # In case 3 -> if for any field 1 of
                # `is_searchable`
                # `original_name`, `type`, `is_array`, `is_keyword` is changed
                # or a source or datatype is added or renamed or dropped
                # schema reingestion job takes place
                # In the schema_update_verdict key -> value is reingestion

                # SCHEMA_VERDICT_DICT
                # {"schema_update": SCHEMA_UPDATE_SUCCESS, "no_change": SCHEMA_NO_CHANGE_SUCCESS,
                # "reingeston": SCHEMA_REINGEST_SUCCESS}
                # if schema_update_verdict from API matches any of the keys in the dict then
                # its corresponding value will be printed

                schema_update_verdict_val = const.SCHEMA_VERDICT_DICT.get(
                    schema_update_verdict, ""
                )
                if schema_update_verdict_val:
                    print(schema_update_verdict_val)
                else:
                    print(const.SCHEMA_UPDATE_GENERIC_MSG)
        except Exception as err:
            raise err

    @Track.track_decorator
    def download_data(self, repo_name, _id: str, internal_call=False):
        """
        To download any dataset, the following function can be used to get the signed URL of the dataset.
        The data can be downloaded by clicking on this URL.
        NOTE: This signed URL expires after 60 minutes from when it is generated.

        The repo_name OR repo_id of an OmixAtlas can be identified by calling the get_all_omixatlas() function.
        The dataset_id can be obtained by querying the metadata at the dataset level using query_metadata().

        This data can be parsed into a data frame for better accessibility using the code under the examples section.
        Args:
              repo_key (str): repo_id OR repo_name. This is a mandatory field.
              payload (dict): The payload is a JSON file which should be as per the structure defined for schema.
              Only data-admin will have the authentication to update the schema.
              internal_call (bool): True if being called internally by other functions. Default is False
        Raises:
              apiErrorException: Params are either empty or its datatype is not correct or see detail.
        """
        if not internal_call:
            # if not an internal call and is called directly, we show deprecation msg
            warnings.simplefilter("always", DeprecationWarning)
            warnings.formatwarning = (
                lambda msg, *args, **kwargs: f"DeprecationWarning: {msg}\n"
            )
            warnings.warn(
                "This method will soon be deprecated. Please use new function download_dataset for downloading"
                + " data files directly.\nFor usage: help(<omixatlas_object>.download_dataset) \n"
                + "For more details: "
                + "https://docs.elucidata.io/polly-python/OmixAtlas/Download%20Data.html#omixatlas.OmixAtlas.download_dataset"
            )
        url = f"{self.resource_url}/{repo_name}/download"
        params = {"_id": _id}
        response = self.session.get(url, params=params)
        error_handler(response)
        return response.json()

    @Track.track_decorator
    def save_to_workspace(
        self, repo_id: str, dataset_id: str, workspace_id: int, workspace_path: str
    ) -> json:
        """
        Function to download a dataset from OmixAtlas and save it to Workspaces.
        Args:
             repo_id (str): repo_id of the Omixatlas
             dataset_id (str): dataset id that needs to be saved
             workspace_id (int): workspace id in which the dataset needs to be saved
             workspace_path (str): path where the workspace resides
        Returns:
             json: Info about workspace where data is saved and of which Omixatlas
        """
        url = f"{self.resource_url}/workspace_jobs"
        params = {"action": "copy"}
        payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "dataset_id": dataset_id,
                    "repo_id": repo_id,
                    "workspace_id": workspace_id,
                    "workspace_path": workspace_path,
                },
            }
        }
        response = self.session.post(url, data=json.dumps(payload), params=params)
        error_handler(response)
        if response.status_code == 200:
            logging.basicConfig(level=logging.INFO)
            logging.info(f"Data Saved to workspace={workspace_id}")
        return response.json()

    @Track.track_decorator
    def format_converter(self, repo_key: str, dataset_id: str, to: str) -> None:
        """
        Function to convert a file format.
        Args:
            repo_key (str) : repo_id.
            dataset_id (str) : dataset_id.
            to (str) : output file format.
        Raises:
            InvalidParameterException : invalid value of any parameter for example like - repo_id/repo_name.
            paramException : Incompatible or empty value of any parameter
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_id/repo_name")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (to and isinstance(to, str)):
            raise InvalidParameterException("convert_to")
        ssl._create_default_https_context = ssl._create_unverified_context
        response_omixatlas = self._get_omixatlas(repo_key)
        data = response_omixatlas.get("data").get("attributes")
        repo_name = data.get("repo_name")
        index_name = data.get("v2_indexes", {}).get("files")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{self.elastic_url}/{index_name}/_search"
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"_index": index_name}},
                        {"term": {"dataset_id.keyword": dataset_id}},
                    ]
                }
            }
        }
        data_type = helpers.get_data_type(self, elastic_url, query)
        if data_type in DATA_TYPES:
            mapped_list = DATA_TYPES[data_type][0]
            if to in mapped_list["format"]:
                supported_repo = mapped_list["supported_repo"]
                repo_found = False
                for details in supported_repo:
                    if repo_name == details["name"]:
                        header_mapping = details["header_mapping"]
                        repo_found = True
                if not repo_found:
                    raise paramException(
                        title="Param Error",
                        detail=f"Incompatible repository error: Repository:'{repo_name}' not yet \
                                 incorporated for converter function",
                    )
                helpers.file_conversion(self, repo_name, dataset_id, to, header_mapping)
            else:
                raise paramException(
                    title="Param Error",
                    detail=f"Incompatible dataformat error: data format= {to} not yet incorporated for converter function",
                )
        else:
            raise paramException(
                title="Param Error",
                detail=f"Incompatible dataype error: data_type={data_type} not yet incorporated for converter function",
            )
        logging.basicConfig(level=logging.INFO)
        logging.info("File converted successfully!")

    @Track.track_decorator
    def create(
        self,
        display_name: str,
        description: str,
        repo_name="",
        image_url="",
        components=[],
        category="private",
        data_type=None,
        org_id="",
    ) -> pd.DataFrame:
        """
        This function is used to create a new omixatlas. \
        The arguments category, data_type and org_id can only be set during creation of Omixatlas and cannot be \
        updated afterwards.
        Args:
            display_name (str): Display name of the omixatlas as shown on the GUI.
            description (str): description of the omixatlas.
            repo_name (str, optional): repo_name which is used to create index in database.
            image_url (str, optional): URL of the image which should be kept as the icon for omixatlas.
            components (list, optional): Optional Parameter.
            category (str, optional): Optional parameter(public/private/diy_poa).Immutable argument. \
            By default it is private.
            data_type (str, optional): Optional Parameter(single_cell/rna_seq).Immutable argument. \
            By default it is None. If category is `public` or `diy_poa` then `data_type` is mandatory.
            org_id (str, optional): Optional Parameter. Org Id is mandatory to be passed when category \
            of omixatlas is `diy_poa`. Org Id can be found on admin panel.
        Returns:
            Dataframe after creation of omixatlas.
        Raises:
            ValueError: Repository creation response is in Incorrect format.
        """
        try:
            omix_hlpr.check_create_omixatlas_parameters(
                display_name,
                description,
                repo_name,
                image_url,
                components,
                category,
                data_type,
                org_id,
            )
            payload = self._get_repository_payload()
            frontend_info = {}
            frontend_info["description"] = description
            frontend_info["display_name"] = display_name
            frontend_info["icon_image_url"] = (
                image_url if image_url else const.IMAGE_URL_ENDPOINT
            )

            if not repo_name:
                repo_name = self._create_repo_name(display_name)
            else:
                repo_name = repo_name

            payload["data"]["attributes"]["repo_name"] = repo_name
            payload["data"]["attributes"]["category"] = category
            if data_type:
                payload["data"]["attributes"]["data_type"] = data_type
            if org_id:
                payload["data"]["attributes"]["org_id"] = org_id
            payload["data"]["attributes"]["frontend_info"] = frontend_info
            payload["data"]["attributes"]["components"] = components
            indexes = payload["data"]["attributes"]["indexes"]

            for key in indexes.keys():
                indexes[key] = f"{repo_name}_{key}"

            repository_url = f"{self.resource_url}"
            resp = self.session.post(repository_url, json=payload)
            error_handler(resp)

            if resp.status_code != const.CREATED:
                raise Exception(resp.text)
            else:
                if resp.json()["data"]["id"]:
                    repo_id = resp.json()["data"]["id"]
                    print(f" OmixAtlas {repo_id} Created  ")
                    return self._repo_creation_response_df(resp.json())
                else:
                    ValueError("Repository creation response is in Incorrect format")
        except Exception as err:
            raise err

    @Track.track_decorator
    def update(
        self,
        repo_key: str,
        display_name="",
        description="",
        image_url="",
        workspace_id="",
        components=[],
    ) -> pd.DataFrame:
        """
        This function is used to update an omixatlas.
        Args:
             repo_key (str/int): repo_name/repo_id for that Omixatlas
             display_name (str, optional): Display name of the omixatlas as shown on the GUI.
             description (str, optional): Description of the omixatlas.
             image_url (str, optional): URL of the image which should be kept as the icon for omixatlas.
             workspace_id (str, optional): ID of the Workspace to be linked to the Omixatlas.
             components (list, optional): List of components to be added.
        """

        omix_hlpr.check_update_omixatlas_parameters(
            display_name,
            description,
            repo_key,
            image_url,
            components,
            workspace_id,
        )

        if isinstance(repo_key, int):
            repo_key = omix_hlpr.make_repo_id_string(repo_key)

        if workspace_id:
            self._link_workspace_to_omixatlas(repo_key, workspace_id)

        repo_curr_data = self._get_omixatlas(repo_key)

        if "attributes" not in repo_curr_data["data"]:
            raise invalidDataException(
                detail="OmixAtlas is not created properly. Please contact admin"
            )

        attribute_curr_data = repo_curr_data["data"]["attributes"]
        if components:
            curr_components = attribute_curr_data.get("components", [])
            for item in components:
                curr_components.append(item)

        repo_curr_data["data"]["attributes"] = attribute_curr_data

        if "frontend_info" not in repo_curr_data["data"]["attributes"]:
            raise invalidDataException(
                detail="OmixAtlas is not created properly. Please contact admin"
            )

        frontendinfo_curr_data = repo_curr_data["data"]["attributes"]["frontend_info"]
        repo_curr_data["data"]["attributes"][
            "frontend_info"
        ] = self._update_frontendinfo_value(
            frontendinfo_curr_data, image_url, description, display_name
        )

        repository_url = f"{self.resource_url}/{repo_key}"
        resp = self.session.patch(repository_url, json=repo_curr_data)
        error_handler(resp)
        if resp.status_code != const.OK:
            raise Exception(resp.text)
        else:
            if resp.json()["data"]["id"]:
                repo_id = resp.json()["data"]["id"]
                print(f" OmixAtlas {repo_id} Updated  ")
                return self._repo_creation_response_df(resp.json())
            else:
                ValueError("Repository Updation response is in Incorrect format")

    def _link_workspace_to_omixatlas(self, repo_key: str, workspace_id: str):
        """
        Link a workspace ID given by the user to an OmixAtlas. Called by the update() function.
        Args:
            repo_key (str): repo_name/repo_id for that Omixatlas
            workspace_id (str): ID of the Workspace to be linked to the Omixatlas
        """
        url = f"{self.discover_url}/repositories/{repo_key}"
        get_response = self.session.get(url)
        get_response = get_response.json()
        get_response["data"]["attributes"]["linked_workspace_id"] = workspace_id
        get_response["data"]["attributes"].pop("repo_name")
        patch_response = self.session.patch(url, data=json.dumps(get_response))
        error_handler(patch_response)
        if patch_response.status_code != const.OK:
            raise Exception(patch_response.text)
        else:
            if patch_response.json()["data"]["id"]:
                repo_id = patch_response.json()["data"]["id"]
                print(f" Workspace ID {workspace_id} linked with OmixAtlas {repo_id}")
            else:
                ValueError("Repository Updation response is in Incorrect format")

    def _construct_metadata_dict_from_files(
        self,
        repo_id: str,
        metadata_file_list: list,
        priority: str,
        destination_folder_path: str,
        data_metadata_mapping: dict,
        metadata_path: str,
        update: str,
    ) -> dict:
        """
        Construct metadata dictionary from metadata file path
        """
        combined_metadata_dict = {}
        # loop over files and append into a single dict
        for file in tqdm(
            metadata_file_list,
            desc="Processing Metadata files",
        ):
            file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
            with open(file_path, "r") as file_to_upload:
                res_dict = json.load(file_to_upload)
                metadata_file_name_for_upload = file
            modified_metadata_dict = {}
            # format the actual metadata according the pre-defined
            # upload format specified for metadata file
            # more information about it -> Technical Proposal Ingestion APIs
            # Link in the function doc
            modified_metadata_dict = self._format_metadata_dict(
                repo_id,
                res_dict,
                destination_folder_path,
                metadata_file_name_for_upload,
                data_metadata_mapping,
                update,
            )
            # added check: modified_metadata_dict could be empty in case
            # no metadata file is being updated.
            if modified_metadata_dict:
                if "data" in combined_metadata_dict.keys():
                    combined_metadata_dict["data"].append(modified_metadata_dict)
                else:
                    combined_metadata_dict["data"] = [modified_metadata_dict]

        # fetch ingestion level metadata if we have combined metadata dict/metadata
        # files to upload
        # adding the ingestion level data only if the combined_metadata_dict has data info,
        # else return empty dict (case where no data/metadata is being updated)
        final_combined_metadata_dict = {}
        if "data" in combined_metadata_dict.keys():
            final_combined_metadata_dict = self._insert_ingestion_level_dict(
                priority, combined_metadata_dict
            )
        # clearing cache for list of files in OA once we have looped through
        # all the files needed to be updated in the metadata folder.
        self._list_files_in_oa.cache_clear()
        return final_combined_metadata_dict

    def _parameter_check_for_add_dataset(
        self,
        repo_id: int,
        source_folder_path: dict,
        destination_folder_path: str,
        priority: str,
    ):
        """
        Sanity check for parameters in add dataset function
        """
        try:
            omix_hlpr.parameter_check_for_repo_id(repo_id)
            omix_hlpr.data_metadata_parameter_check(source_folder_path)
            omix_hlpr.data_metadata_file_ext_check(source_folder_path)
            omix_hlpr.check_data_metadata_file_path(source_folder_path)
            if not isinstance(destination_folder_path, str):
                raise paramException(
                    title="Param Error",
                    detail="`destination_folder_path` should be a string",
                )
            omix_hlpr.parameter_check_for_priority(priority)
        except Exception as err:
            raise err

    def _upload_file_to_s3(
        self, aws_cred: dict, bucket_name: str, file_path: str, object_key: str
    ):
        """
        This function is used to upload file in S3 bucket.
        Args:
            | aws_cred(dict): Dictionary which includes session tokens for authorisation.
            | bucket_name(str): Name of the bucket where file should be uploaded.
            | file_path(str): Specifies file path.
            | object_key(str): Directory path in S3.
        """
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_cred.get("access_key"),
            aws_secret_access_key=aws_cred.get("secret_access_key"),
            aws_session_token=aws_cred.get("session_token"),
        )
        # Transfer config is the configuration class for enabling
        # multipart upload on S3. For more information, please refer -
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig
        file_size = float(os.path.getsize(file_path))
        multipart_chunksize = const.MULTIPART_CHUNKSIZE_SMALL_FILE_SIZE
        io_chunksize = const.IO_CHUNKSIZE_SMALL_FILE_SIZE

        if file_size > const.SMALL_FILE_SIZE and file_size <= const.MEDIUM_FILE_SIZE:
            multipart_chunksize = const.MULTIPART_CHUNKSIZE_MEDIUM_FILE_SIZE
            io_chunksize = const.IO_CHUNKSIZE_MEDIUM_FILE_SIZE
        elif file_size > const.MEDIUM_FILE_SIZE:
            multipart_chunksize = const.MULTIPART_CHUNKSIZE_LARGE_FILE_SIZE
            io_chunksize = const.IO_CHUNKSIZE_LARGE_FILE_SIZE

        config = TransferConfig(
            multipart_threshold=const.MULTIPART_THRESHOLD,
            max_concurrency=const.MAX_CONCURRENCY,
            multipart_chunksize=multipart_chunksize,
            io_chunksize=io_chunksize,
            use_threads=True,
        )

        try:
            s3_client.upload_file(file_path, bucket_name, object_key, Config=config)
        except Exception as err:
            raise err

    def _data_files_for_upload(
        self,
        repo_id: str,
        source_data_path: str,
        data_metadata_mapping: dict,
        destination_folder_path: str,
        update: str,
    ) -> list:
        """Find List of all the metadata files to be uploaded

        Args:
            repo_id (str): repo_id of omixatlas
            source_data_path (str): source data path containing data files
            data_metadata_mapping (dict): data metadata files mapping dict
            destination_folder_path (str) : destination folder path

        Returns:
            list: List of data files which are to be uploaded
        """
        data_directory = os.fsencode(source_data_path)
        data_file_list = []
        for file in os.listdir(data_directory):
            file = file.decode("utf-8")
            # skip hidden files
            if not file.startswith("."):
                # in case of updating datasets -> metadata file may not be given
                # by the user. If metadata file not given by the user
                # Checking if metadata file present in OA from before or not

                if file not in data_metadata_mapping.values():
                    # if data file is not having a metadata in the folder, searching for the
                    # file in the OA
                    # if not then warning is thrown to user and skips the file update
                    # Step 1 is before the if conditon because it is common for both if and else
                    corresponding_data_file_names = (
                        self._get_data_file_from_oa_for_metadata_update(repo_id, file)
                    )
                    # Step 2 : from matching file list, get file present in the same dest folder in
                    # OA as provided by the user
                    possible_corresponding_file_in_oa = (
                        omix_hlpr.get_possible_file_from_matching_filename_list_from_oa(
                            corresponding_data_file_names, file, destination_folder_path
                        )
                    )
                    if not possible_corresponding_file_in_oa:
                        continue
                    data_file_list.append(file)
                elif file in data_metadata_mapping.values() and update:
                    # Step 1 is before the if conditon because it is common for both if and else
                    corresponding_data_file_names = (
                        self._get_data_file_from_oa_for_metadata_update(repo_id, file)
                    )
                    # add the condition for checking if destination folder correct
                    # in case of `update_datasets`
                    # destination folder is passed by the user for updating the data file
                    # the destination folder also can be passed wrong, in that case
                    # raise a warning and skip the file
                    # Step 1 to fetch the files from OA from corresponding data file names
                    # will be fetched that is the destination_folder is before if condition
                    # using the corresponding_data_file_names here even if file is
                    # present in the mapping dict because
                    # destination_folder name is required here which is present in s3
                    # that is what we want to check here if that is right or not
                    # till we don't fetch files from OA
                    # there is no way to know the corresponding destination folder
                    # for the data metadata file pair in the OA
                    is_destination_folder_correct = (
                        omix_hlpr.check_if_destination_folder_correct(
                            corresponding_data_file_names,
                            file,
                            destination_folder_path,
                        )
                    )
                    if not is_destination_folder_correct:
                        continue
                    data_file_list.append(file)
                else:
                    data_file_list.append(file)
        self._list_files_in_oa.cache_clear()
        return data_file_list

    def _upload_data(
        self,
        repo_id: str,
        data_upload_details: dict,
        data_source_folder_path: str,
        destination_folder_path: str,
        file_status_dict: dict,
        final_data_metadata_mapping_dict: dict,
        update=False,
    ) -> dict:
        """
        This function loops in data directory and upload each file to S3 sequentionally.
        Args:
            | repo_id(str/int): Repo Id to which files must be uploaded.
            | data_upload_details(dict): Details for S3 authorisation.
            | data_source_folder_path(str): Specifies file path.
            | destination_folder_path(str): Specified file path in S3 bucket.
            | file_status_dict(dict): Stores file name and it's status of upload.
        """

        # list of data files to be uploaded
        data_file_list = self._data_files_for_upload(
            repo_id,
            data_source_folder_path,
            final_data_metadata_mapping_dict,
            destination_folder_path,
            update,
        )

        # filter data files whose metadata not getting uploaded
        data_file_list = omix_hlpr.filter_data_files_whose_metadata_not_uploaded(
            data_file_list, final_data_metadata_mapping_dict
        )

        for file in tqdm(data_file_list, desc="Uploading data files", unit="files"):
            file_path = str(Path(data_source_folder_path) / Path(os.fsdecode(file)))
            data_file_name_for_upload = file
            try:
                self._upload_file_to_s3(
                    data_upload_details["session_tokens"],
                    data_upload_details["bucket_name"],
                    file_path,
                    data_upload_details["package_name"] + data_file_name_for_upload,
                )
                file_status_dict[data_file_name_for_upload] = const.UPLOAD_URL_CREATED
            # TO-DO: Raise exceptions for access denied or resource not found.
            # In all other cases retrials to upload other files should happen.
            except Exception as err:
                if isinstance(err, S3UploadFailedError) and const.EXPIRED_TOKEN in str(
                    err
                ):
                    (
                        session_tokens,
                        bucket_name,
                        package_name,
                        metadata_directory,
                    ) = self._get_session_tokens(repo_id, destination_folder_path)

                    data_upload_details = {
                        "session_tokens": session_tokens,
                        "bucket_name": bucket_name,
                        "package_name": package_name,
                    }
                    self._upload_file_to_s3(
                        data_upload_details["session_tokens"],
                        data_upload_details["bucket_name"],
                        file_path,
                        data_upload_details["package_name"] + data_file_name_for_upload,
                    )
                    file_status_dict[
                        data_file_name_for_upload
                    ] = const.UPLOAD_URL_CREATED
                else:
                    file_status_dict[
                        data_file_name_for_upload
                    ] = const.UPLOAD_ERROR_CODE
                    raise err
        return file_status_dict

    def _map_data_metadata_files(self, source_folder_path: dict):
        """
        Map data and metadata file names and create a dict and return
        If for a data file name, there is not metadata file raise an error
        """
        # checking if folders are empty
        try:
            data_source_folder_path = source_folder_path["data"]
            data_directory = os.fsencode(data_source_folder_path)
            data_file_names = os.listdir(data_directory)
            data_file_names_str = []
            data_file_names_str = omix_hlpr.create_file_name_with_extension_list(
                data_file_names
            )
            metadata_source_folder_path = source_folder_path["metadata"]
            metadata_directory = os.fsencode(metadata_source_folder_path)
            metadata_file_names = os.listdir(metadata_directory)
            metadata_file_names_str = []
            # convert metadata file names from bytes to strings
            metadata_file_names_str = omix_hlpr.create_file_name_with_extension_list(
                metadata_file_names, file_ext_req=False
            )
            (
                data_metadata_mapping_dict,
                unmapped_data_file_names,
                unmapped_metadata_file_names,
            ) = omix_hlpr.data_metadata_file_dict(
                metadata_file_names_str, data_file_names_str
            )

            final_data_metadata_mapping_dict = (
                omix_hlpr.data_metadata_file_mapping_conditions(
                    unmapped_data_file_names,
                    unmapped_metadata_file_names,
                    data_metadata_mapping_dict,
                )
            )
            return final_data_metadata_mapping_dict
        except Exception as err:
            raise err

    def _upload_metadata(
        self,
        repo_id: str,
        priority: str,
        metadata_upload_details: dict,
        source_metadata_path: str,
        destination_folder_path: str,
        file_status_dict: dict,
        data_metadata_mapping: dict,
        validation_dataset_lvl: dict,
        update=False,
    ) -> dict:
        """
        This function loops in metadata directory, combines all the metadata
        into one file and upload in S3.
        Args:
            | repo_id(str/int): Repo Id to which files must be uploaded.
            | priority(str): Specifies the priority of upload.
            | metadata_upload_details(dict): Details for S3 authorisation.
            | source_metadata_path(str): Specifies file path.
            | destination_folder_path(str): Specified file path in S3 bucket.
            | file_status_dict(dict): Stores file name and it's status of upload.
            | data_metadata_mapping(dict): Specifies metadata name to corresponding file.
        """
        # Looping on metadata_path and fetching metadata files inside the
        # helper function as they all are going to be combined in
        # 1 file and then uploaded

        # fetch the list of metadata files to be uploaded
        metadata_file_list = omix_hlpr.metadata_files_for_upload(
            source_metadata_path,
        )

        validation_dataset_lvl_grouped = omix_hlpr.group_passed_and_failed_validation(
            validation_dataset_lvl
        )

        # apply validation layer on metadata files
        metadata_file_list = omix_hlpr.apply_validation_on_metadata_files(
            metadata_file_list, source_metadata_path, validation_dataset_lvl_grouped
        )

        if not metadata_file_list:
            # no metadata files in the list
            # return empty status dict
            return {}

        # format and combine list of metadata files
        combined_metadata_dict = self._construct_metadata_dict_from_files(
            repo_id,
            metadata_file_list,
            priority,
            destination_folder_path,
            data_metadata_mapping,
            source_metadata_path,
            update,
        )

        if not combined_metadata_dict:
            # no combined metadata file generated
            # no files to upload
            # return empty status dict
            return {}

        with TempDir() as metadata_dir:
            combined_metadata_file_path = str(
                f"{metadata_dir}/{Path(os.fsdecode(const.COMBINED_METADATA_FILE_NAME))}"
            )
            # opening file with `with` block closes the file at the end of with block
            # opening the file in w+ mode allows to both read and write files
            with open(combined_metadata_file_path, "w+") as combined_metadata_file:
                json.dump(combined_metadata_dict, combined_metadata_file, indent=4)

            try:
                self._upload_file_to_s3(
                    metadata_upload_details["session_tokens"],
                    metadata_upload_details["bucket_name"],
                    combined_metadata_file_path,
                    metadata_upload_details["metadata_directory"],
                )
                file_status_dict[
                    const.COMBINED_METADATA_FILE_NAME
                ] = const.UPLOAD_URL_CREATED
            except Exception as err:
                if isinstance(err, S3UploadFailedError) and const.EXPIRED_TOKEN in str(
                    err
                ):
                    (
                        session_tokens,
                        bucket_name,
                        package_name,
                        metadata_directory,
                    ) = self._get_session_tokens(repo_id, destination_folder_path)

                    # Update upload details
                    metadata_upload_details = {
                        "session_tokens": session_tokens,
                        "bucket_name": bucket_name,
                        "metadata_directory": metadata_directory,
                    }
                    self._upload_file_to_s3(
                        metadata_upload_details["session_tokens"],
                        metadata_upload_details["bucket_name"],
                        combined_metadata_file_path,
                        metadata_upload_details["metadata_directory"],
                    )
                    file_status_dict[
                        const.COMBINED_METADATA_FILE_NAME
                    ] = const.UPLOAD_URL_CREATED
                else:
                    file_status_dict[
                        const.COMBINED_METADATA_FILE_NAME
                    ] = const.UPLOAD_ERROR_CODE
                    raise err

            return file_status_dict

    def _get_session_tokens(self, repo_id: str, destination_folder_path: str) -> dict:
        """
        Get the upload session tokens for uploading the files to s3
        Args:
            | repo_id(str/int): repo_name/repo_id for that Omixatlas
            | destination_folder_path(str): Destination folder structure in s3
        """
        # post request for upload urls
        payload = const.GETTING_UPLOAD_URLS_PAYLOAD
        payload["data"]["attributes"]["folder"] = destination_folder_path

        # post request
        repository_url = f"{self.discover_url}/repositories/{repo_id}/files?tokens=true"
        resp = self.session.post(repository_url, json=payload)
        error_handler(resp)
        if resp.status_code != const.OK:
            raise Exception(resp.text)
        else:
            response_data = resp.json()
            session_tokens = {}
            bucket_name = (
                response_data.get("data", {}).get("attributes", {}).get("bucket_name")
            )
            package_name = (
                response_data.get("data", {}).get("attributes", {}).get("package_name")
            )
            metadata_directory = (
                response_data.get("data", {})
                .get("attributes", {})
                .get("metadata_directory")
            )
            session_tokens["access_key"] = (
                response_data.get("data", {})
                .get("attributes", {})
                .get("tokens", {})
                .get("AccessKeyId")
            )
            session_tokens["secret_access_key"] = (
                response_data.get("data", {})
                .get("attributes", {})
                .get("tokens", {})
                .get("SecretAccessKey")
            )
            session_tokens["session_token"] = (
                response_data.get("data", {})
                .get("attributes", {})
                .get("tokens", {})
                .get("SessionToken")
            )
            session_tokens["expiration_stamp"] = (
                response_data.get("data", {})
                .get("attributes", {})
                .get("tokens", {})
                .get("Expiration")
            )
        return session_tokens, bucket_name, package_name, metadata_directory

    def _commit_data_to_repo(self, repo_id: str):
        """
        Inform the infra to commit the data uploaded
        Not raising error in this if commit API Fails because
        even if manual commit fails, files will be picked up in
        automatic update. Users need not know about this
        Args:
            repo_id: str
        """
        try:
            schema_base_url = f"{self.discover_url}/repositories"
            url = f"{schema_base_url}/{repo_id}/files?action=commit"
            resp = self.session.post(url)
            error_handler(resp)
            # 202 is the success code for commit message success
            if resp.status_code == http_codes.ACCEPTED:
                print("\n")
                print(const.DATA_COMMIT_MESSAGE)
        except Exception:
            # no error needs to be raised
            # in case of error manual commit will not happen
            # data will be auto-committed which is the current process
            pass

    @Track.track_decorator
    def add_datasets(
        self,
        repo_id: int,
        source_folder_path: dict,
        destination_folder_path="",
        priority="low",
        validation=False,
    ) -> pd.DataFrame:
        """
        This function is used to add a new data into an OmixAtlas.
        Once user runs this function successfully, it takes 30 seconds to log the ingestion request and within 2 mins, the
        ingestion log will be shown in the data ingestion monitoring dashboard.
        In order to add datasets into Omixatlas the user must be a Data Contributor at the resource level.
        Please contact polly@support.com if you get Access Denied error message.
        Args:
            repo_id (int/str): repo_name/repo_id for that Omixatlas
            source_folder_path (dict): source folder paths from data and metadata files are fetched.In this \
            dictionary, there should be two keys called "data" and "metadata" with value consisting of folders where \
            data and metadata files are stored respectively i.e. {"data":"<data_path>", "metadata":"<metadata_path>"}
            destination_folder_path (str, optional): Destination folder structure in s3.\
            Users should use this only when they want to manage the folder structure in the backend. \
            It is advised to not not give any value for this, by default the data goes in root folder.
            priority (str, optional): Optional parameter(low/medium/high). \
            Priority at which this data has to be ingested into the OmixAtlas. \
            The default value is "low". Acceptable values are "medium" and "high".
            validation (bool, optional): Optional parameter(True/False) Users was to activate validation. By Default False. \
            Means validation not active by default. Validation needs to be activated only when \
            validated files are being ingested.
        Raises:
            paramError: If Params are not passed in the desired format or value not valid.
            RequestException: If there is issue in data ingestion.
        Returns:
            pd.DataFrame: DataFrame showing Upload Status of Files
        """
        try:
            # parameters check
            self._parameter_check_for_add_dataset(
                repo_id, source_folder_path, destination_folder_path, priority
            )
            validation_dataset_lvl = {}
            if validation:
                validation_dataset_lvl = omix_hlpr.check_status_file(source_folder_path)
            (
                session_tokens,
                bucket_name,
                package_name,
                metadata_directory,
            ) = self._get_session_tokens(repo_id, destination_folder_path)

            # folder paths
            data_source_folder_path = source_folder_path["data"]
            metadata_source_folder_path = source_folder_path["metadata"]

            # Upload details
            metadata_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "metadata_directory": metadata_directory,
            }
            data_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "package_name": package_name,
            }

            # data metadata file mapping
            data_metadata_mapping = self._map_data_metadata_files(source_folder_path)

            # list of list which will store all the results
            # at last assign it to a dataframe
            result_list = []
            file_status_dict = {}

            # upload metadata and data files
            file_status_dict = self._upload_metadata(
                repo_id,
                priority,
                metadata_upload_details,
                metadata_source_folder_path,
                destination_folder_path,
                file_status_dict,
                data_metadata_mapping,
                validation_dataset_lvl,
            )

            file_status_dict = self._upload_data(
                repo_id,
                data_upload_details,
                data_source_folder_path,
                destination_folder_path,
                file_status_dict,
                data_metadata_mapping,
            )
            # iterating the status dict
            # generating appropriate messages
            result_list = self._generating_response_from_status_dict(
                file_status_dict, result_list
            )

            # printing the dataframe
            data_upload_results_df = pd.DataFrame(
                result_list, columns=["File Name", "Message"]
            )

            # print message before delay
            print(const.WAIT_FOR_COMMIT)
            # delay added after the files are uploaded
            # before commit API is hit
            time.sleep(30)

            # informing infra to commit the uploaded data in the repository
            self._commit_data_to_repo(repo_id)

            with pd.option_context(
                "display.max_rows",
                800,
                "display.max_columns",
                800,
                "display.width",
                1200,
            ):
                print("\n", data_upload_results_df)

            if validation:
                print("\n")
                print("-----Files which are Not Validated-------")
                helpers.display_df_from_list(
                    omix_hlpr.dataset_level_metadata_files_not_uploaded,
                    "Invalid Metadata Files",
                )
                print("\n")
                helpers.display_df_from_list(
                    omix_hlpr.data_files_whose_metadata_failed_validation,
                    "Invalid Data Files",
                )
            # reset global variables storing validation results
            # flushes out the previous state of variables and creates
            # new state
            omix_hlpr.reset_global_variables_with_validation_results()

            return data_upload_results_df
        except Exception as err:
            raise err

    @Track.track_decorator
    def update_datasets(
        self,
        repo_id: int,
        source_folder_path: dict,
        destination_folder_path="",
        priority="low",
        validation=False,
    ) -> pd.DataFrame:
        """
        This function is used to update a new data into an OmixAtlas.
        Once user runs this function successfully, it takes 30 seconds to log the ingestion request and within 2 mins, the
        ingestion log will be shown in the data ingestion monitoring dashboard.
        In order to update datasets the user must be a Data Contributor at the resource level.
        Please contact polly@support.com if you get Access Denied error message.
        Args:
            repo_id (int/str): repo_name/repo_id for that Omixatlas
            source_folder_path (dict): source folder paths from data and metadata files are fetched.In this \
            dictionary, there should be two keys called "data" and "metadata" with value consisting of folders where \
            data and metadata files are stored respectively i.e. {"data":"<data_path>", "metadata":"<metadata_path>"}
            destination_folder_path (str, optional): Destination folder structure in s3. \
            Users should use this only when they want to manage the folder structure in the backend.\
            It is advised to not not give any value for this, by default the data goes in root folder.
            priority (str, optional): Optional parameter(low/medium/high).\
            Priority at which this data has to be ingested into the OmixAtlas. \
            The default value is "low". Acceptable values are "medium" and "high".
            validation(bool, optional): Optional parameter(True/False) Users was to activate validation. By Default False. \
            Means validation not active by default. Validation needs to be activated only when \
            validated files are being ingested.
        Raises:
            paramError: If Params are not passed in the desired format or value not valid.
            RequestException: If there is issue in data ingestion.
        Returns:
            pd.DataFrame: DataFrame showing Upload Status of Files
        """
        # parameters check
        try:
            self._parameter_check_for_update_dataset(
                repo_id, source_folder_path, destination_folder_path, priority
            )
            validation_dataset_lvl = {}
            # validation is active and metadata folder present
            if validation and source_folder_path.get("metadata"):
                validation_dataset_lvl = omix_hlpr.check_status_file(source_folder_path)
            (
                session_tokens,
                bucket_name,
                package_name,
                metadata_directory,
            ) = self._get_session_tokens(repo_id, destination_folder_path)

            # Upload details
            metadata_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "metadata_directory": metadata_directory,
            }
            data_upload_details = {
                "session_tokens": session_tokens,
                "bucket_name": bucket_name,
                "package_name": package_name,
            }

            # list of list which will store all the results
            # at last assign it to a dataframe
            result_list = []
            file_status_dict = {}

            # check destination folder passed is a valid destination folder
            # or not. If not then raise an error and halt the process
            # If destination_folder_path is empty then it is a valid
            # destination_folder_path -> no need to check for that
            if destination_folder_path:
                self._check_destination_folder(destination_folder_path, repo_id)

            # unmapped_file_names (list): data file names which are not mapped
            # unmapped_metadata_file_names (list): metadata file names which are not mapped
            # final_data_metadata_mapping_dict (dict): dict of data metadata mapping
            (
                final_data_metadata_mapping_dict,
                unmapped_file_names,
                unmapped_metadata_file_names,
            ) = self._map_data_metadata_files_for_update(source_folder_path)

            file_status_dict = self._update_metadata_data(
                repo_id,
                source_folder_path,
                file_status_dict,
                destination_folder_path,
                metadata_upload_details,
                data_upload_details,
                priority,
                final_data_metadata_mapping_dict,
                validation_dataset_lvl,
            )
        except Exception as err:
            raise err

        if file_status_dict:
            result_list = self._generating_response_from_status_dict(
                file_status_dict, result_list
            )

            # printing the dataframe
            data_upload_results_df = pd.DataFrame(
                result_list, columns=["File Name", "Message"]
            )

            # print message before delay
            print(const.WAIT_FOR_COMMIT)

            # delay added after the files are uploaded
            # before commit API is hit
            time.sleep(30)

            # informing infra to commit the uploaded data in the repository
            self._commit_data_to_repo(repo_id)

            with pd.option_context(
                "display.max_rows", None, "display.max_columns", None
            ):
                print("\n", data_upload_results_df)

            if validation:
                print("\n")
                print("-----Files which are Not Validated-------")
                helpers.display_df_from_list(
                    omix_hlpr.dataset_level_metadata_files_not_uploaded,
                    "Invalid Metadata Files",
                )
                print("\n")
                helpers.display_df_from_list(
                    omix_hlpr.data_files_whose_metadata_failed_validation,
                    "Invalid Data Files",
                )

            # reset global variables storing validation results
            # flushes out the previous state of variables and creates
            # new state
            omix_hlpr.reset_global_variables_with_validation_results()

            return data_upload_results_df

    def _check_destination_folder(self, destination_folder_path: str, repo_id: str):
        """Check if the destination folder passed in the parameter, if that is valid destination
        folder.
        Destination folder is a valid destination folder
        When it is returned as a response of list files API in OA in the file_id key
        Merely being a folder present in the s3 bucket of the OA does not make it valid
        destination folder.
        Args:
            destination_folder_path (str): destination folder passed
            repo_id(str): repo_id of the repository
        """
        list_oa_response = self._list_files_in_oa(repo_id)
        oa_data_files_list = []
        for response_data in list_oa_response:
            for item in response_data:
                file_id = item.get("id")
                oa_data_files_list.append(file_id)

        valid_folder_list = helpers.get_folder_list_from_list_of_filepaths(
            oa_data_files_list
        )

        if destination_folder_path not in valid_folder_list:
            raise paramException(
                title="Destination Folder passed does not exist",
                detail=(
                    "Destination folder passed does not exist. "
                    + "Either wrong destination folder passed for the existing data/metadata."
                    + f"Valid destination folders are {valid_folder_list} in this repository. "
                    + "Or data/metadata passed in update does not exist in this repository "
                    + "from before, in that case, please use the add_dataset functionality."
                ),
            )

    def _update_metadata_data(
        self,
        repo_id: str,
        source_folder_path: dict,
        file_status_dict: dict,
        destination_folder_path: str,
        metadata_upload_details: str,
        data_upload_details: str,
        priority: str,
        final_data_metadata_mapping_dict: dict,
        validation_dataset_lvl: dict,
    ) -> dict:
        """
        update data and metadata files (which ever applicable).
        internally calls the upload function for uploading the updated
        metadata/data files.


        Arguments:
            repo_id -- repo id
            source_folder_path -- dict of file path of metadata and data files
            file_status_dict -- dict of status of file uploads (empty initally)
            destination_folder_path
            metadata_upload_details -- upload urls
            data_upload_details -- upload urls
            priority
            final_data_metadata_mapping_dict -- map of metadata and data

        Returns:
            file_status_dict
        """
        # folder paths
        data_source_folder_path = source_folder_path.get("data", "")
        metadata_source_folder_path = source_folder_path.get("metadata", "")

        try:
            if metadata_source_folder_path:
                file_status_dict = self._upload_metadata(
                    repo_id,
                    priority,
                    metadata_upload_details,
                    metadata_source_folder_path,
                    destination_folder_path,
                    file_status_dict,
                    final_data_metadata_mapping_dict,
                    validation_dataset_lvl,
                    update=True,
                )

            if data_source_folder_path:
                file_status_dict = self._upload_data(
                    repo_id,
                    data_upload_details,
                    data_source_folder_path,
                    destination_folder_path,
                    file_status_dict,
                    final_data_metadata_mapping_dict,
                    update=True,
                )
        except Exception as err:
            raise err
        return file_status_dict

    def _map_data_metadata_files_for_update(self, source_folder_path):
        """
        Map data and metadata file names and create a dict and return
        If for a data file name, there is not metadata file raise an error -> NA for update
        """

        """
        unmapped_file_names (list): data file names which are not mapped
        metadata_file_names_str (list): metadata file names list
        data_metadata_mapping_dict (dict): dict of data metadata mapping
        individual_metadata_files (list): metadata file names list which are not mapped
        """

        data_file_names_str = []
        data_source_folder_path = source_folder_path.get("data", "")
        if data_source_folder_path:
            data_file_names = helpers.get_files_in_dir(data_source_folder_path)
            data_file_names_str = omix_hlpr.create_file_name_with_extension_list(
                data_file_names
            )
        metadata_file_names_str = []
        metadata_source_folder_path = source_folder_path.get("metadata", "")
        if metadata_source_folder_path:
            metadata_file_names = helpers.get_files_in_dir(metadata_source_folder_path)
            metadata_file_names_str = omix_hlpr.create_file_name_with_extension_list(
                metadata_file_names, file_ext_req=False
            )
        try:
            (
                data_metadata_mapping_dict,
                unmapped_file_names,
                unmapped_metadata_files,
            ) = omix_hlpr.data_metadata_file_dict(
                metadata_file_names_str, data_file_names_str
            )
        except Exception as err:
            raise err
        return (
            data_metadata_mapping_dict,
            unmapped_file_names,
            unmapped_metadata_files,
        )

    def _parameter_check_for_update_dataset(
        self, repo_id, source_folder_path, destination_folder_path, priority
    ):
        if not isinstance(destination_folder_path, str):
            raise paramException(
                title="Param Error",
                detail="`destination_folder_path` should be a string",
            )
        try:
            omix_hlpr.parameter_check_for_repo_id(repo_id)
            omix_hlpr.parameter_check_for_priority(priority)
            omix_hlpr.data_metadata_parameter_check(source_folder_path, update=True)
            omix_hlpr.check_data_metadata_file_path(source_folder_path)
            omix_hlpr.data_metadata_file_ext_check(source_folder_path)
        except Exception as err:
            raise err

    def _generating_response_from_status_dict(
        self, file_status_dict: dict, result_list: list
    ) -> list:
        """
        Generating the response with File Name and Error Message
        Store the response in the list format
        Response Message Cases
        1. If the whole metadata file not uploaded => `Reupload the metadata again`
        2. If File is uploaded => `File Uploaded`
        3. If the data file is not uploaded => `Reupload the data file and its metadata also`
        """

        for key, value in file_status_dict.items():
            if key == const.COMBINED_METADATA_FILE_NAME and value in [400, 404, 409]:
                response = []
                response.append(key)
                response.append("Metadata Not uploaded, reupload the metadata again")
                result_list.append(response)
            elif value == 204:
                response = []
                response.append(key)
                response.append("File Uploaded")
                result_list.append(response)
            elif value in [400, 404, 409]:
                response = []
                response.append(key)
                response.append(
                    "File Not Uploaded, reupload the file again and also upload the corresponding metadata"
                )
                result_list.append(response)
        return result_list

    def _parse_error_code_from_error_xml(self, err) -> str:
        """
        Parse error code from then error
        """
        error_str_tree = ET.fromstring(err)
        error_code = error_str_tree.find("Code").text
        return error_code

    def _insert_ingestion_level_dict(
        self, priority: str, combined_metadata_dict: dict
    ) -> dict:
        """
        Ingestion level metadata appended in combined metadata dict
        """
        ingestion_level_metadata = const.INGESTION_LEVEL_METADATA
        ingestion_level_metadata["attributes"]["priority"] = priority
        # combined metadata dict structure initialized
        combined_metadata_dict["data"].insert(0, ingestion_level_metadata)
        # combined_metadata_dict["data"].append(ingestion_level_metadata)
        return combined_metadata_dict

    @lru_cache(maxsize=None)
    def _list_files_in_oa(self, repo_id: str):
        """
        Summary:
        for a given repo_id/omixatlas, this function returns all the files
        present in the omixatlas.
        refer to :
        https://elucidatainc.atlassian.net/wiki/spaces/DIS/pages/3654713403/Data+ingestion+APIs+-+technical+proposal
        for more information

        Arguments:
            repo_id -- repo id (str)

        Returns:
            list of file "data" information
        """
        files_api_endpoint = f"{self.discover_url}/repositories/{repo_id}/files"
        next_link = ""
        responses = []
        while next_link is not None:
            if next_link:
                next_endpoint = f"{self.discover_url}{next_link}"
                response = self.session.get(next_endpoint)
            else:
                query_params = {
                    "page[size]": 1000,
                    "page[after]": 0,
                    "include_metadata": "false",
                    "data": "true",
                    "version": "current",
                }
                response = self.session.get(files_api_endpoint, params=query_params)
            response.raise_for_status()
            response_json = response.json()
            responses.append(response_json.get("data"))
            next_link = response_json.get("links").get("next")
        return responses

    def _get_data_file_from_oa_for_metadata_update(
        self, repo_id: str, file: str
    ) -> list:
        """
        This functions checks for the corresponding metadata/data file for a
        given data/metadata file in the repo. This is when the there is no
        mapping for a datafile to a metadata file and visa versa in the
        source folder path while update_datasets.

        if the corresponding metadata/data file is not present in the omixatlas/repo
        then it is not updated and is skipped with a WARNING message to the user.

        Arguments:
            repo_id -- repo id
            file -- the name of the metadata/data file

        returns:
            corresponding_data_file_name : list of absolute file paths from OA which match the name of the file passed
        """
        file_name = omix_hlpr.get_file_name_without_suffixes(file)
        try:
            list_oa_reponse = self._list_files_in_oa(repo_id)
            oa_data_files_list = []
            for response_data in list_oa_reponse:
                for item in response_data:
                    file_id = item.get("id")
                    oa_data_files_list.append(file_id)
            corresponding_data_file_name = []
            for data_file_absolute_path in oa_data_files_list:
                """
                taking just the file name from OA without the path and
                removing the suffixes from the file name to match with
                the metadata/data file name whose corresponding
                data/metadata file is being checked for
                """
                data_file_name = os.path.basename(data_file_absolute_path)
                if file_name == omix_hlpr.get_file_name_without_suffixes(
                    data_file_name
                ):
                    corresponding_data_file_name.append(data_file_absolute_path)
            if not corresponding_data_file_name:
                warnings.formatwarning = (
                    lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
                )
                warnings.warn(
                    "Unable to update metadata/data file "
                    + file
                    + " because corresponding data/metadata file not present in OmixAtlas. "
                    + "Please add the files using add_datasets function. "
                    + "For any questions, please reach out to polly.support@elucidata.io. "
                )
        except Exception as err:
            raise err
        return corresponding_data_file_name

    def _get_data_file_for_metadata_file(
        self,
        repo_id: str,
        metadata_file_name: str,
        data_metadata_mapping: dict,
        destination_folder_path: str,
        update: str,
    ) -> str:
        """Give the data file name for corresponding metadata file

        Args:
            repo_id (str): Repo id of the omixatlas
            metadata_file_name(str): Name of the metadata file
            data_metadata_mapping (dict): Dict containing the mapping of data and metadata files
            destination_folder_path (str): destination folder path

        Returns:
            Data File Name with Extension
        """
        file_name = pathlib.Path(metadata_file_name).stem
        # fetching data file for corresponding metadata file name
        data_file_name = data_metadata_mapping.get(file_name, "")
        """
        in order to reuse this function for update dataset
        Case 1 :-
        Just a metadata file is present in source folder and no corresponding
        data file is present in source folder.
        in this case file will not be present in data_metadata mapping dict
        the path at which the file was initally uploaded/added should match the path where
        the user is trying to update the file as well.

        Case 2 :-
        Both the data and metadata files are present in the case of update but the destination
        folder passed does not match the file pair which has to be updated.
        Data and Metadata File Pair -> Added in dest_1
        Data and Metadata File Pair -> Updated in dest_2
        So if this is the situation => Then a warning needs to be raised depicting this
        and the file needs to be skipped from getting uploaded
        """
        final_data_file_name = ""
        try:
            if not data_file_name:
                # getting list of files from OA having the same name as the metadata file name
                corresponding_data_file_names = (
                    self._get_data_file_from_oa_for_metadata_update(
                        repo_id, metadata_file_name
                    )
                )

                # finding the files from corresponding_data_file_names which have the same folder path
                # as the destination folder path provided
                final_data_file_name = (
                    omix_hlpr.get_possible_file_from_matching_filename_list_from_oa(
                        corresponding_data_file_names,
                        metadata_file_name,
                        destination_folder_path,
                    )
                )
            elif data_file_name and update:
                # getting list of files from OA having the same name as the metadata file name
                corresponding_data_file_names = (
                    self._get_data_file_from_oa_for_metadata_update(
                        repo_id, metadata_file_name
                    )
                )
                # using the corresponding_data_file_names here even if data_file_name is
                # present in the mapping dict because
                # destination_folder name is required here which is present in s3
                # that is what is required to check here
                # till we don't fetch files from OA
                # there is no way to know the corresponding destination folder
                # for the data metadata file pair in the OA
                is_destination_folder_correct = (
                    omix_hlpr.check_if_destination_folder_correct(
                        corresponding_data_file_names,
                        metadata_file_name,
                        destination_folder_path,
                    )
                )
                if is_destination_folder_correct:
                    final_data_file_name = data_file_name
            else:
                # case of add datasets -> no other check needed
                final_data_file_name = data_file_name
            return final_data_file_name
        except Exception as err:
            raise err

    def _format_metadata_dict(
        self,
        repo_id: str,
        metadata_dict: dict,
        destination_folder_path: str,
        filename: str,
        data_metadata_mapping: dict,
        update: str,
    ) -> dict:
        """
        Take metadata dict as input and insert additonal fields in each metadata
        According the the format defined in the technical proposal of Ingestion APIs
        Refer this doc for more information on it -> Technical Proposal -> Section -> File level metadata format
        https://elucidatainc.atlassian.net/wiki/spaces/DIS/pages/3654713403/Data+ingestion+APIs+-+technical+proposal
        """
        formatted_metadata = {}
        data_file_name = self._get_data_file_for_metadata_file(
            repo_id, filename, data_metadata_mapping, destination_folder_path, update
        )
        if data_file_name:
            # no matter if the data_file_name comes with the path or not, we just keep the file name
            # append the destination file path later
            # more of a patch fix for LIB-314 - need to handle in 0.2.10
            data_file_name_without_path = os.path.basename(data_file_name)
            formatted_metadata = {"id": "", "type": "", "attributes": {}}
            if destination_folder_path:
                formatted_metadata[
                    "id"
                ] = f"{destination_folder_path}/{data_file_name_without_path}"
            else:
                formatted_metadata["id"] = f"{data_file_name_without_path}"
            formatted_metadata["type"] = "file_metadata"
            formatted_metadata["attributes"] = metadata_dict
        return formatted_metadata

    # TODO
    # Currently works for repositories having source -> `all` & datatype -> `all`
    # In the datalake only these examples exist for now
    # In future it will be extended for other sources and datatypes
    @Track.track_decorator
    def dataset_metadata_template(
        self, repo_key, source="all", data_type="all"
    ) -> dict:
        """
        This function is used to fetch the template of dataset level metadata in a given OmixAtlas.
        In order to ingest the dataset level metadata appropriately in the OmixAtlas, the user needs
        to ensure the metadata json file contains the keys as per the dataset level schema.
        Args:
            repo_id (str/int): repo_name/repo_id for that Omixatlas
            source (all, optional): Source/Sources present in the schema. Default value is "all"
            data_type (all, optional): Datatype/Datatypes present in the schema. Default value is "all"

        Returns:
            A dictionary with the dataset level metadata

        Raises:
            invalidApiResponseException: attribute/key error

        Returns:
            dictionary with the dataset level metadata

        """
        # for dataset level metadata index is files
        schema_type = "files"

        schema_base_url = f"{self.discover_url}/repositories"

        dataset_url = f"{schema_base_url}/{repo_key}/" + f"schemas/{schema_type}"

        resp = self.session.get(dataset_url)
        error_handler(resp)
        api_resp_dict = resp.json()
        if "data" in api_resp_dict:
            if "attributes" in api_resp_dict["data"]:
                if "schema" in api_resp_dict["data"]["attributes"]:
                    resp_dict = {}
                    resp_dict = api_resp_dict["data"]["attributes"]["schema"][source][
                        data_type
                    ]
                else:
                    raise invalidApiResponseException(
                        title="schema key not present",
                        detail="`schema` key not inside attributes present in the repository schema",
                    )
            else:
                raise invalidApiResponseException(
                    title="attributes key not present",
                    detail="attributes not present in the repository schema",
                )
        else:
            raise invalidApiResponseException(
                title="data key not present",
                detail="data key not present in the repository schema",
            )

        result_dict = {}
        # deleting unnecessary keys
        for field_key, val_dict in resp_dict.items():
            is_array_val = val_dict.get("is_array", None)
            type_val = val_dict.get("type", None)
            original_name_key = val_dict.get("original_name", None)
            if is_array_val is None:
                result_dict[original_name_key] = type_val
            elif is_array_val:
                result_dict[original_name_key] = []
            else:
                result_dict[original_name_key] = type_val

        # adding `__index__` key and its default values
        result_dict["__index__"] = {
            "file_metadata": True,
            "col_metadata": True,
            "row_metadata": False,
            "data_required": False,
        }

        return result_dict

    def _s3_key_dataset(self, repo_id: int, dataset_ids: list) -> dict:
        """
        S3 keys for dataset ids
        """
        # key -> `dataset_id`, value -> single or multiple file keys
        # {<dataset_id>:["list of file ids"] or str}
        # if for a dataset_id there is error message from API
        # str will represent that error message
        s3_keys_dict = {}
        for dataset_id in dataset_ids:
            list_files_resp = self.get_all_file_paths(
                repo_id, dataset_id, internal_call=True
            )
            s3_keys_dict[dataset_id] = list_files_resp

        # clearing the cache of list files after getting file paths
        # for all the dataset_ids
        omix_hlpr.list_files.cache_clear()
        return s3_keys_dict

    def get_all_file_paths(
        self, repo_id: int, dataset_id: str, internal_call=False
    ) -> list:
        """Get all file paths where the file is stored corresponding to the
        repo_id and dataset_id

        Args:
            repo_id (int): repo_id of the omixatlas
            dataset_ids (str): dataset_id present in the omixatlas

        Raises:
            paramError: If Params are not passed in the desired format or value not valid.

        Returns:
            list: all the file paths corresponding to repo_id and dataset_id
            Error: If repo_id or dataset id does not exist in the system
        """
        omix_hlpr.get_all_file_paths_param_check(repo_id, dataset_id)
        # list of the all the file paths in the system
        # corresponding to the passed repo_id and dataset id
        file_paths = []

        # check if omixatlas exists
        # if omixatlas does not exist then it will raise an error
        self._get_omixatlas(repo_id)

        # cache it once and clear the cache once the function execution ends
        list_files_resp_list = omix_hlpr.list_files(self, repo_id)

        # internal_call argument is only for system use
        # It will not be exposed to the users
        # If internal_call is True -> this method called from inside delete datasets
        # in that Only raise exception if Forbidden or Unauthorized
        # In all other cases -> return the error message so that
        # file deletion process does not get halted. Error Message gets logged
        # For these files deletion will be skipped
        # This is to ease out the process of Bulk Delete

        # iterating over list_files_resp_list to get all the list of files
        for list_files_resp in list_files_resp_list:
            if list_files_resp.status_code != const.OK and internal_call:
                if list_files_resp.status_code == http_codes.NOT_FOUND:
                    error_msg = omix_hlpr.extract_error_message(list_files_resp.text)
                    return error_msg
            elif list_files_resp.status_code != const.OK:
                error_handler(list_files_resp)
            else:
                list_files_resp = list_files_resp.json()
                list_files_resp_data = list_files_resp.get("data", [])
                for file_data in list_files_resp_data:
                    file_metadata = file_data.get("attributes", {}).get("metadata", {})
                    file_dataset_id = file_metadata.get("dataset_id", "")
                    if file_dataset_id == dataset_id:
                        # id in the response corresponds to file path
                        # where the file is present
                        file_id = file_data.get("id")
                        file_paths.append(file_id)

                if not file_paths:
                    warnings.formatwarning = (
                        lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
                    )
                    warnings.warn(
                        f"{dataset_id} does not exist in the Omixatlas {repo_id} "
                    )

        return file_paths

    @Track.track_decorator
    def delete_datasets(
        self, repo_id: int, dataset_ids: list, dataset_file_path_dict={}
    ):
        """
        This function is used to delete datasets from an OmixAtlas.
        Once user runs this function successfully, they should be able to see the
        deletion status on the data ingestion monitoring dashboard within ~2 mins.
        A dataframe with the status of the operation for each file(s) will be displayed after the
        function execution.

        In order to delete datasets into Omixatlas the user must be a Data Admin at the resource level.
        Please contact polly.support@elucidata.io if you get Access Denied error message.

        Note -> Because this function takes list as an input, user must not run this function in a loop.

        Args:
            repo_id (int/str): repo_id for that Omixatlas
            dataset_ids (list): list of dataset_ids that users want to delete. It is mandatory for \
            users to pass the dataset_id which they want to delete from the repo in this list.
            dataset_file_path_dict(dict, Optional): Optional Parameter. In case a given dataset ID \
            has multiple files associated with it, then the user has to specifically give the \
            file_path which needs to be deleted. Users can use the function get_all_file_paths \
            to get paths of all the files which correspond to same dataset_id.

        Raises:
            paramError: If Params are not passed in the desired format or value not valid.
            RequestException: If there is issue in data ingestion.

        Returns:
            None
        """
        try:
            # this line is making the code unreachable -> will look into it later
            omix_hlpr.parameter_check_for_delete_dataset(
                repo_id, dataset_ids, dataset_file_path_dict
            )
            # extract s3 keys for dataset_ids
            repo_id = omix_hlpr.make_repo_id_string(repo_id)

            # check if dataset_file_path_dict keys subset of dataset_ids
            omix_hlpr.dataset_file_path_is_subset_dataset_id(
                dataset_ids, dataset_file_path_dict
            )

            # normalise the file path which user has given
            dataset_file_path_dict = omix_hlpr.normalize_file_paths(
                dataset_file_path_dict
            )

            # {"<dataset_id>": ["<file_paths>"]}
            # single file_path => Means single element in the list
            # if multiple file paths => Means multiple elements in the list
            dataset_s3_keys_dict = self._s3_key_dataset(repo_id, dataset_ids)

            # convert the dict to df at last
            result_dict = {}

            # result dict format
            # {'GSE101942_GPL11154': [{'Message': 'Dataset not deleted because file_path for
            #  the dataset_id is incorrect', 'Folder Path': 'transcriptomics_906s/GSE76311_GPL17586.gct'},
            # {'Message': 'Dataset not deleted because file_path for the dataset_id is incorrect',
            # 'Folder Path': 'transcriptomics_907s/GSE76311_GPL17586.gct'}]}
            result_dict = self._delete_datasets_helper(
                repo_id, dataset_s3_keys_dict, dataset_file_path_dict
            )

            valid_deletion_entry = omix_hlpr.check_res_dict_has_file_deleted_entries(
                result_dict
            )

            if result_dict and valid_deletion_entry:
                # if result dict is generated and there is at least
                # 1 deletion entry in the df -> then commit API will be hit
                # to log the deletion status of the valid entry
                # print message before delay
                print(const.WAIT_FOR_COMMIT_DELETE)
                # delay added after the files are uploaded
                # before commit API is hit
                time.sleep(30)

                # informing infra to commit the delete data in the repository
                self._commit_data_to_repo(repo_id)

                omix_hlpr.convert_delete_datasets_res_dict_to_df(result_dict)
            elif result_dict:
                # result dict is generated but there is no valid entry of deletion
                # for any of the dataset_ids in the dict
                # commit API not hit
                omix_hlpr.convert_delete_datasets_res_dict_to_df(result_dict)
            else:
                print(const.DELETION_OPERATION_UNSUCCESSFUL_FOR_ALL_DATASET_IDS)

        except Exception as err:
            raise err

    def _delete_datasets_helper(
        self, repo_id: str, dataset_s3_keys_dict: dict, dataset_file_path_dict: dict
    ):
        """Calls the API to delete the datasets and deletes the dataset

        Args:
            repo_id (str): repo_id of the OmixAtlas
            dataset_s3_keys_dict(dict): Dictionary contaning datasetid and corresponding file paths
            dataset_file_path_dict(dict): In case multiple files are present for the dataset_id \
            The file_paths from where users needs to delete the file can be passed in this. \
            Format -> {<dataset_id>:["<List of file paths from where user wants to delete file>"]}
        """
        result_dict = {}
        for datasetid_key, file_path in dataset_s3_keys_dict.items():
            if isinstance(file_path, str):
                # if only string type value is present corresponding to
                # dataset id means that it is an error message
                # Put the error message for corresponding dataset id directly
                # in the result dict
                res = {"Message": file_path, "Folder Path": ""}
                result_dict[datasetid_key] = res
            elif isinstance(file_path, list):
                if len(file_path) == 1:
                    # this means only single file present in the system for
                    # the dataset id -> so case of single file deletion for
                    # dataset id
                    # passing the file_path present at the 0th index as that is the
                    # only file_path in the list
                    dataset_id_single_res_dict = self._delete_file_with_single_path(
                        repo_id, datasetid_key, file_path[0], dataset_file_path_dict
                    )
                    # append dataset_id_res_dict to main dict
                    # working of update dict
                    """
                    Original Dictionary:
                    {'A': 'Geeks'}
                    Dictionary after updation:
                    {'A': 'Geeks', 'B': 'For', 'C': 'Geeks'}
                    """
                    # here updating the existing dict with key value pair of delete msg
                    # for the current dataset id
                    if dataset_id_single_res_dict:
                        result_dict.update(dataset_id_single_res_dict)
                elif len(file_path) > 1:
                    dataset_id_mulitple_res_dict = (
                        self._delete_file_with_multiple_paths(
                            repo_id, datasetid_key, dataset_file_path_dict, file_path
                        )
                    )
                    if dataset_id_mulitple_res_dict:
                        # if dataset_id_mulitple_res_dict is not empty
                        # means the API request for deletion of dataset id is processed
                        # then df will have entry, update it into resultant df
                        # else skip for this dataset id
                        result_dict.update(dataset_id_mulitple_res_dict)

        return result_dict

    def _delete_file_with_single_path(
        self,
        repo_id: int,
        datasetid_key: str,
        file_path: str,
        dataset_file_path_dict: dict,
    ):
        """Delete File with single path

        Args:
            repo_id (int): repo_id of the OmixAtlas
            datasetid_key (str): dataset_id to be deleted
            file_path (str): file path of the dataset_id with single location in system
            dataset_file_path_dict (dict): dataset_id, file_path dict
        """
        dataset_id_single_res_dict = {}
        # intialising value corresponding to datasetid_key as list
        # corresponding to multiple paths passed by the user
        # there can be multiple entries for a single dataset_id
        dataset_id_single_res_dict[datasetid_key] = []
        # checking if datasetid_key is present in dataset_file_path_dict
        # Ideally if datasetid_key has single path where file is present
        # Passing the path is not required, because the system will find out the
        # path from the list file API and delete the file
        # Giving the path is necessary when the dataset_id is present in multiple
        # files in the Omixatlas, in that system on its own can't decide which file
        # to delete, in that case -> users need to pass the file path from where
        # they want the file to be deleted.
        if datasetid_key in dataset_file_path_dict:
            # dataset_file_path_dict[datasetid_key] -> file_path passed by the user
            # dataset_file_path_dict[datasetid_key] -> list format
            # paths passed by the user already normalised before hand
            # already normalised beforehand
            for user_file_path in dataset_file_path_dict[datasetid_key]:
                # file_path -> file_path of the dataset_id file in the system
                # user_file_path -> file_path of the dataset_id file passed by the user

                if user_file_path != file_path:
                    delete_res_val = omix_hlpr.user_file_path_incorrect(
                        user_file_path, datasetid_key
                    )
                    dataset_id_single_res_dict[datasetid_key].append(delete_res_val)
                else:
                    delete_res_val = self._delete_file_with_single_path_helper(
                        repo_id, user_file_path
                    )
                    dataset_id_single_res_dict[datasetid_key].append(delete_res_val)
        else:
            # file path not passed delete the dataset id from the file path
            # obtained from the system
            delete_res_val = self._delete_file_with_single_path_helper(
                repo_id, file_path
            )
            dataset_id_single_res_dict[datasetid_key].append(delete_res_val)

        return dataset_id_single_res_dict

    def _delete_file_with_single_path_helper(
        self, repo_id: str, file_path: str
    ) -> dict:
        """helper function for single path delete datasets
        Args:
            repo_id(str): repo_id of the Omixatlas
            file_path(str): file_path from where file needs to be deleted
        """
        delete_url = f"{self.discover_url}/repositories/{repo_id}/files/{file_path}"
        resp = self.session.delete(delete_url)
        if resp.status_code == http_codes.ACCEPTED:
            res = {
                "Message": "Request Accepted. Dataset will be deleted in the next version of OmixAtlas",
                "Folder Path": f"{file_path}",
            }
            return res
        elif resp.status_code == http_codes.FORBIDDEN:
            # raising error in the case when the user is forbidden
            # to delete the file which may occur from repository lock
            # or invalid permissions for the user
            # rest in all the cases, no need to raise error
            # just store the error message in the result dict
            # and skip the file
            error_handler(resp)
        else:
            res = {
                "Message": f"Deletion failed because {resp.text}. Please contact polly.support@elucidata.io",
                "Folder Path": f"{file_path}",
            }
            return res

    def _delete_file_with_multiple_paths(
        self,
        repo_id: int,
        datasetid_key: str,
        dataset_file_path_dict: dict,
        file_paths: list,
    ):
        """Delete the files for the datasetid having multiple paths

        Args:
            repo_id (int): repo_id of the OmixAtlas
            datasetid_key (str): dataset_id to be deleted
            file_path (list):
            dataset_file_path_dict (_type_): _description_
        """
        dataset_id_res_dict = {}
        # intialising value corresponding to datasetid_key as list
        # corresponding to multiple paths passed by the user
        # there can be multiple entries for a single dataset_id
        dataset_id_res_dict[datasetid_key] = []
        # dataset id file is not unique in the Omixatlas
        # there are multiple files with same dataset id
        if datasetid_key not in dataset_file_path_dict:
            warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
            warnings.warn(
                f"Unable to delete file with dataset_id: {datasetid_key} "
                + "present in mutiple files/folders. "
                + "Please pass the path of the file which needs to be deleted. "
                + "For getting the list of paths/folders where the dataset_id files are "
                + "can be fetching using <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>). "
                + "For any questions, please reach out to polly.support@elucidata.io. "
            )
            # break line added -> for better UX
            print("\n")
            res = {
                "Message": "Dataset not deleted because no file_path passed.",
                "Folder Path": f"{file_paths}",
            }
            dataset_id_res_dict[datasetid_key].append(res)
        else:
            passed_file_paths = dataset_file_path_dict[datasetid_key]
            if not passed_file_paths:
                raise paramException(
                    title="paramException",
                    detail=(
                        "No file_path passed for this dataset_id. "
                        + "Multiple files are present for the dataset id. "
                        + "Please pass list of paths from which file needs to be deleted. "
                        + f"Please pass paths from this list {file_paths} "
                        + "Alternatively for getting the list of file_paths for the dataset_id "
                        + "call <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>). "
                    ),
                )

            # Intersection of file paths for the dataset_id which are present in the system
            # and what users have passed
            # file_paths -> file paths for the dataset id present in the system
            # passed_file_paths -> file paths passed by the user for the dataset id
            file_paths_to_delete = list(set(file_paths) & set(passed_file_paths))

            # if there are no file paths passed which corresponds to file paths
            # present in the system for the given dataset_id
            if not file_paths_to_delete:
                raise Exception(
                    f"file paths incorrect, it does not belong to dataset_id -> {datasetid_key}"
                    + f". Please pass file path from these {file_paths}. "
                    + "Alternatively for getting the list of file_paths for the dataset_id "
                    + "call <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>). "
                )

            # if from the file paths passed not all the file paths have the
            # file with the given dataset id
            invalid_paths = list(set(passed_file_paths) - set(file_paths_to_delete))

            # raise warning for those invalid file paths
            if invalid_paths:
                # loop over invalid paths, raise warning and log the entry in the df
                for invalid_path in invalid_paths:
                    delete_msg_val = (
                        omix_hlpr.warning_invalid_path_delete_dataset_multiple_paths(
                            invalid_path, datasetid_key
                        )
                    )
                    dataset_id_res_dict[datasetid_key].append(delete_msg_val)

            for valid_file_path in file_paths_to_delete:
                delete_msg_val = self._delete_file_with_single_path_helper(
                    repo_id, valid_file_path
                )
                dataset_id_res_dict[datasetid_key].append(delete_msg_val)

            return dataset_id_res_dict

    def move_data(
        self,
        source_repo_key: str,
        destination_repo_key: str,
        dataset_ids: list,
        priority="medium",
    ) -> str:
        """
        This function is used to move datasets from source atlas to destination atlas.
        This function should only be used when schema of source and destination atlas are compatible with each other.
        Else, the behaviour of data in destination atlas may not be the same or the ingestion may fail.
        Please contact polly@support.com if you get Access Denied error message.

        Args:
            source_repo_key (str/int): src repo key of the dataset ids. Only repo_id supported now,
            destination_repo_key (str/int): destination repo key where the data needs to be transferred
            dataset_ids (list): list of dataset ids to transfer
            priority (str, optional): Optional parameter(low/medium/high). Priority of ingestion. \
            Defaults to "medium".

        Returns:
            None: None
        """
        # right now source_repo_key and destination_repo_key is only supported
        # when sai makes the change in the API both repo_id and repo_name
        # will be supported
        try:
            omix_hlpr.move_data_params_check(
                source_repo_key, destination_repo_key, dataset_ids, priority
            )
            # convert repo_key if int from int to str
            source_repo_key = omix_hlpr.make_repo_id_string(source_repo_key)
            destination_repo_key = omix_hlpr.make_repo_id_string(destination_repo_key)

            src_repo_metadata = self._get_omixatlas(source_repo_key)
            data = src_repo_metadata.get("data").get("attributes", {})
            # repo_name = data.get("repo_name")
            index_name = data.get("v2_indexes", {}).get("files")
            if index_name is None:
                raise paramException(
                    title="Param Error", detail="Invalid Repo Id/ Repo Name passed."
                )
            elastic_url = f"{self.elastic_url}/{index_name}/_search"
            # dataset links to be moved from source to destination
            payload_datasets = []
            for dataset_id in dataset_ids:
                query = helpers.elastic_query(index_name, dataset_id)
                metadata = helpers.get_metadata(self, elastic_url, query)
                source_info = metadata.get("_source", "")
                src_uri = source_info.get("src_uri", "")
                if not src_uri:
                    raise invalidApiResponseException(
                        title="Invalid API Response",
                        detail=f"src_uri for {dataset_id} does not exist.",
                    )
                payload_datasets.append(src_uri)

            move_data_url = f"{self.discover_url}/repositories/ingestion-transactions"
            move_data_payload = omix_hlpr.create_move_data_payload(
                payload_datasets, source_repo_key, destination_repo_key, priority
            )
            # move data API Call
            # json.dumps used so that dict is converted into json
            response = self.session.post(
                move_data_url, data=json.dumps(move_data_payload)
            )
            error_handler(response)
            if response.status_code == http_codes.OK:
                print(const.MOVE_DATA_SUCCESS)
        except Exception as err:
            raise err

    def _update_frontendinfo_value(
        self,
        frontendinfo_curr_data: dict,
        image_url: str,
        description: str,
        display_name: str,
    ) -> dict:
        if image_url:
            frontendinfo_curr_data["icon_image_url"] = image_url
        if description:
            frontendinfo_curr_data["description"] = description
        if display_name:
            frontendinfo_curr_data["display_name"] = display_name
        return frontendinfo_curr_data

    def _repo_creation_response_df(self, original_response) -> pd.DataFrame:
        """
        This function is used to create dataframe from json reponse of
        creation api

        Args:
            | original response(dict): creation api response
        Returns:
            | DataFrame consisting of 6 columns
            | ["Repository Id", "Repository Name", "Display Name", "Description", "Category", "Datatype"]

        """
        response_df_dict = {}
        if original_response["data"]:
            if original_response["data"]["attributes"]:
                attribute_data = original_response["data"]["attributes"]
                response_df_dict["Repository Id"] = attribute_data.get("repo_id", "")
                response_df_dict["Repository Name"] = attribute_data.get(
                    "repo_name", ""
                )
                response_df_dict["Category"] = attribute_data.get("category", "")
                if "data_type" in attribute_data:
                    response_df_dict["Datatype"] = attribute_data.get("data_type", "")
                if attribute_data["frontend_info"]:
                    front_info_dict = attribute_data["frontend_info"]
                    response_df_dict["Display Name"] = front_info_dict.get(
                        "display_name", ""
                    )
                    response_df_dict["Description"] = front_info_dict.get(
                        "description", ""
                    )
        rep_creation_df = pd.DataFrame([response_df_dict])
        return rep_creation_df

    def _create_repo_name(self, display_name) -> str:
        """
        This function is used to repo_name from display_name
        Args:
            | display_name(str): display name of the omixatlas
        Returns:
            | Constructed repo name
        """
        repo_name = display_name.lower().replace(" ", "_")
        return repo_name

    def _get_repository_payload(self):
        """ """
        return {
            "data": {
                "type": "repositories",
                "attributes": {
                    "frontend_info": {
                        "description": "<DESCRIPTION>",
                        "display_name": "<REPO_DISPLAY_NAME>",
                        "explorer_enabled": True,
                        "initials": "<INITIALS>",
                    },
                    "indexes": {
                        "csv": "<REPO_NAME>_csv",
                        "files": "<REPO_NAME>_files",
                        "gct_data": "<REPO_NAME>_gct_data",
                        "gct_metadata": "<REPO_NAME>_gct_metadata",
                        "h5ad_data": "<REPO_NAME>_h5ad_data",
                        "h5ad_metadata": "<REPO_NAME>_h5ad_metadata",
                        "ipynb": "<REPO_NAME>_ipynb",
                        "json": "<REPO_NAME>_json",
                    },
                    "repo_name": "<REPO_NAME>",
                    "category": "<CATEGORY>",
                },
            }
        }

    @Track.track_decorator
    def generate_report(
        self, repo_key: str, dataset_id: str, workspace_id: int, workspace_path=""
    ) -> None:
        """
        This function is used to generate a metadata distribution report for a dataset belonging to the geo repository.
        The generated report is then saved to the workspace provided.
        This is a MVP release to minimise time taken by users to determine relevance of a dataset in their research,
        we’re enabling auto-generation of reports.
        These reports will contain dataset/sample level metadata and graphs showing sample distribution.
        It will help them figure out which cohorts could be of interest in a given dataset.
        This template can be modified and we’re open to user’s feedback.
        This report is available on the user’s local path as well as an option to upload the report to workspaces is given.
        A message will be displayed on the status of the operation.

        Args:
            repo_key (str): repo_name/repo_id for which the report is to be generated
            dataset_id (str): dataset_id for which the report is to be generated
            workspace_id (int): workspace_id to where the report is to be uploaded
            workspace_path (str, optional): workspace_path to which the report is to be uploaded

        Raises:
            InvalidParameterException: Empty or Invalid Parameters
            UnsupportedRepositoryException: repo other than GEO/ Unsupported repo
            UnauthorizedException: unauthorized to perform this task

        Returns:
            None
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (workspace_id and isinstance(workspace_id, int)):
            raise InvalidParameterException("workspace_id")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_name = data.get("repo_name").lower()
        if repo_name not in REPORT_GENERATION_SUPPORTED_REPOS:
            raise UnsupportedRepositoryException
        download_dict = self.download_data(repo_name, dataset_id, internal_call=True)
        if download_dict:
            pass
        query = f"SELECT * FROM {repo_name}.datasets WHERE dataset_id = '{dataset_id}'"
        sel_dataset_info = self.query_metadata(query)
        query = (
            f"SELECT * FROM {repo_name}.samples WHERE src_dataset_id ='{dataset_id}'"
        )
        result_sample = self.query_metadata(query)
        result_sample.fillna("none", inplace=True)
        all_fields = helpers.get_cohort_fields()
        sample_kw_fields = all_fields.get("sample_kw_fields")
        sample_fields = all_fields.get("sample_fields")
        dataset_fields = all_fields.get("dataset_fields")
        extra_fields = all_fields.get("extra_fields")
        total_sample_fields = []
        total_sample_fields = sample_kw_fields + sample_fields
        for col in result_sample.columns:
            if col in extra_fields:
                total_sample_fields.append(col)
        total_sample_fields = list({*total_sample_fields})
        result_sample_sel = result_sample[total_sample_fields]
        deleted_dict, result_sample_sel = self._preprocessing_data(result_sample_sel)
        pie_charts, sunburst = self._get_plots(result_sample_sel)
        sel_dataset_info.reset_index(inplace=True)
        sel_dataset_info = sel_dataset_info[dataset_fields]
        sel_dataset_info.fillna("None", inplace=True)
        sel_dataset_info = sel_dataset_info.astype("str")
        sel_dataset_info = sel_dataset_info.applymap(lambda x: x.strip("[]"))
        sel_dataset_info = sel_dataset_info.applymap(lambda x: x.replace("'", ""))
        sel_dataset_info = sel_dataset_info.applymap(lambda x: x.replace("[", ""))
        drop_data_cols = sel_dataset_info.columns[(sel_dataset_info == "None").any()]
        sel_dataset_info.drop(drop_data_cols, axis=1, inplace=True)
        replace_cols = {
            "total_num_samples": "number_of_samples",
            "description": "title",
            "overall_design": "experimental_design",
        }
        sel_dataset_info.rename(columns=replace_cols, inplace=True)
        sel_dataset_info["platform"] = dataset_id.split("_")[1]
        string_data = []
        for col in sel_dataset_info.columns:
            string_data.append(
                f"**{col.replace('_', ' ').title()} :** {sel_dataset_info[col][0]}"
            )
        deleted_data = []
        for key, val in deleted_dict.items():
            deleted_data.append(f"**{key.replace('_', ' ').title()} :** {val}")
        md_blocks = [dp.Text(st) for st in string_data]
        new_md_blocks = [dp.Text(st) for st in deleted_data]
        self._save_report(
            dataset_id,
            workspace_id,
            workspace_path,
            md_blocks,
            new_md_blocks,
            pie_charts,
            sunburst,
        )

    def _preprocessing_data(self, result_sample_sel: pd.DataFrame):
        """
        Dropping the columns which have same values
        """
        deleted_dict = {}
        for col in result_sample_sel.columns:
            if result_sample_sel[col].explode().nunique() == 1:
                value = list(np.unique(np.array(list(result_sample_sel[col]))))
                if value[0] != "none":
                    deleted_dict[col] = value[0]
                result_sample_sel = result_sample_sel.drop(col, axis=1)
        return deleted_dict, result_sample_sel

    def _get_plots(self, result_sample_sel: pd.DataFrame) -> tuple:
        """
        Function to return plots( pie-chart and sunburst plot)
        """
        if result_sample_sel.shape[1] != 0:
            result_sample_sel = result_sample_sel[
                result_sample_sel.columns[
                    ~(result_sample_sel.applymap(helpers.check_empty) == 0).any()
                ]
            ]
            explode_col = result_sample_sel.columns[
                result_sample_sel.applymap(
                    lambda x: True if type(x) == list else False
                ).any()
            ]
            for col in explode_col:
                result_sample_sel = result_sample_sel.explode(col)
            for col in result_sample_sel.columns:
                for val in result_sample_sel[col].unique():
                    if val.find(":") > 1:
                        result_sample_sel.rename(
                            columns={col: val[: val.find(":")].strip(" ")}, inplace=True
                        )
            sunburst = px.sunburst(
                result_sample_sel,
                path=list(
                    zip(
                        *sorted(
                            {
                                col: result_sample_sel[col].nunique()
                                for col in result_sample_sel.columns
                            }.items(),
                            key=lambda x: x[1],
                        )
                    )
                )[0],
                width=600,
                height=600,
                title="Sample level Metadata",
            )
            pie_charts = []
            for col in result_sample_sel.columns:
                pie_ch = px.pie(
                    result_sample_sel,
                    col,
                    width=600,
                    height=600,
                    title=col.replace("_", " ").title(),
                    hole=0.3,
                )
                pie_ch.update_traces(marker=dict(line=dict(color="white", width=1.5)))
                pie_ch.update_layout(
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        font=dict(size=10),
                        xanchor="right",
                        x=1,
                    )
                )
                pie_charts.append(dp.Plot(pie_ch))

        else:
            pie_charts, sunburst = None, None
        return pie_charts, sunburst

    def _save_report(
        self,
        dataset_id: str,
        workspace_id: int,
        workspace_path: str,
        md_blocks: list,
        new_md_blocks: list,
        pie_charts: list,
        sunburst,
    ) -> None:
        """
        Function to make a report and save it in local and upload to given workspace
        """
        if pie_charts is not None:
            my_pie = dp.Group(blocks=pie_charts, columns=2, label="Pie Charts")
            sunburst_pl = dp.Plot(sunburst, label="Sun Burst")
            report = dp.Report(
                f"### {dataset_id}",
                dp.Group(blocks=md_blocks, columns=1),
                dp.Select(blocks=[my_pie, sunburst_pl]),
            )
        else:
            report = dp.Report(
                f"### {dataset_id}",
                dp.Group(blocks=md_blocks, columns=1),
                dp.Group(blocks=new_md_blocks, columns=1),
            )
        report_name = f"{dataset_id}_report.html"
        report.save(
            path=report_name, formatting=dp.ReportFormatting(width=dp.ReportWidth.FULL)
        )
        access_workspace = helpers.workspaces_permission_check(self, workspace_id)
        if not access_workspace:
            raise AccessDeniedError(
                detail=f"Access denied to workspace-id - {workspace_id}"
            )
        local_path = f"{os.getcwd()}/{report_name}"
        """if workspace_path is not empty and contains anything except whitespaces, then make a valid path, \
        else assign predefined name as the path"""
        if workspace_path and not workspace_path.isspace():
            workspace_path = helpers.make_path(workspace_path, report_name)
        else:
            workspace_path = report_name
        helpers.edit_html(local_path)
        helpers.upload_html_file(self.session, workspace_id, workspace_path, local_path)

    @Track.track_decorator
    def link_report(
        self,
        repo_key: str,
        dataset_id: str,
        workspace_id: int,
        workspace_path: str,
        access_key: str,
    ) -> None:
        """
        This function is used to link a file (html or pdf) present in a workspace with the specified dataset in OmixAtlas.
        On success it displays the access key URL and a success message.
        Org admins can now link a report present in a workspace with the specified datasets in an OmixAtlas.
        Once a report is linked to a dataset in OmixAtlas, it can be fetched both from front-end and polly-python.
        A message will be displayed on the status of the operation.

        Args:
            repo_key (str): repo_name/repo_id of the repository to be linked
            dataset_id (str): dataset_id of the dataset to be linked
            workspace_id (str): workspace_id for the file which is to be linked
            workspace_path (str): workspace_path for the file which is to be linked
            access_key (str): access_key(private or public) depending upon the link access type to be generated.\
            If public, then anyone with a Polly account with the link will be able to see the report.\
            If private, only individuals who have access to the workspace where reports is stored will be able to see them.

        Raises:
            InvalidParameterException: invalid parameters

        Returns:
            None
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (workspace_id and isinstance(workspace_id, int)):
            raise InvalidParameterException("workspace_id")
        if not (workspace_id and isinstance(workspace_path, str)):
            raise InvalidParameterException("workspace_path")
        if not (
            access_key
            and isinstance(access_key, str)
            and access_key.lower() in ["private", "public"]
        ):
            raise InvalidParameterException("access_key")
        sts_url = f"{self.base_url}/projects/{workspace_id}/credentials/files"
        access_url = f"https://{self.session.env}.elucidata.io/manage"
        helpers.verify_workspace_details(self, workspace_id, workspace_path, sts_url)
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        absolute_path = helpers.make_path(workspace_id, workspace_path)
        url = f"{self.base_url}/v1/omixatlases/{repo_id}/reports"
        payload = {
            "data": {
                "type": "dataset-reports",
                "attributes": {
                    "dataset_id": f"{dataset_id}",
                    "absolute_path": f"{absolute_path}",
                },
            }
        }
        response = self.session.post(url, data=json.dumps(payload))
        error_handler(response)
        shared_id = self._get_shared_id(workspace_id, workspace_path)
        if shared_id is None:
            existing_access = "private"
        else:
            existing_access = "public"
        report_id = helpers.get_report_id(self.session, workspace_id, workspace_path)
        if access_key == existing_access == "private":
            file_link = helpers.make_private_link(
                workspace_id, workspace_path, access_url, report_id
            )
        elif access_key == existing_access == "public":
            file_link = f"{access_url}/shared/file/?id={shared_id}"
        else:
            file_link = helpers.change_file_access(
                self, access_key, workspace_id, workspace_path, access_url, report_id
            )
        print(
            f"File Successfully linked to dataset id = {dataset_id}. The URL for the {access_key} access is '{file_link}'"
        )

    @Track.track_decorator
    def link_report_url(
        self, repo_key: str, dataset_id: str, url_to_be_linked: str
    ) -> None:
        """
        This function is used to link a URL with the specified dataset in OmixAtlas.
        A message will be displayed on the status of the operation.

        Args:
            repo_key (str): repo_name/repo_id of the repository to be linked
            dataset_id (str): dataset_id of the dataset to be linked
            url_to_be_linked (str): The url which is to be linked

        Raises:
            InvalidParameterException: invalid parameters

        Returns:
            None
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (url_to_be_linked and isinstance(url_to_be_linked, str)):
            raise InvalidParameterException("url")
        parsed_url = urlparse(url_to_be_linked)
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        # check for components in a url for a basic validation of url
        """
        Format of the parsed string with a sample URL - http://www.cwi.nl:80/%7Eguido/Python.html
        ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
        params='', query='', fragment='')
        """
        if all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]):
            report_url = f"{self.base_url}/v1/omixatlases/{repo_id}/reports"
            payload = {
                "data": {
                    "type": "dataset-reports",
                    "attributes": {
                        "dataset_id": f"{dataset_id}",
                        "absolute_path": f"{url_to_be_linked}",
                    },
                }
            }
            response = self.session.post(report_url, data=json.dumps(payload))
            error_handler(response)
            print(
                f"Dataset - {dataset_id} has been successfully linked with URL {url_to_be_linked} "
            )
        else:
            raise InvalidParameterException("url")

    @Track.track_decorator
    def fetch_linked_reports(self, repo_key: str, dataset_id: str) -> pd.DataFrame:
        """
        Fetch linked reports for a dataset_id in an OmixAtlas.

        Args:
            repo_key (str): repo_name/repo_id of the repository for which to fetch the report
            dataset_id (str): dataset_id of the dataset which to fetch the reports.

        Raises:
            InvalidParameterException : invalid parameters
            RequestException : api request exception
            UnauthorizedException : unauthorized to perform this action

        Returns:
            A Dataframe with the details of the linked reports - who added the report, when it was added and the link.

        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        params = {"dataset_id": f"{dataset_id}"}
        url = f"{self.base_url}/v1/omixatlases/{repo_id}/reports"
        response = self.session.get(url, params=params)
        error_handler(response)
        report_list = response.json().get("data").get("attributes").get("reports")
        access_url = f"https://{self.session.env}.elucidata.io/manage"
        if len(report_list) == 0:
            print("No Reports found to be linked with the given details.")
        else:
            columns = ["Added_by", "Added_time", "URL", "Report_id"]
            all_details = []
            for items in report_list:
                details_list = []
                added_by = items.get("added_by")
                # convertime time fetched in miliseconds to datetime
                added_on = items.get("added_on") / 1000.0
                added_time = datetime.fromtimestamp(added_on).strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
                if "url" in items:
                    """
                    Contents of dict items
                    {
                        "added_by": "circleci@elucidata.io",
                        "added_on": 1669722856247,
                        "report_id": "c048a786-988d-4ff0-96c4-56f06211c9b5",
                        "url": "https://github.com/ElucidataInc/PublicAssets"
                    }
                    """
                    # case where url is linked to the dataset
                    url = items.get("url")
                    report_id = items.get("report_id")
                    details_list.append(added_by)
                    details_list.append(added_time)
                    details_list.append(url)
                    details_list.append(report_id)
                    all_details.append(details_list)
                else:
                    """
                    Contents of dict items
                    {
                        "report_id": str(uuid.uuid4()),
                        "workspace_id": "1456",
                        "file_name": "myreport.html",
                        "absolute_path": "1456/myreport.html",
                        "added_by": "circleci@elucidata.io",
                        "added_on": 1669722856247
                    }
                    """
                    # case where a workspace file is linked to a dataset
                    absolute_path = items.get("absolute_path")
                    workspace_id, workspace_path = helpers.split_workspace_path(
                        absolute_path
                    )
                    try:
                        sts_url = (
                            f"{self.base_url}/projects/{workspace_id}/credentials/files"
                        )
                        status = helpers.check_is_file(
                            self, sts_url, workspace_id, workspace_path
                        )
                    except Exception:
                        print(
                            f"Not enough permissions for the workspace_id : {workspace_id}. Please contact Polly Support."
                        )
                        continue
                    if not status:
                        # the file does not exist in the workspace, hence skipping this file path
                        print(
                            f"The workspace path '{workspace_path}' is invalid. Please contact Polly Support."
                        )
                        continue
                    shared_id = self._get_shared_id(workspace_id, workspace_path)
                    # file_url will be private or public based on shared_id
                    report_id = helpers.get_report_id(
                        self.session, workspace_id, workspace_path
                    )
                    file_url = self._return_workspace_file_url(
                        shared_id, access_url, workspace_id, workspace_path, report_id
                    )
                    report_id = items.get("report_id")
                    details_list.append(added_by)
                    details_list.append(added_time)
                    details_list.append(file_url)
                    details_list.append(report_id)
                    all_details.append(details_list)
            if len(all_details) == 0:
                print("No Reports to be displayed.")
            else:
                df = pd.DataFrame(all_details, columns=columns)
                pd.set_option("display.max_colwidth", None)
                return df

    def _return_workspace_file_url(
        self,
        shared_id,
        access_url: str,
        workspace_id: str,
        workspace_path: str,
        report_id: str,
    ) -> str:
        if shared_id is None:
            # return private url
            file_url = helpers.make_private_link(
                workspace_id, workspace_path, access_url, report_id
            )
        else:
            # return public url
            file_url = f"{access_url}/shared/file/?id={shared_id}"
        return file_url

    @Track.track_decorator
    def delete_linked_report(
        self, repo_key: str, dataset_id: str, report_id: str
    ) -> None:
        """
         Delete the link of the report in workspaces with the specified dataset in OmixAtlas.
         On success displays a success message.

        Arguments:
            repo_key (str): repo_name/repo_id of the repository which is linked.
            dataset_id (str): dataset_id of the dataset to be unlinked
            report_id (str): report id associated with the report in workspaces that is to be deleted. \
            This id can be found when invoking the fetch_linked_report() function.

        Raises:
            InvalidParameterException: Invalid parameter passed

        Returns:
            None
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (report_id and isinstance(report_id, str)):
            raise InvalidParameterException("report_id")
        # getting repo_id from the repo_key entered
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        params = {"dataset_id": f"{dataset_id}", "report_id": f"{report_id}"}
        url = f"{self.base_url}/v1/omixatlases/{repo_id}/reports"
        response = self.session.delete(url, params=params)
        error_handler(response)
        print(f"Linked file with report_id = '{report_id}' deleted.")

    def _get_shared_id(self, workspace_id, workspace_path):
        """
        Returns the shared_id of the file in workspace in case of global access to file, None in case of private access
        """
        # encoding the workspace_path for any special character that might pe present in the file_name,
        # example: 18891/report@name.html
        parsed_path = quote(workspace_path)
        url = f"https://v2.api.{self.session.env}.elucidata.io/projects/{workspace_id}/files/{parsed_path}"
        params = {"action": "file_download"}
        response = self.session.get(url, params=params)
        error_handler(response)
        shared_id = response.json().get("data").get("shared_id")
        return shared_id

    @Track.track_decorator
    def download_metadata(
        self, repo_key: str, dataset_id: str, file_path: str, metadata_key="field_name"
    ) -> None:
        """
        This function is used to download the dataset level metadata into a json file.
        The key present in the json file can be controlled using the `metadata_key` argument of the function.
        Users should use `original_name` for data ingestion.
        Args:
            repo_key (str): repo_name/repo_id of the repository where dataset belongs to.
            dataset_id (str): dataset_id of the dataset for which metadata should be downloaded.
            file_path (str): the system path where the json file should be stored.
            metadata_key (str, optional): Optional paramter. The metadata_key determines the key used in the json file.
            There are two options available `field_name` and `original_name`.
            For ingestion related use-cases, users should use `original_name` and for other purposes
            `field_name` should be preferred.
            The default value is `field_name`.
        Raises:
            InvalidParameterException: Invalid parameter passed
            InvalidPathException: Invalid file path passed
            InvalidDirectoryPathException: Invalid file path passed
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (file_path and isinstance(file_path, str)):
            raise InvalidParameterException("file_path")
        if not (
            (metadata_key.lower() in ["field_name", "original_name"])
            and isinstance(metadata_key, str)
        ):
            raise paramException(
                title="Param Error",
                detail="metadata_key argument should be either of the two values - [field_name, original_name]",
            )
        if not os.path.exists(file_path):
            raise InvalidPathException
        if not os.path.isdir(file_path):
            raise InvalidDirectoryPathException
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        index_name = data.get("indexes", {}).get("files")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{self.elastic_url}/{index_name}/_search"
        query = helpers.elastic_query(index_name, dataset_id)
        metadata = helpers.get_metadata(self, elastic_url, query)
        source_info = metadata.get("_source")
        file_name = f"{dataset_id}.json"
        complete_path = helpers.make_path(file_path, file_name)
        final_data = source_info
        if metadata_key == "original_name":
            # replace field names with original names
            data_type = source_info.get("data_type")
            schema_dict_tuple = self.get_schema(repo_key, return_type="dict")
            schema_dict_datasets = schema_dict_tuple.datasets
            schema_dict_val = (
                schema_dict_datasets.get("data", {})
                .get("attributes", {})
                .get("schema", {})
            )
            dataset_source = schema_dict_val.get("dataset_source")
            final_data = helpers.replace_original_name_field(
                source_info, schema_dict_val, dataset_source, data_type
            )
        with open(complete_path, "w") as outfile:
            json.dump(final_data, outfile)
        print(
            f"The dataset level metadata for dataset = {dataset_id} has been downloaded at : = {complete_path}"
        )

    @Track.track_decorator
    def download_dataset(self, repo_key: str, dataset_ids: list, folder_path=""):
        """
        This functions downloads the data for the provided dataset id list from the repo passed to
        the folder path provided.

        Arguments:
            repo_key (int/str): repo_id OR repo_name. This is a mandatory field.
            dataset_ids (list): list of dataset_ids from the repo passed that users want to download data of
            folder_path (str, optional): folder path where the datasets will be downloaded to. \
            Default is the current working directory.

        Returns:
            None

        Raises:
            InvalidParameterException : invalid or missing parameter
            paramException : invalid or missing folder_path provided
        """
        if not folder_path:
            folder_path = os.getcwd()

        try:
            omix_hlpr.param_check_download_dataset(
                repo_key=repo_key, dataset_ids=dataset_ids, folder_path=folder_path
            )
            repo_key = helpers.make_repo_id_string(repo_key)
            # number of jobs/workers set as 30 as that was the best performing while profiling
            # please refer ticket LIB-314 for more details/tech debt link
            # in sharedmem the memory is shared amongst the threads. Otherwise, for each thread a
            # different session is required, that needs to be authenticated.
            Parallel(n_jobs=30, require="sharedmem")(
                delayed(self._download_data_file)(repo_key, i, folder_path)
                for i in dataset_ids
            )
        except Exception as err:
            raise err

    def _download_data_file(self, repo_name: str, dataset_id: str, folder_path: str):
        try:
            download_response = self.download_data(
                repo_name, dataset_id, internal_call=True
            )
            url = (
                download_response.get("data", {})
                .get("attributes", {})
                .get("download_url")
            )
        except Exception as err:
            print(
                f"error in getting the download url for dataset_id: {dataset_id}. Download of this file will be skipped."
                + f" ERROR: {err}"
            )
            return
        try:
            """
            example URL:
            {'data': {'attributes': {'last-modified': '2022-11-22 18:25:31.000000', 'size': '39.68 KB', 'download_url':
            'https://discover-prod-datalake-v1.s3.amazonaws.com/GEO_data_lake/data/GEO_metadata/GSE7466/GCT/
            GSE7466_GPL3335_metadata.gct?X-Amz-Algorithm=.....f24f472f'}}}
            """
            filename = url.split("/")[-1].split("?")[0]
            filename_path = os.path.join(folder_path, filename)
            with requests.get(url, stream=True) as r:
                total_size_in_bytes = int(r.headers.get("content-length", 0))
                progress_bar = tqdm(
                    total=total_size_in_bytes,
                    unit="iB",
                    unit_scale=True,
                    desc=f"downloading data file:{filename}",
                    position=0,
                    leave=True,
                )
                r.raise_for_status()
                with open(filename_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        progress_bar.update(len(chunk))
                        f.write(chunk)
                progress_bar.close
        except Exception as err:
            # if any error occurs on downloading the data, then if the file is created/partially present
            # we delete that file.
            print(
                f"error in downloading the data from the url for dataset_id: {dataset_id}: {err}"
            )
            if os.path.exists(filename_path):
                os.remove(filename_path)
            return

    @Track.track_decorator
    def get_metadata(
        self, repo_key: str, dataset_id: str, table_name: str
    ) -> pd.DataFrame:
        """
        This function is used to get the sample level metadata as a dataframe.
        Args:
            repo_key(str): repo_name/repo_id of the repository.
            dataset_id(str): dataset_id of the dataset.
            table_name(str): table name for the desired metadata, 'samples','samples_singlecell' supported for now.
        Raises:
              paramException:
              RequestFailureException:
        """
        omix_hlpr.check_params_for_get_metadata(repo_key, dataset_id, table_name)
        repo_key = omix_hlpr.make_repo_id_string(repo_key)
        omixatlas_data = self._get_omixatlas(repo_key)
        v2_index = (
            omixatlas_data.get("data", {}).get("attributes", {}).get("v2_indexes", "")
        )
        # getting the mapped value for table_name from the dictionary
        actual_index = TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP.get(table_name, "")
        if actual_index not in v2_index:
            # this implies that this is an irrelevant index
            raise paramException(
                title="Param Error",
                detail=ERROR_MSG_GET_METADATA,
            )
        # getting the value for this index
        index = v2_index.get(actual_index, "")
        discover_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )
        page_size = 1000  # has to be less than 10k, chose 1000 as an optimal value for fast pagination

        dataframe = self._retrieve_dataframe(discover_url, page_size, dataset_id, index)
        return dataframe

    def _retrieve_dataframe(self, discover_url, page_size, dataset_id, index):
        """
        Function that drives the process of retrieval of dataframe.
        This function can be reused in future for getting metadata for dataset and feature level,
        with argument index being specified for respective metadata.
        """
        # loop for fetching data and setting the lower limit for the page_size
        while page_size > 50:
            query = helpers.make_query_for_discover_api(page_size, dataset_id)
            first_pass_data = self._initiate_retrieval(discover_url, query, index)
            if first_pass_data:
                # first pass yields a valid result for the query
                # sending this data for completing the process
                final_dataframe = self._complete_retrieval(
                    discover_url, first_pass_data
                )
                if final_dataframe is not False:
                    # complete result fetched in a dataframe
                    return final_dataframe
            # process interrupted as query failed due to large page_size, restart the process with page_size as half
            page_size = page_size / 2
        # the page_size reduction will happen only until page_size=50, raise an exception after that
        raise RequestFailureException

    def _initiate_retrieval(self, discover_url, query, index):
        """
        Function to kickstart the retrieval of sample level metadata using the discover endpoint,
        returns the result for the first pass.
        """
        payload = json.dumps(query)
        query_url = discover_url + f"/{index}/_search?scroll=1m"
        response = self.session.post(query_url, data=payload)
        if (
            response.status_code == http_codes.GATEWAY_TIMEOUT
            or response.status_code == http_codes.PAYLOAD_TOO_LARGE
        ):
            # a possible failure due to large page_size in the query
            return False

        try:
            if response.status_code != 200:
                omix_hlpr.handle_elastic_discover_api_error(response)
        except Exception as err:
            raise err

        search_result = json.loads(response.text)
        # search_result is a dictionary conatining the details from the endpoint
        hits = search_result.get("hits", {}).get("hits")
        if not hits:
            # the hits will be an empty list if the index is incorrect for the dataset_id
            raise Exception(
                "The index provided by you is not applicable for this dataset. \
For gct files, please use samples and for h5ad files, please use samples_singlecell. \
Please ensure that the dataset_id mentioned is present in the repo_key mentioned in the function parameters. \
If any issue persists, please contact polly.support@elucidata.io"
            )
        return search_result

    def _complete_retrieval(self, discover_url, search_result):
        """
        Function to complete the retrieval process and return the dataframe.
        """
        all_hits = []  # list for the comlete data
        hits = search_result.get("hits", {}).get("hits")  # results from the first pass
        # hits will be a list containing the data
        while hits:
            # combining hits in the first pass with the paginated results, if any
            all_hits += hits
            scroll_id = search_result["_scroll_id"]
            payload = json.dumps({"scroll": "1m", "scroll_id": scroll_id})
            response = self.session.post(discover_url + "/_search/scroll", data=payload)
            if (
                response.status_code == http_codes.GATEWAY_TIMEOUT
                or response.status_code == http_codes.PAYLOAD_TOO_LARGE
            ):
                # a possible failure due to large page_size in the query
                return False
            error_handler(response)
            search_result = json.loads(response.text)
            hits = search_result.get("hits", {}).get("hits")
        return pd.DataFrame(
            data=[hit.get("_source") for hit in all_hits if "_source" in hit]
        )

    def check_omixatlas_status(self, repo_key: str) -> bool:
        """
        function to check if a repository or omixatlas is locked or not.
        if the repository/omixatlas is locked, it is blocked for any schema or ingestion related processes.
        returns True if locked and False if not locked.
        Arguments:
            repo_key(int/str): repo_id or repo_name in str or int format
        Raises:
            paramException: incorrect parameter
            requestException: request exception
        Returns:
            Boolean: true or false
        """
        try:
            omix_hlpr.parameter_check_for_repo_id(repo_id=repo_key)
        except paramException as exception:
            # the actual exception coming from parameter_check_for_repo_id states just repo_id
            # doing this to raise the same exception but different msg with repo_key
            raise paramException(
                title="Param Error",
                detail="Argument 'repo_key' is either empty or invalid. \
                        It should either be a string or an integer. Please try again.",
            ) from exception
        repo_key = omix_hlpr.make_repo_id_string(repo_key)
        repo_locked_status_messages = {
            "No_Status": f"Unable to fetch the lock status for omixatlas: {repo_key}."
            + " Please contact polly support for assistance.",
            True: f"Omixatlas {repo_key} is locked."
            + " Operations such as data ingestion and editing schema and changing properties of the omixatlas"
            + " are not permitted while the OA is locked.",
            False: f"Omixatlas {repo_key} is not locked."
            + " All operations on the omixatlas are permitted.",
        }
        try:
            response_omixatlas = self._get_omixatlas(repo_key)
            data = response_omixatlas.get("data").get("attributes")
            if "is_locked" in data:
                is_locked = data.get("is_locked")
                if is_locked in repo_locked_status_messages.keys():
                    print(repo_locked_status_messages[is_locked])
                    return is_locked
                else:
                    print(repo_locked_status_messages["No_Status"])
                    return None
            else:
                print(repo_locked_status_messages["No_Status"])
                return
        except Exception as err:
            print(
                f" Error in getting the lock status for omixatlas: {repo_key}."
                + f" ERROR: {err}"
            )
            return


if __name__ == "__main__":
    client = OmixAtlas()
