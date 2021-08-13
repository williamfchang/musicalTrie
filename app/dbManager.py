import sys
sys.path.append("../")

from trie.musicalClasses import *
from scipy.sparse import dok_matrix


# make sparse matrix
trieLinks = dok_matrix((10000, maxRange), type=np.int32)


# uhhhh links ig

# Scipy sparse matrices: https://docs.scipy.org/doc/scipy/reference/sparse.html
# Best sparse matrix for our purpose is probably Dictionary Of Keys: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.dok_matrix.html#scipy.sparse.dok_matrix
# vstack for sparse arrays (to add new rows): https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.vstack.html#scipy.sparse.vstack
# incremental construction of sparse matrices??? https://maciejkula.github.io/2015/02/22/incremental-construction-of-sparse-matrices/
# saving sparse matrix: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.save_npz.html
