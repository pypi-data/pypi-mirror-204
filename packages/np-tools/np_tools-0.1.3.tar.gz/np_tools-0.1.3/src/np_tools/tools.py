"""
Tools for working with Open Ephys raw data files.
"""
from __future__ import annotations
import contextlib
import hashlib
import pathlib
import shutil
import subprocess
import sys
from typing import Iterable
import np_logging


logger = np_logging.get_logger(__name__)


def checksum(path: str | pathlib.Path) -> str:
    path = pathlib.Path(path)
    hasher = hashlib.md5
    blocks_per_chunk = 4096
    multi_part_threshold_gb = 0.2
    if path.stat().st_size < multi_part_threshold_gb * 1024**3:
        return hasher(path.read_bytes()).hexdigest()
    hash = hasher()
    with open(path, 'rb') as f:
        for chunk in iter(
            lambda: f.read(hash.block_size * blocks_per_chunk), b''
        ):
            hash.update(chunk)
    return hash.hexdigest()


def checksums_match(paths: Iterable[pathlib.Path]) -> bool:
    checksums = tuple(checksum(p) for p in paths)
    return all(c == checksums[0] for c in checksums)


def copy(src: pathlib.Path, dest: pathlib.Path) -> None:
    if not pathlib.Path(dest).parent.exists():
        pathlib.Path(dest).parent.mkdir(parents=True, exist_ok=True)
    attempts = 0
    if dest.exists() and dest.is_symlink():
        dest.unlink()
    while True if not dest.exists() else not checksums_match((src, dest)):
        if attempts == 2:
            logger.debug(
                f'Failed to copy {src} to {dest} with checksum-validation after {attempts=}'
            )
            return
        shutil.copy2(src, dest)
        attempts += 1
    logger.debug(f'Copied {src} to {dest} with checksum-validation')


def symlink(src: pathlib.Path, dest: pathlib.Path) -> None:
    """Create a symlink from at `dest`, pointing to `src`.

    - creates parent dirs if needed
    - ignores if symlink already exists and points to `src`
    - replaces existing symlink if it points to a different location

    """
    if 'win' in sys.platform:
        # Remote to remote symlink creation is disabled by default
        subprocess.run('fsutil behavior set SymlinkEvaluation R2R:1')
    if not pathlib.Path(dest).parent.exists():
        pathlib.Path(dest).parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink() and dest.resolve() == src.resolve():
        logger.debug(f'Symlink already exists to {src} from {dest}')
        return
    dest.unlink(missing_ok=True)
    with contextlib.suppress(FileExistsError):
        dest.symlink_to(src)
    logger.debug(f'Created symlink to {src} from {dest}')


def dir_size(path: pathlib.Path) -> int:
    """Return the size of a directory in bytes"""
    if not path.is_dir():
        raise ValueError(f'{path} is not a directory')
    dir_size = 0
    dir_size += sum(
        f.stat().st_size
        for f in pathlib.Path(path).rglob('*')
        if pathlib.Path(f).is_file()
    )
    return dir_size
