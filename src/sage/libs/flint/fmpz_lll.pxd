# distutils: libraries = flint
# distutils: depends = flint/fmpz_lll.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# From the commit 3e2c3a3e091106a25ca9c6fba28e02f2cbcd654a
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    void fmpz_lll_context_init_default(fmpz_lll_t fl) noexcept
    void fmpz_lll_context_init(fmpz_lll_t fl, double delta, double eta, rep_type rt, gram_type gt) noexcept
    void fmpz_lll_randtest(fmpz_lll_t fl, flint_rand_t state) noexcept
    double fmpz_lll_heuristic_dot(const double * vec1, const double * vec2, slong len2, const fmpz_mat_t B, slong k, slong j, slong exp_adj) noexcept
    int fmpz_lll_check_babai(int kappa, fmpz_mat_t B, fmpz_mat_t U, d_mat_t mu, d_mat_t r, double * s, d_mat_t appB, int * expo, fmpz_gram_t A, int a, int zeros, int kappamax, int n, const fmpz_lll_t fl) noexcept
    int fmpz_lll_check_babai_heuristic_d(int kappa, fmpz_mat_t B, fmpz_mat_t U, d_mat_t mu, d_mat_t r, double * s, d_mat_t appB, int * expo, fmpz_gram_t A, int a, int zeros, int kappamax, int n, const fmpz_lll_t fl) noexcept
    int fmpz_lll_check_babai_heuristic(int kappa, fmpz_mat_t B, fmpz_mat_t U, mpf_mat_t mu, mpf_mat_t r, mpf * s, mpf_mat_t appB, fmpz_gram_t A, int a, int zeros, int kappamax, int n, mpf_t tmp, mpf_t rtmp, flint_bitcnt_t prec, const fmpz_lll_t fl) noexcept
    int fmpz_lll_advance_check_babai(int cur_kappa, int kappa, fmpz_mat_t B, fmpz_mat_t U, d_mat_t mu, d_mat_t r, double * s, d_mat_t appB, int * expo, fmpz_gram_t A, int a, int zeros, int kappamax, int n, const fmpz_lll_t fl) noexcept
    int fmpz_lll_advance_check_babai_heuristic_d(int cur_kappa, int kappa, fmpz_mat_t B, fmpz_mat_t U, d_mat_t mu, d_mat_t r, double * s, d_mat_t appB, int * expo, fmpz_gram_t A, int a, int zeros, int kappamax, int n, const fmpz_lll_t fl) noexcept
    int fmpz_lll_shift(const fmpz_mat_t B) noexcept
    int fmpz_lll_d(fmpz_mat_t B, fmpz_mat_t U, const fmpz_lll_t fl) noexcept
    int fmpz_lll_d_heuristic(fmpz_mat_t B, fmpz_mat_t U, const fmpz_lll_t fl) noexcept
    int fmpz_lll_mpf2(fmpz_mat_t B, fmpz_mat_t U, flint_bitcnt_t prec, const fmpz_lll_t fl) noexcept
    int fmpz_lll_mpf(fmpz_mat_t B, fmpz_mat_t U, const fmpz_lll_t fl) noexcept
    int fmpz_lll_wrapper(fmpz_mat_t B, fmpz_mat_t U, const fmpz_lll_t fl) noexcept
    int fmpz_lll_d_with_removal(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_d_heuristic_with_removal(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_mpf2_with_removal(fmpz_mat_t B, fmpz_mat_t U, flint_bitcnt_t prec, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_mpf_with_removal(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_wrapper_with_removal(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_d_with_removal_knapsack(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_wrapper_with_removal_knapsack(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    int fmpz_lll_with_removal_ulll(fmpz_mat_t FM, fmpz_mat_t UM, slong new_size, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
    bint fmpz_lll_is_reduced_d(const fmpz_mat_t B, const fmpz_lll_t fl) noexcept
    bint fmpz_lll_is_reduced_mpfr(const fmpz_mat_t B, const fmpz_lll_t fl, flint_bitcnt_t prec) noexcept
    bint fmpz_lll_is_reduced_d_with_removal(const fmpz_mat_t B, const fmpz_lll_t fl, const fmpz_t gs_B, int newd) noexcept
    bint fmpz_lll_is_reduced_mpfr_with_removal(const fmpz_mat_t B, const fmpz_lll_t fl, const fmpz_t gs_B, int newd, flint_bitcnt_t prec) noexcept
    bint fmpz_lll_is_reduced(const fmpz_mat_t B, const fmpz_lll_t fl, flint_bitcnt_t prec) noexcept
    bint fmpz_lll_is_reduced_with_removal(const fmpz_mat_t B, const fmpz_lll_t fl, const fmpz_t gs_B, int newd, flint_bitcnt_t prec) noexcept
    void fmpz_lll_storjohann_ulll(fmpz_mat_t FM, slong new_size, const fmpz_lll_t fl) noexcept
    void fmpz_lll(fmpz_mat_t B, fmpz_mat_t U, const fmpz_lll_t fl) noexcept
    int fmpz_lll_with_removal(fmpz_mat_t B, fmpz_mat_t U, const fmpz_t gs_B, const fmpz_lll_t fl) noexcept
