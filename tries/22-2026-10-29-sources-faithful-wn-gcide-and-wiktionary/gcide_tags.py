# gcide_tags.py (2026-10-29): how a GCIDE tag or entity is rendered when the dictionary is laid as a source brain.
# The rule (the owner, 10-29): keep ALL the context; strip only formatting; never summarize, drop or change.
# A tag with semantic content becomes "[label: content]" where the label is the tag's name in GCIDE's own tagset.txt;
# a purely typographic tag keeps its content and loses only the tag. The labels are the tagset's words, chosen by me.
import re, unicodedata

# tags that are typography or layout only (tagset.txt "Explicit typographical tags", plus the italic markers of the headword
# inside examples and quotations (ex, qex, xex), the italic marker of a foreign word inside an etymology (ets, etsep), right
# justification (rj), html strays, table layout). Their text stays; the tag goes.
TYPO = set('''plain it i bold b colf ct h1 h2 headrow hwf mitem pre sc str sub subs sups supr sansserif tt universbold vertical
column1 centered rj ex qex xex ets etsep a text nul styp TITLE I H1 CAPTION pl comp sim book item row td th table mtable matrix
matrix2x5 coltitle colheads ttitle tabtitle caption'''.split())
TYPO_RE = re.compile(r'^(point\d+|\w+type)$')

LABEL = {
 'ent': 'entry', 'hw': 'headword', 'mhw': 'headwords', 'wf': 'word form', 'pr': 'pronunciation', 'pos': 'part of speech',
 'epos': 'part of speech', 'vmorph': 'verb forms', 'nmorph': 'noun forms', 'amorph': 'adjective forms', 'conjf': 'conjugated form',
 'decf': 'declension form', 'adjf': 'adjective form', 'plu': 'plural', 'pluf': 'plural form', 'plw': 'plural word', 'sing': 'singular',
 'singf': 'singular form', 'singw': 'singular word', 'wordforms': 'word forms', 'mord': 'morphological derivation',
 'ety': 'etymology', 'sn': 'sense', 'sd': 'subdefinition', 'def': 'definition', 'def2': 'second definition', 'specif': 'specifically',
 'cd': 'collocation definition', 'cd2': 'collocation definition', 'col': 'collocation', 'colp': 'collocation', 'cp': 'collocation',
 'cs': 'collocation segment', 'mcol': 'collocations', 'ecol': 'collocation', 'cref': 'collocation reference', 'er': 'entry reference',
 'see': 'see', 'ref': 'reference', 'refs': 'references', 'fld': 'field', 'sfield': 'subfield', 'mark': 'mark', 'markp': 'mark',
 'note': 'note', 'wnote': 'note', 'comm': 'comment', 'usage': 'usage', 'uex': 'usage example', 'as': 'usage', 'illu': 'illustrative usage',
 'illust': 'illustration', 'iref': 'illustration reference', 'figref': 'figure reference', 'figcap': 'figure caption',
 'figtitle': 'figure title', 'figure': 'figure', 'img': 'image', 'q': 'quotation', 'qau': 'quotation author', 'au': 'authority',
 'qpers': 'speaker', 'qperson': 'speaker', 'syn': 'synonyms', 'ant': 'antonyms', 'contr': 'contrasting word', 'altname': 'alternative name',
 'altnpluf': 'alternative name', 'asp': 'alternative spelling', 'altsp': 'alternative spelling', 'abbr': 'abbreviation',
 'source': 'source', 'fr': 'frequency', 'fu': 'first use', 'ver': 'verified', 'wns': 'WordNet sense', 'wn16s': 'WordNet 1.6 sense',
 'w16ns': 'WordNet 1.6 sense', 'grk': 'Greek', 'xlati': 'translation', 'tran': 'word translated', 'tr': 'translation', 'itran': 'translation',
 'itrans': 'translation', 'sig': 'significance', 'stype': 'subtype', 'stypec': 'subtype', 'mstypec': 'subtypes', 'subtypes': 'subtypes',
 'isa': 'supertype', 'hypen': 'hypernym', 'simto': 'similar to', 'conseq': 'consequence', 'consof': 'consequence of',
 'hascons': 'has consequence', 'part': 'part', 'parts': 'parts', 'partof': 'part of', 'haspart': 'has part', 'contains': 'contains',
 'contxt': 'context', 'grp': 'group', 'membof': 'member of', 'memberof': 'member of', 'member': 'member', 'members': 'members',
 'method': 'method', 'methodfor': 'method for', 'corpn': 'corporation', 'company': 'company', 'org': 'organization', 'corr': 'correlative',
 'prod': 'produces', 'prodp': 'produces', 'prodmac': 'produces', 'prodby': 'produced by', 'stage': 'stage', 'stageof': 'stage of',
 'inv': 'inverse', 'examp': 'example', 'unit': 'unit', 'uses': 'uses', 'usedfor': 'used for', 'usedby': 'used by', 'perf': 'performs',
 'recipr': 'reciprocal', 'causes': 'causes', 'causesp': 'causes', 'causedby': 'caused by', 'causedbyp': 'caused by', 'cnvto': 'converted to',
 'compof': 'composed of', 'emits': 'emits', 'divof': 'division of', 'branchof': 'branch of', 'intensi': 'intensified',
 'spn': 'species name', 'kingdom': 'kingdom', 'phylum': 'phylum', 'subphylum': 'subphylum', 'class': 'class', 'subclass': 'subclass',
 'ord': 'order', 'subord': 'suborder', 'suborder': 'suborder', 'fam': 'family', 'subfam': 'subfamily', 'gen': 'genus', 'var': 'variety',
 'varn': 'variety', 'chform': 'chemical formula', 'chformi': 'chemical formula', 'chname': 'chemical name', 'chreact': 'chemical reaction',
 'cas': 'CAS number', 'mathex': 'mathematical expression', 'ratio': 'ratio', 'fract': 'fraction', 'exp': 'exponent', 'fexp': 'function',
 'funct': 'function', 'root': 'root', 'vinc': 'vinculum', 'person': 'person', 'persfn': 'person', 'bio': 'biography', 'biography': 'biography',
 'city': 'city', 'country': 'country', 'state': 'state', 'geog': 'region', 'river': 'river', 'street': 'street', 'date': 'date', 'datey': 'date',
 'booki': 'book', 'title': 'title', 'jour': 'journal', 'publ': 'publication', 'film': 'film', 'song': 'song', 'ship': 'ship',
 'tradename': 'trade name', 'trademark': 'trade name', 'edi': 'institution', 'ptcl': 'particle', 'musfig': 'music figure',
}

# entities <xxx/ : the webfont.txt table (its Uc column), the Greek letters, fractions and the diacritic pattern <letter+mark/
ENT = {'br': ' ', '?': '(?)', 'ldquo': '“', 'rdquo': '”', 'lsquo': '‘', 'rsquo': '’', 'hand': '☞',
 'ae': 'æ', 'AE': 'Æ', 'oe': 'œ', 'OE': 'Œ', 'edh': 'ð', 'EDH': 'Ð', 'thorn': 'þ', 'yogh': 'ȝ',
 'root': '√', 'cuberoot': '∛', 'sect': '§', 'pound': '£', 'deg': '°', 'prime': '´', 'bprime': '˝',
 'sec': '˝', 'Prime': '″', 'and': 'and', 'or': 'or', 'add': '+', 'bar': '|', 'times': '×', 'divide': '÷', 'min': '−',
 'rarr': '→', 'para': '¶', 'nbsp': ' ', 'middot': '•', 'mdash': '—', 'dagger': '†', 'Dagger': '‡',
 'sharp': '♯', 'flat': '♭', 'natural': '♮', 'segno': '\U0001d10b', 'schwa': 'ə', 'gt': '>', 'lt': '<', 'nsm': 'ṉ',
 'th': 'th', 'cre': '˘', 'breve': '˘', 'umlaut': '¨', 'dot': '˙', 'asper': 'ʽ', 'iques': '¿', 'nabla': '∇',
 'filig': 'fi', 'fllig': 'fl', 'ffllig': 'ffl', 'ai': 'ai', 'colbreak': ' ', 'colret': ' ', 'pause': '\U0001d110', 'dele': '⚑',
 'asterism': '⁂', 'ounceap': '℥', 'upslur': '⁀', 'downslur': '‿', 'lbrace2': '{', 'rbrace2': '}',
 'integral2l': '∬', '8star': '✳', '3dot': '∴', '2dot': '¨', 'astascending': '☊', 'astdescending': '☋',
 'Sun': '☉', 'Mercury': '☿', 'Jupiter': '♃', 'Male': '♂', 'Crev': 'Ɔ', 'aemac': '\u01e3', 'oemac': '\u0153\u0304', 'oomac': 'o\u035eo', 'oocr': 'o\u035do',
 'Aries': '♈', 'Taurus': '♉', 'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
 'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓', 'sigmat': 'ς',
}
GREEK = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι',
 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'omicron': 'ο', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ',
 'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω', 'digamma': 'ϝ'}
for g, c in GREEK.items(): ENT[g] = c; ENT[g.upper()] = c.upper()
MARK = {'mac': '̄', 'cr': '̆', 'breve': '̆', 'sl': '̄̇', 'smac': '̄', 'um': '̈', 'dot': '̇',
 'sdot': '̣', 'cir': '̂', 'til': '̃', 'acute': '́', 'grave': '̀', 'ring': '̊', 'ced': '̧', 'car': '̌',
 'it': '', 'dd': '̤'}
FRAC = re.compile(r'^frac(\d+)(?:x(\d+))?$')
def entity(name):
    if name in ENT: return ENT[name]
    m = FRAC.match(name)
    if m:
        a, b = m.group(1), m.group(2)
        if b: return a + '/' + b
        if len(a) == 2: return a[0] + '/' + a[1]
        if len(a) == 3 and a != '000': return a[0] + '/' + a[1:]
        return a
    m = re.match(r'^([A-Za-z]{1,2}?)(mac|cr|breve|sl|smac|um|dot|sdot|cir|til|acute|grave|ring|ced|car|it|dd)$', name)
    if m and m.group(1).lower() not in ('th',):
        return unicodedata.normalize('NFC', m.group(1) + MARK[m.group(2)])
    return '<' + name + '/'      # unknown: kept as written, so nothing is lost silently
ESC = {'d8': '‖', '94': 'ö', 'fa': '·'}   # the \'xx escapes that occur: foreign-word bar, o umlaut, middle dot
