from ak_cache.main import *
from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

@pytest.fixture
def cache_file(tmpdir):
    return Path(tmpdir) / 'cache.pkl'

@pytest.fixture
def cache(cache_file):
    return Cache(cache_file)

@pytest.fixture
def encrypted_cache(tmpdir):
    password = 'password'
    cache_file = Path(tmpdir) / 'cache.pkl'
    return Cache(cache_file, password)

def test_create_cache_file(cache_file):
    assert not cache_file.exists()
    cache = Cache(cache_file)
    assert cache_file.exists()
    cache._create_cache_file(overwrite_existing=True)
    assert cache_file.exists()

def test_write_and_read(cache):
    data = {'key': 'value'}
    cache.write(data)
    assert cache.read() == data

def test_write_and_read_encrypted(encrypted_cache):
    data = {'key': 'value'}
    encrypted_cache.write(data)
    assert encrypted_cache.read() == data

def test_read_nonexistent_cache(cache_file):
    with pytest.raises(Exception):
        cache = Cache(cache_file)
        cache.read()

def test_read_corrupt_cache(cache_file):
    with open(cache_file, 'w') as f:
        f.write('corrupt data')
    cache = Cache(cache_file)
    with pytest.raises(Exception):
        cache.read()
