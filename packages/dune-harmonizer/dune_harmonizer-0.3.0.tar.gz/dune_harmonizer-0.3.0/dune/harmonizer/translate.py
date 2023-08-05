import re

import sqlglot
from sqlglot import ParseError

from dune.harmonizer.custom_transforms import (
    add_warnings_and_banner,
    double_quoted_param_left_placeholder,
    double_quoted_param_right_placeholder,
    fix_bytearray_lower,
    fix_bytearray_param,
    postgres_transforms,
    prep_query,
    remove_quotes_around_0x_strings,
    single_quoted_param_left_placeholder,
    single_quoted_param_right_placeholder,
    spark_transforms,
)
from dune.harmonizer.errors import DuneTranslationError


def _clean_dataset(dataset):
    for d in ("gnosis", "optimism", "bnb", "polygon", "ethereum"):
        if d in dataset.lower():
            return d
    raise ValueError(f"Unknown dataset: {dataset}")


def _translate_query(query, sqlglot_dialect, dataset=None):
    """Translate a query using SQLGLot plus custom rules"""
    try:
        # Insert placeholders for the parameters we use in Dune (`{{ param }}`), SQLGlot doesn't handle those
        query = query.replace("{{", double_quoted_param_left_placeholder).replace(
            "}}", double_quoted_param_right_placeholder
        )
        query = prep_query(query)

        # Transpile to Trino
        query = sqlglot.transpile(query, read=sqlglot_dialect, write="trino", pretty=True)[0]

        # Perform custom transformations using SQLGlot's parsed representation
        if sqlglot_dialect == "spark":
            query_tree = spark_transforms(query)
        elif sqlglot_dialect == "postgres":
            # Update bytearray syntax
            query = query.replace("\\x", "0x")
            query_tree = postgres_transforms(query, dataset)

        # Turn back to SQL
        query = query_tree.sql(dialect="trino", pretty=True)

        # Replace placeholders with Dune params again
        query = (
            query.replace(double_quoted_param_left_placeholder, "{{")
            .replace(double_quoted_param_right_placeholder, "}}")
            .replace(single_quoted_param_left_placeholder, "{{")
            .replace(single_quoted_param_right_placeholder, "}}")
        )

        # Non-SQLGlot transforms
        query = fix_bytearray_param(query)
        query = fix_bytearray_lower(query)
        query = remove_quotes_around_0x_strings(query)

        return add_warnings_and_banner(query)

    except ParseError as e:
        # SQLGlot inserts terminal style colors to emphasize error location.
        # We remove these, as they mess up the formatting.
        # Also, don't leak intermediate param syntax in error message
        error_message = (
            str(e)
            .replace("\x1b[4m", "")
            .replace("\x1b[0m", "")
            .replace(double_quoted_param_left_placeholder, "{{")
            .replace(double_quoted_param_right_placeholder, "}}")
        )
        # Remove Line and Column information, since it's outdated due to previous transforms.
        error_message = re.sub(
            ". Line [0-9]+, Col: [0-9]+.",
            ".",
            error_message,
        )
        raise DuneTranslationError(error_message)
