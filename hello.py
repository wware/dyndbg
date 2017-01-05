import os
import pexpect
import pprint
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

def hack(brk, expr, script):
    if not brk or not expr:
        return os.popen("python " + script).read()
    if len(expr) == 1 and "," in expr[0]:
        expr = expr[0].split(",")
    log = cStringIO.StringIO()
    here = os.path.realpath(os.curdir)
    child = pexpect.spawn("python -m pdb {0}".format(script))
    child.logfile = log

    def pdb(cmd):
        child.expect(r"\(Pdb\) ", timeout=1)
        child.sendline(cmd)

    pdb("import pprint")
    pdb("import sys")
    pdb("sys.path.append('{0}')".format(here))
    pdb("b " + brk)
    pdb("c")
    while True:
        try:
            child.expect('The program finished and will be restarted', timeout=1)
            break
        except pexpect.TIMEOUT:
            try:
                pdb('print 40*"="')
                pdb('bt')
                pdb('print 40*"-"')
                for e in expr:
                    pdb('pprint.pprint(' + e + ')')
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
    brk = request.args['break']
    expr = request.args.getlist('expr')
    return hack(brk, expr, "static/tryit.py")

if __name__ == '__main__':
    if 'test' in sys.argv[1:]:
        print hack('tryit.py:9', ['R', 'x'], 'static/tryit.py')
    else:
        app.run("0.0.0.0", 8080)
