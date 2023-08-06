from typing import Optional, Tuple, Dict, Any, Iterator, Union, List
import uuid
import numpy

class DynamicScan:
    def check(self, payload: str) -> bool:
        ... 
    def touch(self, payload: str):
        ... 
        
def try_me(obj: DynamicScan):
    ...

def simdjson_version() -> str:
    """
    Version of the SIMDJson library
    """
    ...


def simdjson_threaded() -> bool:
    """
    Returns a flag indicating if the SIMDJson library is build with 
    multithreaded capabilities
    """
    ...


def simdjson_active_runtime() -> Tuple[str, str]:
    """
    Returns the active runtime used by the SIMDJson library.
    """
    ...


def zmq_version() -> Tuple[int, int, int]:
    """
    ZeroMQ version

    Returns
    -------
    typing.Tuple[int, int, int]
        ZeroMQ mayor, minor and build numbers.
    """
    ...

class ExtractorType():

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...  
    def __setstate__(self, state: int) -> None: ...

    @property
    def name(self) -> str:
        """
        :type: str
        """

    @property
    def value(self) -> int:
        """
        :type: int
        """

    Raw     : ExtractorType
    Record  : ExtractorType

    __members__: dict

class Extractor :
    """
    """
    
    @property
    def type( self ) -> ExtractorType :
        ...

    @staticmethod
    def raw( pointer : str ) -> Extractor :
        ...

    @staticmethod
    def record( fields : List[Tuple[str, Extractor]] ) -> Extractor :
        ...


class Bitmap:
    r"""
    A compressed bitmap structure.

    Bitmaps are a generalization of `Roaring Bitmaps <https://roaringbitmap.readthedocs.io/en/latest/>`_,
    (`Apache License 2.0 <https://github.com/RoaringBitmap/RoaringBitmap/blob/master/LICENSE>`_), working
    on a 64 bit addressing space.

    Bitmap instances are iterable, returning the positions of those elements set.

    """

    def __init__(self, indices: Optional[numpy.ndarray[numpy.uint64]] = None) -> None:
        r"""
        Creates a new Bitmap instance.

        Parameters
        ----------
        indices: optional numpy array like, defaults None
            Indices to be set.

        """
        ...     

    def persisted_size(self, portable: bool = True, optimize: bool = True, shrink: bool = True) -> int:
        r"""
        int: Returns the amount of storage (in bytes) that would be required to persist this instance
        """
        ...
        
    @staticmethod
    def read(buffer: memoryview, portable: bool=True) -> Bitmap:
        ...
        
    def write(self, buffer: memoryview, portable: bool=True) -> int:
        ...

    @property
    def cardinality(self) -> int:
        r"""
        int: Returns the number of bits set.  Equivalent to invoke `len` function on this instance.
        """

    @property
    def empty(self) -> bool:
        r"""
        bool: Returns True when this instance doesn't have any bit set; otherwise, it returns False.
        """

    @property
    def first(self) -> Optional[int]:
        r"""
        int: Returns an unsigned integer, which corresponds to the index position of the first bit set; when
        the Bitmap is empty, it returns None, to differentiate from the case where the first set index is
        at position zero.
        """

    @property
    def last(self) -> Optional[int]:
        r"""
        int: Returns an unsigned integer, which corresponds to the index position of the last bit set; when
        the Bitmap is empty, it returns None, to differentiate from the case where the last set index is at
        position zero.
        """

    @property
    def in_memory_size(self) -> int:
        r"""
        int: Returns the amount of memory (in bytes) currently consumed by this instance
        """


    # Extraction methods

    def bool_array(self, *, invert: bool = True, relative: bool = True) -> numpy.ndarray[bool]:
        r"""
        Returns a numpy boolean array.

        Notes
        -----
        This method doesn't make any attempt to protect against memory consumption. If the positions
        of the indices are really high and a non relative to first extraction is requested, it is
        possible the resulting array would be so large it won't fit in memory.

        Parameters
        ----------
        invert: boolean, defaults to True
            When invert is set, flags currently unset in the bitmap will be reported as True in the
            output array; otherwise, there will be no translation in the conversion process.

        relative: boolean, defaults to True
            When relative is set, the first position of the output array (zero) would refer to the
            first position set in the bitmap.  When relative is set to false, the extraction
            process will start at bitmap's position zero.
        """
        ...

    def index_array(self) -> numpy.ndarray[numpy.uint64]:
        """
        Returns a numpy unsigned int (64 bits) array with the indices to the positions currently set.
        """
        ...

    # Bit manipulation methods

    def set(self, position: int, endEx: Optional[int] = None) -> None:
        r"""
        Sets either a single position or a continuous range of positions
        """
        ...

    def unset(self, position: int, endEx: Optional[int] = None) -> None:
        """
        Unsets either a single position or a continuous range of positions
        """
        ...

    def flip(self, position: int, endEx: Optional[int]) -> None:
        """
        Inverts the bit flag of a single position or a continuous range of positions.
        """
        ...

    def contract(self, position: int, by: int) -> None:
        """
        Shifts left a bitmap, by a number of positions, at a particular location.
        """
        ...

    def expand(self, position: int, by: int) -> None:
        """
        Expands a bitmap, by adding a number of positions set to zero, at a particular location
        """
        ...

    def copy(self) -> Bitmap:
        """
        Clones this instance.
        """
        ...

    def slice(self, startInc: int, endInc: int) -> Bitmap:
        """
        Clones (extracts) a continuous range of this instance.
        """
        ...

    # Querying Methods

    def self_or_next(self, position: int) -> Optional[int]:
        """
        Returns the next set position, or position itself when set.
        """
        ...

    def self_or_previous(self, position: int) -> Optional[int]:
        """
        Returns the previous set position, or position itself when set.
        """
        ...

    def lower_cardinality(self, position: int) -> int:
        """
        Returns the total number of bits set whose index is strictly less than the given position.
        """
        ...

    def upper_cardinality(self, position: int) -> int:
        """
        Returns the total number of bits set, whose index is strictly greater than the given position.
        """
        ...

    def contains(self, position: int) -> bool:
        """
        Checks if a particular position is set or unset.

        Notes
        -----
        Bitmap instances has support for `in` idiom, which is
        equivalent to invoke this method.

        Parameters
        ----------
        position: unsigned integer, required
            Position to test

        """
        ...

    def nth(self, ordinal: int) -> int:
        """
        Returns the index of a position set by its relative order.

        Parameters
        ----------
        ordinal: unsigned integer, required
            Ordinal position to query (first, second, third, ...)
        """
        ...
    # Set Operations

    def all(self, startInc: int, endEx: int) -> bool:
        """
        Checks if all bits within a continuous range are set
        """
        ...

    def any(self, startInc: int, endEx: int) -> bool:
        """
        Checks if any bits within a continuous range are set
        """
        ...

    def difference(self, other: Bitmap) -> Bitmap:
        """
        Computes a set difference, that is, it returns a bitmap with all bits
        set in this instance but not set in `other`, union with all bits set
        in `other` but not set in this instance.

        This is equivalent to execute an `xor` operation between Bitmaps.
        """
        ...

    def intersect(self, other: Bitmap) -> Bitmap:
        """
        Computes a set intersection, that is, it returns a new bitmap with
        the common positions between this set and another set.

        This is equivalent to execute an `and` operation between Bitmaps.
        """
        ...

    def symmetric_difference(self, other: Bitmap) -> Bitmap:
        """
        Returns a new Bitmap, whose set positions corresponds to those set positions
        in this instance that are not set in `other` bitmap.

        This is equivalent to an "and not in" operation.
        This is equivalent to execute an `-` operation between Bitmaps.
        """
        ...

    def union(self, other: Bitmap) -> Bitmap:
        """
        Returns a new Bitmap, whose set positions corresponds set positions in either
        this instance or `other` Bitmap.

        This is equivalent to execute an `or` operation between Bitmaps.
        """
        ...

    def strict_subset_of(self, other: Bitmap) -> bool:
        """
        Checks if all bits set in this instance are also set in `other` instance, but
        the cardinality of the sets is difference.
        """
        ...

    def subset_of(self, other: Bitmap) -> bool:
        """
        Checks if all bits set in this instance are also set in `other` instance.
        """
        ...

    def inplace_difference(self, other: Bitmap) -> Bitmap:
        """
        Inplace difference operation.

        See Also
        --------
        difference

        """
        ...

    def inplace_intersect(self, other: Bitmap) -> Bitmap:
        """
        Inplace intersect operation

        See Also
        --------
        intersect

        """
        ...

    def inplace_symmetric_difference(self, other: Bitmap) -> Bitmap:
        """
        Inplace symmetric difference

        See Also
        --------
        symmetric_difference

        """
        ...

    def inplace_union(self, other: Bitmap) -> Bitmap:
        """
        Inplace union operation

        See Also
        --------
        union

        """
        ...

    def __len__(self) -> int: ...
    def __contains__(self, position: int) -> bool: ...
    def __iter__(self) -> Iterator: ...
    def __eq__(self, other: Bitmap) -> bool: ...

    def __and__(self, other: Bitmap) -> Bitmap: ...
    def __iand__(self, other: Bitmap) -> Bitmap: ...
    def __or__(self, other: Bitmap) -> Bitmap: ...
    def __ior__(self, other: Bitmap) -> Bitmap: ...
    def __sub__(self, other: Bitmap) -> Bitmap: ...
    def __isub__(self, other: Bitmap) -> Bitmap: ...
    def __xor__(self, other: Bitmap) -> Bitmap: ...
    def __ixor__(self, other: Bitmap) -> Bitmap: ...

    __hash__ = None
    pass


class ScanOperation():

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...  
    def __setstate__(self, state: int) -> None: ...

    @property
    def name(self) -> str:
        """
        :type: str
        """

    @property
    def value(self) -> int:
        """
        :type: int
        """

    EQ  : ScanOperation 
    NE  : ScanOperation
    LT  : ScanOperation
    GT  : ScanOperation
    LE  : ScanOperation
    GT  : ScanOperation
    IN  : ScanOperation
    NI  : ScanOperation
    DEF : ScanOperation
    BTW : ScanOperation

    __members__: dict





class JSONStore:
    def __init__(self, mem_budget: int, work_dir: str, port_number: int) -> None:
        """
        Creates a new JSON store.
        """
        ...

    def run(self, num_threads: int) -> None:
        """
        Starts the server 

        Parameters
        ----------
        num_threads: int 
            Number of current writers.

        """
        ...
    
    def is_running() -> False:
        """
        Check if server is running

        Returns
        -------
        True: An instance of the server is already running
        False: Server is not running

        """
        ...

    @property
    def end_address(self) -> int:
        """
        Returns the last known address, aka, the end of the log.

        Returns
        -------
        int
        """
        ... 

    def recover(self, index_token: uuid.UUID, log_token: uuid.UUID) -> Tuple[int, int]:
        """
        Starts the server from a previous session.

        Parameters
        ----------
        index_token: uuid.UUID
            Token obtained from a snapshot operation
        log_token: uuid.UUID
            Token obtained from a snapshot operation

        Returns
        -------
        A tuple whose first parameter is the version of the store recovered and 
        its second parameter is the number of sessions restored (threads).                    

        """
        ...

    def pause(self) -> None:
        """
        Pauses the data ingestion.  

        It requires the service to be running.
        """
        ...

    def resume(self) -> None:
        """
        Resumes the ingestion of data.

        It requires the service to be running.
        """
        ...

    def stop(self) -> None:
        """
        Stops the server completely gracefully.
        """
        ...

    def snapshot(self) -> Dict[str, Any]:
        """
        Takes a persistent snapshot of the store, committing the in memory porting of 
        the store to disk.

        This task doesn't require the service to be stopped and should occur naturally 
        whilst the ingestion process is happening.

        The caller will be blocked for the duration of the task.

        Returns
        -------
        A dictionary containing the status of the operation and the recovery UUIDs.
        """
        ...

    def stats(self) -> Tuple[int, int]:
        """
        Returns basic statistics of the service 

        This is a non blocking call.

        Returns
        -------
        typing.Tuple[int, int]
            The first value in the tuple is the total number of bytes ingested since 
            the service was started; the second value of the tuple refers to the 
            total number of messages processed. 
        """
        ...
    
    def lock_data_ingestion(self) -> None:
        """
        Avoids data ingestion in REC. It disables only the calls to save method (normally, through HTTP queries).
        Data ingestion through ZMQ messages is allowed
        """
        ...

    def unlock_data_ingestion(self) -> None:
        """
        Allows data ingestion in REC. 
        """
        ...
        
    def is_locked(self) -> bool:
        """
        It returns a boolean indicating whether data ingestion is locked
        Returns
        -------
        bool
            True means data ingestion is locked. False indicates data ingestion is allowed.
        """
        ...
        
    def get_all_projections(self) -> List[str]:
        """TODO"""
        ...

    def projection_exits(self, path: str) -> bool:
        "returns true if a projection already exists"
        ... 

    def create_new_projection(self, path: str) -> int:
        """Creates a new projection and it returns the address in which 
        the new projection is active
        """
        ...

    def delete_all_projections(self) -> None:
        """Removes all projections"""
        ...

    def delete_projection(self, path: str) -> None:
        """Deletes an existing projection; otherwise throws."""
        ...

    def scan(self, proj: str, op: ScanOperation, value: Union[int, float, str, bool], 
            fromAddress: Optional[int] = None, toAddress: Optional[int] = None) -> Bitmap:
        ...

    def extract( self, extr : Extractor, bm : Bitmap ) -> str:
        """
        Executes the extractor instructions by iterations in the positions set on a bitmap
        

        Parameters
        ----------
        extr : Extractor
            Instructions to extract, transform and build the resulting data set
        bm : Bitmap
            Positions to iterate

        Returns
        -------
        str
            Base64 buffer representing an Arrow Table.
        """
        ...

    def projection(self, jsonPointer: str) -> int:
        """
        Creates a projection.

        It requires the service to be running.
        """
        ...
