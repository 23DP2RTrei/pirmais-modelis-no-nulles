# Rezultātu interpretācija

## Datu avots un jēga

UCI Adult ir 1994. gada ASV tautas skaitīšanas ierakstu izlase. Rinda apraksta vienu cilvēku ar vecuma, izglītības, darba un citām pazīmēm. Mērķa kolonna `income` norāda, vai avota ierakstā ienākumi pārsniedza 50 000 ASV dolāru gadā. Tas ir vēsturisks slieksnis un nav pielīdzināms mūsdienu ienākumiem.

## Tīrīšana

Palaižot `python 01_tirisana.py`, iegūti šādi skaitļi:

- Sākotnējās rindas: **32 561**
- Izmestās rindas ar trūkstošām vērtībām: **2 399**. Tās izņēmu, jo šajā vienkāršajā pieejā nepieņemu minējumus par trūkstošām darba, profesijas vai valsts kategorijām.
- Izmestie dublikāti: **23**. Tos izņēmu, lai viens un tas pats ieraksts neietekmētu rezultātu vairākas reizes.
- Nederīgas skaitliskās vērtības: **0**. UCI failā šajā pārbaudē netika atrasta kļūdaini nolasīta skaitliska vērtība vai vecums/darba stundu skaits ārpus izvēlētajiem nosacījumiem.
- Palikušās rindas: **30 139**

## Modeļa rezultāts

Modeli apmācīju ar 75% tīro datu un vērtēju ar atlikušo 25% testa daļu. `random_state=42` padara sadalījumu atkārtojamu.

- Biežākās klases bāzes līnijas testa precizitāte: **0,751**
- Loģistiskās regresijas testa precizitāte: **0,805**
- Starpība ir **0,054** jeb 5,4 procentpunkti. Šajā testa sadalījumā modelis ir labāks par minējumu, kas vienmēr izvēlas biežāko klasi.
- Divas kolonnas ar lielāko vidējo absolūto koeficientu: **capital_gain** un **marital_status**. Koeficientu lielums parāda, kuras pazīmes šajā modelī saistās ar prognozi; tas pats par sevi neparāda cēloņsakarību.

Klasi `>50K` modelis atpazina ar precision **0,575**, recall **0,825** un F1 **0,678**. Tas atrod lielu daļu šīs klases cilvēku, bet no prognozētajiem `>50K` daļa ir kļūdaini pozitīvi. Kļūdu matrica (rindas ir īstā klase, kolonnas ir prognoze; secība `<=50K`, `>50K`) ir:

```text
[[4515 1143]
 [ 329 1548]]
```

Precizitāte viena pati nav pietiekama, jo ienākumu klases ir nevienādas. Tāpēc skripts izvada arī precision, recall, F1 un kļūdu matricu. Svarīgi: pazīmju svars parāda saistību modeļa iekšienē, nevis pierāda cēloni.

## Viena kļūda un ierobežojums

Viens kļūdaini klasificēts testa ieraksts:

```text
age=50, workclass=Federal-gov, fnlwgt=36489, education=Some-college,
education_num=10, marital_status=Divorced, occupation=Exec-managerial,
relationship=Unmarried, race=White, sex=Male, capital_gain=0,
capital_loss=0, hours_per_week=40, native_country=United-States
Īstā klase: <=50K; modeļa prognoze: >50K
```

Tā ir kļūda, jo modeļa atbilde nesakrīt ar ieraksta `income` vērtību. Iespējams, ka modelim prognozi virzienā uz `>50K` pabīdīja vecums un profesija; viena rinda pati par sevi neļauj droši noteikt, kurš faktors bija izšķirošais. Reālie ienākumi atkarīgi arī no pazīmēm, kuru datos nav.

Šādu modeli nedrīkstētu izmantot kredīta piešķiršanai, jo viena kļūdaina prognoze var ietekmēt cilvēka piekļuvi pakalpojumam, bet modelis ir mācīts uz 1994. gada ASV datiem un izmanto arī demogrāfiskas pazīmes. Tas nav pārbaudīts mūsdienu Latvijas iedzīvotājiem un nav taisnīguma novērtējuma.

## Pašvērtējums

Izdevās izveidot atkārtojamu datu tīrīšanas procesu un pārbaudīt modeli pret vienkāršu bāzes līniju. Sarežģītākā daļa bija atšķirt kopējo precizitāti no tā, cik labi modelis atrod katru ienākumu klasi. Nākamreiz salīdzinātu vēl vienu modeli un rūpīgāk pārbaudītu, kā rezultāti atšķiras starp demogrāfiskām grupām.

## AI palīdzības atzīme

AI palīgs palīdzēja sagatavot sākotnējo skriptu un dokumentācijas karkasu. Datu interpretācija, izvades skaitļi un pašvērtējums jāaizpilda pēc programmas palaišanas un paša izpratnes; autoram jāspēj paskaidrot pieņemtos lēmumus.

