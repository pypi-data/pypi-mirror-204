from .api_service import ApiService, autobricks_logging
from typing import List, Union

from ._decode_utils import (
    base64_encode,
    base64_decode,
    format_path_for_os,
    format_path_for,
    OS,
)
import os

from enum import Enum

_logger = autobricks_logging.get_logger(__name__)

endpoint = "workspace"


_api_service = ApiService()


class DeployMode(Enum):
    DEFAULT = "DEFAULT"
    MOVE = "MOVE"
    PARENT = "PARENT"
    CHILD = "CHILD"
    ROOT_CHILD = "ROOT_CHILD"


class Extension(Enum):
    py = "py"
    html = "html"
    ipynb = "ipynb"
    dbc = "dbc"
    sql = "sql"


class Format(Enum):
    SOURCE = "SOURCE"
    HTML = "HTML"
    JUPYTER = "JUPYTER"
    DBC = "DBC"
    AUTO = "AUTO"


class Language(Enum):
    SCALA = "SCALA"
    PYTHON = "PYTHON"
    SQL = "SQL"
    R = "R"


class ObjectType(Enum):
    DIRECTORY = "DIRECTORY"
    NOTEBOOK = "NOTEBOOK"
    LIBRARY = "LIBRARY"
    FILE = "FILE"
    REPO = "REPO"


def get_language(extension: Extension):

    if extension == Extension.py:
        return Language.PYTHON
    elif extension == Extension.sql:
        return Language.SQL
    else:
        raise Exception("unknown language for extension")


def workspace_import(
    from_path: str,
    to_path: str,
    format: Format = Format.AUTO,
    language: Language = None,
    overwrite=True,
):

    with open(from_path, "rb") as file:
        content = base64_encode(file.read())

    data = {
        "path": to_path,
        "format": format.name,
        "content": content,
        "overwrite": overwrite,
    }

    if language:
        data["language"] = language.name

    _logger.info(f"workspace import {from_path} to {to_path}")

    return _api_service.api_post(endpoint, "import", data)


def workspace_delete(path: str, recursive: True):

    data = {"path": path, "recursive": recursive}
    _logger.info(f"workspace deleting path {path} recursive {str(recursive)}")
    return _api_service.api_post(endpoint, "delete", data)


def workspace_get_status(path: str):

    data = {"path": path}
    _logger.info(f"workspace getting status path {path}")
    return _api_service.api_get(endpoint, "get-status", data)


def workspace_list(path: str):

    data = {"path": path}
    _logger.info(f"workspace listing path {path}")
    return _api_service.api_get(endpoint, "list", data)


def workspace_mkdirs(path: str):

    data = {"path": path}
    _logger.info(f"workspace making dirs {path}")
    return _api_service.api_post(endpoint, "mkdirs", data)


def workspace_get_folder_id(path: str):

    dir = os.path.basename(path)
    parent = path.replace(dir, "")
    ls = workspace_list(parent)["objects"]
    try:
        gen = (d for d in ls if d["path"] == path)
        dir_data = next(gen)
        object_id = dir_data["object_id"]
    except Exception as e:
        msg = f"Path {path} not found in directory listing {ls}"
        raise Exception(msg) from e

    return object_id


def workspace_find_paths(
    folder_ids: List[str], root_folders: Union[str, List[str]] = None
):

    if not root_folders:
        return _workspace_find_paths(folder_ids)
    if isinstance(root_folders, str):
        return _workspace_find_paths(folder_ids, f"/{root_folders}")
    if isinstance(root_folders, list):
        workpsace_paths = {}
        for folder in root_folders:
            paths = _workspace_find_paths(folder_ids, f"/{folder}")
            workpsace_paths = {**workpsace_paths, **paths}

        return workpsace_paths


def _workspace_find_paths(folder_ids: List[str], path="/"):
    folder_ids = list(dict.fromkeys(folder_ids))
    ls = workspace_list(path)
    folder_paths = {}
    if ls:
        ls = ls["objects"]

        folder_paths = {}

        for folder in ls:
            id = folder["object_id"]
            object_type = ObjectType(folder["object_type"])
            path = folder["path"]
            if str(id) in folder_ids:
                folder_paths[str(id)] = folder["path"]
            if object_type == ObjectType.DIRECTORY:
                sub_folder_paths = _workspace_find_paths(folder_ids, path)
                folder_paths = {**folder_paths, **sub_folder_paths}

    return folder_paths


def workspace_export(from_path: str, format: Format, to_path: str):

    data = {"path": from_path, "format": format.name.upper(), "direct_download": False}

    _logger.info(
        f"workspace exporting from path {from_path} format {format.name.upper()}"
    )
    response = _api_service.api_get(endpoint, "export", data)

    file_type = response["file_type"]
    filename = os.path.basename(from_path)
    file_path = f"{to_path}/{filename}.{file_type}"

    content = base64_decode(response["content"])
    with open(file_path, "wb") as file:
        file.write(content)

    if file_type == "py":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.SOURCE.name,
        }

    elif file_type == "html":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.HTML.name,
        }

    elif file_type == "ipynb":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.JUPYTER.name,
        }

    elif file_type == "dbc":
        response = {
            "from_path": from_path,
            "to_path": file_path,
            "file_type": Format.DBC.name,
        }

    return response


def workspace_dir_exists(path: str):

    try:
        reponse = workspace_get_status(path)
    except Exception:
        return False

    return reponse.get("object_type") == "DIRECTORY" and reponse.get("path") == path


def workspace_notebook_exists(path: str):

    try:
        reponse = workspace_get_status(path)
    except Exception:
        return False

    return reponse.get("object_type") == "NOTEBOOK" and reponse.get("path") == path


def workspace_import_dir(
    from_notebook_root: str,
    source_dir: str = "/",
    target_dir: str = None,
    deploy_mode: DeployMode = DeployMode.DEFAULT,
):

    if deploy_mode == DeployMode.DEFAULT and target_dir:

        _logger.error(
            f"target_dir is not required for {deploy_mode.name} deployment mode"
        )
        raise Exception(
            f"target_dir is not required for {deploy_mode.name} deployment mode"
        )

    elif deploy_mode != DeployMode.DEFAULT and not target_dir:

        _logger.error(f"target_dir is required for {deploy_mode.name} deployment mode")
        raise Exception(
            f"target_dir is required for {deploy_mode.name} deployment mode"
        )

    # automaticall adjust for user entered paths using the wrong separators
    source_dir = format_path_for_os(source_dir)
    from_root_path = os.path.abspath(format_path_for_os(from_notebook_root))

    response = {
        "from_notebook_root": from_notebook_root,
        "source_dir": source_dir,
        "target_dir": target_dir,
        "actions": [],
    }

    deploy_this = False

    _logger.info(
        f"Start deploying from from_root_path={from_root_path} source_dir={source_dir} target_dir={target_dir} deploy_mode={deploy_mode.name}"
    )

    for root, subdirs, files in os.walk(from_root_path):

        deploy_dir = root.replace(from_root_path, "")

        _logger.debug(
            f"Checking if deploy_dir={deploy_dir} starts with source_dir={source_dir}"
        )

        if deploy_dir.startswith(source_dir) or not source_dir or source_dir == "/":

            deploy_this = True
            if deploy_dir == "":
                deploy_dir = "/"

        else:
            deploy_this = False
            _logger.debug(
                f"Skipping dir source_dir={source_dir} deploy_dir={deploy_dir} target_dir={target_dir} deploy_mode={deploy_mode.name}"
            )

        if deploy_this:

            _logger.debug(
                f"Deploying dir source_dir={source_dir} deploy_dir={deploy_dir} target_dir={target_dir} deploy_mode={deploy_mode.name}"
            )

            action = _deploy_dir(source_dir, deploy_dir, target_dir, deploy_mode)
            if action:
                response["actions"].append(action)

            # deploy the notebooks
            for filename in files:

                from_file_path = os.path.join(root, filename)
                to_file_path = from_file_path.replace(from_root_path, "")

                _logger.debug(
                    f"Deploying from_file_path={from_file_path} source_dir={source_dir} deploy_dir={deploy_dir} target_dir={target_dir} deploy_mode={deploy_mode.name}"
                )

                action = _deploy_file(
                    from_file_path, source_dir, to_file_path, target_dir, deploy_mode
                )
                response["actions"].append(action)

    return response


def _deploy_file(
    from_file_path: str,
    source_dir: str,
    to_file_path: str,
    target_dir: str,
    deploy_mode: DeployMode,
):

    to_file_path = _modify_deploy_path(
        to_file_path, source_dir, target_dir, deploy_mode
    )

    action = {
        "action": "import",
        "from_file_path": from_file_path,
        "to_file_path": to_file_path,
    }

    workspace_import(from_path=from_file_path, to_path=to_file_path)

    return action


def _deploy_dir(
    source_dir: str, deploy_dir: str, target_dir: str, deploy_mode: DeployMode
):

    # insert the root sub-dir to support along side nested deployment if given.
    deploy_dir = _modify_deploy_path(deploy_dir, source_dir, target_dir, deploy_mode)

    # make the directory it's not the root
    action = None
    if deploy_dir != "/":
        action = {"action": "mkdirs", "path": deploy_dir}
        workspace_mkdirs(deploy_dir)

    return action


def _modify_deploy_path(
    deploy_dir: str, root: str, modifier: str, deploy_mode: DeployMode
):

    _logger.debug(
        f"Modifying path based on deploy_mode={deploy_mode.name} path deploy_dir={deploy_dir} root={root} modifier={modifier}"
    )

    if deploy_mode == DeployMode.DEFAULT:
        new_path = deploy_dir

    elif deploy_mode == DeployMode.MOVE:
        new_path = deploy_dir.replace(root, modifier)

    elif deploy_mode == DeployMode.PARENT:
        modify_to = f"{modifier.replace('/.','')}{root}"
        new_path = deploy_dir.replace(root, modify_to)

    elif deploy_mode == DeployMode.CHILD:
        modify_to = f"{root}{modifier}"
        new_path = deploy_dir.replace(root, modify_to)

    elif deploy_mode == DeployMode.ROOT_CHILD:

        clean_modifier = modifier.replace("\\", "/")
        if clean_modifier.startswith("/"):
            clean_modifier = clean_modifier[1:]
        if clean_modifier.endswith("/"):
            clean_modifier = clean_modifier[:-1]

        folders = root.split("/")
        folders.insert(2, clean_modifier)
        modify_to = "/".join(folders)
        new_path = deploy_dir.replace(root, modify_to)

    # databricks runs on linux
    new_path = format_path_for(new_path, OS.LINUX)

    _logger.debug(f"Modified deploy path deploy_dir={new_path}")

    return new_path
