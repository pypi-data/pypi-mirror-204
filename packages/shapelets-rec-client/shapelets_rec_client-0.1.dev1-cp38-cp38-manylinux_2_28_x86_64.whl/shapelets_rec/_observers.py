from typing import Optional
import pathlib
from tqdm import tqdm

class BatchObserver:
    
    def __init__(self) -> None:
        pass
    
    def batch_start(self, num_files: int, batch_size: int):
        """
        Informs of the total size (in bytes) of the operation

        Parameters
        ----------
        num_files: int 
            Total number of files to process
        batch_size : int
            Total batch size in bytes
        """
        pass
        
    def file_start(self, path: pathlib.Path, size: int):
        """
        Informs a file is being processed

        Parameters
        ----------
        path : pathlib.Path
            Path being processed
        size:  int
            File size
        """
        pass
    
    def file_progress(self, path: pathlib.Path, offset: int, records: Optional[int] = None):
        """
        Reports the current offset on a file

        Parameters
        ----------
        path : pathlib.Path
            Path being processed
        offset : int
            Current offset within the file
        records: optional int, defaults to None
            When known, it returns the number of records processed.
        """
        pass
        
    def file_end(self, path: pathlib.Path):
        """
        Informs a file is completed

        Parameters
        ----------
        path : pathlib.Path
            Path being processed

        """
        pass

    def batch_completed(self):
        """Batch has terminated"""
        pass

class TQDMObserver(BatchObserver):
    
    __slots__ = ('_total_bar', '_file_bar', '_single_bar_mode', '_print_file_paths')
    
    def __init__(self, single_bar: bool = False, print_file_paths: bool = False) -> None:
        """
        Creates a batch observer using tqdm

        Parameters
        ----------
        single_bar : bool, optional, default False
            Single bar display.
        """
        self._total_bar = None 
        self._file_bar = None
        self._single_bar_mode = single_bar 
        self._print_file_paths = print_file_paths
        super().__init__()
    
    def batch_start(self, num_files: int, batch_size: int):
        self._single_bar_mode |= num_files == 1
        self._total_bar = tqdm(total=batch_size, unit='B', unit_scale=True, leave=True, unit_divisor=1024, desc = '            Progress')
         
    def file_start(self, path: pathlib.Path, size: int):
        if self._single_bar_mode:
            return 
        
        p = str(path.absolute())
        if len(p) < 20:
            p = (' ' * (20 - len(p) )) + p 
        else:
            p = '...' + p[-17:]
        
        if self._file_bar is None:
            self._file_bar = tqdm(total = size+1, unit='B', unit_scale=True, leave=True, unit_divisor=1024, desc=p)
        else:
            self._file_bar.clear()
            self._file_bar.set_description(p)
            self._file_bar.reset(size)
        
    def file_progress(self, path: pathlib.Path, offset: int, records: Optional[int] = None):
        self._total_bar.update(offset)
        if not self._single_bar_mode:
            self._file_bar.update(offset)
            
    def file_end(self, path: pathlib.Path):
        if self._print_file_paths:
            self._file_bar.write(f'🟢 {path}') # ✘ ✔ 🟢 🔴
        
    def batch_completed(self):
        if self._total_bar is not None:
            self._total_bar.close()
        if self._file_bar is not None:
            self._file_bar.close() 
        
