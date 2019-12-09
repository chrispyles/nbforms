###############################
###### nbforms Python API #####
###############################

from .widgets import *

import datascience as ds
import pandas as pd
import requests
import os
from io import StringIO
from getpass import getpass
from ipywidgets import interact, Button, VBox, HBox, interactive_output, Label
from IPython.display import display

class Notebook:
    """nbforms class for interacting with an nbforms server"""

    def __init__(self, config_path="nbforms_config.py"):
        assert os.path.exists(config_path) and os.path.isfile(config_path), \
        "{} is not a valid config path".format(config_path)

        with open(config_path) as f:
            contents = f.read()

        exec_dict = {}
        exec(contents, exec_dict)
        assert "nbforms_config" in exec_dict, "inable to execute config file"
        self._config = exec_dict["nbforms_config"]

        assert all([i in self._config for i in ["server_url", "questions", "notebook"]]), \
        "config file missing required information"

        self._server_url = self._config["server_url"]
        self._notebook = self._config["notebook"]

        self._auth_url = os.path.join(self._server_url, "auth")
        self._submit_url = os.path.join(self._server_url, "submit")
        self._data_url = os.path.join(self._server_url, "data")

        self._questions = self._config["questions"]
        
        self._identifiers = []
        self._widgets = {}
        self._responses = {}

        for q in self._questions:
            assert all([t in q.keys() for t in ["identifier", "type", "question"]]), "a question is missing a required key"
            
            self._identifiers += [q["identifier"]]
            widget = TYPE_MAPPING[q["type"]](q)
            self._widgets[q["identifier"]] = widget

        # ask user for a username and password
        print("Please enter a username and password for nbforms.")
        self._username = input("Username: ")
        password = getpass("Password: ")

        # auth to get API key
        auth_response = requests.post(self._auth_url, {
            "username": self._username,
            "password": password
        })

        # check that sign in was OK, store API key
        assert auth_response.text != "INVALID USERNAME", "Incorrect username or password"
        self._api_key = auth_response.text

    def _save_current_response(self, identifier, response):
        self._responses[identifier] = response

    def _send_response(self, identifier):
        requests.post(self._submit_url, {
            "identifier": identifier,
            "username": self._username,
            "api_key": self._api_key,
            "notebook": str(self._notebook),
            "response": str(self._responses[identifier]),
        })

    def _get_data(self, identifiers, user_hashes=False):
        response = requests.get(self._data_url, {
            "questions": ",".join(identifiers),
            "notebook": str(self._notebook),
            "user_hashes": (0, 1)[user_hashes]
        })
        return response.text

    def _create_submit_button(self, identifier):
        button = Button(
            description="Submit"
        )
        button.on_click(lambda b: self._send_response(identifier))
        return button

    def _arrange_single_widget(self, identifier):
        label, widget = self._widgets[identifier].to_widget_tuple()
        interactive = interactive_output(lambda response: self._save_current_response(identifier, response),
                                 {"response": widget})
        button = self._create_submit_button(identifier)
        ui = VBox([VBox([label, widget]), button])
        return ui, interactive

    def ask(self, identifier):
        assert identifier in self._identifiers, "question {} does not exist".format(identifier)
        ui, interactive = self._arrange_single_widget(identifier)
        display(ui, interactive)

    def to_table(self, *identifiers, user_hashes=False):
        csv_string = self._get_data(identifiers, user_hashes=user_hashes)
        df = pd.read_csv(StringIO(csv_string))
        return ds.Table.from_df(df)

    def to_df(self, *identifiers, user_hashes=False):
        csv_string = self._get_data(identifiers, user_hashes=user_hashes)
        df = pd.read_csv(StringIO(csv_string))
        return df
        
