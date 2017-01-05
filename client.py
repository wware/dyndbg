#!/usr/bin/env python

import re

R = open("README.txt").read()
m = re.compile('\n    ').search(R)
R = R[m.start():]
m = re.compile('\n\n').search(R)
R = R[:m.start()]
R = R.replace("\n    ", "\n")
exec(R)
