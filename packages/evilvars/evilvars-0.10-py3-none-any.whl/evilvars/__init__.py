import ctypes
import sys
import numpy as np


def go_to_purgatory(v, new):
    """
    Copies the bytes of a new value to a buffer of an existing value.

    Args:
        v (Any): The existing value to copy the bytes to.
        new (Any): The new value to copy the bytes from.

    Returns:
        bool: True if the bytes were successfully copied, False otherwise.
    """
    # tuple value to buffer

    buff = (ctypes.c_uint8 * (sys.getsizeof(v))).from_address(id(v))
    ax = np.frombuffer(buff, dtype=np.uint8)

    # new value to buffer
    buff2 = (ctypes.c_uint8 * (sys.getsizeof(new))).from_address(id(new))
    ax2 = np.frombuffer(buff2, dtype=np.uint8)

    # copying each byte from one buffer to the other one.
    for i in range(len(ax2)):
        try:
            ax[i] = ax2[i]
        except Exception:
            return False
    return True


