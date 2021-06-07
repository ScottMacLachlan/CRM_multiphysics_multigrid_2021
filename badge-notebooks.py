#! /usr/bin/env python3
"""badge/unbadge notebooks

usage:
    Run from the root directory

    To remove a badge in the first cell from all *.ipynb files:
        badge-notebooks.py remove somedirectory

    To add a badge in the first cell to all *.ipynb files:
        badge-notebooks.py add githuborg/repo somedirectory
"""
import glob
import json
import sys
import os

if len(sys.argv) >= 2:
    if sys.argv[1] == 'remove':
        remove = True
        dirname = sys.argv[2]
    elif sys.argv[1] == 'add':
        remove = False
        githuborgrepo = sys.argv[2]
        dirname = sys.argv[3]
    else:
        raise ValueError('Need to add or remove')
else:
    raise ValueError('Need arguments')

if not os.path.isdir(dirname):
    raise ValueError(f'{dirname} not a directory')

dirname = dirname.lstrip('.')  # ./somedir/ ->  /somedir/
dirname = dirname.lstrip('/')  #  /somedir/  ->  somedir/
dirname = dirname.rstrip('/')  #   somedir/  ->  somedir
fnames = glob.glob(os.path.join(dirname,'*.ipynb'))

for fname in fnames:

    with open(fname, "rt", encoding="utf-8") as inf:
        d = json.load(inf)

    if not remove:
        s = fr'<a href="https://colab.research.google.com/github/{githuborgrepo}/blob/master/{fname}" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
        #s = fr'[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lukeolson/imperial-multigrid/blob/master/{dirname}/{fname})'
        newcell = {}
        newcell['cell_type'] = "markdown"
        newcell['metadata'] = {"colab_type": "text",
                               "id": "view-in-github"}
        newcell['source'] = [s]

    topcell = d['cells'][0]

    doit = False
    if 'id' in topcell['metadata'].keys():
        if topcell['metadata']['id'] != 'view-in-github':
            doit = True
        else:
            print(f'{fname}: already badged')
            if remove:
                d['cells'].pop(0)
    else:
        doit = not remove

    if doit:
        print(f'{fname}: adding badge')
        d['cells'].insert(0, newcell)

    with open(fname, "wt") as outf:
        json.dump(d, outf, indent=1, sort_keys=True)
        outf.write("\n")
