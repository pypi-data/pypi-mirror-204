import gzip

def gzip_agnostic_open(file_path, mode, tar=None, **kwargs):
    return (gzip.open(tar.extractfile(file_path) if tar is not None
                      else file_path, mode, **kwargs)
            if str(file_path).endswith('.gz')
            else open(tar.extractfile(file_path) if tar is not None
                      else file_path, mode, **kwargs))