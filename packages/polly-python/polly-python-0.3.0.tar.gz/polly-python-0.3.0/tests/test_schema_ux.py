from typing import Dict
from polly.auth import Polly
from polly import omixatlas
import pandas as pd
import os
import pytest
from polly.errors import paramException, RequestException

key = "TEST_POLLY_REFRESH_TOKEN"
token = os.getenv(key)


def test_obj_initialization():
    assert Polly.get_session(token, env="testpolly") is not None
    assert omixatlas.OmixAtlas(token, env="testpolly") is not None


def test_get_schema_with_repo_id_and_both_dataset_and_sample_schema_param():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"dataset": "files", "sample": "gct_metadata"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    source = ""
    data_type = ""
    schema = schema_obj._get_schema_from_api(
        repo_id, schema_type_dict, source, data_type
    )
    assert isinstance(schema, Dict)
    assert schema["dataset"] is not None
    assert schema["sample"] is not None


def test_get_schema_with_repo_id_and_sample_schema_param():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"sample": "gct_metadata"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    source = ""
    data_type = ""
    schema = schema_obj._get_schema_from_api(
        repo_id, schema_type_dict, source, data_type
    )
    assert isinstance(schema, Dict)
    assert schema["sample"] is not None


def test_get_schema_full_payload():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"dataset": "files", "sample": "gct_metadata"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema = schema_obj._get_full_schema_payload_from_api(repo_id, schema_type_dict)

    assert isinstance(schema, Dict)
    # directly payload of API is returned
    assert schema["dataset"] is not None
    assert schema["sample"] is not None


def test_get_schema_with_repo_id_and_dataset_schema_param():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"dataset": "files"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    source = ""
    data_type = ""
    schema = schema_obj._get_schema_from_api(
        repo_id, schema_type_dict, source, data_type
    )
    assert isinstance(schema, Dict)
    assert schema["dataset"] is not None


def test_get_schema_type_dataset_schema_level_single_cell_bool_false_as_params():
    schema_level = ["dataset", "sample"]
    data_type = "others"
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = schema_obj._get_schema_type(schema_level, data_type)
    assert isinstance(schema_type, Dict)
    assert schema_type["dataset"] is not None
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "gct_metadata"


def test_get_schema_type_dataset_schema_level_single_cell_bool_true_as_params():
    schema_level = ["dataset", "sample"]
    data_type = "single_cell"
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = schema_obj._get_schema_type(schema_level, data_type)
    assert isinstance(schema_type, Dict)
    assert schema_type["dataset"] is not None
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "h5ad_metadata"


def test_get_schema_type_dataset_as_params():
    schema_level = ["dataset"]
    data_type = "single_cell"
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = schema_obj._get_schema_type(schema_level, data_type)
    assert isinstance(schema_type, Dict)
    assert schema_type["dataset"] is not None


def test_get_schema_type_schema_level_single_cell_bool_true_as_params():
    schema_level = ["sample"]
    data_type = "single_cell"
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = schema_obj._get_schema_type(schema_level, data_type)
    assert isinstance(schema_type, Dict)
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "h5ad_metadata"


def test_get_schema_type_schema_level_single_cell_bool_false_as_params():
    schema_level = ["sample"]
    data_type = "others"
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = schema_obj._get_schema_type(schema_level, data_type)
    assert isinstance(schema_type, Dict)
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "gct_metadata"


def test_get_schema_full_payload_dict_when_return_type_dict():
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all", return_type="dict"
    )

    assert isinstance(resp.dataset, Dict)


def test_get_schema_default_return_type():
    # default return type is dataframe
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all"
    )
    assert isinstance(resp.dataset, pd.DataFrame)


def test_get_schema_with_valid_table_names():
    # default return type is dataframe
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    resp = omix_obj_test.get_schema(
        repo_key_1, ["datasets", "samples"], source="all", data_type="all"
    )
    assert isinstance(resp.datasets, pd.DataFrame)
    assert isinstance(resp.samples, pd.DataFrame)


def test_get_schema_with_valid_schema_level_values():
    # dataset, sample are valid schema lvl values
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all"
    )
    assert isinstance(resp.dataset, pd.DataFrame)


def test_get_schema_schema_level_param_empty_by_default_all_values():
    # neither valid table name or schema level value passed
    # should take all the table names
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(repo_key_1, [], source="all", data_type="all")
    # will take all the table names present for this repo
    # for this repo 3 table names are there
    # datasets, samples, features
    # all three should be present in the schema
    assert resp.datasets is not None
    assert isinstance(resp.datasets, pd.DataFrame)

    assert resp.samples is not None
    assert isinstance(resp.samples, pd.DataFrame)


"""def test_get_schema_with_valid_schema_level_value_and_incorrect_data_type_value():
    # valid schema level sample with "single cell" as data_type
    # as data_type is only `all` -> there is no single_cell datatype in the schema
    # it should return error
    repo_key_2 = "sc_data_lake"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    with pytest.raises(
        RequestException,
        match=r".*Datatype passed in the query param does not existfor this source: all. You can try these instead ['all']*",
    ):
        omix_obj_test.get_schema(
            repo_key_2, ["sample"], source="all", data_type="single_cell"
        )"""


def test_get_schema_with_valid_schema_table_value_return_type_dict():
    # valid schema table value and return type dict
    # it should return dict in response
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    resp = omix_obj_test.get_schema(
        repo_key_1,
        ["datasets", "samples"],
        source="all",
        data_type="all",
        return_type="dict",
    )
    assert isinstance(resp.datasets, dict)
    assert isinstance(resp.samples, dict)


def test_get_schema_with_valid_schema_level_value_return_type_dict():
    # valid schema  value and return type dict
    # it should return dict in response
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all", return_type="dict"
    )
    assert isinstance(resp.dataset, dict)


def test_get_schema_wrong_repo_key_param():
    # repo key wrong passed here
    repo_key_2 = "abc"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    with pytest.raises(
        RequestException,
        match=r".*Repository with repo key abc not found.*",
    ):
        omix_obj_test.get_schema(repo_key_2, ["sample"], source="all", data_type="all")


def test_get_schema_valid_table_name_in_schema_level_wrong_source():
    # wrong source passed
    # ingestion_test_1
    repo_key_2 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    with pytest.raises(
        RequestException,
        match=r".*Source passed in the query param not found.You can try these instead ['all']*",
    ):
        omix_obj_test.get_schema(
            repo_key_2, ["datasets", "samples"], source="abc", data_type="all"
        )


def test_get_schema_invalid_schema_level_value_passed():
    # wrong source passed
    # ingestion_test_1
    repo_key_2 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    with pytest.raises(
        paramException,
        match=r".*schema_level input is incorrect. Use the query SHOW TABLES IN <repo_name>.*",
    ):
        omix_obj_test.get_schema(repo_key_2, ["abc"], source="all", data_type="all")


def test_get_schema_type_info():
    # returns the schema level based on schema type / table name
    # ingestion_test_1
    repo_key = "1654268055800"
    # table names in geo
    schema_level = ["datasets", "samples"]
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    res = omix_obj_test._get_schema_type_info(repo_key, schema_level, "")

    assert isinstance(res, dict)
    assert res.get("datasets") == "files"
    assert res.get("samples") == "gct_metadata"
