# Exercises


## Main exercises


### 1. Create a stub for a new asset
**TODO** steps to incorporate the following asset stub and invoke it in the GUI.
```Python
@asset
def planet_stats(homeworlds_clean: pd.DataFrame) -> pd.DataFrame:
    logger = get_dagster_logger()  # get a logger that makes messages appear in dagster web GUI
    logger.info(homeworlds_clean)  # print the input asset so we can see what's going on during development!
    return homeworlds_clean
```


### 2. Compute something in the new asset
**TODO** steps to incorporate the following asset into the asset stub.
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

### 3. Modify the IO-manager
**TODO** In code: include the PandasCSVIOManager
**TODO** For an exercise: make the IOManager store stuff as tab-delimited ".tsv" in custom folder instead of as comma-delimited ".csv" in dagster folder, or something similarly challenging


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


### 2. Create an IO-manager
**TODO** very brief suggestions for a database IO Manager that overwrites tables when materializing (need to mention `context.asset_key`)


## WIP Notes


- Asset definitioner hot loading.
  - Köra igång dagster
  - kopiera en färdigbyggd asset i assets filen
  - importera asseten genom att lägga till referenser till asseten i Definitions objektet
  - Gå in på dagster UIt, refresha definitionerna, se asseten ploppa upp och starta en körning.
- Skriv en dagster Asset som hämtar från en ny endpoint (Ships?).
  - Skriv koden för asseten
  - Starta en körning för den asseten.
- Lägga till en färdigskriven Asset och lägga till Asseten från uppgift 2 som dependcy
- Skriv en Asset som gör en join Mellan Asset från uppgift 3 och homeworld_clean.
- Lägg till en io_manager till Asset från uppgift 4 (csv) och öppna filen för resultatet.