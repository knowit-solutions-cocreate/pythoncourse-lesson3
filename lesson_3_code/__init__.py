from dagster import Definitions, load_assets_from_modules

from lesson_3_code import assets
from lesson_3_code.io import PandasDataFrameIOManager


defs = Definitions(
    load_assets_from_modules([assets]),
    # dagster will use the IOManager supplied here as default for all assets
    resources={'io_manager': PandasDataFrameIOManager(base_dir='data/assets')}
)
