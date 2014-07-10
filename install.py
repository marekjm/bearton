import glob
import os
import shutil
import sys


TESTING = '--testing' in sys.argv or '-t' in sys.argv


def install():
    # Install bearton modules
    home = os.path.expanduser('~')
    path = ''
    for p in [p for p in sys.path if p.startswith(home)]:
        if p.endswith('site-packages') and os.path.isdir(p):
            path = p
            break

    looks = [('bearton',),
             ('bearton', 'page'),
             ('bearton', 'schemes'),
             ('bearton', 'servers'),
             ('bearton', 'util'),
    ]

    files = []
    for i in looks: files.extend(glob.glob(os.path.join(os.path.join(*i), '*.py')))

    for i in looks:
        ipath = os.path.join(path, *i)
        if not os.path.isdir(ipath):
            os.mkdir(ipath)
    files = sorted(files)

    width = 0
    for f in files:
        n = len(f)
        width = (n if n > width else width)
    width += 4

    for f in files:
        source = f
        target = os.path.join(path, f)
        print('cp:', source.ljust(width), '->', target)
        shutil.copy(source, target)

    if TESTING:
        print('NOTICE: for testing purposes UIs and shared resources are not being installed: run install.py without -t/--testing option to install them')
        return
    # Install default Bearton scheme
    share_path = os.path.join(home, '.local', 'share', 'bearton')
    if not os.path.isdir(share_path): os.mkdir(share_path)

    schemes_path = os.path.join(share_path, 'schemes')
    print('installing schemes in:', schemes_path)
    if os.path.isdir(schemes_path): shutil.rmtree(schemes_path)
    shutil.copytree('./schemes', schemes_path)

    ui_path = os.path.join(share_path, 'ui')
    print('installing ui descriptions in:', ui_path)
    if not os.path.isdir(ui_path): os.mkdir(ui_path)
    uis = glob.glob('./ui/*.json')
    width = 0
    for f in uis:
        n = len(f)
        width = (n if n > width else width)
    width += 4
    for f in uis:
        source = f
        target = os.path.normpath(os.path.join(share_path, f))
        print('cp:', source.ljust(width), '->', target)
        shutil.copy(source, target)

    bin_path = os.path.join(home, '.local', 'bin')
    print('installing executables in:', bin_path)
    if not os.path.isdir(bin_path):
        print('could not install Bearton executables')
    else:
        uis = [f for f in glob.glob('./ui/*.py') if 'template-ui' not in f]
        width = 0
        for f in uis:
            n = len(f)
            width = (n if n > width else width)
        width += 4
        for f in uis:
            source = f
            target = os.path.join(bin_path, os.path.splitext(os.path.split(f)[1])[0])
            print('cp:', source.ljust(width), '->', target)
            shutil.copy(source, target)


if __name__ == '__main__': install()
