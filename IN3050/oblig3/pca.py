from numpy.linalg.linalg import EigResult
import numpy as np


def center_data(X: np.ndarray) -> np.ndarray:
    return X - X.mean(axis=0)


def compute_covariance_matrix(X: np.ndarray) -> np.ndarray:
    centered = center_data(X)
    return (centered.T @ centered) / (X.shape[0] - 1)


def compute_eigenvalue_eigenvectors(X: np.ndarray) -> EigResult:
    eig = np.linalg.eig(X)
    return EigResult(eig.eigenvalues.real, eig.eigenvectors.real)


def sort_eigenvalue_eigenvectors(eigval: np.ndarray, eigvec: np.ndarray) -> EigResult:
    sorted_indicies = np.argsort(eigval)[::-1]
    return EigResult(eigval[sorted_indicies], eigvec[:, sorted_indicies])
