import win32api
import os
from os import path
def main():
    get_pyfiles()

def uncompy(f,p='.'):
    #os.system('dir /b')
    command = 'uncompyle6 '+path.join(p,f)+'>'+os.path.join(p,f[:-3])+'py'
    os.system(command)
    print('targit:',f[:-3]+'py')

def get_pyfiles(p='tool'):
    for p,d,f in os.walk(p):
        for _ in f:
            if _[-3:].lower()=='pyc':
                print('src:',_)
                uncompy(_,p)

if __name__ == '__main__':
    main()