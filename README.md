# Pirmais modelis no nulles

Neliels klasifikācijas projekts ar UCI Adult datu kopu. Mērķis ir salīdzināt loģistisko regresiju ar vienkāršu bāzes līniju, kas vienmēr izvēlas biežāko ienākumu klasi.

## Sākšana

Python 3.10 vai jaunāks:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python 01_tirisana.py
python 02_modelis.py
```

Pirmais skripts lejupielādē oriģinālo UCI `adult.data` failu mapē `data/`, saglabājot to nemainītu kā `adult_raw.data`, izveido `tirs.csv` un izdrukā rindu skaitu pirms un pēc tīrīšanas. Otrs skripts izmanto `tirs.csv`.

## Projekta struktūra

```text
data/
  AVOTS.txt
  adult_raw.data       # pēc 01_tirisana.py palaišanas
01_tirisana.py
02_modelis.py
tirs.csv               # pēc 01_tirisana.py palaišanas
rezultati.md
README.md
requirements.txt
```

## Ierobežojumi

Dati ir no ASV 1994. gada tautas skaitīšanas izlases, tāpēc tie nav piemēroti mūsdienu cilvēku ienākumu vai Latvijas iedzīvotāju prognozēšanai. Tie satur sensitīvas demogrāfiskas pazīmes un vēsturisku nevienlīdzību. Modeli nevajag izmantot darbā pieņemšanā, kredītu piešķiršanā vai individuālu lēmumu pieņemšanā. Tas ir mācību piemērs, nevis reāls novērtēšanas rīks.

## Par darba tapšanu

Šis ir mācību darbs, kurā izmantots AI palīgs: tas palīdzēja izveidot sākotnējo koda struktūru un pārbaudīt idejas. Autors pirms iesniegšanas pārskata katru koda daļu, palaiž skriptus un spēj saviem vārdiem izskaidrot datu tīrīšanu, modeļa salīdzinājumu un ierobežojumus.

