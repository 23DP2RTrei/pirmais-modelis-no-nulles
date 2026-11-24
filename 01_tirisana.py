"""Lejupielādē un sakārto UCI Adult datus reproducējamā veidā."""

from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RAW_PATH = DATA_DIR / "adult_raw.data"
CLEAN_PATH = ROOT / "tirs.csv"
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country",
    "income",
]


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not RAW_PATH.exists():
        print("Lejupielādēju Adult datu kopu no UCI...")
        urlretrieve(URL, RAW_PATH)

    # UCI fails ir bez galvenes; tukšie lauki un '?' tiek uztverti kā trūkstoši.
    df = pd.read_csv(
        RAW_PATH,
        header=None,
        names=COLUMNS,
        skipinitialspace=True,
        na_values=["?", ""],
        dtype={"income": "string"},
    )
    sākumā = len(df)

    # Tukšumi sastopami galvenokārt darba klasē, profesijā un dzimšanas valstī;
    # bez šīm pazīmēm ierakstu nevar korekti izmantot šajā salīdzinājumā.
    missing = df.isna().any(axis=1)
    pēc_trūkstošajiem = df.loc[~missing].copy()
    izmeta_trūkstošos = sākumā - len(pēc_trūkstošajiem)

    # Identiski ieraksti nedrīkst mākslīgi palielināt vienu un to pašu piemēru svaru.
    dup = pēc_trūkstošajiem.duplicated(keep="first")
    clean = pēc_trūkstošajiem.loc[~dup].copy()
    izmeta_dublikātus = len(pēc_trūkstošajiem) - len(clean)

    # Vērtības ir skaitliskas pēc UCI shēmas; kļūdainas rindas tiek atdalītas,
    # nevis klusām pārvērstas par nullēm.
    numeric = [
        "age", "fnlwgt", "education_num", "capital_gain", "capital_loss",
        "hours_per_week",
    ]
    for column in numeric:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")
    invalid = clean[numeric].isna().any(axis=1) | (clean["age"] <= 0) | (clean["hours_per_week"] <= 0)
    izmeta_nederīgos = int(invalid.sum())
    clean = clean.loc[~invalid].copy()

    clean["income"] = clean["income"].str.rstrip(".").str.strip()
    clean = clean[clean["income"].isin(["<=50K", ">50K"])].copy()
    clean.to_csv(CLEAN_PATH, index=False)

    # ASCII izvade darbojas arī Windows konsolēs ar vecāku kodējumu.
    print(f"Rindu sakuma: {sākumā}")
    print(f"Izmeta trukstosu vertibu del: {izmeta_trūkstošos}")
    print(f"Izmeta dublikatu del: {izmeta_dublikātus}")
    print(f"Izmeta nederigu skaitlisku vertibu del: {izmeta_nederīgos}")
    print(f"Rindu beigas: {len(clean)}")
    print(f"Saglabats: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
