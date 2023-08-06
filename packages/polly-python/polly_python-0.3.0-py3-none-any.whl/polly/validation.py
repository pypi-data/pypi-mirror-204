from polly.help import example
from polly.auth import Polly
from polly import helpers, constants as const
from polly.omixatlas import OmixAtlas
import pandas as pd
import copy
import polly.validation_hlpr as validation_hlpr
from polly_validator.validators import dataset_metadata_validator


class Validation:
    """Validation Class for Integrating External Validation Library"""

    example = classmethod(example)

    def __init__(
        self,
        token=None,
        env="",
        default_env="polly",
    ) -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)

    def validate_datasets(self, repo_id: int, source_folder_path: dict) -> pd.DataFrame:
        """Validate the dataset level metadata for datasets to be Ingested
        Args:
            repo_id(int/string): Repo id of OmixAtlas
            source_folder_path(dict): Source folder path of data and metadata files.
        Returns:
            err_dataset(DataFrame): All the errors
            status_dict(Dictionary): Status of all the Files
        """
        # add method to validate the params
        try:
            self._check_validate_dataset_params(repo_id, source_folder_path)
            repo_id = helpers.make_repo_id_string(repo_id)
            return self._validate_dataset_level_metadata(repo_id, source_folder_path)
        except Exception as err:
            raise err

    def _check_validate_dataset_params(self, repo_id: str, source_folder_path: dict):
        """Check passed params in validate datasets
        Args:
            repo_id(int/string): Repo id of the repo
            source_folder_path(dict): Source folder path from data and metadata files are fetched
        """
        try:
            helpers.parameter_check_for_repo_id(repo_id)
            validation_hlpr.data_metadata_parameter_check(source_folder_path)
        except Exception as err:
            raise err

    def _validate_dataset_level_metadata(
        self, repo_id: str, source_folder_path: dict
    ) -> pd.DataFrame:
        """Validate Dataset level metadata
        Args:
            repo_id(int/string): Repo id of OmixAtlas
            source_folder_path(dict): Source folder path of data and metadata files.
            validation_level(str): Level to validate on, by default advanced level
        Returns:
            err_dataset(DataFrame): All the errors
            status_dict(Dictionary): Status of all the Files
        """
        # list of metadata files to validate
        # metadata files grouped in a list
        # grouping is done on validation level parameter
        try:
            # construct dataframe of schema for the repo
            # formatted schema DF based on Input Required by Validation Lib
            # Formatted DF has 2 rows -> Field Name and Type
            schema_df_dataset = self._construct_df_of_schema(repo_id)
            combined_metadata = (
                validation_hlpr.construct_combined_metadata_for_validation(
                    source_folder_path
                )
            )
            # key1 -> "error" & val -> list of error DFs
            # key2 -> "status" & val -> list of status dicts
            validation_lib_res = {}
            validation_lib_res["error"] = []
            validation_lib_res["status"] = []

            # calling schema functions for different `validate_on` values
            # validate_on val is fetched from scope of validation from metadata file
            # right now there are only two i.e basic -> schema and advanced -> value

            # Only run validation if there are files to be validated
            if combined_metadata:
                for (
                    validate_on_val,
                    metadata_list_of_dicts,
                ) in combined_metadata.items():
                    (
                        err_dataset,
                        status_dict_from_validation,
                    ) = dataset_metadata_validator.check_metadata_for_errors(
                        repo=repo_id,
                        schema_df=schema_df_dataset,
                        metadata_list=metadata_list_of_dicts,
                        validate_on=validate_on_val,
                        env=self.session.env,
                        auth_token=self.session.token,
                        print_table=True,
                    )

                    # status and err dataset for each group
                    validation_lib_res.get("error").append(err_dataset)
                    validation_lib_res.get("status").append(status_dict_from_validation)

            error_df = helpers.merge_dataframes_from_list(
                validation_lib_res.get("error")
            )
            status_dict = helpers.merge_dicts_from_list(
                validation_lib_res.get("status")
            )
            validation_hlpr.create_status_file(
                status_dict, source_folder_path["metadata"]
            )
            return error_df, status_dict
        except Exception as err:
            raise err

    def _construct_df_of_schema(self, repo_id: str) -> pd.DataFrame:
        """Construct DF of schema from schema dict
        Schema Dict Format(For Every Field In Schema)
        Field Name -----> Type
        Type here for every field name should be SQL Type
        Args:
            repo_id (str/int): repo id of the repo
        Returns:
            pd.DataFrame: DataFrame of Schema of that repo
            DataFrame contains Fields of the schema and types(SQL types)
        """
        omix_obj = OmixAtlas()
        schema_dict_tuple = omix_obj.get_schema(repo_id, return_type="dict")
        schema_dict_datasets = schema_dict_tuple.datasets
        schema_dict_val = (
            schema_dict_datasets.get("data", {}).get("attributes", {}).get("schema", {})
        )
        schema_type_dict = {}
        for source_key, source_val in schema_dict_val.items():
            for datatype_key, datatype_val in source_val.items():
                for field_name, field_attributes in datatype_val.items():
                    schema_type_dict[field_name] = {}
                    schema_type_dict[field_name]["type"] = field_attributes["type"]
                    schema_type_dict[field_name]["is_array"] = field_attributes[
                        "is_array"
                    ]

        all_fields_type_dict = []

        # fields not needed by validation lib
        not_needed_schema_fields = copy.deepcopy(const.NOT_NEEDED_SCHEMA_FIELDS)

        for field_name, field_attributes in schema_type_dict.items():
            if field_name not in not_needed_schema_fields:
                field_type_dict = {}
                field_type_dict["column_name"] = field_name
                if field_attributes["is_array"]:
                    if field_attributes["type"] == "text":
                        data_type = "string"
                    else:
                        data_type = field_attributes["type"]
                    full_datatype = f"array<{data_type}>"
                    field_type_dict["column_type"] = full_datatype
                else:
                    if field_attributes["type"] == "text":
                        field_type_dict["column_type"] = "string"
                    else:
                        field_type_dict["column_type"] = field_attributes["type"]

                all_fields_type_dict.append(field_type_dict)

        schema_df = pd.DataFrame(all_fields_type_dict)
        return schema_df
