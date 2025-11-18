from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import mpmath as mp
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mp.mp.dps = 80  # presisi tinggi

# ---------------------------------------
# Manual explicit special_cases (keep these)
# (I keep your original explicit ones up to 19)
# ---------------------------------------
special_cases: Dict[int, str] = {
     3:\quad 
\zeta(3) &= \frac{2\pi^{2}}{7}\left(\ln \pi - \frac{1}{2} - \sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right), \\[1em]
5:\quad 
\zeta(5) &= \frac{6\pi^{2}}{31}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{4} - 2\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right), \\[1em]
7:\quad 
\zeta(7) &= \frac{10\pi^{2}}{127}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{6} - 3\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right), \\[1em]
9:\quad 
\zeta(9) &= \frac{14\pi^{2}}{511}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{8} - 4\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right), \\[1em]
11:\quad 
\zeta(11) &= \frac{18\pi^{2}}{2047}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{10} - 5\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right), \\[1em]
13:\quad 
\zeta(13) &= \frac{22\pi^{2}}{8191}\left(\zeta(11) - \frac{\pi^{2}}{9}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{12} - 6\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right)\right), \\[1em]
15:\quad 
\zeta(15) &= \frac{26\pi^{2}}{32767}\left(\zeta(13) - \frac{\pi^{2}}{9}\left(\zeta(11) - \frac{\pi^{2}}{9}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{14} - 7\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right)\right)\right), \\[1em]
17:\quad 
\zeta(17) &= \frac{30\pi^{2}}{131071}\left(\zeta(15) - \frac{\pi^{2}}{9}\left(\zeta(13) - \frac{\pi^{2}}{9}\left(\zeta(11) - \frac{\pi^{2}}{9}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{16} - 8\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right)\right)\right)\right), \\[1em]
19:\quad 
\zeta(19) &= \frac{34\pi^{2}}{524287}\left(\zeta(17) - \frac{\pi^{2}}{9}\left(\zeta(15) - \frac{\pi^{2}}{9}\left(\zeta(13) - \frac{\pi^{2}}{9}\left(\zeta(11) - \frac{\pi^{2}}{9}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{18} - 9\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right)\right)\right)\right)\right).
}

# ---------------------------------------
# Programmatic template generator up to n=39
# ---------------------------------------
def generate_symbolic_template(n: int) -> str:
    """
    Create a LaTeX template for the odd zeta reconstruction up to n.
    This produces a structurally-correct LaTeX expression using placeholders
    for polynomial coefficients when an explicit closed form is not provided.
    """
    if n % 2 == 0 or n < 3:
        return r"Invalid: use odd n >= 3"

    # If we already have an explicit formula, return it
    if n in special_cases:
        return special_cases[n]

    l = (n - 1) // 2

    # Build polynomial placeholders: a_0 π^{2l} + a_1 π^{2(l-1)} ζ(3) + ...
    # We'll create terms down to ζ(3) (if applicable). Use symbolic coefficients α_j.
    poly_terms = []
    # number of lower odd zetas included = l-1 (for n>=5)
    # We'll produce terms for j from 0..(l-1): coefficient * π^{2*(l-j)} * ζ(2*j+1?) pattern is illustrative
    for j in range(0, l):
        power_pi = 2 * (l - j)
        lower_zeta_idx = 2 * j + 1  # 1,3,5,... but j=0 gives zeta(1) which is ill-defined; skip zeta(1)
        if lower_zeta_idx == 1:
            # treat constant-only term
            poly_terms.append(rf"\alpha_{{{j}}}\pi^{{{power_pi}}}")
        else:
            poly_terms.append(rf"\alpha_{{{j}}}\pi^{{{power_pi}}}\zeta({lower_zeta_idx})")

    poly_str = " + ".join(poly_terms) if poly_terms else r"\text{(polynomial in }\pi\text{)}"

    # summation tail
    summation = rf"\tfrac{{1}}{{2}}\sum_{{k=1}}^{{\infty}} \frac{{\zeta(2k)}}{{k(k+{l})2^{{2k}}}}"

    template = rf"\zeta({n}) = {poly_str} - {summation}"
    return template

# pre-populate templates up to 39 (do not override explicit ones)
for n in range(3, 40, 2):
    if n not in special_cases:
        special_cases[n] = generate_symbolic_template(n)

# ---------------------------------------
# Endpoint: /symbolic?n=...  (returns LaTeX template)
# ---------------------------------------
@app.get("/symbolic")
def get_symbolic(n: int = Query(..., description="odd n >= 3, up to 39")):
    if n % 2 == 0 or n < 3:
        return {"error": "Use odd n >= 3"}
    if n > 39:
        return {"warning": "Templates generated up to 39 only", "n": n}

    return {"n": n, "symbolic": special_cases.get(n, generate_symbolic_template(n))}

# ---------------------------------------
# Endpoint: /calculate?n=...&limit=...
# ---------------------------------------
@app.get("/calculate")
def calculate(n: int = Query(..., description="odd n >= 3"), limit: int = 1000):
    if n % 2 == 0 or n < 3:
        return {"error": "Gunakan hanya n ganjil >= 3"}

    partial_sums = []
    total = mp.mpf('0')
    for k in range(1, limit + 1):
        total += mp.power(k, -n)
        partial_sums.append({"term": k, "partialSum": float(total)})  # ✅ ubah jadi dict

    true_val = mp.zeta(n)

    return {
        "n": n,
        "series_value": str(true_val),
        "series_value_float": float(true_val),
        "recursion": special_cases.get(n, generate_symbolic_template(n)),
        "convergence_data": partial_sums  # ✅ sekarang cocok buat Recharts
    }
