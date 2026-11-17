# Diplomska-naloga

## Naslov: 
### [SLO] Vizualizacija lidarskih podatkov v arheologiji: Vpliv izbire tehnik in njihovih parametrov na vidnost arheoloških struktur
### [ENG] Visualization of LiDAR Data in Archaeology: The Impact of Technique Selection and Parameter Settings on the Visibility of Archaeological Features

## Opredelitev teme:

Lidarsko snemanje je v zadnjem desetletju postalo ena temeljnih metod prepoznavanja in dokumentiranja arheoloških struktur, zlasti na gozdnatih območjih. Na DEM datoteki pa sam po sebi ni primeren za interpretacijo, zato se uporabljajo različne vizualizacijske tehnike, ki poudarijo drobne reliefne oblike. Nobena tehnika ni univerzalna: vidnost posamezne strukture je odvisna od izbrane metode in od njenih parametrov, predvsem od prostorskega merila.

Diplomska naloga se osredotoča na štiri tehnike: Sky-View Factor, Openness, Simple Local Relief Model (SLRM) in Multidirectional Hillshade. Navaden hillshade služi kot izhodišče za primerjavo. Naloga obravnava teoretične osnove teh tehnik ter njihovo praktično uporabo na izbranem najdišču. Za območje raziskave je predvideno najdišče Cvinger pri Dolenjskih Toplicah, ki ima raznolike arheološke sledi.

Praktični del vključuje lastno implementacijo izbranih tehnik v Pythonu. Rezultati se primerjajo z obstoječimi orodji, predvsem z Relief Visualization Toolbox (RVT.py). Parametri tehnik se sistematično spreminjajo, da se ugotovi njihov vpliv na vidnost in prepoznavnost struktur. Prepoznavnost se ovrednoti tudi z objektivnimi merili, ne le z vizualno oceno.


## Namen naloge (oz. cilj naloge): 

predstaviti teoretične osnove LiDAR-ja (na splošno, raba v arheologiji) in parametre izbranih štirih tehnik

izdelati in preveriti lastne implementacije ter jih primerjati z RVT

ugotoviti, kako parametri (zlasti merilo) vplivajo na prepoznavnost struktur

primerjati tehnike glede na tip strukture in podati priporočila za prakso


## Raziskovalno vprašanje: 

Kako izbira parametrov, predvsem prostorskega merila, vpliva na prepoznavnost arheoloških struktur v posamezni tehniki?

Katera tehnika je najprimernejša za katere tipe struktur, ki so prisotne na Cvingerju pri Dolenjskih Toplicah?

Kako se lastne implementacije ujemajo z referenčnimi izhodi iz RVT?


