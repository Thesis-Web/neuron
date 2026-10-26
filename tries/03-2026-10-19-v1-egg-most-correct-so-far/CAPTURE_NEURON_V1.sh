#!/usr/bin/env bash
# Run in WSL as exnulla. Collection only: never starts Neuron or loads its code.
set -Eeuo pipefail
umask 077

SRC="${NEURON_DIR:-$HOME/neuron/v1}"
OUT="${NEURON_EXPORT_DIR:-/mnt/c/Users/AdLibitumVita/Downloads}"

command -v python3 >/dev/null || { echo 'ERROR: python3 is required.' >&2; exit 1; }
[[ -f "$SRC/brain.db" ]] || { echo "ERROR: No brain.db at $SRC/brain.db" >&2; exit 1; }
[[ -d "$OUT" && -w "$OUT" ]] || { echo "ERROR: Downloads directory unavailable: $OUT" >&2; exit 1; }

python3 - "$SRC" "$OUT" <<'PY'
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import stat
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone
from uuid import uuid4

src = Path(sys.argv[1]).resolve(strict=True)
out = Path(sys.argv[2]).resolve(strict=True)
db = src / 'brain.db'
if db.is_symlink():
    raise SystemExit('ERROR: brain.db is a symlink; use the actual V1 directory.')

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
name = 'neuron-v1-review-' + stamp + '-' + uuid4().hex[:8]
archive = out / (name + '.tar.gz')
partial = out / ('.' + name + '.tar.gz.partial')
checksum = out / (name + '.tar.gz.sha256')
meta = {'source_directory': str(src), 'started_utc': now(),
        'sqlite_version': sqlite3.sqlite_version,
        'capture_method': 'SQLite backup API; source opened mode=ro',
        'source_files_are_not_an_atomic_snapshot_with_database': True}
skipped = []

try:
    with tempfile.TemporaryDirectory(prefix='neuron-v1-capture-') as work:
        root = Path(work) / name
        root.mkdir()
        print('Reading:', db, flush=True)
        deadline = time.monotonic() + 900
        def progress(status, remaining, total):
            if time.monotonic() > deadline:
                raise TimeoutError('Database backup exceeded 15 minutes; source unchanged.')

        live = sqlite3.connect(db.as_uri() + '?mode=ro', uri=True, timeout=10)
        copy = sqlite3.connect(str(root / 'brain.db'))
        try:
            live.execute('PRAGMA query_only=ON')
            meta['source_journal_mode'] = live.execute('PRAGMA journal_mode').fetchone()[0]
            live.backup(copy, pages=1024, progress=progress, sleep=0.05)
            # This changes ONLY the new copy, to make it a standalone database.
            if copy.execute('PRAGMA journal_mode=DELETE').fetchone()[0] != 'delete':
                raise RuntimeError('Could not finalize the standalone database copy.')
            meta['backup_finished_utc'] = now()
            schema = copy.execute(
                'SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY type,name'
            ).fetchall()
            (root / 'schema.sql').write_text(
                '\n\n'.join(row[0].rstrip(';') + ';' for row in schema) + '\n',
                encoding='utf-8')
            # Diagnostics run on the copy. A missing custom function is recorded,
            # not worked around by loading untrusted extensions.
            check_deadline = time.monotonic() + 120
            copy.set_progress_handler(lambda: int(time.monotonic() > check_deadline), 10000)
            try:
                checks = [row[0] for row in copy.execute('PRAGMA quick_check')]
                meta['quick_check'] = checks
            except sqlite3.Error as exc:
                meta['quick_check'] = {'inconclusive': str(exc)}
            finally:
                copy.set_progress_handler(None, 0)
        finally:
            copy.close()
            live.close()

        print('Capturing construction/hop source (not executing it).', flush=True)
        omit_dirs = {'.git', '.hg', '.svn', '.venv', 'venv', 'node_modules',
                     '__pycache__', '.cache', '.pytest_cache', '.mypy_cache',
                     '.ruff_cache', 'build', 'dist', 'target', 'backups',
                     'snapshots', 'exports', 'keys', 'secrets', 'credentials', '.ssh'}
        suffixes = {'.sql', '.py', '.sh', '.c', '.h', '.cc', '.cpp', '.hpp',
                    '.go', '.rs', '.md', '.txt', '.toml', '.yaml', '.yml',
                    '.json', '.lay', '.ini', '.cfg', '.mk', '.cmake', '.asm'}
        special = {'makefile', 'cmakelists.txt', 'readme', 'license', 'copying'}
        count = 0
        for parent, dirs, files in os.walk(src, followlinks=False):
            for d in list(dirs):
                p = Path(parent) / d
                if d.lower() in omit_dirs or p.is_symlink():
                    dirs.remove(d)
                    skipped.append(str(p.relative_to(src)) + '/ [directory excluded]')
            for filename in sorted(files):
                p = Path(parent) / filename
                rel = p.relative_to(src)
                low = filename.lower()
                secret = (low.startswith('.env') or
                          any(word in low for word in ('secret', 'credential', 'password', 'token', 'api_key', 'apikey')) or
                          p.suffix.lower() in {'.key', '.pem', '.p12', '.pfx'})
                if p.is_symlink() or not stat.S_ISREG(p.lstat().st_mode) or secret:
                    skipped.append(str(rel) + ' [link/nonregular/secret-named file excluded]')
                    continue
                if p.suffix.lower() not in suffixes and low not in special:
                    skipped.append(str(rel) + ' [not a selected source/document file]')
                    continue
                before = p.stat()
                target = root / 'source' / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, target)
                after = p.stat()
                if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                    raise RuntimeError('Source changed during capture: ' + str(rel))
                count += 1
        meta['source_file_count'] = count
        meta['finished_utc'] = now()
        meta['database_is_unredacted'] = True
        (root / 'capture.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
        (root / 'EXCLUDED.txt').write_text('\n'.join(sorted(skipped)) + '\n', encoding='utf-8')

        members = sorted(p for p in root.rglob('*') if p.is_file())
        hashes = {p.relative_to(root).as_posix(): digest(p) for p in members}
        (root / 'SHA256SUMS.txt').write_text(
            ''.join(h + '  ' + path + '\n' for path, h in hashes.items()), encoding='utf-8')
        print('Packing and verifying archive...', flush=True)
        with tarfile.open(partial, 'w:gz') as tf:
            tf.add(root, arcname=name)
        # Read the archive back and verify every payload against its manifest.
        with tarfile.open(partial, 'r:gz') as tf:
            for rel, expected in hashes.items():
                f = tf.extractfile(name + '/' + rel)
                if f is None:
                    raise RuntimeError('Missing archived file: ' + rel)
                h = hashlib.sha256()
                with f:
                    for block in iter(lambda: f.read(1024 * 1024), b''):
                        h.update(block)
                if h.hexdigest() != expected:
                    raise RuntimeError('Archive verification failed: ' + rel)
        partial.rename(archive)
        checksum.write_text(digest(archive) + '  ' + archive.name + '\n', encoding='utf-8')
        if meta.get('quick_check') != ['ok']:
            print('WARNING: SQLite quick_check was not OK; details are in capture.json.')
        print('\nUPLOAD THESE TWO FILES:')
        print(archive)
        print(checksum)
        print('Archive size: %.2f MiB' % (archive.stat().st_size / 1048576))
except Exception as exc:
    partial.unlink(missing_ok=True)
    raise SystemExit('CAPTURE FAILED: ' + str(exc))
PY
