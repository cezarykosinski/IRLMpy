# Infinite Rogue-Like Map Generator (*i aka. Torchman)

_Currently not usable._

#### IN PROGRES/TODO:
* [x] [GROUP] Finishing drilling <!--with randomized width of corridor. -->
* [x] [CELL/MAP/PROPERTIES] Reimplementing cell value calculation to include itself in the process.
* [ ] [GROUP/MAP] Implementing map escape invariant.
* [ ] [MAP] Reimplementing CA to take under consideration borders of neighbours

#### TO_REFACTOR:
- [ ] camelCase or snake_case
- [ ] append or +=
- [ ] constants as maps or classes
- [ ] logging(?) 
- [ ] swap temporary solutions with the stl ones

#### STAGE 1
##### Single map operations

- [x] Map initialization
- [x] Automat
- [x] Bordering and Grouping
- [ ] Groups connecting
- [x] Map escape assurance
- [ ] Code cleaning, optimising, classes and variables renaming

 Stage 2 
Multiple maps control
- [x] Initiating base map
- [x] Map accessing
- [ ] Code cleaning, optimising mem usage(seed storing), classes and variables renaming
<!--
Stage 3
Player control
(placing a player, controlling it and map interaction with him)

Stage 4
Agents based maps rating
(Torchman system, spawning fireplaces among groups )

Stage 5
Generating _"interesting"_ wages vectors based on 'Stage 4' agents

Stage 6 
Applying textures

Stage 7+
Converting project into 3rd dimension

-->
