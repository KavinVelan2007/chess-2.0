from distutils.core import setup
from Cython.Build import cythonize
from os import remove
from shutil import rmtree


files = ["brains.pyx"]
setup(ext_modules=cythonize(files, compiler_directives={"language_level": "3"}))

for file in files:
    remove(file.replace(".pyx", ".c"))

rmtree("build", ignore_errors=True)


# command for compiling : python setup.py build_ext --inplace