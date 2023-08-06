#cython: wraparound=False
#cython: boundscheck=False
#cython: nonecheck=False

import numpy as np
cimport numpy as np
cimport cython
from cython cimport floating

DTYPE = np.int
ctypedef np.int_t DTYPE_t

__all__ = ["_find_valid_defect_index", "_make_combinations"]


def _make_flat_index(np.ndarray[DTYPE_t, ndim=2] pos_ri_slices):
    """
    Auxiliary function to find_valid_defect regions. Finds valid indices to place
    pos_ri_slices slices.
    """

    res = np.zeros_like(pos_ri_slices)
    cdef np.ndarray[DTYPE_t, ndim=1] tmp_diff
    tmp_diff = pos_ri_slices[1, :] - pos_ri_slices[0, :]
    res[1, :] = tmp_diff.cumsum()
    res[0, :] = res[1, :] - tmp_diff
    return res


def _find_valid_defect_index(floating min_dp, floating max_dp,
                             floating min_dn, floating max_dn,
                             floating d, np.intp_t r, floating tol,
                             np.ndarray[floating, ndim=2] pos_r_to_d,
                             np.ndarray[DTYPE_t, ndim=2] pos_r_to_i,
                             np.ndarray[floating, ndim=2] neg_r_to_d):
    """
    Auxiliary function to guess_formula. regions with valid remainder and mass
    defects.

    Returns
    -------
    pos_coeff_index: numpy.array
        An array where each element is a index to a valid coefficient row in
        `pos`.
    neg_ri_slices: numpy.array
        An array with two columns and the same number of rows that
        pos_ri_slices.size. Each row has index to a slice with valid
        coefficients in neg.ri_array.

    """
    # max and min possible defects are analized relative to d, the same is done
    # with r
    cdef floating tmp_max_dp = max_dp
    max_dp = d - min_dp
    min_dp = d - tmp_max_dp

    cdef np.ndarray[DTYPE_t, ndim=1] rel_neg_r = r - np.arange(12)
    rel_neg_r[rel_neg_r < 0] += 12

    # find valid positive slices in pos_ri array
    pos_ri_slices = np.zeros((2, 12), dtype=pos_r_to_i.dtype)
    cdef np.ndarray[floating, ndim=2] rel_pos_r_to_d = d - pos_r_to_d
    # print(min_dp, max_dp)
    # print(rel_pos_r_to_d[0])

    cdef np.intp_t rn
    cdef np.intp_t rp

    for rp in range(rel_neg_r.size):
        # rn = rel_neg_r[rp]
        pos_ri_slices[:, rp] = \
            np.searchsorted(rel_pos_r_to_d[rp, :], (min_dp, max_dp))

    # convert slices to an array of indices
    pos_ri_slices[1, :] += 1
    pos_ri_index = _make_flat_index(pos_ri_slices)
    # print(pos_ri_slices)
    cdef np.intp_t pos_ri_size = (pos_ri_slices[1, :] - pos_ri_slices[0, :]).sum()


    # find matching negative slices in ri and find positive coefficients
    # indices
    pos_coeff_index = np.zeros(pos_ri_size, dtype=int)
    neg_ri_slices = np.zeros((pos_ri_size, 2), dtype=int)
    neg_r = np.zeros(pos_ri_size, dtype=int)

    cdef np.intp_t ls
    cdef np.intp_t le
    cdef np.intp_t rs
    cdef np.intp_t re

    for rp in range(rel_neg_r.size):
        # left start, left end, right start, right end
        rn = rel_neg_r[rp]
        ls = pos_ri_index[0, rp] 
        le = pos_ri_index[1, rp]
        rs = pos_ri_slices[0, rp]
        re = pos_ri_slices[1, rp]

        pos_coeff_index[ls:le] = pos_r_to_i[rp, rs:re]
        neg_ri_slices[ls:le, 0] = np.searchsorted(neg_r_to_d[rn, :],
                                         rel_pos_r_to_d[rp, rs:re] - tol)
        neg_ri_slices[ls:le, 1] = np.searchsorted(neg_r_to_d[rn, :],
                                         rel_pos_r_to_d[rp, rs:re] + tol)
        neg_r[ls:le] = rn

    # remove elements with empty negative regions.
    neg_valid_slices = (neg_ri_slices[:, 1] - neg_ri_slices[:, 0]) > 0
    pos_coeff_index = pos_coeff_index[neg_valid_slices]
    neg_ri_slices = neg_ri_slices[neg_valid_slices, :]
    neg_r = neg_r[neg_valid_slices]
    return pos_coeff_index, neg_ri_slices, neg_r


def _make_combinations(np.ndarray[DTYPE_t, ndim=1] pos_nominal_r,
                       np.ndarray[DTYPE_t, ndim=1] pos_nominal_q,
                       np.ndarray[DTYPE_t, ndim=1] neg_nominal_q,
                       np.ndarray[DTYPE_t, ndim=2] neg_r_to_index,
                       np.ndarray[DTYPE_t, ndim=1] pos_coeff_index,
                       np.ndarray[DTYPE_t, ndim=2] neg_coeff_slices,
                       np.ndarray[DTYPE_t, ndim=1] neg_r,
                       int r, int q):
    """
    Auxiliary function to guess_formula. converts results to arrays where each
    element in pos_coeff_index has a matching element in neg_coeff_index.

    Returns
    -------
    pos_index: np.array:
        An array where each element is a index to a valid coefficient row in
        `pos`.
    neg_index_flat: np.array:
        An array with the same size as pos_index and where each element is a
        index to a valid coefficient row in `neg`.
    pos_q: np.array.
        quotient of positive nominal mass associated to pos_coeff_index,
        corrected by q and pos_r.
    qn: np.array.
        quotient of negative nominal mass associated to neg_coeff_slices.
    """

    cdef np.ndarray[DTYPE_t, ndim=1] pos_r = r - pos_nominal_r[pos_coeff_index]
    cdef np.ndarray[DTYPE_t, ndim=1] pos_q = q - pos_nominal_q[pos_coeff_index]
    cdef np.ndarray rp_mask = pos_r < 0
    
    # correct remainders and quotient values
    pos_q[rp_mask] -= 1
    pos_r[rp_mask] += 12

    # remove invalid roi (pos_q must be >= 0)
    neg_valid_slices = pos_q >= 0
    pos_q = pos_q[neg_valid_slices]
    pos_r = pos_r[neg_valid_slices]
    pos_coeff_index = pos_coeff_index[neg_valid_slices]
    neg_coeff_slices = neg_coeff_slices[neg_valid_slices, :]
    neg_r = neg_r[neg_valid_slices]

    # get the number of pairs of negative and positive coefficients
    cdef np.ndarray[DTYPE_t, ndim=1] neg_ri_slices_diff
    neg_ri_slices_diff = neg_coeff_slices[:, 1] - neg_coeff_slices[:, 0]
    cdef int flat_size = neg_ri_slices_diff.sum()


    neg_index_flat = np.zeros(flat_size, dtype=neg_coeff_slices.dtype)
    pos_index_flat = np.repeat(pos_coeff_index, neg_ri_slices_diff)
    pos_q_flat = np.repeat(pos_q, neg_ri_slices_diff)
    cdef np.intp_t counter = 0
    cdef np.intp_t neg_ri_slices_size = pos_coeff_index.size
    cdef np.intp_t start = 0
    cdef np.intp_t end = 0
    cdef np.intp_t size = 0
    cdef np.intp_t rn = 0
    for k in range(neg_ri_slices_size):
        start = neg_coeff_slices[k, 0]
        end = neg_coeff_slices[k, 1]
        rn = neg_r[k]
        size = end - start
        neg_index_flat[counter:counter + size] = neg_r_to_index[rn, start:end]
        counter += size

    cdef np.ndarray[DTYPE_t, ndim=1] qn = neg_nominal_q[neg_index_flat]
    return pos_index_flat, neg_index_flat, pos_q_flat, qn
