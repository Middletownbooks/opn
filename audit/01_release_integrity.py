#!/usr/bin/env python3
"""Check the published SHA256SUMS.txt of release C-small-2026-07 against the
tagged content, distinguishing genuine content drift from CRLF/LF normalisation."""
import hashlib, os, sys
D = sys.argv[1] if len(sys.argv) > 1 else \
    '/home/user/mantovanelli1110/opn-small-prime-closure-certificates'
exp = {}
for line in open(os.path.join(D, 'SHA256SUMS.txt')):
    line = line.rstrip('\n')
    if not line.strip():
        continue
    h, f = line.split(None, 1)
    exp[f.strip()] = h.lower()
def sha(b):
    return hashlib.sha256(b).hexdigest()
drift, crlf, lf = [], [], []
for f, e in sorted(exp.items()):
    b = open(os.path.join(D, f), 'rb').read()
    variants = {
        'LF': b,
        'CRLF': b.replace(b'\n', b'\r\n'),
        'LF_nofinal': b.rstrip(b'\n'),
        'CRLF_nofinal': b.replace(b'\n', b'\r\n').rstrip(b'\r\n'),
        'CRLF_BOM': b'\xef\xbb\xbf' + b.replace(b'\n', b'\r\n'),
        'LF_BOM': b'\xef\xbb\xbf' + b,
    }
    hit = [k for k, v in variants.items() if sha(v) == e]
    if not hit:
        drift.append(f)
    elif 'CRLF' in hit[0]:
        crlf.append(f)
    else:
        lf.append(f)
    print(f"{f:55s} {'MATCH:' + ','.join(hit) if hit else 'CONTENT DRIFT'}")
print()
print(f"matched as committed (LF)      : {len(lf)}")
print(f"matched only after CRLF-ifying : {len(crlf)}  -> {crlf}")
print(f"no variant matches (real drift) : {len(drift)} -> {drift}")
