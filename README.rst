+++++++++++++
pytracemalloc
+++++++++++++

Debug tool tracking Python memory allocations. Provide the following
information:

 * Allocated size and number of allocations per file,
   or optionally per file and line number
 * Compute the average size of memory allocations
 * Compute delta between two "snapshots"
 * Source of a memory allocation: filename and line number

Example (compact)::

    2013-02-28 23:40:18: Top 5 allocations per file
    #1: .../Lib/test/regrtest.py: 3998 KB
    #2: .../Lib/unittest/case.py: 2343 KB
    #3: .../ctypes/test/__init__.py: 513 KB
    #4: .../Lib/encodings/__init__.py: 525 KB
    #5: .../Lib/compiler/transformer.py: 438 KB
    other: 32119 KB
    Total allocated size: 39939 KB

Another example (full)::

    2013-03-04 01:01:55: Top 10 allocations per file and line
    #1: .../2.7/Lib/linecache.py:128: size=408 KiB (+408 KiB), count=5379 (+5379), average=77 B
    #2: .../unittest/test/__init__.py:14: size=401 KiB (+401 KiB), count=6668 (+6668), average=61 B
    #3: .../2.7/Lib/doctest.py:506: size=319 KiB (+319 KiB), count=197 (+197), average=1 KiB
    #4: .../Lib/test/regrtest.py:918: size=429 KiB (+301 KiB), count=5806 (+3633), average=75 B
    #5: .../Lib/unittest/case.py:332: size=162 KiB (+136 KiB), count=452 (+380), average=367 B
    #6: .../Lib/test/test_doctest.py:8: size=105 KiB (+105 KiB), count=1125 (+1125), average=96 B
    #7: .../Lib/unittest/main.py:163: size=77 KiB (+77 KiB), count=1149 (+1149), average=69 B
    #8: .../Lib/test/test_types.py:7: size=75 KiB (+75 KiB), count=1644 (+1644), average=46 B
    #9: .../2.7/Lib/doctest.py:99: size=64 KiB (+64 KiB), count=1000 (+1000), average=66 B
    #10: .../Lib/test/test_exceptions.py:6: size=56 KiB (+56 KiB), count=932 (+932), average=61 B
    3023 more: size=1580 KiB (+1138 KiB), count=12635 (+7801), average=128 B
    Total: size=3682 KiB (+3086 KiB), count=36987 (+29908), average=101 B

Python module developed by Wyplay: http://www.wyplay.com/

Project homepage: https://github.com/wyplay/pytracemalloc


Usage: Display top 25
=====================

Display the 25 files allocating the most memory every minute::

    import tracemalloc
    tracemalloc.enable()
    top = tracemalloc.DisplayTop(25)
    top.start(60)
    # ... run your application ...


By default, the top 25 is written into sys.stdout. You can write the output
into a file (here opened in append mode)::

    import tracemalloc
    tracemalloc.enable()
    log = open("tracemalloc.log", "a")
    top = tracemalloc.DisplayTop(25, file=log)
    top.start(60)
    # ... run your application ...
    log.close()


Usage: Take snapshots
=====================

For deeper analysis, it's possible to take a snapshot every minute::

    import tracemalloc
    tracemalloc.enable()
    take_snapshot = tracemalloc.TakeSnapshot()
    # take_snapshot.filename_template = "/tmp/trace-$pid-$timestamp.pickle"
    take_snapshot.start(60.0)
    # ... run your application ...

By default, files called "tracemalloc-XXXX.pickle" are created in the current
directory. Uncomment and edit the "filename_template" line in the example to
customize the filename. The filename template can use the following variables:
``$pid``, ``$timestamp``, ``$counter``.

To display and compare snapshots, use the following command::

    python -m tracemalloc trace1.pickle [trace2.pickle trace3.pickle ...]

To get the help, type::

    python -m tracemalloc --help

It is also possible to take a snapshot explicitly::

   snapshot = tracemalloc.Snapshot.create()
   snapshot.write(filename)


Installation
============

You need a modified Python runtime:

 * Download Python source code
 * Apply python2.7.patch or python3.4.patch
 * Compile and install Python
 * It can be installed in a custom directory

Dependencies:

 * `Python <http://www.python.org>`_ 2.5 - 3.4
 * `glib <http://www.gtk.org>`_ version 2

Install::

    python setup.py install


API
===

Call ``tracemalloc.enable()`` as early as possible to get the most complete
statistics. Otherwise, some Python memory allocations made by your application
will be ignored by tracemalloc.

disable() is automatically called at exit using the atexit module.

The version can be read a string from ``tracemalloc.__version__``.

Functions
---------

enable():

   Start tracing Python memory allocations.

disable():

   Stop tracing Python memory allocations
   and stop the timer started by start_timer().

get_source(obj) -> (filename: str, lineno: int)

   Get the source of an object.

   Return ``(filename, lineno)`` if the source is known,
   ``None`` otherwise.

get_stats():

   Get statistics on Python memory allocation.

   Return a dict:
   ``{filename (str): {lineno (int) -> (size (int), count (int))}}``.

   *filename* may be ``"???"`` and *lineno* may be ``None`` if tracemalloc
   failed to get the source of the memory allocation.

start_timer(delay: int, func: callable, args: tuple=(), kwargs: dict={})

   Start a timer calling ``func(*args, **kwargs)`` every *delay* seconds.

   The timer is based on the Python memory allocator, it is not real time.
   *func* is called at least after *delay* seconds, it is not called exactly
   after *delay* seconds if no Python memory allocation occurred.

   If start_timer() is called twice, previous parameters are replaced. The
   timer has a resolution of 1 second.

   start_timer() is used by DisplayTop and TakeSnapshot to run regulary a task.

stop_timer()

   Stop the timer started by start_timer().


Classes
-------

 * DisplayTop(count: int): Displaying to top N of the biggest allocation.
   Methods:

   - display(): display the top
   - start(delay: int): start a task using tracemalloc timer to display
     the top every delay seconds
   - stop(): stop the task started by the start() method

   Attributes:

   - compare_with_previous (bool, default: True): if True, compare with the
     previous top, otherwise compare with the first one
   - filename_parts (int, default: 3): Number of displayed filename parts
   - show_average (bool, default: True): if True, show the average size of
     allocations
   - show_count (bool, default: True): if True, show the number of allocations
   - show_lineno (bool, default: False): if True, use also the line number,
     not only the filename
   - show_size (bool, default: True): if True, show the size of allocations

 * Snapshot: Snapshot of Python memory allocations. Use TakeSnapshot to
   regulary take snapshots.
   Methods:

   - create(): take a snapshot
   - filter_filenames(pattern, include): remove filenames not matching pattern
     if include is True, or remove filenames matching pattern if include is
     False (exclude). See fnmatch.fnmatch() for the syntax of patterns.
   - write(filename): write a snapshot into a file

   Attributes:

   - pid (int): identifier of the process which created the snapshot
   - stats (dict): raw memory allocation statistics
   - timestamp (str): date and time of the creation of the snapshot

 * TakeSnapshot: Task taking snapshots of Python memory allocations: write them
   into files.
   Methods:

   - start(delay: int): start a task taking a snapshot every delay seconds
   - stop(): stop the task started by the start() method
   - take_snapshot(): take a snapshot

   Attribute:

   - filename_template (str): template to create a filename. "Variables" can
     be used in the template: "$pid" (identifier of the current process),
     "$timestamp" (current date and time) and "$counter" (counter starting at 1
     and incremented at each snapshot).


Changelog
=========

Version 0.8

 - automatically disable tracemalloc at exit

Version 0.7 (2013-03-04)

 - First public version


See also
========

 * `Meliae: Python Memory Usage Analyzer
   <https://pypi.python.org/pypi/meliae>`_
 * `Issue #3329: API for setting the memory allocator used by Python
   <http://bugs.python.org/issue3329>`_
 * `Guppy-PE: umbrella package combining Heapy and GSL
   <http://guppy-pe.sourceforge.net/>`_
 * `PySizer <http://pysizer.8325.org/>`_: developed for Python 2.4
