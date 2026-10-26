# NEURON SOURCES

*2026-10-19. Every source the brain can connect to in turn one. Each was tested from hp2 on 10-19, and the ones that answered are marked live. The owner: "the more and better sources it can connect to, the better, and the less it will have to believe you or I on truth."*

**How the brain uses these.** This list is told connection information, not facts. The brain reads a source itself, through runs (CALL), when a gap or a question sends it there. Nothing on this list is bulk-loaded into the graph (blueprint §18). Trust is kept per source and per topic, and no source is 100% (blueprint §10).

**Kinds** follow blueprint §10.1:
- **Grounded:** reference works, official bodies, curated data.
- **To a degree:** crowd-edited, or not peer-reviewed.
- **Never grounded:** LLMs.

---

## 1. What is already on each machine (hp and hp2)

| What | Where | Kind |
|---|---|---|
| Merriam-Webster API keys (Collegiate Dictionary, Collegiate Thesaurus) | `~/neuron-build/keys/mw_collegiate.key`, `mw_thesaurus.key` (mode 600). The builder installs them where the brain can read them (blueprint §17, step 1). Both keys were tested live on 10-19. | grounded |
| Local dictionary server (`dictd`) | `dict -h localhost -d <db> <word>`. Databases: `gcide` (Webster's 1913), `wn` (WordNet 3.0), `foldoc` (computing), `elements` (chemistry) | grounded |
| WordNet 3.0 (Princeton) | `/usr/share/wordnet/` (data.*, index.*); command `wn` | grounded |
| Open English WordNet 2025 (the maintained successor to WordNet) | `/srv/sources/wordnet/oewn-2025/`: `english-wordnet-2025/` in the WordNet 3.0 file layout, and `english-wordnet-2025-json/` | grounded |
| man pages, `/usr/share/doc` | `man <thing>` | grounded, for computer actions |
| Go documentation | `go doc <pkg>.<name>`; the language spec at https://go.dev/ref/spec | grounded, for computer actions |

**Note for builders.** `/home/james` is mode 700 on both machines, so the `neuron` user can't read anything under it. Anything the brain must read (sources, the kernel binary, lay files, keys) has to live outside it, for example in `/srv/sources/`, which every user can read.

## 2. Language: dictionaries, thesauruses, meaning and actions

| Source | How to reach | Kind | Notes |
|---|---|---|---|
| Merriam-Webster Collegiate Dictionary | `https://www.dictionaryapi.com/api/v3/references/collegiate/json/<word>?key=<dictionary key>` | grounded | live; non-commercial use is free, with a daily limit (see dictionaryapi.com) |
| Merriam-Webster Collegiate Thesaurus | `.../references/thesaurus/json/<word>?key=<thesaurus key>` | grounded | live; each key works for its own reference only |
| dict.org (274 databases) | `curl dict://dict.org/d:<word>:<db>`; the list: `dict://dict.org/show:db` | grounded | live. Useful databases: `gcide`, `wn`, `moby-thesaurus` (Moby Thesaurus II), `foldoc`, `elements`, `vera` (acronyms), and `fd-*` (bilingual FreeDict dictionaries, for other human languages). `devil` is satire and never grounded. `world02` and `gaz2k-*` date from 2000–2002. |
| Roget's Thesaurus (1911) | `https://www.gutenberg.org/cache/epub/10681/pg10681.txt` | grounded | live |
| VerbNet (verb classes: what verbs do) | `https://github.com/cu-clear/verbnet` | grounded | live. Linguist-built; describes verbs as actions with roles. Close to "meaning is action". |
| FrameNet 1.7 (the situations words call up) | `https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/framenet_v17.zip` | grounded | live (Berkeley) |
| CMU Pronouncing Dictionary | `https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict` | grounded | live |
| Unicode CLDR (number words and locale data for many languages) | `https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-rbnf/rbnf/<lang>.json` | grounded | live; how each language spells out numbers |
| Natural Semantic Metalanguage (the 65 primes) | `https://nsm-approach.net/` | grounded | live (web pages); the source of the primes in blueprint §16 |
| Wiktionary | `https://en.wiktionary.org/api/rest_v1/page/definition/<word>` | to a degree | live; crowd-edited; includes etymology and translations |

## 3. Encyclopedias, libraries, books

| Source | How to reach | Kind | Notes |
|---|---|---|---|
| Stanford Encyclopedia of Philosophy | `https://plato.stanford.edu/entries/<entry>/` | grounded | live (web pages); peer-reviewed |
| Encyclopaedia Britannica 1911 (on Wikisource) | `https://en.wikisource.org/w/api.php?action=query&list=search&srsearch=<q>&format=json` | grounded, but 1911 | live; public domain, dated |
| Library of Congress | `https://www.loc.gov/search/?q=<q>&fo=json` | grounded | live |
| Internet Archive | `https://archive.org/advancedsearch.php?q=<q>&fl[]=identifier&output=json` | depends on the book | live; holds many public-domain reference books |
| Project Gutenberg | `https://www.gutenberg.org/ebooks/search/?query=<q>`; catalog: `https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv` | depends on the book | live (Gutendex, a third-party Gutenberg search API, timed out) |
| Open Library | `https://openlibrary.org/search.json?q=<q>` | catalog | live; book metadata |
| Wikipedia | `https://en.wikipedia.org/api/rest_v1/page/summary/<title>` | to a degree | live; Wikimedia asks for a descriptive User-Agent |
| Wikidata (structured facts, with references) | `https://www.wikidata.org/w/api.php?action=wbsearchentities&search=<q>&language=en&format=json`; SPARQL: `https://query.wikidata.org/sparql?format=json&query=<q>` | to a degree | live |

## 4. Textbooks

| Source | How to reach | Kind | Notes |
|---|---|---|---|
| OpenStax (peer-reviewed free textbooks: math, physics, chemistry, biology, history and more) | list: `https://openstax.org/apps/cms/api/v2/pages/?type=books.Book&fields=title&limit=200` (129 books); source text: `https://github.com/openstax/osbooks-<book>` (for example `osbooks-calculus-bundle`, `osbooks-university-physics-bundle`, `osbooks-college-algebra-bundle`, `osbooks-introductory-statistics-bundle`, `osbooks-us-history`) | grounded | live |
| NCBI Bookshelf (biology and medicine textbooks) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=books&term=<q>&retmode=json` | grounded | live |
| Open Textbook Library (a catalog of reviewed open textbooks) | `https://open.umn.edu/opentextbooks` | grounded | live (web pages) |
| LibreTexts | `https://<subject>.libretexts.org/` | to a degree | live (web pages); review varies |

## 5. Math

| Source | How to reach | Kind | Notes |
|---|---|---|---|
| OEIS (integer sequences) | `https://oeis.org/search?q=<terms>&fmt=json` | grounded | live; numbers and their relationships |
| NIST Digital Library of Mathematical Functions | `https://dlmf.nist.gov/` | grounded | live (web pages) |
| Wolfram MathWorld | `https://mathworld.wolfram.com/<Topic>.html` | grounded | live (web pages) |
| Metamath set.mm (machine-checked proofs, built up from axioms) | `https://raw.githubusercontent.com/metamath/set.mm/develop/set.mm`; browsable at `https://us.metamath.org/mpeuni/mmset.html` | grounded | live; every step is verified |

## 6. Science and the physical world

| Source | How to reach | Kind | Notes |
|---|---|---|---|
| NIST CODATA physical constants | `https://physics.nist.gov/cuu/Constants/Table/allascii.txt` | grounded | live (2022 CODATA adjustment) |
| NIST SI units | `https://physics.nist.gov/cuu/Units/units.html` | grounded | live |
| NIST Chemistry WebBook | `https://webbook.nist.gov/chemistry/` | grounded | live (web pages) |
| PubChem (compounds, elements) | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/<name>/property/MolecularFormula,MolecularWeight/JSON`; periodic table: `.../rest/pug/periodictable/JSON` | grounded | live |
| UniProt (proteins; reviewed Swiss-Prot entries) | `https://rest.uniprot.org/uniprotkb/search?query=<q>&format=json` | grounded | live |
| GBIF (species backbone) | `https://api.gbif.org/v1/species/match?name=<name>` | grounded | live (Salmo trutta, the brown trout, matched) |
| ITIS (US government taxonomy) | `https://www.itis.gov/ITISWebService/jsonservice/searchByScientificName?srchKey=<name>` | grounded | live |
| JPL Horizons (solar system bodies and positions) | `https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='<id>'` | grounded | live |
| JPL Small-Body Database | `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=<name>` | grounded | live |
| USDA FoodData Central | `https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query=<q>` | grounded | live with the shared `DEMO_KEY`; a free personal key comes from api.data.gov |
| MedlinePlus health topics (NIH) | `https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term=<q>` | grounded | live (XML) |
| USGS earthquakes (live data) | `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=<date>` | grounded | live |
| World Bank indicators | `https://api.worldbank.org/v2/country/<code>/indicator/<id>?format=json` | grounded | live; official statistics |
| CIA World Factbook (JSON mirror) | `https://raw.githubusercontent.com/factbook/factbook.json/master/<region>/<code>.json` | grounded (mirror) | live |
| OpenStreetMap Nominatim (places) | `https://nominatim.openstreetmap.org/search?q=<q>&format=json` | to a degree | live; crowd-mapped; at most one request a second |
| PubMed (peer-reviewed research abstracts) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<q>&retmode=json` | to a degree | live; findings, not settled reference; about 3 requests a second without an NCBI key |
| Europe PMC (open research, often full text) | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<q>&format=json` | to a degree | live |
| arXiv (preprints, not peer-reviewed) | `http://export.arxiv.org/api/query?search_query=<q>` | to a degree (lowest) | live; space requests about 3 seconds apart |
| Crossref, OpenAlex (research metadata) | `https://api.crossref.org/works?query=<q>`; `https://api.openalex.org/works?search=<q>` | metadata only | live. OpenAlex without a key shares a small free daily budget with the whole IP address. |

## 7. Computers: what the machine can do, and how

| Source | How to reach | Kind | Notes |
|---|---|---|---|
| man pages, `go doc` | local | grounded | the first place to look |
| POSIX (The Open Group Base Specifications) | `https://pubs.opengroup.org/onlinepubs/9799919799/` | grounded | live |
| RFCs (internet standards) | `https://www.rfc-editor.org/rfc/rfc<N>.txt`; index: `https://www.rfc-editor.org/rfc-index.xml` | grounded | live |
| Unicode Character Database (every character and key) | `https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt` | grounded | live; for "every key has its own neuron" |
| Go: spec and packages | `https://go.dev/ref/spec`; `https://pkg.go.dev/<pkg>` | grounded | live |
| SQLite documentation | `https://sqlite.org/lang.html` | grounded | live |
| Python documentation | `https://docs.python.org/3/` | grounded | live |
| Linux kernel documentation | `https://docs.kernel.org/` | grounded | live |
| DevDocs (official documentation for hundreds of tools, as JSON) | list: `https://devdocs.io/docs.json` | as its sources | live |
| MDN Web Docs | `https://developer.mozilla.org/api/v1/search?q=<q>` | to a degree | live |
| cppreference (C and C++) | `https://en.cppreference.com/w/c` | to a degree | live |

## 8. Never grounded: friends

| Friend | How | Rule |
|---|---|---|
| Claude (the same account the builders use) | `claude -p "<question>"` on the machine | Ask the owner first ("would you like me to phone a friend?"). The answer is a guess, weighed by trust per topic (blueprint §10.4). |

## 9. Not usable right now (10-19)

| Source | Why |
|---|---|
| Wordnik (American Heritage, Century and more) | needs a free key; the owner can get one at developer.wordnik.com |
| Etymonline (etymology), ProofWiki, Princeton's WordNet site | block scripts behind a "just a moment" check. Etymology is also in GCIDE and Wiktionary, and WordNet 3.0 is installed locally. |
| ConceptNet | down (502), and fuzzy anyway |
| Gutendex, Free Dictionary API | timed out. Use gutenberg.org directly; Free Dictionary is a copy of Wiktionary anyway. |
| REST Countries v3.1 | deprecated |

**Later:** the owner's own benchtop references (for example the fly-tying books) can be added as files when they are scanned.
