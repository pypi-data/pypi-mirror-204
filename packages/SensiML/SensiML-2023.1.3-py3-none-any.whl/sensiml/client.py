import json
import logging
import os
import re
from ast import Str
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional, Tuple
from xml.dom import ValidationErr

import requests
from appdirs import user_config_dir
from packaging import version

try:
    from qgrid import show_grid
except:
    pass

from time import sleep

import pandas as pd
from pandas import DataFrame

import sensiml.base.utility as utility
from sensiml.base.snippets import Snippets, function_help
from sensiml.connection import Connection
from sensiml.datamanager import (
    ClientPlatformDescriptions,
    Functions,
    Projects,
    SegmenterSet,
    Team,
)
from sensiml.datamanager.captures import CaptureExistsError
from sensiml.datamanager.knowledgepack import delete_knowledgepack, get_knowledgepack
from sensiml.datasets import DataSets
from sensiml.dclproj.upload import upload_project, upload_project_dcli

# from sensiml.base.exceptions import *
from sensiml.pipeline import Pipeline

config_dir = user_config_dir(__name__.split(".")[0], False)

SERVER_URL = "https://sensiml.cloud/"

AUTH2_PRIMARY = True

logger = logging.getLogger("SensiML")

__version__ = "2023.1.3"


def project_set(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if self._project is None:
            print("Project must be set.")
            return None
        else:
            return func(*args, **kwargs)

    return wrapper


def print_list(func):
    """This is a wrapper for printing out lists of objects stored in SensiML Cloud"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if len(result.keys()) == 0 and kwargs.get("silent", False) == False:
            print(
                "No {} stored on SensiML Cloud for this project.".format(
                    " ".join(func.__name__.split("_")[1:])
                )
            )
            return None
        if kwargs.get("get_objects", False) is True:
            return result

        tmp_dict = [
            {
                "Name": name,
                "UUID": item.uuid,
                "Created": item.created_at,
                "Last Modified": item.created_at
                if not hasattr(item, "last_modified")
                else item.last_modified,
            }
            for name, item in result.items()
        ]

        extra = {}
        additional_keys = []
        if func.__name__ == "list_queries":
            extra = [
                {"Cached": True if item.cache else ""} for name, item in result.items()
            ]
            additional_keys = ["Cached"]

        if func.__name__ == "list_sandboxes":
            extra = [
                {"CPU Used (seconds)": item.cpu_clock_time}
                for name, item in result.items()
            ]
            additional_keys = ["CPU Used (seconds)"]

        for index, value in enumerate(extra):
            tmp_dict[index].update(value)

        return DataFrame(
            tmp_dict,
            columns=["Name", "Last Modified", "Created", "UUID"] + additional_keys,
        )

    return wrapper


class Client(object):
    def __init__(
        self,
        server=SERVER_URL,
        path="connect.cfg",
        use_jedi=False,
        insecure=False,
        skip_validate=False,
        verbose_connection=False,
        **kwargs,
    ):

        self._project = None
        self._pipeline = None
        auth_url = server + "oauth/"

        self._connection = Connection(
            server=server,
            auth_url=auth_url,
            path=path,
            insecure=insecure,
            oauth2_primary=AUTH2_PRIMARY,
            debug=verbose_connection,
            **kwargs,
        )

        if not self.validate_client_version(skip_validate):
            return
        self.projects = Projects(self._connection)
        self.datasets = DataSets()
        self.functions = Functions(self._connection)
        self.platforms_v2 = ClientPlatformDescriptions(self._connection)
        self.platforms = self.platforms_v2
        self.team = Team(self._connection)
        self.snippets = Snippets(
            self.list_functions(kp_functions=False, qgrid=False),
            self.functions.function_list,
        )
        self._feature_files = None

        if use_jedi is False:
            self.setup_jedi_false()

    def setup_jedi_false(self):
        """This is a temporary bug fix in ipython autocomplete"""
        try:
            mgc = get_ipython().magic
            mgc("%config Completer.use_jedi = False")
        except:
            pass

    def validate_client_version(self, skip_validate=True):
        """Perform a Validation check to see if this version of SensiML is up to date with the latest."""

        if skip_validate:
            return True

        url = "version/"

        response = self._connection.request("get", url)
        response_data, err = utility.check_server_response(response)

        if response_data.get("SensiML_Python_Library_Windows_Minimum") is None:
            return True

        if version.parse(
            response_data["SensiML_Python_Library_Windows_Minimum"]
        ) > version.parse(__version__):
            print(
                f"Error: The SensiML Python SDK is out of date.\n\n\tCurrent installed version = {__version__}. \n\tMinimum supported version = {response_data['SensiML_Python_Library_Windows_Minimum']}."
            )
            print(
                "\nTo update the SensiML Python SDK run \n\n\tpip install sensiml -U\n\nIf you are in a notebook, you can execute the following in a cell then restart the shell.\n\n\t!pip install sensiml -U"
            )
            print(
                "\nTo disable this validation check and connect anyway you can use the skip_validate parameter\n\n\tclient = Client(skip_validate=True)"
            )
            return False

        return True

    def logout(self, name=None):
        """Logs out of the current connection."""
        if name is None:
            name = self._connection.server_name

        Connection.logout(name)

    def get_url(self, url):

        response = self._connection.request("get", url)
        print(response.json())
        return response

    def account_info(self):
        """Get information about your account Usage"""

        url = "team-info/"
        return self.get_url(url)

    def account_subscription(self):
        """Get information about your account Subscription"""

        url = "team-subscription/"
        return self.get_url(url)

    def get_function(self, name):
        """Gets a function method call"""
        return self.functions.function_list[name]

    def function_description(self, name):
        """Gets a description of a pipeline function."""
        print(self.functions.create_function_call(name).__doc__)

    def function_help(self, name):
        """Prints a shortened description of a function."""
        print(function_help(self.functions.function_list[name]))

    def list_functions(
        self, functype=None, subtype=None, kp_functions=False, qgrid=False
    ):
        """Lists all of the functions available on SensiML Cloud

        Returns:
            Dataframe

        Args:
            functype (str, None): Return only functions with the specified type. ie. "Segmenter"
            subtype (str, None): Return only functions with the specified subtype. ie. "Sensor"
            kp_functions (boolean, True): Return only functions that run on the loaded device.
            Excludes functions such as feature selection and model training.
        """

        df = (
            DataFrame(
                [
                    {
                        "NAME": f.name,
                        "TYPE": f.type,
                        "DESCRIPTION": f.description.lstrip("\n").lstrip(" ")
                        if f.description
                        else "",
                        "SUBTYPE": f.subtype,
                        "KP FUNCTION": f.has_c_version,
                        "UUID": f.uuid,
                        "LIBRARY": f.library_pack,
                        "AVAILABLE": f.automl_available,
                    }
                    for name, f in self.functions.function_list.items()
                ]
            )
            .sort_values(by=["TYPE", "SUBTYPE"])
            .reset_index(drop=True)[
                [
                    "NAME",
                    "TYPE",
                    "SUBTYPE",
                    "DESCRIPTION",
                    "KP FUNCTION",
                    "AVAILABLE",
                    "UUID",
                    "LIBRARY",
                ]
            ]
        )

        if functype:
            df = df[df["TYPE"] == functype]

        if subtype:
            df = df[df["SUBTYPE"] == subtype]

        if kp_functions:
            df = df[df["KP FUNCTION"] == True][
                ["NAME", "TYPE", "SUBTYPE", "DESCRIPTION", "LIBRARY"]
            ]

        if qgrid:
            return show_grid(df.reset_index(drop=True))
        else:
            return df.reset_index(drop=True)

    def delete_project(self):
        """Deletes a project"""
        if self._project is not None:
            self._project.delete()

    @print_list
    def list_projects(self, get_objects=False, silent=False):
        """Lists all of the projects on SensiML Cloud

        Returns:
            DataFrame: projects on SensiML Cloud
        """
        return self.projects.build_project_dict()

    def list_segmenters(
        self,
    ):
        if self._project is None:
            print("project must be set to list segmenters.")
            return None

        segmenters = SegmenterSet(self._connection, self._project)

        if not len(segmenters.objs):
            print("No segmenters stored on the Cloud.")
            return None

        return segmenters.to_dataframe()

    def get_knowledgepack(self, uuid):
        """Retrieve a Knowledge Pack by uuid from the server associated with current project

        Args:
            uuid (str): unique identifier for Knowledge Pack

        Returns:
            TYPE: a Knowledge Pack object
        """

        return get_knowledgepack(uuid, self._connection)

    def delete_knowledgepack(self, uuid):
        """Delete Knowledge Pack by uuid from the server associated with current project

        Args:
            uuid (str): unique identifier for Knowledge Pack

        Returns:
            TYPE: a Knowledge Pack object
        """

        return delete_knowledgepack(uuid, self._connection)

    @property
    def project(self):
        """The active project"""
        return self._project

    def get_featurefile(self, uuid):
        """Get a FeatureFile by uuid

        Args:
            get_objects (bool, False): Also return the FeatureFile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._feature_files.get_featurefile(uuid)

    def get_datafile(self, uuid):
        """Get a datafile by uuid

        Args:
            get_objects (bool, False): Also return the datafile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._feature_files.get_featurefile(uuid)

    @print_list
    def list_featurefiles(self, get_objects=False, silent=False):
        """List all feature and data files for the active project.

        Args:
            get_objects (bool, False): Also return the featurefile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._feature_files.build_featurefile_list()

    @print_list
    def list_datafiles(self, get_objects=False, silent=False):
        """List all feature and data files for the active project.

        Args:
            get_objects (bool, False): Also return the featurefile objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._feature_files.build_datafile_list()

    @print_list
    def list_captures(self, get_objects=False, force=False):
        """List all captures for the active project

        Args:
            get_objects (bool, False): Also return the capture objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._captures.build_capture_list(force=force)

    @print_list
    def refresh_capture_list(self, get_objects=False):
        """Refresh the internal capture list from the server

        Args:
            get_objects (bool, False): Also return the capture objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._captures.build_capture_list(force=True)

    @project_set
    def get_captures(self, force: bool = True):
        """Returns the capture set object"""
        return self._project._captures.build_capture_list(force=force)

    def download_capture(
        self, filename: str, outdir: Optional[str] = None, force: bool = False
    ):
        """Downloads the capture file from the server

        Args:
            filename (str): name of the file to download
            outdir (Optional[str], optional): directory to put the downloaded file, defaults to current directory.
            force (bool, optional): refresh the capture list

        """
        return self._project._captures.build_capture_list(force=force)[
            filename
        ].download(outdir=outdir)

    def _download_captures(
        self,
        filenames: List[str],
        outdir: Optional[str] = None,
        expires_in: int = 100,
        verbose=True,
    ):

        capture_response = self.project.captures.get_capture_urls_by_name(
            filenames, expires_in=expires_in
        )

        for capture in capture_response:
            url = capture["url"]

            if capture.get("local"):
                response = self._connection.request("get", url)
            else:
                response = requests.get(url)

            if outdir is None:
                outdir = "./"

            if capture["name"][-4:] == ".csv":
                with open(os.path.join(outdir, capture["name"]), "w") as out:
                    out.write(response.text)
                    if verbose:
                        print(
                            f"Capture saved to {os.path.join(outdir, capture['name'])}"
                        )

            elif capture["name"][-4:] == ".wav":
                with open(os.path.join(outdir, capture["name"]), "wb") as out:
                    out.write(response.content)
                    if verbose:
                        print(
                            f"Capture saved to {os.path.join(outdir, capture['name'])}"
                        )

            else:
                raise Exception("Unknown file type")

        return "Success"

    def _download_capture_parallel_multithreading_urls(
        self,
        filenames: List[str],
        outdir: Optional[str] = None,
        batch_size: int = 10,
        max_workers: int = 12,
        expires_in=300,
    ):
        batch_size = batch_size
        file_batches = []
        last = 0
        for i in range(0, len(filenames), batch_size):
            file_batches.append(filenames[i : i + batch_size])
            last = i + batch_size
        file_batches.append(filenames[last:])

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_key = {
                executor.submit(
                    self._download_captures, batch, outdir, expires_in, False
                ): batch
                for batch in file_batches
            }

            for future in futures.as_completed(future_to_key):
                key = future_to_key[future]
                exception = future.exception()

                if not exception:
                    yield key, future.result()
                else:
                    yield key, exception

    def download_captures(
        self,
        filenames: List[str],
        outdir: Optional[str] = None,
        max_workers: int = 8,
        batch_size=10,
    ):
        """Downloads a list of capture files from the server

        Args:
            filenames (List[str]): List of file names to download
            outdir (Optional[str], optional): Directory to download files to. Defaults to None.
            max_workers (int, optional): number of worker threads to use. Defaults to 8.
            batch_size (int, optional): batch size to use in each worker thread. Defaults to 10.
        """
        count = 0
        for key, result in self._download_capture_parallel_multithreading_urls(
            filenames, outdir=outdir, max_workers=max_workers, batch_size=batch_size
        ):
            count += batch_size
            print(f"{count}/{len(filenames)} {key} result: {result}")

    @print_list
    def list_capture_configurations(self, get_objects=False):
        """List all captures for the active project

        Args:
            get_objects (bool, False): Also return the capture objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")

        return self._project._capture_configurations.build_capture_list()

    def capture_configurations(self):
        """Returns the capture set object"""
        return self._project._capture_configurations.build_capture_list()

    @print_list
    def list_sandboxes(self, get_objects=False):
        """List all sandboxes for the active project.

        Args:
            get_objects (bool, False): Also return the sandbox objects.

        """
        print("list_sanboxes has been deprecated in favor of list_pipelines.")
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._sandboxes.build_sandbox_list()

    @project_set
    def get_pipelines(self):
        """Returns the pipeline set dictionary"""
        return self._project._sandboxes.build_sandbox_list()

    @print_list
    def list_pipelines(self, get_objects=False):
        """List all pipelines for the active project.

        Args:
            get_objects (bool, False): Also return the sandbox objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._sandboxes.build_sandbox_list()

    @print_list
    def list_queries(self, get_objects=False):
        """List all queries for the active project.

        Args:
            get_objects (bool, False): Also return the query objects.

        """
        if self._project is None:
            raise Exception("Project must be set to perform this action.")
        return self._project._queries.build_query_list()

    @project_set
    def get_queries(self):
        """Returns the query set dictionary"""
        return self._project._queries.build_query_list()

    @project.setter
    def project(self, name):
        self._project = self.projects.get_or_create_project(name)

    @property
    def pipeline(self):
        """The active pipeline"""
        return self._pipeline

    @pipeline.setter
    def pipeline(self, name):
        if self._project is None:
            raise Exception("Project must be set before a pipeline can be created")

        self._pipeline = Pipeline(self, name=name)

    def create_query(
        self,
        name: str,
        columns: list = [],
        metadata_columns: list = [],
        metadata_filter: str = "",
        segmenter=None,
        label_column: str = "",
        combine_labels=None,
        force: bool = False,
        renderer=None,
        capture_configurations: str = "",
    ):
        """Create a query to use as input data in a pipeline.

        Args:
            name (str): Name of the query.
            columns (list, optional): Columns to add to the query result.
            metadata_columns (list, optional): Metadata to add to the query result.
            metadata_filter (str, optional): Filter to apply to the query.
            segmenter (int, optional): Segmenter to filter query by.
            force (bool, False): If True overwrite the query on kb cloud.

        Returns:
            object: Returns a query object that was created.
        """

        query = self.project.queries.get_query_by_name(name)

        new = False
        if query is not None and not force:
            raise Exception("Query already exists. Set force=True to overwrite.")
        elif query is not None and force:
            query.columns.clear()
            query.metadata_columns.clear()
            query.metadata_filter = ""
            query.label_column = ""
            query.capture_configurations = ""
            query.segmenter = None

        else:
            query = self.project.queries.new_query()
            query.name = name
            new = True

        for col in columns:
            logger.debug("query_column:" + str(col))
            query.columns.add(col)

        for col in metadata_columns:
            logger.debug("query_metadata_column:" + str(col))
            query.metadata_columns.add(col)

        if metadata_filter:
            logger.debug("query_metadata_filter:" + str(metadata_filter))
            query.metadata_filter = metadata_filter

        if label_column:
            query.label_column = label_column

        if combine_labels:
            query.combine_labels = combine_labels

        if capture_configurations:
            query.capture_configurations = capture_configurations

        query.metadata_columns.add("segment_uuid")

        if isinstance(segmenter, str):
            segmenters = self.list_segmenters()
            segmenter_id = segmenters[segmenters["name"] == segmenter].id
            if segmenter_id.shape[0] != 1:
                raise Exception("Segmenter {} not found".format(segmenter))

            query.segmenter = int(segmenter_id.values[0])
        else:
            query.segmenter = segmenter

        if new:
            query.insert(renderer=renderer)
        else:
            query.update(renderer=renderer)

        return query

    def get_query(self, name):
        if self.project is None:
            print("Project must be set first")
            return

        return self.project.queries.get_query_by_name(name)

    def upload_data_file(
        self, name: str, path: str, force: bool = False, is_features: bool = False
    ):
        """Upload a .CSV file as either a FeatureFile or DataFile to the server.

        FeatureFiles are a collection of feature vectors and can be used in any step after the feature generation step
        DataFiles include sensor data and metadata and are used in any step prior to feature generation

        Args:
            name (str): Name of the file when it is uploaded
            path (str): The path to the file to upload
            force (bool, optional): Will overwrite if already exists. Defaults to False.
            is_features (bool, optional): If True, will upload as a feature file, if False will upload as a DataFile. Defaults to False.

        Returns:
            response: The response as a request object
        """
        logger.debug("set_feature_file:" + name + ":" + path)
        print('Uploading file "{}" to SensiML Cloud.'.format(name))
        if name[-4:] != ".csv":
            name = "{}.csv".format(name)

        feature_file = self._project._feature_files.get_by_name(name)
        if feature_file is None:
            new = True
            feature_file = self._project.featurefiles.new_featurefile()
        else:
            new = False
            if not force:
                raise Exception(
                    "A file with this name already exists. Use force=True to override"
                )

        feature_file.filename = name
        feature_file.is_features = is_features
        feature_file.path = path
        if new:
            return feature_file.insert()
        else:
            return feature_file.update()

    def upload_dataframe(
        self,
        name: str,
        dataframe: DataFrame,
        force: bool = False,
        is_features: bool = False,
    ):
        """Upload a pandas DataFrame as either a FeatureFile or DataFile to the server.

        FeatureFiles are a collection of feature vectors and can be used in any step after the feature generation step
        DataFiles include sensor data and metadata and are used in any step prior to feature generation

        Args:
            name (str): Name of the file when it is uploaded
            dataframe (DatFrame): Pandas DataFrame
            force (bool, optional): Will overwrite if already exists. Defaults to False.
            is_features (bool, optional): If True, will upload as a feature file, if False will upload as a DataFile. Defaults to False.

        Returns:
            response: The response as a request object
        """

        logger.debug("set_data:" + name)

        with NamedTemporaryFile(delete=False) as temp:
            dataframe.to_csv(temp.name, index=False)
            logger.debug("set_dataframe:" + name + ":" + temp.name)
            result = self.upload_data_file(
                name, temp.name, force=force, is_features=is_features
            )

        os.remove(temp.name)

        return result

    def upload_sensor_dataframe(
        self, name: str, dataframe: DataFrame, force: bool = False
    ):
        """Upload a pandas DataFrame as a DataFile to the server.

        DataFiles include sensor data and metadata and can be used in any any step prior to feature generation

        Args:
            name (str): Name of the file when it is uploaded
            dataframe (DatFrame): Pandas DataFrame
            force (bool, optional): Will overwrite if already exists. Defaults to False.

        Returns:
            response: The response as a request object
        """
        logger.debug("set_data:" + name)

        with NamedTemporaryFile(delete=False) as temp:
            dataframe.to_csv(temp.name, index=False)
            logger.debug("set_dataframe:" + name + ":" + temp.name)
            result = self.upload_data_file(
                name, temp.name, force=force, is_features=False
            )

        os.remove(temp.name)

        return result

    def upload_feature_dataframe(
        self, name: str, dataframe: DataFrame, force: bool = False
    ):
        """Upload a pandas DataFrame as a FeatureFile to the server.

        FeatureFiles are a collection of feature vectors and can be used in any step after the feature generation step

        Args:
            name (str): Name of the file when it is uploaded
            dataframe (DatFrame): Pandas DataFrame
            force (bool, optional): Will overwrite if already exists. Defaults to False.

        Returns:
            response: The response as a request object
        """
        logger.debug("set_data:" + name)

        with NamedTemporaryFile(delete=False) as temp:
            dataframe.to_csv(temp.name, index=False)
            logger.debug("set_dataframe:" + name + ":" + temp.name)
            result = self.upload_data_file(
                name, temp.name, force=force, is_features=True
            )

        os.remove(temp.name)

        return result

    def clear_session_cache(self):
        for _, _, filenames in os.walk(config_dir):
            for filename in filenames:
                if re.match(r"_token.json$", filename):
                    os.unlink(filename)

    def get_feature_statistics_results(self, query_name: str):
        query = self._project.queries.get_query_by_name(query_name)

        for i in range(100):
            results = query.get_feature_statistics()

            if results.get("results", None):
                return pd.DataFrame(results["results"])
            sleep(5)

        print("Not able to reach the results in the expected time. ")
        return results

    def upload_project(self, name: str, dclproj_path: str):
        """Upload a .dclproj file to the server

        Args:
            name (str): name of the project to create
            dclproj_path (str): path to the .dclproj file
        """
        if name in self.list_projects()["Name"].values:
            print("Project with this name already exists.")
            return

        upload_project(self, name, dclproj_path)

    def upload_project_dcli(self, name: str, dcli_path: str):
        """Upload a .dcli project to the server

        Args:
            name (str): name of the project to create
            dcli_path (str): path to the .dclproj file
        """
        if name in self.list_projects()["Name"].values:
            print("Project with this name already exists.")
            return

        upload_project_dcli(self, name, dcli_path)
