# This is the client.py module for movemapp_client package

import carto
from carto.auth import APIKeyAuthClient
from carto.api_keys import APIKeyManager
from carto.datasets import DatasetManager
import re


class MovemappClient:
    def __init__(self,
                 geodb_master_api_key,
                 geodb_url,
                 lga_number,
                 lga_name=None,
                 **kwargs
                 ):
        self.geodb_master_api_key = geodb_master_api_key
        self.geodb_url = geodb_url
        self.lga_number = lga_number
        # infer schema from the url based on the regex for
        self.schema = re.search(
            r"https://\w+\.geodb\.host/user/(\w+)/?", geodb_url).group(1)

        # raise an error if the schema is not found
        if self.schema is None:
            raise ValueError("The schema could not be inferred from the url")

        self.dataset_search_pattern = f"movemapp_{self.lga_number}_*"
        self.api_key_name = f"mvmp_{self.lga_number}_ro"

        # create a carto-python SDK client
        self.geodb_auth_client = APIKeyAuthClient(
            self.geodb_url,
            self.geodb_master_api_key
        )

        self.geodb_api_key_manager = APIKeyManager(
            self.geodb_auth_client
        )

        self.geodb_dataset_manager = DatasetManager(
            self.geodb_auth_client
        )

    def get(self, resource):
        # add support for the datasets resource
        if resource == "datasets":
            return self.get_datasets()
        elif resource == "api_key":
            return self.get_api_key_as_dict()
        else:
            return []

    def get_api_key_as_dict(self):
        api_key = self.get_api_key()
        return {
            "token": api_key.token,
            "name": api_key.name
        }

    def create(self, resource):
        if resource == "api_key":
            return self.create_api_key()
        else:
            return []

    def delete(self, resource):
        if resource == "api_key":
            return self.delete_api_key()
        else:
            return []

    def get_api_key(self):
        # get the list of api keys
        api_keys = self.geodb_api_key_manager.all()
        # filter the list of api keys to find the one that matches
        # the api key name pattern
        api_key = next(
            (api_key for api_key in api_keys
             if api_key.name.startswith(self.api_key_name)),
            None
        )
        # if the api key is not found, create it
        if api_key is None:
            api_key = self.create("api_key")

        return api_key

    def get_datasets(self):
        self.datasets = self.geodb_dataset_manager.filter(
            q=self.dataset_search_pattern
        )

        # get the list of table_names
        return [dataset.name for dataset in self.datasets]

    def create_api_key(self):
        grants = [
            {
                "schema": self.schema,
                "name": table,
                "permissions": ["select"]
            } for table in self.get_datasets()
        ]

        api_key = self.geodb_api_key_manager.create(
            name=self.api_key_name,
            apis=['sql', 'maps'],
            tables=grants
        )

        return api_key

    def delete_api_key(self):
        api_key = self.get_api_key()
        api_key.delete()
