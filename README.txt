Dynamic debugger

At my job, I maintain and extend a Buildbot system. I do a lot of debugging in the course of
doing feature enhancements. A lot of that amounts to querying the values of variables at
different points in Python scripts. These Python scripts are generally invoked using
the Buildbot ShellCommand class. I haven't done all the digging, but I assume it's
doing something like an os.popen or os.system call.

Here I am trying to set something up where I can invoke the PDB debugger without changing
the server-side code. This hack enables a client to specify a source line, and a list of
expressions to be printed when you get there, and it also prints a stack trace at that
point.

Here is what a Python use case looks like.

    print hack(
        ['example.py', 'foo', 'bar'],
        [
            'example.py:5:x*',     # at line 5, print x and stack trace (asterisk)
            'example.py:7:z',      # at line 7, print z
            'example.py:9:R,x',    # at line 9, print R and x
        ]
    )

The format of the output is pretty messy, but adequate for debugging.
