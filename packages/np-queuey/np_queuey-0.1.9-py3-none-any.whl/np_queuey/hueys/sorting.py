from __future__ import annotations

import contextlib
import json
import pathlib
import shutil
import subprocess
from typing import Generator

import huey as _huey
# import np_config
import np_logging
import np_session
import np_tools
from typing_extensions import Literal

import np_queuey
import np_queuey.utils as utils
from np_queuey.jobs.sorting import Sorting

logger = np_logging.getLogger()

huey = _huey.SqliteHuey('sorting.db')

@huey.periodic_task(_huey.crontab(minute='*/1', strict=True))
def sort_outstanding_sessions() -> None:
    enqueued_job: Sorting | None = Sorting.next()
    if enqueued_job is None:
        logger.info('No outstanding sessions to sort')
        return
    logger.info('Found session %s for sorting', enqueued_job.session)
    run_sorting(enqueued_job)

@contextlib.contextmanager
def set_flags(job: Sorting) -> Generator[None, None, None]:
    try:
        np_logging.web('np_queuey').info('Starting sorting %s', job.session)
        job.set_started()
        yield
    except Exception as exc:
        job.set_errored(exc)
        np_logging.web('np_queuey').exception('Exception during sorting %s', job.session)
        return
    else:
        job.set_finished()
        np_logging.web('np_queuey').info('Sorting completed successfully for %s', job.session)

@huey.task()
def run_sorting(job: Sorting) -> None:
    with set_flags(job):
        remove_existing_sorted_folders_on_npexp(job)
        start_sorting(job)
        move_sorted_folders_to_npexp(job)
        remove_raw_data_on_acq_drives(job)

def probe_folders(job: Sorting) -> tuple[str]:
    return tuple(f'{job.session.folder}_probe{probe_letter}_sorted' for probe_letter in job.probes)

def remove_existing_sorted_folders_on_npexp(job: Sorting) -> None:
    for probe_folder in probe_folders(job):
        if (job.session.npexp_path / probe_folder).exists():
            logger.info('Removing existing sorted folder %s', probe_folder)
            shutil.rmtree(probe_folder, ignore_errors=True)

def start_sorting(job: Sorting) -> None:
    args = ' '.join((job.session.folder, ''.join(_ for _ in str(job.probes))))
    subprocess.run(fR'call c:\Users\svc_neuropix\Documents\GitHub\ecephys_spike_sorting\ecephys_spike_sorting\scripts\full_probe3X_from_extraction_nopipenv.bat %{args}%')
 
def move_sorted_folders_to_npexp(job: Sorting) -> None:
    """Move the sorted folders to the npexp drive
    Assumes D: processing drive - might want to move this to rig for
    specific-config.    
    """
    pattern = f'{job.session.folder}_probe?_sorted*'
    logger.info('Moving D:/%s to npexp', pattern)
    subprocess.run(['robocopy', 'D:', str(job.session.npexp_path), pattern, '/MOVE', '/E' '/R:0', '/W:0', '/MT:32'])       

def remove_raw_data_on_acq_drives(job: Sorting) -> None:
    for drive in ('A:', 'B:'):
        for path in pathlib.Path(drive).glob(f'{job.session.folder}*'):
            logger.info('Removing %r', path)
            shutil.rmtree(path, ignore_errors=True)
        


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=False)
