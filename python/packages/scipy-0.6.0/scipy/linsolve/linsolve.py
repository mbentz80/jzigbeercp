from scipy.sparse import isspmatrix_csc, isspmatrix_csr, isspmatrix, spdiags
import _superlu
from numpy import asarray

import umfpack
if hasattr( umfpack, 'UMFPACK_OK' ):
    isUmfpack = True
else:
    del umfpack
    isUmfpack = False
useUmfpack = True

def use_solver( **kwargs ):
    """
    Valid keyword arguments with defaults (other ignored):
      useUmfpack = True
      assumeSortedIndices = False
      
    The default sparse solver is umfpack when available. This can be changed by
    passing useUmfpack = False, which then causes the always present SuperLU
    based solver to be used.
    
    Umfpack requires a CSR/CSC matrix to have sorted column/row indices. If
    sure that the matrix fulfills this, pass assumeSortedIndices =
    True to gain some speed.
    """
    if kwargs.has_key( 'useUmfpack' ):
        globals()['useUmfpack'] = kwargs['useUmfpack']

    if isUmfpack:
        umfpack.configure( **kwargs )

def _toCS_superLU( A ):
    if hasattr(A, 'tocsc') and not isspmatrix_csr( A ):
        mat = A.tocsc()
        csc = 1
    elif hasattr(A, 'tocsr'):
        mat = A.tocsr()
        csc = 0
    else:
        raise ValueError, "matrix cannot be converted to CSC/CSR"
    return mat, csc

def _toCS_umfpack( A ):
    if isspmatrix_csr( A ) or isspmatrix_csc( A ):
        mat = A
    else:
        if hasattr(A, 'tocsc'):
            mat = A.tocsc()
        elif hasattr(A, 'tocsr'):
            mat = A.tocsr()
        else:
            raise ValueError, "matrix cannot be converted to CSC/CSR"
    return mat

def spsolve(A, b, permc_spec=2):
    if isspmatrix( b ):
        b = b.toarray()

    if b.ndim > 1:
        if max( b.shape ) == b.size:
            b = b.squeeze()
        else:
            raise ValueError, "rhs must be a vector (has shape %s)" % (b.shape,)
    
    if not hasattr(A, 'tocsr') and not hasattr(A, 'tocsc'):
        raise ValueError, "sparse matrix must be able to return CSC format--"\
              "A.tocsc()--or CSR format--A.tocsr()"
    if not hasattr(A, 'shape'):
        raise ValueError, "sparse matrix must be able to return shape" \
                " (rows, cols) = A.shape"
    M, N = A.shape
    if (M != N):
        raise ValueError, "matrix must be square (has shape %s)" % (A.shape,)
    if M != b.size:
        raise ValueError, "matrix - rhs size mismatch (%s - %s)"\
              % (A.shape, b.shape)
       
    if isUmfpack and useUmfpack:
        mat = _toCS_umfpack( A )

        if mat.dtype.char not in 'dD':
            raise ValueError, "convert matrix data to double, please, using"\
                  " .astype(), or set linsolve.useUmfpack = False"

        family = {'d' : 'di', 'D' : 'zi'}
        umf = umfpack.UmfpackContext( family[mat.dtype.char] )
        return umf.linsolve( umfpack.UMFPACK_A, mat, b,
                             autoTranspose = True )

    else:
        mat, csc = _toCS_superLU( A )
        index0 = mat.indices
        ftype, lastel, data, index1 = mat.ftype, mat.nnz, mat.data, mat.indptr
        gssv = eval('_superlu.' + ftype + 'gssv')
        b = asarray(b, dtype=data.dtype)
        return gssv(N, lastel, data, index0, index1, b, csc, permc_spec)[0]

def splu(A, permc_spec=2, diag_pivot_thresh=1.0,
         drop_tol=0.0, relax=1, panel_size=10):
    """
    A linear solver, for a sparse, square matrix A, using LU decomposition where
    L is a lower triangular matrix and U is an upper triagular matrix.

    Returns a factored_lu object. (scipy.linsolve._superlu.SciPyLUType)

    See scipy.linsolve._superlu.dgstrf for more info.
    """
    M, N = A.shape
    if (M != N):
        raise ValueError, "can only factor square matrices"

##     if isUmfpack:
##         print "UMFPACK is present - try umfpack.numeric and umfpack.solve instead!"

    csc = A.tocsc()
    gstrf = eval('_superlu.' + csc.ftype + 'gstrf')
    return gstrf(N, csc.nnz, csc.data, csc.indices, csc.indptr, permc_spec,
                 diag_pivot_thresh, drop_tol, relax, panel_size)

def factorized( A ):
    """
    Return a fuction for solving a sparse linear system, with A pre-factorized.

    Example:
      solve = factorized( A ) # Makes LU decomposition.
      x1 = solve( rhs1 ) # Uses the LU factors.
      x2 = solve( rhs2 ) # Uses again the LU factors.
    """
    if isUmfpack and useUmfpack:
        mat = _toCS_umfpack( A )

        if mat.dtype.char not in 'dD':
            raise ValueError, "convert matrix data to double, please, using"\
                  " .astype(), or set linsolve.useUmfpack = False"

        family = {'d' : 'di', 'D' : 'zi'}
        umf = umfpack.UmfpackContext( family[mat.dtype.char] )

        # Make LU decomposition.
        umf.numeric( mat )

        def solve( b ):
            return umf.solve( umfpack.UMFPACK_A, mat, b, autoTranspose = True )
            
        return solve
    else:
        return splu( A ).solve

def _testme():
    from scipy.sparse import csc_matrix
    from numpy import array
    from scipy.linsolve import spdiags, spsolve, use_solver

    print "Inverting a sparse linear system:"
    print "The sparse matrix (constructed from diagonals):"
    a = spdiags([[1, 2, 3, 4, 5], [6, 5, 8, 9, 10]], [0, 1], 5, 5)
    b = array([1, 2, 3, 4, 5])
    print "Solve: single precision complex:"
    use_solver( useUmfpack = False )
    a = a.astype('F')
    x = spsolve(a, b)
    print x
    print "Error: ", a*x-b

    print "Solve: double precision complex:"
    use_solver( useUmfpack = True )
    a = a.astype('D')
    x = spsolve(a, b)
    print x
    print "Error: ", a*x-b

    print "Solve: double precision:"
    a = a.astype('d')
    x = spsolve(a, b)
    print x
    print "Error: ", a*x-b

    print "Solve: single precision:"
    use_solver( useUmfpack = False )
    a = a.astype('f')
    x = spsolve(a, b.astype('f'))
    print x
    print "Error: ", a*x-b


if __name__ == "__main__":
    _testme()
