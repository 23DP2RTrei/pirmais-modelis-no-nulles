"""Salīdzina loģistisko regresiju ar biežākās klases bāzes līniju."""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "tirs.csv"


def main() -> None:
    if not DATA_PATH.exists():
        raise SystemExit("Nav tirs.csv. Vispirms palaidiet: python datu_sagatavosana.py")

    df = pd.read_csv(DATA_PATH)
    y = df["income"].astype(str)
    X = df.drop(columns="income")
    # Jēgpilnas nosaukumu kolonnas palīdz izskaidrot rezultātus.
    categorical = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric = X.select_dtypes(include=["number"]).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Bāzes līnija vienmēr izvēlas biežāko klasi; tā parāda, cik daudz dod pats modelis.
    baseline_prediction = [y_train.mode().iloc[0]] * len(y_test)
    baseline_accuracy = accuracy_score(y_test, baseline_prediction)

    # Skaitliskās pazīmes tiek standartizētas, kategorijas pārvērstas indikatoros.
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ])
    prep = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric),
        ("categorical", categorical_pipeline, categorical),
    ])
    model = Pipeline([
        ("prep", prep),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    model_accuracy = accuracy_score(y_test, prediction)

    # Koeficientus apkopojam līdz sākotnējai kolonnai, lai atbilde būtu saprotama.
    feature_names = model.named_steps["prep"].get_feature_names_out()
    coefficients = abs(model.named_steps["classifier"].coef_[0])
    importance = pd.DataFrame({"feature": feature_names, "weight": coefficients})
    def original_column(encoded_name: str) -> str:
        encoded_name = encoded_name.split("__", maxsplit=1)[-1]
        # Kategoriju nosaukumos pašos var būt pasvītrojumi, tāpēc meklējam
        # pilnu sākotnējās kolonnas nosaukumu, nevis dalām pie pirmās svītras.
        candidates = sorted(numeric + categorical, key=len, reverse=True)
        for column in candidates:
            if encoded_name == column or encoded_name.startswith(column + "_"):
                return column
        return encoded_name

    importance["column"] = importance["feature"].map(original_column)
    top_columns = importance.groupby("column")["weight"].mean().sort_values(ascending=False).head(2)

    print(f"Testa rindas: {len(y_test)}")
    print(f"Bazes linijas precizitate: {baseline_accuracy:.3f}")
    print(f"Modela precizitate: {model_accuracy:.3f}")
    print("Classification report (precision, recall, F1):")
    print(classification_report(y_test, prediction, digits=3))
    print("Kludu matrica (rindas = ista klase, kolonnas = prognoze):")
    print(confusion_matrix(y_test, prediction, labels=["<=50K", ">50K"]))
    print("Divas kolonnas ar lielako koeficientu svaru (nav celonsakariba):")
    print(top_columns.to_string())

    # Viena kļūdaina piemēra izdruka vajadzīga, lai rezultātu varētu izskaidrot.
    errors = X_test.loc[y_test != prediction].copy()
    if not errors.empty:
        example = errors.iloc[0]
        true_value = y_test.loc[example.name]
        predicted_value = model.predict(example.to_frame().T)[0]
        print("Pirmais kludaini klasificetais testa piemers:")
        print(example.to_string())
        print(f"Istena klase: {true_value}; prognoze: {predicted_value}")


if __name__ == "__main__":
    main()
