# Source verification

Sources below were checked on 5 November 2026. A verified source statement is distinguished from a literature-search inference. This record does not imply that external proofs were formally verified or computationally reproduced.

## Originating conjecture

H. Abbaszadehpeivasti and M. Zamani, *On the convergence rate of the Douglas–Rachford splitting algorithm*, [arXiv:2509.06676v2](https://arxiv.org/html/2509.06676v2), dated 13 September 2025. The [canonical version history](https://arxiv.org/abs/2509.06676) listed v2 as the latest version when checked.

Conjecture 3.5 assumes a convex subdifferential A, a beta-cocoercive B, stepsize gamma in (0,beta), and relaxation lambda in (0,2). Its squared-residual bound and indexing match the conjecture stated in this paper. The separate objective-value conjectures in Section 5 are not refuted here.

## Sharp proximal-point constant

G. Gu and J. Yang, *Optimal nonergodic sublinear convergence rate of proximal point algorithm for maximal monotone inclusion problems*, [arXiv:1904.05495v2](https://arxiv.org/pdf/1904.05495v2), dated 12 July 2019.

Equation (2.6) defines the residual after N proximal updates from the initial point. Proposition 4.1 and equation (4.4), PDF page 7, give the upper constant N^N/(N+1)^(N+1); Section 5 supplies matching two-dimensional examples. In this paper's scalar-policy theorem, their N is our m. The sharp firmly nonexpansive upper bound is inherited from this source, not claimed as a new result.

## Rotation-product antecedent

D. Sarkar and V. Aggarwal, *Non-Expansive Two-Time-Scale Stochastic Approximation: A Fixed-Schedule One-Quarter Barrier and Bias-Corrected Acceleration*, [arXiv:2607.13414v1](https://arxiv.org/html/2607.13414v1), dated 15 July 2026.

Appendix A, proof of Theorem 4.1, derives the planar rotation product and its final-residual expression for prescribed Krasnoselskii–Mann schedules. With their step parameter equal to lambda_j/(2c) and their squared chordal distance equal to 4c²q, this becomes the product used here, with the corresponding change of residual normalisation. The adaptive-policy penalty identity in this paper is a refinement of that algebra combined with the Gu–Yang upper bound.

## Unresolved full-text comparison

S. He, Q.-L. Dong, H. Tian and X.-H. Li, *On the optimal relaxation parameters of Krasnosel'ski–Mann iteration*, **Optimization** 70(9) (2021), 1959–1986; published online 21 May 2020. [Publisher record and abstract](https://www.tandfonline.com/doi/abs/10.1080/02331934.2020.1767101).

The abstract discusses optimal parameter sequences depending on fixed points, computable approximations, and splitting applications. Full text could not be retrieved: the publisher PDF returned HTTP 403, and no repository copy was located through the checked metadata and searches. Its precise overlap with the adaptive minimax formulation remains unknown. The abstract alone cannot establish either equivalence or non-overlap.

## Contraction polynomial inequality

M. Hartz, *On von Neumann's inequality on the polydisc*, **Mathematische Annalen** 391 (2025), 5235–5264; published online 2 December 2024. [Publisher full text](https://link.springer.com/article/10.1007/s00208-024-03040-2).

Section 2, Proposition 2.3 and its complete proof were inspected on 5 November 2026. It gives constant one for a contraction and polynomial coefficients doubly commuting with it. Scalar multiples of the identity meet that condition; normality is unnecessary. The proof uses a positive Poisson-type kernel and a unital completely positive integral map, with contraction-boundary cases obtained by scaling and continuity. Only this passage and its surrounding definitions were audited, not the entire article.

Application check: for a real matrix R, its complexification satisfies ||R(x+iy)||²=||Rx||²+||Ry||², hence has the same Euclidean operator norm. Apply Proposition 2.3 to that contraction and the scalar polynomial obtained by substituting (1-z)/(2c) into the residual polynomial. This justifies Theorem 5 for nonnormal real matrices as well as normal ones.

## Other foundations

The paper cites Giselsson for resolvent averagedness and Contreras–Cominetti for nearby prescribed-schedule barriers. The resolvent constants are also proved directly in the manuscript. These two references were not independently reopened in this particular source-verification pass; their inclusion should not be read as an additional full-text verification claim.
