import pandas as pd
from dagster import ConfigurableIOManager, OutputContext, InputContext


class PandasDataFrameIOManager(ConfigurableIOManager):

    # the super class automatically makes this a constructor argument so that
    # we can instantiate as in `PandasDataFrameIOManager(base_dir="my_data_folder")`
    base_dir: str

    # dagster calls this after an asset has been materialized, to save it
    def handle_output(self, context: OutputContext, obj: pd.DataFrame) -> None:
        asset_name = context.asset_key.to_user_string()
        obj.to_csv(f'{self.base_dir}/{asset_name}.csv', sep=',', index=False)

    # dagster calls this to load the asset so it can be used as input to another asset
    def load_input(self, context: InputContext) -> pd.DataFrame:
        asset_name = context.asset_key.to_user_string()
        obj = pd.read_csv(f'{self.base_dir}/{asset_name}.csv', sep=',')
        return obj
