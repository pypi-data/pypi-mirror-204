# CORE
from core import core

# MODULES
import re
from typing import Dict, List, Union, Optional, Any

# MODELS
from ..models.main import AlphaException, AlphaCore

# UTILS
from ..utils.database import init as init_database_fct
from ..utils.database.init import replace_to_date


def init_databases(
    core: AlphaCore,
    tables: List[str] | Dict[str, str] = None,
    binds: List[str] = None,
    create: bool = False,
    drop: bool = False,
    truncate: bool = False,
    sqlite: bool = True,
    force: bool = True,
    init: bool = False,
):
    """Initialise les bases de données en fonction des paramètres fournis. Cette fonction est la principale et appelle les autres fonctions pour effectuer diverses tâches.

    Args:
        core (AlphaCore): objet Core contenant les informations de base et les configurations
        tables (List[str] | Dict[str, str], optional): Liste ou dictionnaire des noms des tables à traiter. Defaults to None.
        binds (List[str], optional): Liste des binds à traiter. Defaults to None.
        create (bool, optional): Booléen indiquant si les tables doivent être créées. Defaults to False.
        drop (bool, optional): Booléen indiquant si les tables doivent être supprimées. Defaults to False.
        truncate (bool, optional):  Booléen indiquant si les tables doivent être vidées. Defaults to False.
        sqlite (bool, optional): Booléen indiquant si SQLite doit être utilisé. Defaults to True.
        force (bool, optional): Booléen indiquant si la configuration doit être forcée à 'local'. Defaults to True.
        init (bool, optional): Booléen indiquant si les fichiers d'initialisation doivent être traités. Defaults to False.
    """
    # Vérifie que la configuration est 'local' ou que le paramètre 'force' est True
    if core.configuration != "local" and not force:
        if core.log:
            core.log.error("Configuration must be <local>")
        return

    # Normalise le paramètre 'tables'
    tables = init_database_fct.__normalize_tables(tables)

    # Normalise le paramètre 'binds' et vérifie que les binds sont valides
    binds = init_database_fct.__normalize_and_check_binds(binds, core)

    # Récupère les modèles de tables à partir des paramètres 'tables' et 'binds'
    tables_models = core.db.get_tables_models(tables, binds)

    # Récupère et normalise la configuration d'initialisation des bases de données
    init_databases_config = init_database_fct.__get_normalized_init_config(core)

    # Initialise les bases de données en fonction des paramètres
    core.db.init_all(
        tables=tables_models, create=create, drop=drop, sqlite=sqlite, log=core.log
    )

    # Vide les tables si le paramètre 'truncate' est True
    if tables is not None and truncate:
        for table_model in tables_models:
            core.db.truncate(table_model)

    # Charge les fichiers d'initialisation si le paramètre 'init' est True
    if init:
        init_database_fct.process_init_files(core, binds, tables, init_databases_config)


def get_table_content(
    bind: str,
    tablename: str,
    order_by: str,
    direction: str,
    page_index: int,
    page_size: int,
    limit: int = None,
):
    model = core.db.get_table_model(tablename, bind)
    return core.db.select(
        model,
        page=page_index,
        per_page=page_size,
        order_by=order_by,
        order_by_direction=direction,
        limit=limit,
    )


def where_used(
    core: AlphaCore,
    data_type: str,
    value,
    bind: str,
    column_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Find where a value is used in columns of a certain data type.

    :param core: AlphaCore instance to work with.
    :param data_type: Data type to search for in columns.
    :param value: Value to search for in columns.
    :param bind: Bind name to work with.
    :param column_name: Optional column name to match (default is None).
    :return: A dictionary containing table names, column names, and rows with matching values.
    """
    query = f"""
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE data_type = '{data_type}';
    """
    outputs = {}
    results = core.db.get_query_results(query, bind=bind)

    outputs = __process_results(results, column_name, outputs)

    return __filter_matching_rows(core, bind, value, outputs)


def __process_results(results, column_name, outputs):
    """
    Process query results to filter columns by optional column_name.

    :param results: Query results.
    :param column_name: Optional column name to match.
    :param outputs: Dictionary to store processed outputs.
    :return: A dictionary containing table names and their filtered columns.
    """
    for r in results:
        if not r["table_name"] in outputs:
            outputs[r["table_name"]] = []

        if column_name is not None:
            matches = re.findall(column_name, r["column_name"])
            if len(matches) == 0:
                continue

        outputs[r["table_name"]].append(r["column_name"])

    outputs = {x: list(set(y)) for x, y in outputs.items() if len(y) != 0}
    return outputs


def __filter_matching_rows(core, bind, value, outputs):
    """
    Filter rows by matching value.

    :param core: AlphaCore instance to work with.
    :param bind: Bind name to work with.
    :param value: Value to search for in columns.
    :param outputs: Dictionary containing table names and their columns.
    :return: A dictionary containing table names, column names, and rows with matching values.
    """
    outputs_filtered = {}

    for table_name, columns in outputs.items():
        outputs_filtered[table_name] = {}

        for column in columns:
            query = f"""SELECT * FROM {table_name} WHERE {column} = {value}"""
            rows = core.db.get_query_results(query, bind=bind)

            if len(rows) != 0:
                outputs_filtered[table_name][column] = rows

    return outputs_filtered
