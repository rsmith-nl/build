# file: build.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2016-04-24 17:06:48 +0200
# Last modified: 2020-10-25T19:39:35+0100
"""Create runnable archives from program files and custom modules."""

import os
import py_compile
import tempfile
import zipfile as z


def main():
    """Main entry point for build script"""
    # nm = "program"
    # if os.name == "nt":
    #     nm += ".pyz"
    # mkarchive(nm, "module", main="console.py")
    pass


def mkarchive(name, modules, main="__main__.py"):
    """
    Create a runnable archive.

    Arguments:
        name: Name of the archive.
        modules: Module name or iterable of module names to include.
        main: Name of the main file. Defaults to __main__.py
    """
    print(f"Building {name}", end="... ")
    std = "__main__.py"
    shebang = b"#!/usr/bin/env python\n"
    if isinstance(modules, str):
        modules = [modules]
    if main != std:
        remove(std)
        os.link(main, std)
    # Optimization level for compression
    lvl = 2
    # Forcibly compile __main__.py lest we use an old version!
    py_compile.compile(std, optimize=lvl)
    tmpf = tempfile.TemporaryFile()
    with z.PyZipFile(tmpf, mode="w", compression=z.ZIP_DEFLATED, optimize=lvl) as zf:
        zf.writepy(std)
        for m in modules:
            zf.writepy(m)
    if main != std:
        remove(std)
    tmpf.seek(0)
    archive_data = tmpf.read()
    tmpf.close()
    with open(name, "wb") as archive:
        archive.write(shebang)
        archive.write(archive_data)
    os.chmod(name, 0o755)
    print("done.")


def remove(path):
    """Remove a file, ignoring directories and nonexistant files."""
    try:
        os.remove(path)
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        pass


if __name__ == "__main__":
    main()
