# TODO: Eliminate dupe
from enum import Enum, IntEnum, unique, auto

class DataType(IntEnum):
    NONE = 0
    BOOL = 1
    INT8 = 2
    INT16 = 3
    INT32 = 4
    INT64 = 5

    FLOAT = 10
    DOUBLE = 11

    STRING = 20
    VARCHAR = 21

    BINARY_VECTOR = 100
    FLOAT_VECTOR = 101

    UNKNOWN = 999

@unique
class IndexType(str, Enum):
    FLAT = "FLAT"
    IVF_FLAT = "IVF_FLAT"
    IVF_SQ8 = "IVF_SQ8"
    IVF_PQ = "IVF_PQ"
    HNSW = "HNSW"
    ANNOY = "ANNOY"
    RHNSW_FLAT = "RHNSW_FLAT"
    RHNSW_PQ = "RHNSW_PQ"
    RHNSW_SQ = "RHNSW_SQ"

    # Binary Vectors
    BIN_FLAT = "BIN_FLAT"
    BIN_IVF_FLAT = "BIN_IVF_FLAT"


@unique
class VectorSpace(str, Enum):
    # for floating point vectors:
    L2 = "L2"
    IP = "IP"
    # for binary vectors:
    JACCARD = "JACCARD"
    TANIMOTO = "TANIMOTO"
    HAMMING = "HAMMING"
    SUPERSTRUCTURE = "SUPERSTRUCTURE"
    SUBSTRUCTURE = "SUBSTRUCTURE"

@unique
class HashAlgo(str,  Enum):
    md5 = auto()
    sha1 = auto()
    sha256 = auto()
    sha512 = auto()
    sha3_224 = auto()
    sha3_256 = auto()
    sha3_384 = auto()
    sha3_512 = auto()
    # TODO: Require length
    # "shake_128" = auto()
    # "shake_256" =  auto()
    blake2b = auto()
    blake2 = auto()
