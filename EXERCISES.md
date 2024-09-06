# Exercises

## Main exercises

### 1. Create a stub for a new asset
Dagster permits a nice development workflow in which you expand the graph of assets without restarting the tool. Try it out with the following steps.

1. paste the following stub for a new asset into assets.py
```Python
@asset
def planet_stats(homeworlds_clean: pd.DataFrame) -> pd.DataFrame:
    logger = get_dagster_logger()  # get a logger that makes messages appear in dagster web GUI
    logger.info(homeworlds_clean)  # print the input asset so we can see what's going on during development!
    return homeworlds_clean
```
2. inspect `__init__.py` to see that it gets included in the code (you will find that it is, via `load_assets_from_modules`)
3. go to [http://localhost:3000/asset-groups](http://localhost:3000/asset-groups) and make the new asset appear by pressing Reload definitions
4. mark the asset and press Materialize selected
5. inspect the results in the file data/assets/planet_stats.csv and in the GUI run log corresponding to the materialization, which you can find in at [http://localhost:3000/runs](http://localhost:3000/runs)


### 2. Compute something in the new asset
You may have noticed that the asset you added in the previous step doesn't do much - it just passes through the input asset that we already had! Populate the `planet_stats` as in the following, so it actually does compute some statistics. Then, press Reload definitions in the GUI and materialize the asset again, to inspect the resulting file and run log, all the same as in the previous section. To feel completely sure the that the asset definition got reloaded as expected, add some new log message in the asset code and make sure you can find it in the run's log in the Dagster GUI.
```Python
@asset
def planet_stats(homeworlds_clean: pd.DataFrame) -> pd.DataFrame:
    logger = get_dagster_logger()

    df = homeworlds_clean
    logger.info(df.columns)
    df = (
        homeworlds_clean.groupby('name_of_planet')  # for each planet...
        .aggregate(  # ... gather all rows into one by...
            {
                'name_of_person': 'count',  # ... counting the persons...
                'diameter': 'first'  # ... and including the diameter of the planet
            }
        )
        .rename(columns={'name_of_person': 'number_of_characters'})
    )
    logger.info(df)
    return df
```

### 3. Modify the IOManager persistence format
Writing and reloading of data computed by the assets in this code base is handled by an IOManager defined in io.py. This programming model separates the (data engineering) concern of how data is stored from the (data science) concern of how it is computed.

The current IOManager persists dataframes as comma-separated values. Let's tweak the `PandasDataFrameIOManager` to work with tab-separated .tsv files instead, as this is a little bit safer (in that fields will be able to contain commas) and may render more readably in our editor.

Hints:
- study io.py to understand what needs to be modified
- `to_csv` and `read_csv` can be configured to work with tab-separated format with the right parameters


## Bonus exercises

### 1. Incorporate a new input asset directly connected to the Star Wars API
Let's continue building assets! There are multiple endpoints in the Star Wars API that we have not explored yet. One is *ships*. Let's create an asset representing ships, hooked up to fetch data directly from the REST source, then join this with one of our existing assets to create a new *pilots* asset.

#### a. Fetch data and construct dataframe from the the ships endpoint
Hints: you may start with the asset stub below. Modify it to point towards `ships` instead of `vehicles` and to handle pagination as indicated by inline comments.
```Python
import requests

@asset
def vehicles_page_one() -> pd.DataFrame:
    # NOTE SWAPI is paginated and this query will only return page 1
    # TODO to gather everything, we may loop over pages 1, 2, ... until
    # response_as_dict == {'detail': 'Not found'} then break
    page = 1
    response = requests.get(f'https://swapi.dev/api/vehicles?page={page}')
    response_as_dict = response.json()
    df = pd.DataFrame(response_as_dict['results'])
    get_dagster_logger().debug(df)
    return df
```

#### b. Join ships with people to create the pilots asset
Hints:
- start by writing the function signature (the `@asset` decorated `def pilots(...)` line) and have it appear in the GUI
- there are examples of dataframe joins in the code of this as well as the previous lesson
- not all ships have a list of pilots and not all people are pilots - whether you want to include people with a NULL ship value and/or vice versa is up to you


### 2. Create an IOManager that saves materializations as database tables
Suppose our end users turn out to prefer SQL tables over files. Because Dagster separates the asset persistence code from the asset graph definition code, we can make this happen without modifying the latter at all. This task is to implement an IOManager that achieves it using SQLite, a `PandasDataFrameSQLiteIOManager`, say.

Hints:
- copy the code of `PandasDataFrameIOManager` as a starting point
- set up and interact with a SQLite database as [shown in lesson 2](https://github.com/knowit-solutions-cocreate/pythoncourse-lesson2/tree/main)
- in the IOManagers `handle_output` and `load_input` methods: write to and read from a table with the same name as the asset key
- in `handle_output`: make sure the table gets removed or emptied if it already exists, to keep the pipeline conveniently rerunnable

