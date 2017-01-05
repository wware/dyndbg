import os

x = {'abc': 'def', 'ghi': ['jklmnopqrstuvwxyz', '1674740283710482340721', 'klasfj;djas;fjdshafldksjhfaa']}

def readfile(f):
    z = 'Extraneous Crud'
    R = open(f).read()
    R += z
    return R[:-len(z)]

print readfile('static/tryit.html')
