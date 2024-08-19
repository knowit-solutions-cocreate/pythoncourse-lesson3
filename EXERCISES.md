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


### 1. Create a new input asset
**TODO** ships


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