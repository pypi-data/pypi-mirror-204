"""This module contains a LoadFlatFile class that contains logic to load flat files in a clean an easy manner."""


import os

import chardet
import clevercsv as csv
import pandas as pd

import logging

logger = logging.getLogger(__name__)


class LoadFlatFile:
    """
    This class contains methods to load and inspect csv files from a directory, and to return them
    as a dictionary of Pandas dataframes.

    Args: 
        dir_path (str):                         Path to the directory that contains the files
        file_extensions (list, optional):       List of possible file extensions. 
                                                Defaults to csv
        default_encodings (list, optional):     List of possible encodings
                                                Defaults to ascii and utf-8
        possible_delimiters (str, optional):    A string containing the possible delimiters
                                                Defaults to , ; | \t

    """

    def __init__(
        self,
        dir_path: str,
        file_extensions: list = ["csv"],
        load_as_varchar = None,
        default_encodings: list = ["ascii", "utf-8"],
        possible_delimiters: str = ",;|\t",
        ):
        self.dir_path = dir_path
        self.possible_delimiters = possible_delimiters
        self.load_as_varchar = load_as_varchar
        self.file_paths = [
            entry
            for entry in os.scandir(self.dir_path)
            if entry.name.lower().endswith(tuple(file_extensions))
        ]
        self.file_params = {
            file: {"header": None, "encoding": list(set(default_encodings)), "delimiter": None}
            for file in self.file_paths
        }

        if len(self.file_paths) == 0:
            raise ValueError(
                f"Could not find any .csv files in the directory path {self.dir_path}."
            )

    def load(self, file_paths: list = None) -> dict:
        """
        Calls the functions in this class to read the files and return them in a dict of df's 

        Args:
            file_paths (list, optional): A list of paths to the files. Defaults to None.

        Returns:
            dict_of_dfs: A dictinory of Pandas dataframes
        """
        self.get_encodings()
        self.get_delimiter()
        self.get_headers()
        dict_of_dfs = self.read_files(file_paths)

        return dict_of_dfs

    def _retrieve_all_encodings(self) -> None:
        """
        Returns a list of lists of the most likely encoding(s) for each file.
        """
        for file in self.file_paths:
            try:
                with open(file, "rb") as rawdata:
                    result = chardet.detect(rawdata.read(10000))
            except Exception as error:  # this exception needs to be more specific
                logger.error(
                    f"Error: chardet encoding of file {file.name} detection failed: {error}"
                )
                try:
                    with open(file) as f:
                        f = str(f)
                except Exception as error:  # this exception needs to be more specific
                    logger.error(
                        f"Error: using the filereader to detect encoding of file {file.name} failed: {error}"
                    )
                else:
                    file_enc = f.split("encoding='")[1].split("'")[0]
            else:
                file_enc = result["encoding"]

            if file_enc not in self.file_params[file]["encoding"]:
                self.file_params[file]["encoding"].insert(0, file_enc)

    def get_encodings(self) -> None:
        """
        Tries to find the encodings for all files in the directory

        Args: 
            None, class attributes will be used

        Returns: 
            None

        """
        self._retrieve_all_encodings()
        remove_file = []

        for file_path, params in self.file_params.items():
            for encode in params["encoding"]:
                with open(file_path, "r", encoding=encode) as file:
                    try:
                        file.read(1024)
                        self.file_params[file_path]["encoding"] = encode
                    except UnicodeDecodeError as error:
                        # logger.error(f"Error: the encoding {encode} for file {file.name} does not work, try UTF-8 or ascii: {error}")
                        pass
                    except csv.Error as error:
                        logger.error(
                            f"Error: the file {file.name} contains NULL bytes: {error} \n"
                        )
            if isinstance(params["encoding"], list):
                logger.error(
                    f"Error: the detection of the encoding failed for the file {file_path.name}, this file will not be loaded"
                )
                remove_file.append(file_path)

        for item in remove_file:
            self.file_paths.remove(item)
            del self.file_params[item]

    def get_delimiter(self) -> None:
        """
        Updates the file_params dictionary with the most probable delimiter of the file

        Args: 
            None, class attributes will be used

        Returns: 
            None

        """
        for file_path, params in self.file_params.items():
            with open(file_path, 'r', encoding=params["encoding"]) as file:
                dialect = csv.Sniffer().sniff(file.read(1024), self.possible_delimiters)
                self.file_params[file_path]["delimiter"] = dialect.delimiter

    def get_headers(self) -> None:
        """
        Updates the file_params dictionary with knowledge if file seems to have a header.
        
        Args: 
            None, class attributes will be used

        Returns: 
            None

        """
        for file_path, params in self.file_params.items():
            with open(file_path, "r", encoding=params["encoding"]) as file:
                if csv.Sniffer().has_header(file.read(1024)):
                    self.file_params[file_path]["header"] = "infer"

    def read_files(self, file_paths: list = None, load_as_varchar = None) -> dict:
        """
        Reads files and eturns a dictionary of dataframes for each flat file.

        Args:
            file_paths (list, optional): A list of paths to the files. Defaults to None.

        Returns:
            data_dict: A dictinory of dataframes
        """
        if file_paths is None:
            files_to_load = self.file_params
        else:
            files_to_load = {file: self.file_params[file] for file in file_paths}
        
        if load_as_varchar is None:
           load_as_varchar = self.load_as_varchar
            
        assert len(files_to_load) > 0, "There are no files selected to load"

        data_dict = {}

        for file, params in files_to_load.items():
            try:
                                  
                if load_as_varchar:
                    temp_df = pd.read_csv(
                    file,
                    sep=params["delimiter"],
                    encoding=params["encoding"],
                    header=params["header"],
                    dtype=str,
                    na_filter=False    
                    )
                else:
                    temp_df = pd.read_csv(
                    file,
                    sep=params["delimiter"],
                    encoding=params["encoding"],
                    header=params["header"],
                    dtype=None
                    )
            except Exception as error:
                logger.error(f"Error @ file {file.name}: {error}")
            else:
                data_dict[f"{file.name}"] = temp_df

        return data_dict
