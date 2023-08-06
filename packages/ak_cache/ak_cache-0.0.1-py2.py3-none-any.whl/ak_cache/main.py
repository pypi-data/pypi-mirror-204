from pathlib import Path
import ak_file
import _pickle as cPickle

class Cache:
    def __init__(self, filename: Path= Path("Cache.pkl")) -> None:
        self.filename = Path(str(filename))
        self.file = ak_file.File(str(filename))
        self._create_cache_file(overwrite_existing=False)

    def __str__(self) -> str:
        return f"Cache class located at {self.filename}"

    def __repr__(self) -> str:
        return f"Cache(filename={self.filename})"
    
    def _create_cache_file(self, overwrite_existing: bool = False) -> Path:
        if (not self.file.exists()) or overwrite_existing:
            with open(self.filename, 'w') as f:
                pass
        return self.filename
    
    def write(self, data) -> Path:
        self._create_cache_file(overwrite_existing = False)
        with open(self.filename, 'wb') as f:
            cPickle.dump(data, f)
        return self.filename
    
    def read(self):
        with open(self.filename, 'rb') as f:
            return cPickle.load(f)