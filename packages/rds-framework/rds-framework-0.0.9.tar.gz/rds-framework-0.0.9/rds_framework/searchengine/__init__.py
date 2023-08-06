"""
Documentar.
"""

import datetime
from typing import Dict, Union, Any, List
import opensearchpy
import elasticsearch
from dynaconf.utils.boxing import DynaBox
from rds_framework.config import settings
from rds_framework.helpers import instantiate_class


__search_engine_cache: Dict[str, Any] = {}


def get_search_engine_config(alias: str = 'default') -> DynaBox:
    assert settings.SEARCH_ENGINES and alias in settings.SEARCH_ENGINES, \
        f"Não existe um search engine com o apelido '{alias}' nas settings"
    return settings.SEARCH_ENGINES[alias]


def search_engine(alias: str = 'default') -> Union[opensearchpy.OpenSearch, elasticsearch.Elasticsearch]:
    se_config = get_search_engine_config(alias)

    if alias not in __search_engine_cache:
        engine = se_config['engine']
        params = {k: v for k, v in se_config.items() if
                  k not in ('username', 'password', 'engine', 'dsl_engine', 'hosts')}
        params['http_auth'] = (se_config['username'], se_config['password'])
        client = instantiate_class(engine, se_config['hosts'].split(','), **params)
        __search_engine_cache[alias] = client
    return __search_engine_cache[alias]


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


def create_index_if_not_exists(index_name: str, alias: str = 'default', **kwargs) -> bool:
    """ Cria um índice caso não exista. Retorna True se criou e False se não criou.

        Args:
            index_name (str): nome do índice a ser criado
            alias (str): alias para o search engine

        Raises:
            exception: Erro conforme retornado pelo Search Engine.

        Returns:
            bool: True se criou. False se não criou.
    """
    try:
        search_engine(alias).indices.create(index_name, body={}, **kwargs)
        return True
    except Exception as e:
        if getattr(e, 'error') == 'resource_already_exists_exception':
            return False
        raise e


def delete_index_if_exists(index_name: str, alias: str = 'default', **kwargs) -> bool:
    """ Apaga um índice caso exista. Retorna True se apagou e False se não apagou.

        Args:
            index_name (str): nome do índice a ser criado
            alias (str): alias para o search engine

        Raises:
            exception: Erro conforme retornado pelo Search Engine.

        Returns:
            bool: True se criou. False se não criou.
    """
    try:
        search_engine(alias).indices.delete(index_name, **kwargs)
        return True
    except Exception as e:
        if getattr(e, 'error') == 'index_not_found_exception':
            return False
        raise e


def query(index_name: str,
          query_string: Union[str, int, float, datetime.date, datetime.datetime],
          fields: Union[List, None] = None,
          alias: str = "default") -> Any:
    if fields is None:
        fields = []
    response = search_engine(alias).search(
        index=index_name,
        body={
            'size': 5,
            'query': {
                'multi_match': {
                    'query': query_string,
                    'fields': fields
                }
            }
        }
    )
    return response['hits']['hits'], response['hits']['total']['value']


def search(index_name: str, body: dict, alias: str = "default") -> Any:
    response = search_engine(alias).search(
        index=index_name,
        body=body
    )
    return response['hits']['hits'], response['hits']['total']['value']


def index(index_name: str,
          body: Dict,
          _id: Any = None,
          alias: str = "default",
          **kwargs) -> Union[Any, Any]:
    response = search_engine(alias).index(
        index=index_name,
        body=body,
        id=_id,
        **kwargs
    )
    return response


def search_engine_healthy(alias: str = 'default') -> bool:
    return search_engine(alias).ping()
