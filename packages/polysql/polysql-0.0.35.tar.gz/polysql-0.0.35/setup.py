import os
import sys
from setuptools import setup
from setuptools.command.install import install
from distutils.ccompiler import new_compiler
from distutils.unixccompiler import UnixCCompiler
from os import path
from platform import system
from tempfile import TemporaryDirectory
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def build_library(output_path, repo_paths):
    source_paths = []
    for repo_path in repo_paths:
        src_path = path.join(repo_path, "src")
        source_paths.append(path.join(src_path, "parser.c"))
        source_paths.append(path.join(src_path, "scanner.cc"))

    compiler = new_compiler()
    if isinstance(compiler, UnixCCompiler):
        compiler.compiler_cxx[0] = "c++"

    with TemporaryDirectory(suffix="polysql") as out_dir:
        object_paths = []
        for source_path in source_paths:
            if system() == "Windows":
                flags = None
            else:
                flags = ["-fPIC"]
                if source_path.endswith(".c"):
                    flags.append("-std=c99")
            object_paths.append(
                compiler.compile(
                    [source_path],
                    output_dir=out_dir,
                    include_dirs=[path.dirname(source_path)],
                    extra_preargs=flags,
                )[0]
            )
        compiler.link_shared_object(object_paths, output_path, target_lang="c++")


class InstallCommand(install):
    def run(self):
        build_library(
            os.path.join(sys.prefix, "lib/polysql/languages.so"),
            [
                "bigquery",
                "postgres",
            ],
        )
        install.run(self)


setup(
    name="polysql",
    version="0.0.35",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Grammar and parser used to parse SQL",
    packages=["polysql"],
    package_dir={
        "polysql": "bindings/python",
        "polysql.bigquery": "bigquery/src",
        "polysql.postgres": "postgres/src",
    },
    install_requires=["tree_sitter>=0.20.1"],
    cmdclass={"install": InstallCommand},
)
