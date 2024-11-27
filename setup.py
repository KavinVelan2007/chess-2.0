from distutils.core import setup # type: ignore
from Cython.Build import cythonize
from os import remove, rmdir
from shutil import rmtree

files = ["main.pyx"]
setup(
    ext_modules=cythonize(
        files, compiler_directives={"language_level": "3"}
    )
)
for file in files:
    remove(file.replace(".pyx", ".c"))

rmtree("build", ignore_errors=True)

# terminal command: python setup.py build_ext --inplace
