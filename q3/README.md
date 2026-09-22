# q = 3 scripts

Standard library only. Findings in `../NOTES_Q3.md`.

| script | establishes |
|---|---|
| `01_tools_and_qr.py` | what dies and survives at `q = 3`; Lemma QR, Lemma 3MOD12 (general `N`), Lemma NO2CYCLE, each with verification |
| `02_three_adic_balance.py` | exact component `v₃` formulas; the 3-adic balance identity for `3 \| N`; the `11 mod 12` parity constraint; why the abundancy floor is vacuous at `q = 3` |
| `03_sharp.py` | the sharp power-residue form of the production condition; the tournament theorem; prediction test against 336 literature pairs |
| `04_qr_integrity.py` | the power-residue condition as an integrity check on factor-tree data: 882 claims in `3p2.txt`, both corrupt ones caught |
