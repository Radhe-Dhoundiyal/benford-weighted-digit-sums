# Theorem specification and audit status

Statuses are assigned only after the audit run documented in `outputs/reports/FINAL_VERIFICATION_REPORT.md`.

## A. Classical inputs

| Input | Status | Scope |
|---|---|---|
| Uniform theta induces logarithmic mantissa measure | EXTERNAL-INPUT | Elementary change of variables |
| Weyl equidistribution for irrational rotations | EXTERNAL-INPUT | Used only for fixed Riemann-integrable digit observables |
| Multiplicative independence of integers a,b iff log_b(a) is irrational | EXTERNAL-INPUT | Elementary unique factorization argument |
| Stirling expansion for log Gamma | EXTERNAL-INPUT | DLMF 5.11.1 and the positive-real remainder theorem in DLMF 5.11(ii) |

Ordinary discrepancy means the supremum over all half-open intervals `[u,v)`; star discrepancy uses `[0,v)`. For a finite atomic empirical measure, one-sided endpoint values matter.

## B. Candidate new analytic results

| Claim | Statement (notation as in audit prompt) | Status |
|---|---|---|
| A1 | Exact raw logarithmic digit probability | PASS |
| A2 | Log-Gamma digit probability | PASS |
| A3 | Expected first digit | PASS |
| A4 | Closed log-Gamma expected later digit | PASS |
| A5 | Exact finite cumulative bias | PASS |
| A6 | Finite expected digit-sum/factorial identity | PASS |
| A7 | `c_b = b/2 - (b-1)log_b(2*pi)/2` | PASS |
| A8 | Deep-digit expansion with stated first coefficient | PASS |
| A9 | Expected-digit expansion with stated first coefficient | PASS |
| A10 | Two-term tail expansion with explicit non-strict remainder bound | PASS |

### A10 analytic closure

For (x>0), write Stirling's expansion in the form

\[
\log\Gamma(x)=\left(x-\frac12\right)\log x-x+\frac12\log(2\pi)
+\frac{1}{12x}-\frac{1}{360x^3}+\rho(x),
\]

where the classical positive-real Stirling remainder theorem gives

\[
0<\rho(x)\le \frac{1}{1260x^5}.
\]

This is the first-neglected-term result in NIST DLMF 5.11(ii), applied to the Stirling series in equation 5.11.1. Define

\[
R(x)=\frac{1}{12x}-\frac{1}{360x^3}+\rho(x).
\]

The already independently verified exact finite-bias identity reduces, after cancellation of the elementary Stirling terms, to

\[
c_b-c_{b,L}=\frac{bR(x)-R(bx)}{\log b},\qquad x=b^{L-1}.
\]

Substitution gives

\[
bR(x)-R(bx)
=\frac{b-b^{-1}}{12x}
-\frac{b-b^{-3}}{360x^3}
+b\rho(x)-\rho(bx).
\]

Because (x=b^{L-1}),

\[
\frac{b-b^{-1}}{x}=(b^2-1)b^{-L},\qquad
\frac{b-b^{-3}}{x^3}=(b^4-1)b^{-3L}.
\]

Therefore

\[
c_b-c_{b,L}=
\frac{b^2-1}{12\log b}b^{-L}
-\frac{b^4-1}{360\log b}b^{-3L}
+\epsilon_{b,L},
\]

with

\[
\epsilon_{b,L}=\frac{b\rho(x)-\rho(bx)}{\log b}.
\]

Since (b\ge2), (log b>0). The triangle inequality and the two remainder bounds give

\[
\begin{aligned}
|\epsilon_{b,L}|
&\le \frac{b\rho(x)+\rho(bx)}{\log b}\\
&\le \frac{1}{1260\log b}\left(\frac{b}{x^5}+\frac{1}{b^5x^5}\right)\\
&=\frac{b^6+1}{1260\log b}\,b^{-5L}.
\end{aligned}
\]

This holds for every integer (b\ge2) and (L\ge1), since then (x=b^{L-1}>0). The only change from the previous candidate A10 is that the remainder bound is stated with the rigorously supported non-strict relation `<=` instead of strict `<`. The 220-digit numerical stress tests remain supplementary checks, not the proof.

Reference: NIST Digital Library of Mathematical Functions, [5.11.1 and 5.11(ii), Stirling series and positive-real error bound](https://dlmf.nist.gov/5.11).

## C. Candidate deterministic results

| Claim | Statement | Status |
|---|---|---|
| D1 | Exactly `(b-1)b^(j-2)` disjoint components | PASS |
| D2 | Digit-frequency error at most `K_j D_N`, with explicit short-length handling | PASS |
| D3 | Leading-window observable identity when `L_n>=J` | PASS |
| D4 | Integral of `G_J` equals `J mu_b-c_{b,J}` | PASS |
| D5 | Stated finite leading-bias bound | PASS |
| D6 | Conditional second-order deterministic asymptotic | PASS |

## D. External theoretical inputs

The fixed-position transfer to deterministic powers uses Weyl's theorem. D6 is conditional on the displayed discrepancy hypotheses; this audit does not claim those hypotheses for every multiplicatively independent pair or every chosen `J(N)`.

## E. Empirical or heuristic claims not proved here

Prime-dependent fluctuation scaling, mixing, independence, CLTs, entropy/randomness interpretations, and unconditional rates for `D_N(log_b a)` are outside the proved package. The optional Fourier magnitude heuristic was not promoted to a rigorous result.
