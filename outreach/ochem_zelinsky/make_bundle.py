#!/usr/bin/env python3
"""
Build ochem_zelinsky_bundle.zip, the attachment for the note to the authors.

Every file in the zip is a byte-for-byte copy of a file in this repository, so an
auditor can confirm that the attachment is exactly what was checked.  The script
prints a SHA-256 of each file.  The authors' own files (loopless.cpp,
checkfacts.txt) are NOT included: they have them.

Run:  python3 outreach/ochem_zelinsky/make_bundle.py
"""
import os, zipfile, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
R = lambda *p: os.path.join(ROOT, "restrained", *p)
FILES = [   # (source in repo, name in zip)
    (os.path.join(HERE, "BUNDLE_README.md"), "README.md"),
    (R("13_sieve.c"), "13_sieve.c"),
    (R("12_algorithm1_reference.py"), "12_algorithm1_reference.py"),
    (R("14_bound_from_run.py"), "14_bound_from_run.py"),
    (R("15_tree_pilot.py"), "15_tree_pilot.py"),
    (R("05_loopless_overflow.py"), "05_loopless_overflow.py"),
    (R("10_section4_reconcile.py"), "10_section4_reconcile.py"),
    (R("11_wrap_signature.py"), "11_wrap_signature.py"),
    (R("loopless_build", "gmp.h"), "loopless_build/gmp.h"),
    (R("runs", "13_z_Q2e35_checkpoints.txt"), "results/13_z_Q2e35_checkpoints.txt"),
    (R("runs", "14_bound_z_Q2e35.txt"), "results/14_bound_z_Q2e35.txt"),
    (R("runs", "13_1e12_Q2e35_checkpoints.txt"), "results/13_1e12_Q2e35_checkpoints.txt"),
    (R("runs", "14_bound_1e12_Q2e35.txt"), "results/14_bound_1e12_Q2e35.txt"),
    (R("runs", "13_1e10_exact_checkpoints.txt"), "results/13_1e10_exact_checkpoints.txt"),
    (R("runs", "loopless_released_1h.txt"), "results/loopless_released_1h.txt"),
    (R("runs", "15_tree_full_range.txt"), "results/15_tree_full_range.txt"),
]
out = os.path.join(HERE, "ochem_zelinsky_bundle.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for src, name in FILES:
        data = open(src, "rb").read()
        zi = zipfile.ZipInfo("ochem_zelinsky_bundle/" + name, date_time=(2026, 9, 28, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, data)
        print(f"{hashlib.sha256(data).hexdigest()[:16]}  {name}")
print(f"wrote {os.path.relpath(out, ROOT)} ({os.path.getsize(out):,} bytes)")
