# lampone23_task
Repozitář se základem (kostrou kódů) k řešení v rámci letního robotického kempu Campo Lampone 2023. Účastníci jsou rozděleni do týmů. Každý tým plní úlohu zvlášť jako celek. Sami si pak mezi sebou v týmu rozdělí podúlohy. 

## Popis úlohy
Pracovním prostorem úlohy je plachta s bílým pozadím a černou mřížku s 8 x 8 buňkami o velikosti 250 x 250 mm s tloušťkou čáry 25 mm. Nad touto plachtou je uchycena kamera tak, aby snímala celou plachtu. Na plachtě jsou rozmístěny objekty, které symbolizují cílový bod a překážky. Na počátku úlohy je na náhodnou buňku mřížky umístěn pohyblivý robot. Cílem úlohy je ovládat robota tak, aby co nejkratší cestou dojel do cílové buňky, aniž by po cestě projel buňkou označenou jako překážka.

# Možné varianty úlohy
- Robot se snaží dostat do cíle a při tom se vyhnout překážkám
- Každý krok robota stojí 1 bod. Ve dráze jsou nyní rozmístěny objekty, které body **přidávají**. Cílem je ujet dráhu s co největším počtem bodů
- Ve dráze jsou nyní umístěny objekty, které **ubírají** větší počet bodů
- Na robota je namotnován elektromagnet, který dokáže zdvihnout lehký kovový objekt. Na dráze je nyní jeden takový umístěný. Úkolem je přenést tento objekt do cílové destinace za cenu minimálního počtu kroků.
- Přidané bodované objekty

## Rozbor řešení úlohy
Celková úloha se dělí na několik podúloh. Tyto podúlohy si členové týmu rozdělí podle svých schopností a znalostí. Řešení jednotlivých podúloh doplňují do připravené kostry `base_solution.py`. Formátu vstupů a výstupů jednotlivých podúloh záleží na domluvě mezi příslušnými částmi týmů!

Kamera má dostatečné rozlišení tak, aby bylo z obrazu možné detekovat objekty v mřížce. Robot je zeshora osazen ArUCo kódem, který usnadní detekci jeho pozice a natočení. Objekty reprezentující překážku, cíl, ... jsou vyrobeny z tenkého materiálu (papír) s barvou odlišnou pozadí a mřížce. Cílem týmu je odeslat na vyhoodnocovací server posloupnost příkazů, kterými se robot musí řídit aby se dostal do cíle.

# `load_frame()`
Obraz z kamery je dostupný na našem serveru. Cíem této podúlohy je načíst tento obrázek do požadovaného formátu. 

# `detect_playground()`
V načteném obrázku se detekuje mřížka. Výstupem jsou souřadnice středů buněk mřížky.

# `detect_robot()`
V načteném obrázku se detekuje robot pomocí ArUCo tagu umístěného na jeho "zádech". Výstupem je souřadnice robota.

# `recognize_objects()`
V načteném obrázku se detekují ostatní objekty (mimo robota). Výstupem jsou souřadnice jednotlivých objektů a jejich typ (překážka, cíl, ...)!

# `analyze_playground()`
Analýza získaných dat z načteného obrázku. Výstupem je graf nebo numpy array, který reprezentuje celkový stav úlohy - kde se nachází robot, překážky, cíl, ...

# `generate_path()`
Nalezení nejkratší cesty v prostoru reprezentovaným grafem nebo numoy array. Z této cesty poté převod na příkazy pro robota (rovně, rovně, zatoč doleva, rovně, ...).

# `send_solution()`
Odeslání řešení úlohy na vyhodnocovací server pomocí UTP spojení.
