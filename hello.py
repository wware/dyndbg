import os
import pexpect
import pprint
import re
import sys
import cStringIO

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    R = open('README.txt').read()
    return '<pre>{0}</pre>'.format(
        R.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )

def hack(brk, args, script):
    cmd = script + " " + " ".join(args)
    if not brk:
        return os.popen("python " + cmd).read()

    log = cStringIO.StringIO()
    here = os.path.realpath(os.curdir)
    child = pexpect.spawn("python -m pdb " + cmd)
    child.logfile = log

    def pdb(cmd):
        child.expect(r"\(Pdb\) ", timeout=1)
        child.sendline(cmd)

    breakpoints = []
    for b in brk:
        m = re.search(r"([^:]*):([^:]*):([^:]*)", b)
        if m:
            def show(vbls=m.group(3).split(",")):
                for v in vbls:
                    pdb('pprint.pprint(' + v + ')')
            breakpoints.append((
                m.group(1) + "(" + m.group(2) + ")",
                m.group(1) + ":" + m.group(2),
                show
            ))

    pdb("import pprint")
    pdb("import sys")
    pdb("sys.path.append('" + here + "')")
    for _, where, _ in breakpoints:
        pdb("b " + where)
    pdb("c")
    while True:
        try:
            child.expect('The program finished and will be restarted', timeout=0.1)
            break
        except pexpect.TIMEOUT:
            buf = child.buffer
            try:
                pdb('print 40 * "="')
                pdb('bt')
                pdb('print 40 * "-"')
                for k, _, show in breakpoints:
                    if k in buf:
                        show()
                pdb('c')
            except pexpect.TIMEOUT:
                break
        except pexpect.EOF:
            break
    r = log.getvalue()
    log.close()
    return r

@app.route("/tryit")
def tryit():
    brk = request.args.getlist('break')
    args = request.args.getlist('args')
    return hack(brk, args, "static/tryit.py")

if __name__ == '__main__':
    if 'test' in sys.argv[1:]:
        print hack(
            [
                'tryit.py:6:x',
                'tryit.py:8:z',
                'tryit.py:10:R,x',
            ],
            ['foo', 'bar'],
            'static/tryit.py'
        )
    else:
        app.run("0.0.0.0", 8080)
