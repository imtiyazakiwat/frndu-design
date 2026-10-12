"""Build all Frndu frames, then validate + render contact sheets.

Usage: python3 design/_gen/build.py [module ...]
"""
import glob
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib  # noqa: E402

MODULES = ['screens_a', 'screens_b', 'screens_c', 'screens_d', 'screens_e', 'screens_f', 'screens_g', 'screens_h', 'screens_i', 'components']


def main():
    mods = sys.argv[1:] or MODULES
    for m in mods:
        try:
            mod = __import__(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                print('skip', m)
                continue
            raise
        mod.gen_all()
    print('frames written:', len(lib.REGISTRY))
    bad = 0
    for _, _, _, rel, _ in lib.REGISTRY:
        p = os.path.join(lib.ROOT, rel)
        r = subprocess.run(['xmllint', '--noout', p], capture_output=True, text=True)
        if r.returncode:
            bad += 1
            print('XML ERROR', rel, r.stderr[:400])
    print('xml errors:', bad)
    # registry dump for README
    with open('/tmp/frndu_registry.tsv', 'a') as f:
        for row in lib.REGISTRY:
            f.write('\t'.join(row) + '\n')
    if not sys.argv[1:]:
        import proto
        proto.main()


if __name__ == '__main__':
    main()
