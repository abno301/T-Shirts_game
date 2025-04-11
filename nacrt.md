# Definicija problema

Igra **T-shirts** predstavlja konkretno simulacijo koordinacije med agenti s pomočjo lokalnih informacij.
Predstavljajmo si, da imamo 100 agentov, kjer je vsak agent na začetku naključno oblečen v modro ali rdečo majico.
Vsak agent ne pozna identitete drugih in deluje samo na podlagi opaženih informacij ob srečanju z naključno izbranimi partnerji.
V vsakem krogu se agenti porazdelijo v pare, pri čemer vsak agent opazi barvo majice svojega sogovornika.
Na podlagi opaženega podatka in izbrane strategije (ki jo lahko definiramo glede na predlagano literaturo) se agent odloči, ali bo spremenil svojo barvo, ali jo bo obdržal.
Cilj igre je doseči **globalni konsenz** – stanje, kjer vsi agenti nosijo isto barvo majic (npr. vsi modri ali vsi rdeči) in to dosežejo  na podlagi lastnih odločitev, brez prisile.

Pri tem primeru želimo analizirati, katera strategija preoblačenja – definirana glede na pravila, kot so "kopiraj opaženo barvo" ali "obdrži svojo, razen če opaži ponavljajočo se spremembo pri partnerjih" – vodi do najhitrejšega dosega konsenza. Poleg tega bomo preučili, kako sprememba števila agentov (npr. 50, 100, 200) vpliva na čas konvergence.

**Ključne besede:** agenti, konsenz, norm, koordinacija, simulacija

---

# Pregled sorodnih del in pregled evaluacije rešitve problema

V literaturi so opisani koncepti, ki se navezujejo na nastajanje socialnih konvencij in konsenza v večagentnih sistemih. Med ključnimi deli so:

### 1. Consensus Learning for Cooperative Multi-Agent Reinforcement Learning
**Zhiwei Xu, Bin Zhang, Dapeng Li, Zeren Zhang, Guangchong Zhou, Hao Chen, Guoliang Fan**
*Institute of Automation, Chinese Academy of Sciences*
*School of Artificial Intelligence, University of Chinese Academy of Sciences*
*Beijing, China*
Članek obravnava **učenje konsenza** v **večagentnih sistemih** z uporabo **ojačevalnega učenja** in **kontrastnega učenja**. Avtorji so razvili metodo **COLA (Consensus Learning Algorithm)**, ki omogoča agentom, da **dosežejo skupno odločitev brez neposredne komunikacije**.

**Meri se uspešnost sodelovanja**: Primerjali so **hitrost učenja**, **natančnost odločanja**, **uspešnost v igrah** in **stabilnost rešitve**.
**Analiza vpliva hiperparametrov**: Raziskali so, kako različne nastavitve modela vplivajo na rezultate.

Iz članka lahko uporabimo:
- **Consensus Learning**: Agenti spreminjajo barvo majice na podlagi **lokalnega soglasja** (če srečajo več rdečih, postanejo rdeči).
- **Contrastive Learning**: Agenti se učijo, katera strategija je najboljša, s primerjavo različnih interakcij.
- **Majority Rule**: Če agent večkrat zapored vidi isto barvo, se ji prilagod

Primerjava z člankom:
- **Meri hitrost doseganja soglasja** (koliko krogov je potrebnih, da vsi agenti nosijo isto barvo).
- **Primerjaj različne strategije preoblačenja** (npr. hitrost "majority rule" vs. hitrost "random switch").
- **Simuliraj igro z različnim številom agentov** in preveri, kako to vpliva na čas do konsenza

### 2. Multi-Agent Flag Coordination Games
**David Kohan Marzagão, Nicolás Rivera, Colin Cooper, Peter McBurney, Kathleen Steinhöfel**
*King’s College London, UK*
Raziskuje **večagentno koordinacijo**, kjer agenti izbirajo med omejenim številom možnosti (barve zastav) in skušajo doseči **želen globalni vzorec** le na podlagi lokalnih interakcij. To je podobno T-shirts igri, kjer agenti spreminjajo barve majic na podlagi srečanj z drugimi agenti.

Iz članka lahko uporabimo:
- Naključno kopiranje barve soseda.
- Odločanje na podlagi verjetnostne porazdelitve – Lahko implementiramo različne strategije, kjer agenti ne kopirajo vedno barve, ampak upoštevajo tudi pretekle izkušnje.
- **Uporaba Nashovega ekvilibrija** – Če dodamo možnost, da agent poskuša spremeniti barvo soseda (namesto svoje), lahko testiramo, ali to pospeši ali upočasni doseganje soglasja.

Primerjava z člankom:
- Primerjava razlicne zacetne razporeditve
- Testiranje verjetnostnega soglasja (agent spreminja barvo z doloceno verjetnostjo)

### 3. Consensus in Multi-Agent Systems with Communication Constraints 
**Guanghui Wen, Zhisheng Duan, Wenwu Yu**
*Guanrong Chen Peking University, Southeast University, City University of Hong Kong, China*

Članek se osredotoča na problem drugega reda soglasja v večagentnih sistemih, kjer agenti komunicirajo prek prekinjenih (intermittent) časovnih intervalov. Razviti so bili protokoli, ki s pomočjo sinhronih lokalnih meritev in uporabe orodij iz algebrske teorije grafov ter Lyapunovove analize omogočajo, da se kljub omejitvam v komunikaciji doseže eksponentna konvergenca stanj vseh agentov.


  
Iz članka lahko uporabimo:
• Pristop k doseganju soglasja v sistemih z intermittentno komunikacijo, ki je primeren za okolja z nezanesljivimi komunikacijskimi povezavami.
• Določitev matematičnih pogojev (na splošno algebrajsko povezanost grafa) za zagotovitev robustnosti in stabilnosti koordinacije. 
• Uporabo Lyapunovove metode za analizo eksponentne konvergence dinamičnih stanj agentov.


Primerjava z člankom: 
- Lahko primerjamo hitrost soglasja v T-Shirts igri pri **stalni in prekinjeni komunikaciji**.
- Testiramo različne strategije preoblačenja in preverimo, katera je najbližje matematičnemu modelu iz članka.
- Analiziramo algebrajsko povezanost v grafu agentov in preverimo njen vpliv na čas do soglasja.



---

# Načrt rešitve

## Projektna skupina in sodelavci

- **Projektna skupina:** Povezljivi Sistemi 2025  
- **Sodelavci:**  
  - Jernej Hozjan

## Repozitorij

- **Povezava do repozitorija:** [repo](https://github.com/abno301/T-Shirts_game)

## Izbran programski jezik in orodja

- **Python** – zaradi preprostosti implementacije simulacij ter bogate podpore knjižnic za statistično analizo in vizualizacijo (npr. NumPy, Matplotlib).
- **Simulacijsko okolje:** Za testiranje in primerjalno analizo učinkovitosti različnih strategij preoblačenja.

## Razvojne iteracije

Projekt boma izvedla v štirih razvojnih iteracijah:

1. **Prva iteracija:**
   - Oblikovanje osnovne arhitekture simulacije.
   - Implementacija osnovnega modela agenta, z naključno dodeljenimi barvami (modra in rdeča).
   - Inicializacija sistema s fiksnim številom agentov (npr. 100).

2. **Druga iteracija:**
   - Implementacija interakcij med agenti: naključna razporeditev parov in prenos opaženih informacij.
   - Razvoj prve strategije preoblačenja (npr. "kopiraj opaženo barvo").

3. **Tretja iteracija:**
   - Integracija dodatnih strategij preoblačenja (npr. strategije, ki temeljijo na večkratnih opažanjih in statistični analizi preteklih interakcij).
   - Testiranje sistema z različnimi številkami agentov (50, 100, 200) in zbiranje podatkov o času konvergence.

4. **Četrta iteracija:**
   - Celovita evalvacija in primerjalna analiza učinkovitosti različnih strategij.
   - Izvedba lastne strategije preoblačenja, ki jo primerjamo z obstoječimi.
   - Optimizacija in priprava zaključne dokumentacije ter predstavitve projekta.

## Opis rešitve in UML diagram

Rešitev temelji na simulaciji zaporednih interakcij med agenti, kjer vsak agent, glede na opaženo barvo partnerja, uporabi svojo strategijo preoblačenja. Sistem beleži, koliko krogov je potrebno, da se doseže konsenz, in omogoča primerjavo več strategij. Na primer, strategija A lahko preprosto kopira opaženo barvo, medtem ko strategija B upošteva tudi statistiko preteklih interakcij. S tem pristopom želimo oceniti, katera strategija pripelje do hitrejšega in stabilnejšega dosega globalnega konsenza.

Spodaj je prikazan primer UML diagrama, ki ponazarja osnovno strukturo sistema:

![[UMLDiagram.png]]

*Opomba: UML diagram prikazuje glavne razrede, kot so `Agent`, `Simulator`, `Strategy` ter medsebojne odnose, ki definirajo interakcije med agenti med simulacijo.*















