#cython: wraparound=False
#cython: boundscheck=False
#cython: nonecheck=False


import numpy as np
from scipy.signal import fftconvolve
cimport numpy as np
cimport cython
from cython cimport floating

DTYPE = np.int
ctypedef np.int_t DTYPE_t

__all__ = ["_combine_element_abundances", "_combine_array_abundances"]


def _combine_element_abundances(np.ndarray[DTYPE_t, ndim=1] nom1,
                                np.ndarray[floating, ndim=1] exact1,
                                np.ndarray[floating, ndim=1] ab1,
                                np.ndarray[DTYPE_t, ndim=1] nom2,
                                np.ndarray[floating, ndim=1] exact2,
                                np.ndarray[floating, ndim=1] ab2,
                                max_length: np.intp_t, floating min_p
                                ):
    """
    Computes de nominal mass, exact mass and abundances for two elements.
    All arrays must have the same size.

    Returns
    -------
    nominal: np.ndarray
        nominal mass of the possible combinations
    exact: np.ndarray
        exact mass of the possible combinations
    abundances: np.array
        abundances of the possible combinations
    """
    abundance = np.convolve(ab1, ab2)
    nominal = np.zeros(max_length, dtype=nom1.dtype)
    exact = np.zeros(max_length, dtype=exact1.dtype)
    cdef floating p_k
    cdef np.ndarray[floating, ndim=1] nom_k_array
    cdef np.ndarray[floating, ndim=1] exact_k_array
    for k in range(nom1.size):
        p_k = (ab1[:k + 1] * ab2[k::-1]).sum()
        if p_k > min_p:
            nom_k_array = ((ab1[:k + 1] * nom1[:k + 1] * ab2[k::-1]) +
                           (ab1[:k + 1] * nom2[k::-1] * ab2[k::-1]))
            nominal[k] = round(nom_k_array.sum() / p_k)
            exact_k_array = ((ab1[:k + 1] * exact1[:k + 1] * ab2[k::-1]) +
                             (ab1[:k + 1] * exact2[k::-1] * ab2[k::-1]))
            exact[k] = exact_k_array.sum() / p_k
    abundance = abundance[:max_length]
    abundance[abundance < min_p] = 0
    return nominal, exact, abundance


def _combine_array_abundances(np.ndarray[DTYPE_t, ndim=2] nom1,
                              np.ndarray[floating, ndim=2] exact1,
                              np.ndarray[floating, ndim=2] ab1,
                              np.ndarray[DTYPE_t, ndim=2] nom2,
                              np.ndarray[floating, ndim=2] exact2,
                              np.ndarray[floating, ndim=2] ab2,
                              length: np.intp_t, floating min_p):
    """
    Computes de nominal mass, exact mass and abundances for two elements.
    All arrays must have the same size.

    Returns
    -------
    nominal: numpy array
        nominal mass of the possible combinations
    exact: numpy array
        exact mass of the possible combinations
    abundances: numpy array
        abundances of the possible combinations
    """
    abundance = fftconvolve(ab1, ab2, axes=1)

    # abundance[np.abs(abundance) < (2 * EPS)] = 0

    cdef np.intp_t n_rows = nom1.shape[0]
    cdef np.intp_t n_cols = nom1.shape[1]
    nominal = np.zeros((n_rows, length), dtype=nom1.dtype)
    exact = np.zeros((n_rows, length), dtype=ab1.dtype)
    cdef np.ndarray[floating, ndim=1] p_k
    cdef np.ndarray[floating, ndim=2] exact_k
    cdef np.ndarray[floating, ndim=2] nom_k
    cdef np.ndarray mask
    for k in range(n_cols):
        p_k = (ab1[:, :k + 1] * ab2[:, k::-1]).sum(axis=1)
        mask = p_k > min_p
        nom_k = ((ab1[:, :k + 1] * nom1[:, :k + 1] * ab2[:, k::-1]) +
                 (ab1[:, :k + 1] * nom2[:, k::-1] * ab2[:, k::-1]))
        nominal[mask, k] = np.round(nom_k[mask].sum(axis=1) / p_k[mask])
        exact_k = ((ab1[:, :k + 1] * exact1[:, :k + 1] * ab2[:, k::-1]) +
                   (ab1[:, :k + 1] * exact2[:, k::-1] * ab2[:, k::-1]))
        exact[mask, k] = exact_k[mask].sum(axis=1) / p_k[mask]
    abundance = abundance[:, :length]
    abundance[abundance < min_p] = 0
    return nominal, exact, abundance