import os
import pexpect
import re
import sys
import cStringIO

def hack(cmd, brk, log=False):
    if not brk:
        return os.popen("python " + " ".join(cmd)).read()

    child = pexpect.spawn("python -m pdb " + " ".join(cmd))

    def pdb(cmd):
        child.expect(r"\(Pdb\) ", timeout=1)
        child.sendline(cmd)
    def pdbcommand(cmd):
        child.expect(r"\(com\) ", timeout=1)
        child.sendline(cmd)

    if log:
        log = cStringIO.StringIO()
        child.logfile = log
    else:
        devnull = open("/dev/null", "w")
        child.logfile = devnull

    pdb("sys.path.append('" + os.path.realpath(os.curdir) + "')")
    breaknum = 1
    for b in brk:
        filename = linenum = vbls = ""
        show_stack = False

        m = re.search(r"([^:]*):([^:]*):([^:]*)\*", b)
        if m:
            filename, linenum, vbls = m.groups()
            show_stack = True
        else:
            m = re.search(r"([^:]*):([^:]*):([^:]*)", b)
            if m:
                filename, linenum, vbls = m.groups()
            else:
                m = re.search(r"([^:]*):([^:]*)", b)
                if m:
                    filename, linenum = m.groups()
        if not filename or not linenum:
            continue
        vbls = vbls and vbls.split(",")
        pdb("break {0}:{1}".format(filename, linenum))
        pdb("commands {0}".format(breaknum))
        breaknum += 1
        pdbcommand("import pprint")
        if show_stack:
            pdbcommand("print '=== STACKTRACE ==='")
            pdbcommand("bt")
            pdbcommand("print")
        if vbls:
            pdbcommand("print '=== VARIABLES ==='")
            for v in vbls:
                pdbcommand("print '{0}'".format(v))
                pdbcommand("pprint.pprint({0})".format(v))
        pdbcommand("continue")

    pdb("continue")
    if log:
        child.logfile = log
    else:
        child.logfile = sys.stdout
    pdb("continue")
    if log:
        r = log.getvalue()
        log.close()
        return r

if __name__ == '__main__':
    R = open("README.txt").read()
    m = re.compile('\n    ').search(R)
    R = R[m.end():]
    m = re.compile('\n\n').search(R)
    R = R[:m.start()]
    R = R.replace("\n    ", "\n") + "\n"
    exec(R)
