from setuptools import setup, find_packages

setup(
    name = 'xjm',
    version = '0.0.4',

    author = 'Jimmy',
    author_email = '1150213628@qq.com',

    description = 'some fundamental functions, such as visualization, \
      data split, Web image crawler, etc',

    # install_requires = [
    #     'python',
    #     'opencv-python',
    #     'numpy',
    #     'torch',
    # ],
    packages =  find_packages(exclude=['downloads']),
    # data_files=[('ckpt', ['']),('',['requirments.txt'])]

)