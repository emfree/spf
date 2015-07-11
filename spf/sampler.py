import collections
import signal


class Sampler(object):
    def __init__(self, interval=0.001):
        self.interval = interval
        self._stack_counts = collections.defaultdict(int)
        self._started = False

    def start(self):
        if self._started:
            # Already started, do nothing.
            return
        try:
            signal.signal(signal.SIGALRM, self._sample)
            # Prevent 'interrupted system call' errors
            signal.siginterrupt(signal.SIGALRM, False)
        except ValueError:
            raise ValueError('Can only sample on the main thread')

        self._started = True
        # TODO(emfree): consider using signal.ITIMER_PROF instead?
        signal.setitimer(signal.ITIMER_REAL, self.interval, 0)

    def stop(self):
        try:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
        except ValueError:
            raise ValueError('Can only sample on the main thread')
        self._started = False

    def reset(self):
        self._stack_counts = collections.defaultdict(int)

    def _sample(self, signum, frame):
        stack = []
        while frame is not None:
            stack.append(self._format_frame(frame))
            frame = frame.f_back

        stack = ';'.join(reversed(stack))
        self._stack_counts[stack] += 1
        signal.setitimer(signal.ITIMER_REAL, self.interval, 0)

    def _format_frame(self, frame):
        return '{}({})'.format(frame.f_code.co_name,
                               frame.f_globals.get('__name__'))

    def stats(self):
        return self._stack_counts
