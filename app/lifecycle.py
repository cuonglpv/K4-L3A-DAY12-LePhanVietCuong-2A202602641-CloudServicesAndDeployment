"""Readiness state and cooperative SIGTERM/SIGINT handling."""

import signal


class Lifecycle:
    def __init__(self) -> None:
        self.shutting_down = False
        self._previous: dict[int, object] = {}

    def request_shutdown(self, signum=None, frame=None) -> None:
        self.shutting_down = True
        previous = self._previous.get(signum)
        if callable(previous):
            previous(signum, frame)

    def install(self) -> None:
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                self._previous[sig] = signal.getsignal(sig)
                signal.signal(sig, self.request_shutdown)
            except ValueError:
                return


lifecycle = Lifecycle()
