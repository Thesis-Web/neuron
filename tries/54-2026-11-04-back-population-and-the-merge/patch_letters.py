# patch_letters.py (tries/54): the encoder's letter rule made sequence-aware: a non-ASCII character continues a word unless it is punctuation
# (Latin-1 supplement symbols U+0080-00BF; general punctuation U+2000-206F: quotes, dashes, the hyphenation point, the ellipsis). The first C27
# form (any byte >= 0x80 is a letter) glued closing quotes to words: spend”, consume”.
import os
os.chdir(os.path.expanduser('~/nk-c27'))
c = open('nk.c').read()
old_fn = "static int is_letter(unsigned char c){ return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_' || c >= 0x80; }"
assert c.count(old_fn) == 1
new_fn = ("static int is_letter(unsigned char c){ return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'; }"
          "/* C27 (the owner, 11-04 04:30): a word is one symbol in any script. A character of another script continues the word; the punctuation of other\n"
          "   scripts does not: U+0080-00BF (the Latin-1 symbols: middle dot, guillemets, degree) and U+2000-206F (quotes, dashes, the hyphenation point,\n"
          "   the ellipsis). Returns the byte length of the letter at s, 0 when s does not begin a letter. */\n"
          "static int letter_len(const unsigned char *s, size_t rem){\n"
          "  if(!rem) return 0; unsigned char c = s[0];\n"
          "  if(c < 0x80) return is_letter(c) ? 1 : 0;\n"
          "  int n = u8len(c); if((size_t)n > rem) return 0;\n"
          "  if(c == 0xC2) return 0;                                              /* U+0080-00BF */\n"
          "  if(c == 0xE2 && n == 3 && (s[1] == 0x80 || s[1] == 0x81)) return 0;   /* U+2000-207F: general punctuation, super/subscripts kept out of a word? no: U+2070-207F are superscripts; keep them */\n"
          "  return n;\n"
          "}")
c = c.replace(old_fn, "static int is_letter(unsigned char c){ return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'; }", 1)
u8 = "static int u8len(unsigned char c){ if(c < 0x80) return 1; if((c >> 5) == 6) return 2; if((c >> 4) == 14) return 3; if((c >> 3) == 30) return 4; return 1; }"
assert c.count(u8) == 1
c = c.replace(u8, u8 + "\n" + new_fn[len("static int is_letter(unsigned char c){ return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'; }"):], 1)
# the three cut loops: a letter run gathered by letter_len
loops = [
 ("    if(is_letter((unsigned char)text[i])){ while(j < L && is_letter((unsigned char)text[j])) j++; }\n    else j = i + u8len((unsigned char)text[i]);",
  "    if(letter_len((const unsigned char*)text + i, L - i)){ int k; while(j < L && (k = letter_len((const unsigned char*)text + j, L - j))) j += k; }\n    else j = i + u8len((unsigned char)text[i]);"),
 ("  while(i < L){ size_t j = i; if(is_letter((unsigned char)s[i])){ while(j < L && j - i < sizeof buf - 1 && is_letter((unsigned char)s[j])) j++; } else j = i + u8len((unsigned char)s[i]); if(j > L) j = L;\n    size_t m = j - i; memcpy(buf, s + i, m); buf[m] = 0; int gt = label_gate(b, buf); if(!gt) gt = label_new(b, buf);",
  "  while(i < L){ size_t j = i; if(letter_len((const unsigned char*)s + i, L - i)){ int k; while(j < L && j - i < sizeof buf - 8 && (k = letter_len((const unsigned char*)s + j, L - j))) j += k; } else j = i + u8len((unsigned char)s[i]); if(j > L) j = L;\n    size_t m = j - i; memcpy(buf, s + i, m); buf[m] = 0; int gt = label_gate(b, buf); if(!gt) gt = label_new(b, buf);"),
 ("  while(i < L){ size_t j = i; if(is_letter((unsigned char)text[i])){ while(j < L && is_letter((unsigned char)text[j])) j++; } else j = i + u8len((unsigned char)text[i]); if(j > L) j = L;\n    size_t m = j - i; if(m >= sizeof buf) m = sizeof buf - 1; memcpy(buf, text + i, m); buf[m] = 0;\n    if(*n >= SEQCAP)",
  "  while(i < L){ size_t j = i; if(letter_len((const unsigned char*)text + i, L - i)){ int k; while(j < L && (k = letter_len((const unsigned char*)text + j, L - j))) j += k; } else j = i + u8len((unsigned char)text[i]); if(j > L) j = L;\n    size_t m = j - i; if(m >= sizeof buf) m = sizeof buf - 1; memcpy(buf, text + i, m); buf[m] = 0;\n    if(*n >= SEQCAP)"),
 ("  while(i < L){ size_t j = i; if(is_letter((unsigned char)s[i])){ while(j < L && j - i < sizeof buf - 1 && is_letter((unsigned char)s[j])) j++; } else j = i + u8len((unsigned char)s[i]); if(j > L) j = L;\n    size_t m = j - i; memcpy(buf, s + i, m); buf[m] = 0; if(!label_gate(b, buf)){ label_new(b, buf); born++; } i = j; }",
  "  while(i < L){ size_t j = i; if(letter_len((const unsigned char*)s + i, L - i)){ int k; while(j < L && j - i < sizeof buf - 8 && (k = letter_len((const unsigned char*)s + j, L - j))) j += k; } else j = i + u8len((unsigned char)s[i]); if(j > L) j = L;\n    size_t m = j - i; memcpy(buf, s + i, m); buf[m] = 0; if(!label_gate(b, buf)){ label_new(b, buf); born++; } i = j; }"),
]
for old, new in loops:
    assert c.count(old) == 1, old[:80]
    c = c.replace(old, new, 1)
open('nk.c', 'w').write(c); print('nk.c: letter_len and the four cut loops patched')
