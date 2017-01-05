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

Here is what a Python client call looks like. The file being examined is static/tryit.py.

    import requests
    params={
        'break': 'static/tryit.py:9',
        'expr': ['R', 'x']
    }
    r = requests.get("http://localhost:8080/tryit", params=params)
    print r.text

The result of doing that looks like this:

    > /var/www/demoapp/static/tryit.py(1)<module>()
    -> import os
    (Pdb) import pprint
    import pprint
    (Pdb) import sys
    import sys
    (Pdb) sys.path.append('/var/www/demoapp')
    sys.path.append('/var/www/demoapp')
    (Pdb) b static/tryit.py:9
    b static/tryit.py:9
    Breakpoint 1 at /var/www/demoapp/static/tryit.py:9
    (Pdb) c
    c
    > /var/www/demoapp/static/tryit.py(9)readfile()
    -> return R[:-len(z)]
    (Pdb) print 40*"="
    print 40*"="
    ========================================
    (Pdb) bt
    bt
      /usr/lib/python2.7/bdb.py(400)run()
    -> exec cmd in globals, locals
      <string>(1)<module>()
      /var/www/demoapp/static/tryit.py(11)<module>()
    -> print readfile('static/tryit.html')
    > /var/www/demoapp/static/tryit.py(9)readfile()
    -> return R[:-len(z)]
    (Pdb) print 40*"-"
    print 40*"-"
    ----------------------------------------
    (Pdb) pprint.pprint(R)
    pprint.pprint(R)
    '<html>\n<h1>Here is a title</h1>\nAnd here is some text under the title.\n</html>\nExtraneous Crud'
    (Pdb) pprint.pprint(x)
    pprint.pprint(x)
    {'abc': 'def',
     'ghi': ['jklmnopqrstuvwxyz',
             '1674740283710482340721',
             'klasfj;djas;fjdshafldksjhfaa']}
    (Pdb) c
    c
    <html>
    <h1>Here is a title</h1>
    And here is some text under the title.
    </html>

    The program finished and will be restarted
