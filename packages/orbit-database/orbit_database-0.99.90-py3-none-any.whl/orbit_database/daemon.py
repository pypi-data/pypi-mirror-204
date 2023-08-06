"""

    Copyright (c) 2021 - Mad Penguin Consulting Ltd

"""
from orbit_database import Manager
from multiprocessing import Process
from posix_ipc import Semaphore, O_CREAT, BusyError, SignalError
from orbit_database import FullTextHandler
from signal import signal, SIGTERM
from time import sleep
from struct import unpack
from orbit_database import Progress, ProgressType
from os import getpid

try:
    from loguru import logger as log
except Exception:
    import logging as log


class Daemon:

    MAX_BATCH_SIZE = 5000

    def __init__(self, path, config, conf):
        self._path = path
        self._config = config
        self._conf = conf
        self._proc = Process(target=self.run, daemon=False)
        signal(SIGTERM, self.handler)

    def handler(self, *args):
        self._running = False

    def start(self):
        self._proc.start()

    def stop(self):
        self._proc.terminate()
        self._proc.join()

    def run(self):
        """
        """
        log.debug(f'[daemon] running (pid={getpid()}')
        self._running = True
        self._database = Manager().database('db', self._path, config=self._config)
        self._env = self._database.env
        self._semaphore = Semaphore(self._database.replication.semaphore_name, flags=O_CREAT)
        try:
            while self._running:
                try:
                    self._semaphore.acquire()
                except KeyboardInterrupt:
                    self._running = False
                    continue
                except (SignalError, BusyError):
                    sleep(0.1)
                    continue

                journal = self._database.replication.table
                documents = 0
                batch = journal.records()
                self._conf['outgoing'].put(Progress(ProgressType.MAX, 'INDX', batch))
                while journal.records():
                    keys = []
                    page_size = min(journal.records(), self.MAX_BATCH_SIZE)
                    documents += page_size
                    keys = [unpack('=Q', result.oid)[0] for result in journal.filter(page_size=page_size)]
                    log.debug(f'submitting batch of {page_size} documents to indexer (of {journal.records()})')
                    with FullTextHandler(self._path, self._database) as handler:
                        for key in keys:
                            self._conf['outgoing'].put(Progress(ProgressType.PROGRESS, 'INDX', 1))
                            handler.run(key)
                    journal.delete(keys)
                self._conf['outgoing'].put(Progress(ProgressType.FLUSH, 'INDX'))
                sleep(1)
                self._conf['outgoing'].put(Progress(ProgressType.END, 'INDX'))

                for i in range(documents - 1):
                    try:
                        self._semaphore.acquire(timeout=0)
                    except (SignalError, BusyError):
                        break
        except KeyboardInterrupt:
            pass
        log.debug(f'[daemon] stopped (pid={getpid()}')
