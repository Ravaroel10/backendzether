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
    3: r"""
\zeta(3) = \frac{2\pi^{2}}{7}\left(\ln \pi - \frac{1}{2} - \sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)
""",

    5: r"""
\zeta(5) = \frac{6\pi^{2}}{31}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{4} - 2\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)
""",

    7: r"""
\zeta(7) = \frac{10\pi^{2}}{127}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{6} - 3\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)
""",

    9: r"""
\zeta(9) = \frac{14\pi^{2}}{511}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{8} - 4\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)
""",

    11: r"""
\zeta(11) = \frac{18\pi^{2}}{2047}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{10} - 5\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right)
""",

    13: r"""
\zeta(13) = \frac{22\pi^{2}}{8191}\left(\zeta(11) - \frac{\pi^{2}}{9}\left(\zeta(9) - \frac{\pi^{2}}{9}\left(\zeta(7) - \frac{\pi^{2}}{9}\left(\zeta(5) - \frac{\pi^{2}}{9}\left(\zeta(3) - \frac{\pi^{2}}{9}\left(\ln \pi - \frac{1}{12} - 6\sum_{k=1}^{\infty} \frac{\zeta(2k)}{k(k+1)2^{2k}}\right)\right)\right)\right)\right)\right)
""",

    15: r"""
\zeta(15) = 
\frac{26\pi^{2}}{32767}\Big(
  \zeta(13)
  - \frac{\pi^{2}}{9}\Big(
      \zeta(11)
      - \frac{\pi^{2}}{9}\Big(
          \zeta(9)
          - \frac{\pi^{2}}{9}\Big(
              \zeta(7)
              - \frac{\pi^{2}}{9}\Big(
                  \zeta(5)
                  - \frac{\pi^{2}}{9}\Big(
                      \zeta(3)
                      - \frac{\pi^{2}}{9}\Big(
                          \ln \pi - \frac{1}{14}
                          - 7\sum_{k=1}^{\infty}
                            \frac{\zeta(2k)}{k(k+1)2^{2k}}
                      \Big)
                  \Big)
              \Big)
          \Big)
      \Big)
  \Big)
\Big)
""",


    17: r"""
\zeta(17) =
\frac{30\pi^{2}}{131071}\Big(
  \zeta(15)
  - \frac{\pi^{2}}{9}\Big(
      \zeta(13)
      - \frac{\pi^{2}}{9}\Big(
          \zeta(11)
          - \frac{\pi^{2}}{9}\Big(
              \zeta(9)
              - \frac{\pi^{2}}{9}\Big(
                  \zeta(7)
                  - \frac{\pi^{2}}{9}\Big(
                      \zeta(5)
                      - \frac{\pi^{2}}{9}\Big(
                          \zeta(3)
                          - \frac{\pi^{2}}{9}\Big(
                              \ln \pi - \frac{1}{16}
                              - 8\sum_{k=1}^{\infty}
                                \frac{\zeta(2k)}{k(k+1)2^{2k}}
                          \Big)
                      \Big)
                  \Big)
              \Big)
          \Big)
      \Big)
  \Big)
\Big)
""",


    19: r"""
\zeta(19) =
\frac{34\pi^{2}}{524287}\Big(
  \zeta(17)
  - \frac{\pi^{2}}{9}\Big(
      \zeta(15)
      - \frac{\pi^{2}}{9}\Big(
          \zeta(13)
          - \frac{\pi^{2}}{9}\Big(
              \zeta(11)
              - \frac{\pi^{2}}{9}\Big(
                  \zeta(9)
                  - \frac{\pi^{2}}{9}\Big(
                      \zeta(7)
                      - \frac{\pi^{2}}{9}\Big(
                          \zeta(5)
                          - \frac{\pi^{2}}{9}\Big(
                              \zeta(3)
                              - \frac{\pi^{2}}{9}\Big(
                                  \ln \pi - \frac{1}{18}
                                  - 9\sum_{k=1}^{\infty}
                                    \frac{\zeta(2k)}{k(k+1)2^{2k}}
                              \Big)
                          \Big)
                      \Big)
                  \Big)
              \Big)
          \Big)
      \Big)
  \Big)
\Big)
"""
}



def generate_symbolic_template(n: int) -> str:
    """
    Create a LaTeX template for the odd zeta reconstruction up to n.
    This produces a structurally-correct LaTeX expression using placeholders
    for polynomial coefficients when an explicit closed form is not provided.
    """
    if n % 2 == 0 or n < 3:
        return r"Invalid: use odd n >= 3"

    
    if n in special_cases:
        return special_cases[n]

    l = (n - 1) // 2

    
    poly_terms = []
    
    for j in range(0, l):
        power_pi = 2 * (l - j)
        lower_zeta_idx = 2 * j + 1 
        if lower_zeta_idx == 1:

            poly_terms.append(rf"\alpha_{{{j}}}\pi^{{{power_pi}}}")
        else:
            poly_terms.append(rf"\alpha_{{{j}}}\pi^{{{power_pi}}}\zeta({lower_zeta_idx})")

    poly_str = " + ".join(poly_terms) if poly_terms else r"\text{(polynomial in }\pi\text{)}"

 
    summation = rf"\tfrac{{1}}{{2}}\sum_{{k=1}}^{{\infty}} \frac{{\zeta(2k)}}{{k(k+{l})2^{{2k}}}}"

    template = rf"\zeta({n}) = {poly_str} - {summation}"
    return template


for n in range(3, 40, 2):
    if n not in special_cases:
        special_cases[n] = generate_symbolic_template(n)


@app.get("/symbolic")
def get_symbolic(n: int = Query(..., description="odd n >= 3, up to 39")):
    if n % 2 == 0 or n < 3:
        return {"error": "Use odd n >= 3"}
    if n > 39:
        return {"warning": "Templates generated up to 39 only", "n": n}

    return {"n": n, "symbolic": special_cases.get(n, generate_symbolic_template(n))}


@app.get("/calculate")
def calculate(n: int = Query(..., description="odd n >= 3"), limit: int = 1000):
    if n % 2 == 0 or n < 3:
        return {"error": "Gunakan hanya n ganjil >= 3"}

    partial_sums = []
    total = mp.mpf('0')
    for k in range(1, limit + 1):
        total += mp.power(k, -n)
        partial_sums.append({"term": k, "partialSum": float(total)})  

    true_val = mp.zeta(n)

    return {
        "n": n,
        "series_value": str(true_val),
        "series_value_float": float(true_val),
        "recursion": special_cases.get(n, generate_symbolic_template(n)),
        "convergence_data": partial_sums  # ✅ sekarang cocok buat Recharts
    }
