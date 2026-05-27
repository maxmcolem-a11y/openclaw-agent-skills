#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

WORKSPACE = Path('/Users/mmm/.openclaw/workspace')
DEFAULT_SOURCE = WORKSPACE / 'artifacts' / 'westfield-presentations' / 'timber-ridge-daypack-development-clean'
DEFAULT_DEST_ROOT = WORKSPACE / 'artifacts' / 'westfield-presentations'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Clone the current canonical Westfield presentation template into a new deck folder.'
    )
    parser.add_argument('slug', help='New deck folder name, for example: my-new-deck')
    parser.add_argument(
        '--source',
        type=Path,
        default=DEFAULT_SOURCE,
        help=f'Template source directory (default: {DEFAULT_SOURCE})',
    )
    parser.add_argument(
        '--dest-root',
        type=Path,
        default=DEFAULT_DEST_ROOT,
        help=f'Destination repo root (default: {DEFAULT_DEST_ROOT})',
    )
    parser.add_argument('--force', action='store_true', help='Overwrite the destination if it already exists')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    dest_root = args.dest_root.expanduser().resolve()
    dest = dest_root / args.slug

    if not source.exists() or not source.is_dir():
        raise SystemExit(f'Source template does not exist: {source}')

    if dest.exists():
        if not args.force:
            raise SystemExit(f'Destination already exists: {dest}\nUse --force to replace it.')
        shutil.rmtree(dest)

    shutil.copytree(source, dest, ignore=shutil.ignore_patterns('.git', '.DS_Store', '__pycache__'))

    print(f'Created: {dest}')
    print('Next: replace project-specific copy, logos, assets, and review the live deck path before publishing.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
