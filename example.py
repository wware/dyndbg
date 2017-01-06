import sys

x = {'abc': 'def', 'ghi': ['jklmnopqrstuvwxyz', '1674740283710482340721', 'klasfj;djas;fjdshafldksjhfaa']}

def do_stuff():
    z = 'Extraneous Crud'
    R = 'Some stupid long string that does nothing.'
    R += z
    return R[:-len(z)]

for arg in sys.argv[1:]:
    x['ghi'].append(arg)
print do_stuff()
