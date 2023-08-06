"""
Documentar.
"""

import datetime
from typing import Dict, Union, Any, List
import opensearchpy
import elasticsearch
from dynaconf.utils.boxing import DynaBox
from rds_core.config import settings
from rds_core.helpers import instantiate_class


__search_engine_cache: Dict[str, Any] = {}


def get_search_engine_config(alias: str = "default") -> DynaBox:
    return settings.SEARCH_ENGINES[alias]


def search_engine(
    alias: str = "default",
    username: Union[str, None] = None,
    password: Union[str, None] = None,
) -> Union[opensearchpy.OpenSearch, elasticsearch.Elasticsearch]:
    se_config = get_search_engine_config(alias)

    engine = se_config["engine"]
    params = {
        k: v
        for k, v in se_config.items()
        if k not in ("username", "password", "engine", "dsl_engine", "hosts")
    }
    username = username if username else se_config["username"]
    password = password if password else se_config["password"]
    params["http_auth"] = (username, password)
    client = instantiate_class(engine, se_config["hosts"].split(","), **params)
    __search_engine_cache[alias] = client
    return client


# def dsl_connection(alias: str = 'default') -> Union[opensearchpy.OpenSearch, elasticsearch.Elasticsearch]:
#     se_config = get_search_engine_config(alias)
#
#     dsl_connections = get_variable_by_pathname(se_config['dsl_engine'])
#     if alias not in dsl_connections.connections:
#         dsl_connections.add_connection(alias, search_engine(alias))
#     # dsl_connections.create_connection(
#     #     alias=alias,
#     #     http_auth=(se_config['user'], se_config['password']),
#     #     **{k:v for k,v in se_config.items() if k not in ('user', 'password', 'engine', 'dsl_engine')},
#     # )
#     return dsl_connections.get_connection(alias)


def create_index_if_not_exists(
    index: str,
    body: Union[dict, None] = None,
    params: Union[Dict[str, Any], None] = None,
    headers: Union[Dict[str, Any], None] = None,
    alias: str = "default"
) -> bool:
    """Cria um índice caso não exista. Retorna True se criou e False se não criou.

    Args:
        index (str): nome do índice a ser criado
        body (dict|None): corpo do índice
        params (dict|None): parametros
        headers (dict|None): cabeçalhos
        alias (str): alias para o search engine

    Raises:
        exception: Erro conforme retornado pelo Search Engine.

    Returns:
        bool: True se criou. False se não criou.
    """
    if not body:
        body = {}
    try:
        search_engine(alias).indices.create(index, body=body, params=params, headers=headers)  # type: ignore
        return True
    except Exception as e:
        if getattr(e, "error", None) == "resource_already_exists_exception":
            return False
        raise e


def delete_index_if_exists(index_name: str,
                           params: Union[Dict[str, Any], None] = None,
                           headers: Union[Dict[str, Any], None] = None,
                           alias: str = "default",
                           fail: bool = False) -> bool:
    """Apaga um índice caso exista. Retorna True se apagou e False se não apagou.

    Args:
        index_name (str): nome do índice a ser criado
        params (Dict[str, Any] | None):
        headers (Dict[str, Any] | None): Union[Dict[str, Any], None] = None,
        alias (str): alias para o search engine

    Raises:
        Exception: Erro conforme retornado pelo Search Engine.

    Returns:
        bool: True se criou. False se não criou.
    """
    try:
        search_engine(alias).indices.delete(index_name, params=params, headers=headers)  # type: ignore
        return True
    except Exception as e:
        if getattr(e, "error", None) == "index_not_found_exception":
            return False
        raise Exception(e)


def query(
    index_name: str,
    query_string: Union[str, int, float, datetime.date, datetime.datetime],
    fields: Union[List, None] = None,
    alias: str = "default",
) -> Any:
    if fields is None:
        fields = []
    response = search_engine(alias).search(
        index=index_name,
        body={
            "size": 5,
            "query": {"multi_match": {"query": query_string, "fields": fields}},
        },
    )
    return response["hits"]["hits"], response["hits"]["total"]["value"]


def search(index_name: str, body: dict, alias: str = "default") -> Any:
    response = search_engine(alias).search(index=index_name, body=body)
    return response["hits"]["hits"], response["hits"]["total"]["value"]


def index(
    index_name: str,
    body: Union[dict, None] = None,
    id: Any = None,
    params: Union[Dict[str, Any], None] = None,
    headers: Union[Dict[str, Any], None] = None,
    alias: str = "default"
) -> Union[Any, Any]:
    if not body:
        body = {}
    return search_engine(alias).index(index=index_name, body=body, id=id, params=params, headers=headers)  # type: ignore



def search_engine_healthy(params: Union[Dict[str, Any], None] = None,
                          headers: Union[Dict[str, Any], None] = None,
                          alias: str = "default") -> bool:
    print(search_engine(alias).ping)
    return search_engine(alias).ping(params=params, headers=headers)
