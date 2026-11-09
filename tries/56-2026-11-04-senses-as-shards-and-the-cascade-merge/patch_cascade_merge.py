# patch_cascade_merge.py (tries/56): C28 part 2, the cascade merge rule as kernel physics at the span: when a BUILD span closes, every symbol of
# it that is an uppercase ASCII word (two letters or more) whose lowercase twin is a defined point (node rows) merges into the twin (nk_merge).
# The owner, 11-04 05:00: "what should happen when that word exists in the graph, insert, table, integer, etc, all of those hand laids ...
# should merge with the correct neuron for that word". A hand laid symbol is one used inside a BUILD span; a word of a source (WHO) is never
# touched because it never stands in a span.
import os
os.chdir(os.path.expanduser('~/nk-c27'))
c = open('nk.c').read()
old = "      int from = r->build_pos; r->build_pos = -1;\n      char *text = decode_span(b, run, from, pos);"
assert c.count(old) == 1, c.count(old)
new = r'''      int from = r->build_pos; r->build_pos = -1;
      /* C28 (the owner, 11-04 05:00): a hand laid symbol in this span, an uppercase word whose lowercase twin is a defined point, merges into the twin */
      for(int p = from + 1; p < pos; p++){ int g = r->seq[p - 1]; if(g <= 0 || g > b->label.n) continue; const char *s = b->label.sym[g]; size_t L = strlen(s); if(L < 2) continue;
        int up = 1; for(size_t i = 0; i < L; i++) if(s[i] < 'A' || s[i] > 'Z'){ up = 0; break; } if(!up) continue;
        char lo[256]; if(L >= sizeof lo) continue; for(size_t i = 0; i <= L; i++) lo[i] = s[i] >= 'A' && s[i] <= 'Z' ? s[i] + 32 : s[i];
        int t = label_gate(b, lo); if(!t || t == g) continue; Neuron *tn = neuron_of(b, t); if(!tn || !tn->nnode) continue;
        char out[512]; nk_merge(b, g, t, out, sizeof out); }
      char *text = decode_span(b, run, from, pos);'''
c = c.replace(old, new, 1); open('nk.c', 'w').write(c); print('nk.c: the cascade merge at the span closing')
