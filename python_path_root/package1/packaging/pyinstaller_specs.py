import os

datas = [ #TODO: add a data file
]

datas += rgbd_specs.datas


def processAnalysis(a, exclude_mpl=True):
    return a


hiddenimports = []
try:
    if rgbd_specs.hiddenimports is not None:
        hiddenimports += rgbd_specs.hiddenimports
except:
    pass
