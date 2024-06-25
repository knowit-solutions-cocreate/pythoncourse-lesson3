import pandas as pd
from dagster import asset


@asset
def people_raw() -> pd.DataFrame:
    return pd.read_csv('data/people.csv')

@asset
def planets_raw() -> pd.DataFrame:
    return pd.read_csv('data/planets.csv')

@asset
def homeworlds_raw(people_raw: pd.DataFrame, planets_raw: pd.DataFrame) -> pd.DataFrame:
    return pd.merge(
        people_raw,
        planets_raw,
        left_on='homeworld',
        right_on='url',
        suffixes=('_of_person', '_of_planet')
    )

@asset
def homeworlds_clean(homeworlds_raw: pd.DataFrame) -> pd.DataFrame:
    df = homeworlds_raw

    first_row = df.iloc[0]
    looks_like_url = first_row.str.contains('https://', na=False)
    df = df.loc[:, ~looks_like_url]

    df = df.replace(["unknown", "none", "null", "na", ""], None)

    df['height'] = pd.to_numeric(df['height'], downcast='integer')
    df['mass'] = pd.to_numeric(df['mass'].str.replace(',', ''), downcast='float')
    df['birth_year'] = pd.to_numeric(
        df['birth_year'].str.replace('BBY', ''), downcast='float'
    )

    return df
