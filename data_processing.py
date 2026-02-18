import pandas as pd


def rename_columns(df_raw):
    df = df_raw.copy()

    cols = pd.Index(df.columns).astype(str)
    cols = cols.str.strip().str.lower()
    cols = cols.str.replace(r"\s+", "_", regex=True)
    cols = cols.str.replace("original_titlê", "original_title", regex=False)
    cols = cols.str.replace("genrë¨", "genre", regex=False)
    cols = cols.str.replace("unnamed:_8", "unnamed_8", regex=False)

    df.columns = cols
    return df


def remove_fully_null_columns_rows(df_columns_renamed):
    df = df_columns_renamed.copy()
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    return df


def clean_and_fill_content_rating(df_fully_null_removed):
    df = df_fully_null_removed.copy()
    s = df["content_rating"].replace("Not Rated", "Unrated")
    df["content_rating"] = s.fillna("Unrated")
    return df


def clean_release_year(df_clean_content_rating):
    df = df_clean_content_rating.copy()
    df["release_year_coerce"] = pd.to_datetime(
        df["release_year"], errors="coerce"
    )
    df["release_year_mixed"] = pd.to_datetime(
        df["release_year"], errors="coerce", format="mixed"
    )
    return df


def clean_income(df_clean_release_year):
    df = df_clean_release_year.copy()

    s = df["income"].astype(str).str.strip()
    s = s.replace({"nan": pd.NA, "None": pd.NA, "": pd.NA, "-": pd.NA})
    s = s.str.replace("$", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    s = s.str.replace(r"\s+", "", regex=True)
    s = s.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    s = s.str.replace(r"[^0-9\.\-]", "", regex=True)

    numeric = pd.to_numeric(s, errors="coerce")

    if numeric.isna().any():
        df["income"] = numeric.round(0).astype("Int64")
    else:
        df["income"] = numeric.round(0).astype("int64")

    return df
