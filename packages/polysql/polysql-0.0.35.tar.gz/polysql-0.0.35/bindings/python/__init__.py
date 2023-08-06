import os
import sys
from tree_sitter import Parser, Language

parser_path = os.path.join(sys.prefix, "lib/polysql/languages.so")

BigqueryLanguage = Language(parser_path, "bigquery")
PostgresLanguage = Language(parser_path, "postgres")

__all__ = [
    Parser,
    BigqueryLanguage,
    PostgresLanguage,
]
