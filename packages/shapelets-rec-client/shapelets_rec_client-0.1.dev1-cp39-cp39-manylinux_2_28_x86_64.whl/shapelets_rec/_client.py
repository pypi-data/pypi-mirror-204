from typing import Callable, Union, Optional, List, Dict, Any, overload, Tuple

import sys
import pathlib
from uuid import UUID
from rodi import Services

from .services import (InputStream, Outcome, BatchImportService,
                       ExtractionService, BachRuntime, InputStreamFactory,
                       ServerInfo, ServerInfoService, ScanService,
                       FieldScan)

from .services import connect as default_connect
from ._observers import BatchObserver
from ._native import Bitmap
from . import _extractor as ext


class Recorder:
    """
    Recorder client 
    """
    __slots__ = ('_services', )

    def __init__(self, server: str, port: int, connect: Optional[Callable[[str, int], Services]] = None) -> None:
        """
        Constructs a new instance of a recorder client, connected to a server.
        """
        self._services = (connect or default_connect)(server, port)

    @property
    def server_info(self) -> ServerInfo:
        return self._services.get(ServerInfoService).info

    @property
    def batch_defaults(self) -> BachRuntime:
        return self._services.get(BachRuntime)

    def batch_import(self,
                     path: Union[str, pathlib.Path, List[Union[str, pathlib.Path]]],
                     doc_sep: Optional[str] = None,
                     block_size: Optional[int] = None,
                     concurrency: Optional[int] = None,
                     observer: Optional[BatchObserver] = None):
        """
        Imports multiple JSON files stored in a single file. 

        Notes
        -----
        If the document separator is also included in the JSON 
        files, is safer to leave it unset.  The import process 
        will safely scan for the last known end of a document 
        within a buffer, allowing for parallel execution of the 
        import process.

        The import process accepts two parameters to determine 
        the level of concurrency and block size for the import 
        operation.  

        The first time the operation is executed, these parameters 
        will be computed if not provided.  Although the best 
        parameters may depend on your infrastructure, a good rule 
        of thumb is to choose a desired concurrency level and make 
        the block size equal to the total size of L3 case divided 
        by the concurrency.

        Parameters
        ----------
        path : Union[str, pathlib.Path]
            Path to the file to be imported.

        doc_sep : Optional[str], defaults to None
            When set, the algorithm will look for the last occurrence 
            of the given character to determine a safe position where 
            the file can be split for parallel load operations.  If 
            the character is also contained within the documents, leave 
            the parameter set to None; in this case, a fast scan of the 
            document will be performed to determine the safe breaking 
            point of the file.

        block_size : Optional[int], defaults to None
            Buffer size.

        credit : Optional[int], defaults to None 
            Number of concurrent operations to launch.
        """
        if (concurrency is None or block_size is None):
            rt = self._services.get(BachRuntime)
            _default_block_size = rt.block_size
            _default_credit = rt.credit

        observer = observer or BatchObserver()
        block_size = block_size or _default_block_size
        concurrency = concurrency or _default_credit

        importer = self._services.get(BatchImportService)

        unchecked_paths = path if isinstance(path, list) else [path]
        checked_paths: List[(pathlib.Path, int)] = []
        total_size = 0
        for up in unchecked_paths:
            if not isinstance(up, (str, pathlib.Path)):
                raise ValueError(f"{up} should be a string or a pathlib.Path")
            up = pathlib.Path(up) if isinstance(up, str) else up
            if not up.exists():
                raise ValueError(f"{up} does not exists")
            if not up.is_file():
                raise ValueError(f"{up} is not a file")
            stat = up.stat()
            total_size += stat.st_size
            checked_paths.append((up, stat.st_size))

        observer.batch_start(len(checked_paths), total_size)
        for (p, s) in checked_paths:
            observer.file_start(p, s)
            importer.import_file(p, observer.file_progress, block_size, concurrency, doc_sep)
            observer.file_end(p)
        observer.batch_completed()

    def stream(self, call_back: Callable[[Outcome], None],
               max_msgs: int = sys.maxsize,
               time_out: int = 1000,
               max_size: int = 10*1024*1024) -> InputStream:
        """
        Constructs a new instance of an input stream.

        Notes
        -----
        The arguments `max_msgs`, `time_out` and `max_size` controls the runtime 
        behaviour of the input stream.  By changing this parameters one can 
        trade latency vs throughput.

        The default values would try to buffer messages up to one second, which 
        is a setting that should satisfy clients with a throughput preference. 

        Parameters
        ----------
        call_back : Callable[[Outcome], None]
            Asynchronous callback that will be invoked when a push operation is 
            completed on the server side.
        max_msgs : int, optional
            Maximum number of messages that may be temporally stored in clients 
            memory before sent to the server. The default value (sys.maxsize) 
            renders this value inoperative.
        time_out : int, optional
            Maximum waiting time for a message stored in a temporal buffer before 
            sending it to the server; by default, messages may be stored one 
            second before flushing the buffer.
        max_size : int, optional
            Maximum amount of memory used by intermediate buffers, responsible 
            for storing and grouping messages before sending them as batches to 
            the server.

        Returns
        -------
        InputStream
            A new instance of an input stream.
        """
        factory = self._services.get(InputStreamFactory)
        return factory.create(call_back, max_msgs, time_out, max_size)

    @overload
    def extract(self, spec: Dict[str, Any], bm: Bitmap)-> Tuple[int, int, Any]:
        ...

    @overload
    def extract(self, spec: Dict[str, Any],
                field_scan: Optional[FieldScan] = None,
                from_address: Optional[int] = None,
                to_address: Optional[int] = None,
                limit: Optional[int] = None) -> Tuple[int, int, Any]:
        ...

    def extract(self, spec: Dict[str, Any],
                bm: Optional[Bitmap] = None,
                field_scan: Optional[FieldScan] = None,
                from_address: Optional[int] = None,
                to_address: Optional[int] = None,
                limit: Optional[int] = None) -> Tuple[int, int, Any]:
        """
        Runs an extraction process, returning an Arrow XXX, based on the 
        user defined specification. 

        Parameters
        ----------
        spec : Dict[str, Any]
            Specification
        bm : Optional[Bitmap], optional
            Records to extract information from.
        field_scan : Optional[FieldScan], optional
            TODO            
        from_address : Optional[int], optional
            TODO
        to_address : Optional[int], optional
            TODO
        limit : Optional[int], optional
            TODO

        Returns
        -------
        Tuple[int, int, Any]
            The first and second values are the first and last address scanned 
            from the server; the last value is the arrow XXX 
        """
        svc = self._services.get(ExtractionService)
        return svc.run(ext.extractor(spec), bm, field_scan, from_address, to_address, limit)

    @overload
    def scan(self, operation: FieldScan,
             from_address: Optional[int] = None,
             to_address: Optional[int] = None) -> Tuple[int, Bitmap]:
        ...

    @overload
    def scan(self, operation: List[FieldScan],
             from_address: Optional[int] = None,
             to_address: Optional[int] = None) -> Tuple[int, Dict[UUID, Bitmap]]:
        ...

    def scan(self, operation: Union[FieldScan, List[FieldScan]], from_address: Optional[int] = None, to_address: Optional[int] = None):
        return self._services.get(ScanService).execute(operation, from_address, to_address)
