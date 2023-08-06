import shutil
def create():
    import akira3d
    path = akira3d.__file__.split('\\')
    del path[-1]
    shutil.unpack_archive('\\'.join(path)+'\\sample.zip', '')