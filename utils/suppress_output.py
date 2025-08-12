import os
import sys
import contextlib
import ctypes

@contextlib.contextmanager
def suppress_output_python_level():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = devnull
            sys.stderr = devnull
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


@contextlib.contextmanager
def suppress_output_c_level():
    """
    Suppress output at the Python and C level (handles printf-style output from C extensions).
    Cross-platform.
    """
    null_device = 'nul' if os.name == 'nt' else '/dev/null'

    # Open devnull
    devnull = open(null_device, 'w')
    devnull_fd = devnull.fileno()

    # Flush Python buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Flush C buffers
    libc = ctypes.CDLL(None)
    if os.name != 'nt':
        libc.fflush(None)  # flush all open C output streams

    # Save original fds
    stdout_fd = sys.stdout.fileno()
    stderr_fd = sys.stderr.fileno()

    saved_stdout_fd = os.dup(stdout_fd)
    saved_stderr_fd = os.dup(stderr_fd)

    # Redirect stdout and stderr to devnull
    os.dup2(devnull_fd, stdout_fd)
    os.dup2(devnull_fd, stderr_fd)

    try:
        yield
    finally:
        # Restore fds
        os.dup2(saved_stdout_fd, stdout_fd)
        os.dup2(saved_stderr_fd, stderr_fd)
        os.close(saved_stdout_fd)
        os.close(saved_stderr_fd)
        devnull.close()

