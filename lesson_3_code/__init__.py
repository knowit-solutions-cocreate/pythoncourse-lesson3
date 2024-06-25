from dagster import Definitions, load_assets_from_modules

from lesson_3_code import assets


defs = Definitions(load_assets_from_modules([assets]))
