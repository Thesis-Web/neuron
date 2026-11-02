#!/usr/bin/env python3
# g34/page_patch5.py (2026-11-01, 19:10). The relationship formulas, a first table, as the page's pull laws (the look stays: a kind is a line,
# its pull a slider, its direction a choice). The owner: "each one of these relationships represents a mathematical formula that connects
# points to each other and pushes or pulls points away or together, some are between multiple points ... the formulas are reusable and can be
# the same formula for a relationship like opposite or inverse, or alike".
#  - The kinds the brain now lays from the definitions get a pull, a rest length, a colour and a direction: is (the class above, +y),
#    includes (the member below, -y), part/has/member (close, no direction), similar/related (middle), derived and alias (closest),
#    implies and causes (the consequence east, +x), past (the base form west, -x), before/after (the time axis, x), topic/context/use (weak).
#  - One new law, "the kind's own vector": the kind's displacement is not an axis but the mean of its pairs' displacements, learned each step;
#    every pair of that kind is pulled to the same vector. Two pairs of one kind then satisfy a:b as c:d (the catalog's analogy and
#    transformation: "one state or value becomes another", the same operation the same vector). Offered per kind in the direction choice.
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp'
P = D + '/NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html'
s = open(P, encoding='utf-8').read()
pairs = [
    # the kinds and their pulls
    ("['topic', 0.3, ''], ['context', 0.3, ''], ['category', 0.3, ''], ['method', 0.3, '']];",
     "['topic', 0.3, ''], ['context', 0.3, ''], ['category', 0.3, ''], ['method', 0.3, ''], ['member', 0.7, 'member of; a WordNet member holonym'], ['related', 0.4, 'related terms; Wiktionary'], ['implies', 0.6, 'entailment; WordNet'], ['causes', 0.6, 'cause; WordNet'], ['property', 0.5, 'attribute; WordNet'], ['alias', 0.9, 'an alternative form; Wiktionary']];"),
    # the kind words the brain writes, to the page's kinds
    ("var REL_OF = { like: 'alike', alike: 'alike',", "var REL_OF = { like: 'alike', alike: 'alike', synonym: 'alike', antonym: 'opposite', member: 'member', related: 'related', implies: 'implies', causes: 'causes', property: 'property', alias: 'alias',"),
    # colours
    ("topic: 0x909cb0, context: 0x98a4b8, category: 0xa0acc0, method: 0xa8b4c8 };", "topic: 0x909cb0, context: 0x98a4b8, category: 0xa0acc0, method: 0xa8b4c8, member: 0x7fb0d8, related: 0xb0b8c4, implies: 0xc9a86a, causes: 0xd9865f, property: 0xa88fd0, alias: 0xe8e8e8 };"),
    # rest lengths
    ("var REST = { 'dna before': 14, 'dna trigger': 14, 'dna call': 16, 'dna spawn': 16, 'made-of': 16, definition: 18, answered: 22, memory: 12, alike: 10, similar: 14, is: 22, includes: 22, has: 24, part: 24, opposite: 64, inverse: 64, contradicts: 64 };",
     "var REST = { 'dna before': 14, 'dna trigger': 14, 'dna call': 16, 'dna spawn': 16, 'made-of': 16, definition: 18, answered: 22, memory: 12, alike: 10, similar: 14, is: 22, includes: 22, has: 24, part: 24, opposite: 64, inverse: 64, contradicts: 64, member: 16, related: 18, 'derived-from': 10, alias: 6, implies: 20, causes: 20, property: 16, past: 12, before: 16, after: 16 };"),
    # directions: the class above, the member below, the consequence east, the base form and the earlier west; the kind's own vector offered
    ("var DIRS = [['', 'any way'], ['x', 'east +x'], ['-x', 'west -x'], ['y', 'north +y'], ['-y', 'south -y'], ['z', 'up +z'], ['-z', 'down -z'], ['across', 'across origin']];\n  var DEFAULT_DIR = { opposite: 'across', inverse: 'across', contradicts: 'across' };",
     "var DIRS = [['', 'any way'], ['x', 'east +x'], ['-x', 'west -x'], ['y', 'north +y'], ['-y', 'south -y'], ['z', 'up +z'], ['-z', 'down -z'], ['across', 'across origin'], ['shared', \"the kind's own vector\"]];\n  var DEFAULT_DIR = { opposite: 'across', inverse: 'across', contradicts: 'across', is: 'y', includes: '-y', implies: 'x', causes: 'x', past: '-x', before: 'x', after: '-x' };"),
    ("dir: RELSET[l[2]].dir === 'across' ? 'across' : dirVec(RELSET[l[2]].dir) }; });",
     "dir: RELSET[l[2]].dir === 'across' ? 'across' : RELSET[l[2]].dir === 'shared' ? 'shared' : dirVec(RELSET[l[2]].dir) }; });"),
    # the shared vector per kind, learned each step from the kind's pairs
    ("      for (i = 0; i < n; i++) { sp = SPRINGS[i]; sp.a.f = sp.a.f || new THREE.Vector3(); sp.b.f = sp.b.f || new THREE.Vector3(); sp.a.f.set(0, 0, 0); sp.b.f.set(0, 0, 0); }\n",
     "      for (i = 0; i < n; i++) { sp = SPRINGS[i]; sp.a.f = sp.a.f || new THREE.Vector3(); sp.b.f = sp.b.f || new THREE.Vector3(); sp.a.f.set(0, 0, 0); sp.b.f.set(0, 0, 0); }\n"
     "      var SHARED = {}; for (i = 0; i < n; i++) { sp = SPRINGS[i]; if (sp.dir !== 'shared') continue; var sv = SHARED[sp.kind] || (SHARED[sp.kind] = { v: new THREE.Vector3(), n: 0 }); sv.v.add(sp.b.pos).sub(sp.a.pos); sv.n++; } for (var sk in SHARED) SHARED[sk].v.multiplyScalar(1 / SHARED[sk].n);   // the kind's own vector: the mean displacement of its pairs; every pair is pulled to it (a:b as c:d)\n"),
    ("        } else if (sp.dir) {\n          _F.copy(sp.a.pos).addScaledVector(sp.dir, sp.rest).sub(sp.b.pos).multiplyScalar(-sp.k * .04);\n",
     "        } else if (sp.dir === 'shared') {\n          _F.copy(sp.a.pos).add(SHARED[sp.kind].v).sub(sp.b.pos).multiplyScalar(-sp.k * .04);\n"
     "        } else if (sp.dir) {\n          _F.copy(sp.a.pos).addScaledVector(sp.dir, sp.rest).sub(sp.b.pos).multiplyScalar(-sp.k * .04);\n"),
]
for old, new in pairs:
    assert s.count(old) == 1, (s.count(old), old[:90])
    s = s.replace(old, new)
open(P, 'w', encoding='utf-8').write(s); print('patched', P, len(pairs))
