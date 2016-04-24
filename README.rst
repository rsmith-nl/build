Building Python executable archives
###################################


Introduction
============

On UNIX-like platforms it is easy to build executable Python archives with
standard tools, like ``make`` and ``zip``.

However, on some platforms like ms-windows these tools are not available.

A possible solution is to check the archives in the source control system.
But this is error-prone and causes unnecessary bloat in the repository.

My goal for this project was to build a helper that can build executable
archives on any platform.

Usage
=====

Copy ``build.py`` into your project.
Then customize the part after ``in __name__ == '__main__'``, based on the
example given below.

Suppose the directory ``src`` contains several Python files, ``eggs.py``,
``ham.py`` and ``foo.py``.
It also contains a subdirectory ``spam``, which contains a Python module that
is used by all scripts.
The following code will create three executable archives, ``eggs``, ``ham``
and ``foo``.

.. code-block:: python

    if __name__ == '__main__':
        from shutil import copy
        os.chdir('src')
        programs = [f for f in os.listdir('.') if f.endswith('.py')]
        for pyfile in programs:
            name = pyfile[:-3]
            mkarchive(name, 'spam', pyfile)
            copy(name, '../'+name)
            os.remove(name)
