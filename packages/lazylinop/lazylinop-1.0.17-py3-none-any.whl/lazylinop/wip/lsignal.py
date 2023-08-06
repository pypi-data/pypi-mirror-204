"""
Module for signal processing related LazyLinearOps (work in progress).
"""
import numpy as np
import scipy as sp
from lazylinop import *


def fft(n, backend='scipy', **kwargs):
    """
    Returns a LazyLinearOp for the DFT of size n.

    Args:
        backend:
             'scipy' (default) or 'pyfaust' for the underlying computation of the DFT.
        kwargs:
            any key-value pair arguments to pass to the scipy of pyfaust dft backend
            (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html,
            https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600).

    Example:
        >>> #from lazylinop.wip.lsignal import fft
        >>> import numpy as np
        >>> lfft1 = fft(32, norm='ortho')
        >>> lfft2 = fft(32, backend='pyfaust')
        >>> x = np.random.rand(32)
        >>> np.allclose(lfft1 @ x, lfft2 @ x)
        True
        >>> y = lfft1 @ x
        >>> np.allclose(lfft1.H @ y, x)
        True
        >>> np.allclose(lfft2.H @ y, x)
        True

    """
    from scipy.fft import fft, ifft

    if backend == 'scipy':
        def scipy_scaling(kwargs):
            if 'norm' in kwargs:
                if kwargs['norm'] == 'ortho':
                    return 1
                elif kwargs['norm'] == 'forward':
                    return 1 / n
                elif kwargs['norm'] == 'backward':
                    return n
                else:
                    raise ValueError('Invalid norm value for scipy backend')
            else: # default is backward
                return n
        lfft = LazyLinearOperator(matmat=lambda x: fft(x, axis=0, **kwargs),
                                  rmatmat=lambda x: ifft(x, axis=0, **kwargs) *
                                  scipy_scaling(kwargs), shape=(n, n))
    elif backend == 'pyfaust':
        from pyfaust import dft
        lfft = aslazylinearoperator(dft(n, **kwargs))
    else:
        raise ValueError('backend '+str(backend)+' is unknown')
    return lfft

def fft2(shape, backend='scipy', **kwargs):
    """Returns a LazyLinearOp for the 2D DFT of size n.

    Args:
        shape:
             the signal shape to apply the fft2 to.
        backend:
             'scipy' (default) or 'pyfaust' for the underlying computation of the 2D DFT.
        kwargs:
             any key-value pair arguments to pass to the scipy or pyfaust dft backend
                (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft2.html,
                https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600).

    Example:

        >>> #from lazylinop.wip.lsignal import fft2
        >>> import numpy as np
        >>> lfft2_scipy = fft2((32, 32), norm='ortho')
        >>> lfft2_pyfaust = fft2((32, 32), backend='pyfaust')
        >>> x = np.random.rand(32, 32)
        >>> np.allclose(lfft2_scipy @ x.ravel(), lfft2_pyfaust @ x.ravel())
        True
        >>> y = lfft2_scipy @ x.ravel()
        >>> np.allclose(lfft2_scipy.H @ y, x.ravel())
        True
        >>> np.allclose(lfft2_pyfaust.H @ y, x.ravel())
        True

    """
    s = shape[0] * shape[1]
    if backend == 'scipy':
        from scipy.fft import fft2, ifft2
        return LazyLinearOperator(
            (s, s),
            matvec=lambda x: fft2(x.reshape(shape), **kwargs).ravel(),
            rmatvec=lambda x: ifft2(x.reshape(shape), **kwargs).ravel())
    elif backend == 'pyfaust':
        from pyfaust import dft
        K = kron(dft(shape[0], **kwargs), dft(shape[1], **kwargs))
        return LazyLinearOperator((s, s), matvec=lambda x: K @ x,
                                  rmatvec=lambda x: K.H @ x)
    else:
        raise ValueError('backend '+str(backend)+' is unknown')

def convolve2d(signal_shape, kernel, backend='full_scipy'):
    """
    Builds the LazyLinearOp to convolves a kernel and a signal of shape signal_shape in 2D.

    Args:
        signal_shape:
             the shape of the signal this operator will convolves.
        kernel: (numpy array)
             the kernel to convolve.
        backend:
             'pyfaust' or 'scipy' to use lazylinop.fft2(backend='scipy') or 'full_scipy' to use scipy.signal.convolve2d.

    Returns:
        The LazyLinearOp for the 2D convolution.

    Example:
        >>> import numpy as np
        >>> #from lazylinop.wip.lsignal import convolve2d
        >>> from scipy.signal import convolve2d as sconvolve2d
        >>> X =  np.random.rand(64, 64)
        >>> K = np.random.rand(4, 4)
        >>> C1 = convolve2d(X.shape, K, backend='scipy')
        >>> C2 = convolve2d(X.shape, K, backend='pyfaust')
        >>> C3 = convolve2d(X.shape, K, backend='full_scipy')
        >>> np.allclose((C1 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
        >>> np.allclose((C2 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
        >>> np.allclose((C3 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True

    """

    import pylops
    signal_shape = np.array(signal_shape)
    if 'full_scipy'== backend:
        from scipy.signal import convolve2d as sconvolve2d, correlate2d
        return \
                LazyLinearOperator(shape=(signal_shape.prod(),signal_shape.prod()),
                                   matvec=lambda x:
                                   sconvolve2d(x.reshape(signal_shape), kernel,
                                              'same').ravel(),
                                   rmatvec=lambda x: correlate2d(x.reshape(signal_shape), kernel,
                                              'same').ravel())
    # Compute the extended shape for input and kernel to overlap
    new_shape = np.array(signal_shape) + np.array(kernel.shape) - 1
    # It must be a power of two
    new_shape = 2 ** (1 + np.int64(np.log2(new_shape)))

    # Input will be centered in the extended shpae
    pad_x = pylops.Pad(
        dims=signal_shape,
        pad=(
            ((new_shape[0] - signal_shape[0])//2, (new_shape[0] - signal_shape[0])//2),
            ((new_shape[1] - signal_shape[1])//2, (new_shape[1] - signal_shape[1])//2)
            )
    )

    # Kernel is spread at corners in the extended shape
    # TODO: Not sure of what I am doing...
    w_topleft = kernel[kernel.shape[0]//2-1:, kernel.shape[0]//2-1:]
    w_topright = kernel[kernel.shape[0]//2-1:, :kernel.shape[0]//2-1]
    w_bottomleft = kernel[:kernel.shape[0]//2-1, kernel.shape[0]//2-1:]
    w_bottomright = kernel[:kernel.shape[0]//2-1, :kernel.shape[0]//2-1]

    w_topright = np.vstack((w_topright, np.zeros((w_topleft.shape[0]-w_topright.shape[0], w_topright.shape[1]))))
    w_bottomleft = np.vstack((np.zeros((w_topleft.shape[0]-w_bottomleft.shape[0], w_bottomleft.shape[1])), w_bottomleft))
    w_bottomright = np.vstack((np.zeros((w_topleft.shape[0]-w_bottomright.shape[0], w_bottomright.shape[1])), w_bottomright))

    W_padded = np.vstack((
        np.hstack((w_topleft, np.zeros((w_topleft.shape[0], new_shape[1]-w_topleft.shape[1]-w_topright.shape[1])), w_topright)),
        np.zeros((new_shape[0]-w_topleft.shape[0]-w_bottomleft.shape[0], new_shape[1])),
        np.hstack((w_bottomleft, np.zeros((w_bottomleft.shape[0], new_shape[1]-w_bottomleft.shape[1]-w_bottomright.shape[1])), w_bottomright))
        )).ravel()
    # TODO: This make lazylinop crash
    #W_padded = scipy.sparse.csc_array(W_padded).reshape((-1, 1))

    #dft2_ = dft2(new_shape)
    if backend == 'pyfaust':
        dft2_ = fft2(new_shape, backend=backend, normed=True, diag_opt=True)
    elif backend == 'scipy':
        dft2_ = fft2(new_shape, backend=backend, norm='ortho')
    else:
        raise ValueError('Unknown backend')
    # For Fourier normalization
    n = new_shape.prod()

    dft2_W = dft2_ @ W_padded

    # TODO: Make it more efficient using sparse or operator?

    return LazyLinearOperator(
        (signal_shape.prod(), signal_shape.prod()),
        matvec=lambda x: pad_x.H @ (1 / np.sqrt(n) * dft2_.H @ (n * dft2_W * (dft2_ @ pad_x @ x))),
                       # pad_x.H is used to reproject from the extended shpae to the original one
        rmatvec=lambda x: (pad_x.H @ (1 / np.sqrt(n) * dft2_.H @ (n * dft2_W * (dft2_ @ pad_x @ x[::-1]) )))[::-1]
         # TODO: something clever for the adjoint?
    )
def _binary_dtype(A_dtype, B_dtype):
    if isinstance(A_dtype, str):
        A_dtype = np.dtype(A_dtype)
    if isinstance(B_dtype, str):
        B_dtype = np.dtype(B_dtype)
    if A_dtype is None:
        return B_dtype
    if B_dtype is None:
        return A_dtype
    if A_dtype is None and B_dtype is None:
        return None
    kinds = [A_dtype.kind, B_dtype.kind]
    if A_dtype.kind == B_dtype.kind:
        dtype = A_dtype if A_dtype.itemsize > B_dtype.itemsize else B_dtype
    elif 'c' in [A_dtype.kind, B_dtype.kind]:
        dtype = 'complex'
    elif 'f' in kinds:
        dtype = 'double'
    else:
        dtype = A_dtype
    return dtype

def _is_power_of_two(n: int) -> bool:
    """return True if integer 'n' is a power of two.

    Args:
        :n: int

    Returns:
        bool
    """
    return ((n & (n - 1)) == 0) and n > 0


def flip(shape: tuple, start: int = 0, end: int = None):
    """Constructs flip lazy linear operator.

    Args:
        shape:
            tuple, shape of the input
        start:
            int, optional, flip from start, default is 0
        end:
            int, optional, stop flip (not included), default is None

    Returns:
        The flip LazyLinearOperator

    Raises:
        ValueError
            start is < 0
        ValueError
            start is > N
        ValueError
            end is < 1
        ValueError
            end is > N
        ValueError
            end is <= start

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.lsignal import flip
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> y = flip(x.shape, 0, 5) @ x
        >>> y
        array([4, 3, 2, 1, 0, 5, 6, 7, 8, 9])
        >>> y = flip(x.shape, 2, 7) @ x
        >>> y
        array([0, 1, 6, 5, 4, 3, 2, 7, 8, 9])
    """
    N = shape[0]
    if start < 0:
        raise ValueError("start is < 0.")
    if start > N:
        raise ValueError("start is > N.")
    if not end is None and end < 1:
        raise ValueError("end is < 1.")
    if not end is None and end > N:
        raise ValueError("end is > N.")
    if not end is None and end <= start:
        raise ValueError("end is <= start.")
    def _matmat(x, start, end):
        if x.ndim == 1:
            y = np.copy(x.reshape(x.shape[0], 1))
            x_is_1d = True
            y[start:end, 0] = x[end - 1 - (np.arange(start, end, 1) - start)]
        else:
            y = np.copy(x)
            x_is_1d = False
            y[start:end, :] = x[end - 1 - (np.arange(start, end, 1) - start), :]
        if x_is_1d:
            return y.ravel()
        else:
            return y
    return LazyLinearOperator(
        (N, N),
        matmat=lambda x: _matmat(x, start, N if end is None else end),
        rmatmat=lambda x: _matmat(x, start, N if end is None else end)
    )


def decimation(shape: tuple, start: int = 0, end: int = None, every: int = 2, axis: int = 0):
    """Constructs decimation lazy linear operator.
    If the shape of the signal is (N, M) the operator has a shape = ((end - start) / every, N).
    Lazy linear operator computes decimation per column.

    Args:
        shape:
            tuple, shape of the input
        start:
            int, optional, first element to keep, default is 0
        end:
            int, optional, stop decimation, default is None
        every:
            int, optional, keep element every this number, default is 2
        axis:
            int, optional
            if axis=0 (default) decimation per column, if axis=1 decimation per row.
            it does not apply if shape[1] is None.

    Returns:
        The decimation LazyLinearOperator

    Raises:
        ValueError
            every is < 1.
        ValueError
            axis expects 0 or 1.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.lsignal import decimation
        >>> x = np.full(10, 2)
        >>> x
        array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        >>> y = decimation(x.shape, 0, 10, every=2) @ x
        >>> y
        array([2, 2, 2, 2, 2])
        >>> X = np.arange(30).reshape((10, 3))
        >>> X
        array([[ 0,  1,  2],
               [ 3,  4,  5],
               [ 6,  7,  8],
               [ 9, 10, 11],
               [12, 13, 14],
               [15, 16, 17],
               [18, 19, 20],
               [21, 22, 23],
               [24, 25, 26],
               [27, 28, 29]])
        >>> decimation(X.shape, 0, 10, every=2) @ X
        array([[ 0,  1,  2],
               [ 6,  7,  8],
               [12, 13, 14],
               [18, 19, 20],
               [24, 25, 26]])
    """
    if every < 1:
        raise ValueError("every is < 1.")
    N = shape[0]
    if start < 0:
        raise ValueError("start is < 0.")
    if start > N:
        raise ValueError("start is > number of rows.")
    if not end is None and end < 1:
        raise ValueError("end is < 1.")
    if not end is None and end > N:
        raise ValueError("end is > number of rows.")
    if not end is None and end <= start:
        raise ValueError("end is <= start.")
    if axis != 0 and axis != 1:
        raise ValueError("axis expects 0 or 1.")
    def _matmat(x, start, end, every, axis):
        D = end - start
        if x.ndim == 1:
            y = np.zeros(((D + D % every) // every, 1), dtype=x.dtype)
            indices = np.arange(y.shape[0])
            y[indices, 0] = x[start + indices * every]
            return y.ravel()
        else:
            # TODO: benchmark decimation(Op.shape, 1, None, every=2) versus Op[1::2]
            if axis == 0:
                # decimation per column
                y = np.zeros(((D + D % every) // every, x.shape[1]), dtype=x.dtype)
                x_is_1d = False
                indices = np.arange(y.shape[0])
                y[indices, :] = x[start + indices * every, :]
                return y
            elif axis == 1:
                # decimation per row
                y = np.zeros((x.shape[0], (D + D % every) // every), dtype=x.dtype)
                x_is_1d = False
                indices = np.arange(y.shape[0])
                y[:, indices] = x[:, start + indices * every]
                return y
            else:
                pass
    def _rmatmat(x, start, end, every):
        D = end - start
        if x.ndim == 1:
            y = np.zeros(((D + D % every) // every, 1), dtype=x.dtype)
            indices = np.arange(y.shape[0])
            y[indices, 0] = x[start + indices * every]
            return y.ravel()
        else:
            y = np.zeros(((D + D % every) // every, x.shape[1]), dtype=x.dtype)
            x_is_1d = False
            indices = np.arange(y.shape[0])
            y[indices, :] = x[start + indices * every, :]
            return y
    last = N if end is None else end
    D = last - start
    # TODO: check the adjoint
    return LazyLinearOperator(
        ((D + D % every) // every, N),
        matmat=lambda x: _matmat(x, start, last, every, axis),
        rmatmat=lambda x: _rmatmat(x, start, last, every, axis)
    )


def _dwt_qmf_decimation(hfilter: np.ndarray, lfilter: np.ndarray, shape: tuple, filters: str = 'all'):
    """Constructs high and low filters plus decimation as lazy linear operator

    Args:
        :hfilter: np.ndarray, quadrature mirror high-pass filter
        :lfilter: np.ndarray, quadrature mirror low-pass filter
        :shape: tuple, shape of the input
        :filters: str, optional, apply low and high-pass filters (default)
                  if filters = 'low' apply only low-pass filter
                  if filters = 'high' apply only high-pass filter

    Returns:
        The high or/and low filter(s) plus decimation LazyLinearOperator.
    """
    # low-pass filter
    if filters == 'all' or filters == 'low':
        G = convolveND(shape, lfilter, mode='same', boundary='fill', method='lazy.scipy.signal.convolve')
    # high-pass filter
    if filters == 'all' or filters == 'high':
        H = convolveND(shape, hfilter, mode='same', boundary='fill', method='lazy.scipy.signal.convolve')
    # decimation and return vertical stack
    # pywavelet starts from 1
    if filters == 'all':
        if False:
            return vstack((G[1::2, :], H[1::2, :]))
        else:
            return vstack((decimation(G.shape, 1, None, 2) @ G, decimation(H.shape, 1, None, 2) @ H))
    else:
        if filters == 'low':
            if False:
                return G[1::2, :]
            else:
                return decimation(G.shape, 1, None, 2) @ G
        else:
            if False:
                return H[1::2, :]
            else:
                return decimation(H.shape, 1, None, 2) @ H


def _old_dwt(hfilter: np.ndarray, lfilter: np.ndarray, mode: str = 'zero', level: int = -1, **kwargs):
    """Constructs Discrete Wavelet Transform (DWT) as lazy linear operator.
    Because of the decomposition, the size of the data has to be a power of 2.

    Args:
        :hfilter: np.ndarray, quadratic mirror high-pass filter
        :lfilter: np.ndarray, quadratic mirror low-pass filter
        :mode: str, optional, see pywavelet documentation for more details, zero is default
        :level: int, decomposition level, by default (level < 0) return all
        :kwargs:
            :N: int, size of the input signal
            :shape: tuple, shape of the input signal

    Returns:
        The DWT LazyLinearOperator.

    Raises:
        ValueError
            size of the input is not a power of two.
    """
    if 'N' in kwargs.keys() and 'shape' in kwargs.keys():
        raise ValueError("function expects N or shape argument but not both.")
    if not ('N' in kwargs.keys() or 'shape' in kwargs.keys()):
        raise ValueError("function expects N or shape argument.")
    use_1d, use_2d = False, False
    for key, value in kwargs.items():
        if key == 'N':
            N = value
            use_1d = True
            if not _is_power_of_two(N):
                raise ValueError("size of the input is not a power of two.")
        elif key == 'shape':
            shape = value
            use_2d = True
            if not (_is_power_of_two(shape[0]) and _is_power_of_two(shape[1])):
                raise ValueError("size of the input is not a power of two.")
        else:
            pass
    if use_1d:
        # because of the decomposition the size
        # of the input has to be a power of 2^k
        K = int(np.log2(N))
        # first iteration of hih-pass and low-pass filters + decimation
        # return vertical stack of high-pass and low-pass filters lazy linear operator
        D = K if level < 1 else min(K, level)
        A = [None] * (D)
        A[0] = _dwt_qmf_decimation(hfilter, lfilter, (N, ))
        M = [N // 2]
        for i in range(1, D, 1):
            # low-pass filter output goes through low-pass and high-pass filters
            A[i] = block_diag(*[_dwt_qmf_decimation(hfilter, lfilter, (M[i - 1], )), eye(N - M[i - 1], n=N - M[i - 1], k=0)], mt=True) @ A[i - 1]
            M.append(M[i - 1] // 2)
        return A[len(A) - 1]
    if use_2d:
        # TODO, does not work.
        print("Work in progress ...")
        # image has been flattened vec = (row1, row2, ..., rowR) with size = R * C
        # number of rows, columns
        R, C = shape[0], shape[1]
        # low and high-pass filter for each row
        # A = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, )), use_pylops=True)
        G = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "low"), use_pylops=True)
        # result is vec = (gdrow1, gdrow2, ..., gdrowR)
        H = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "high"), use_pylops=True)
        print(H)
        # result is vec = (hdrow1, hdrow2, ..., hdrowR)
        # now we work on the columns
        # get first column
        # P[r, r * N / 2] = 1 where r = 0 to R
        
        # result is ((G_1, H_1), (G_2, H_2), ..., (G_R, H_R)) with size = R * C
        B = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (R, )), use_pylops=True)
        return H


def _dwt(hfilter: np.ndarray, lfilter: np.ndarray, mode: str = 'zero', level: int = -1, **kwargs):
    """Constructs Discrete Wavelet Transform (DWT) as lazy linear operator.
    Because of the decomposition, the size of the data has to be a power of 2.

    Args:
        hfilter:
            np.ndarray, quadratic mirror high-pass filter
        lfilter:
            np.ndarray, quadratic mirror low-pass filter
        mode:
            str, optional, see pywavelet documentation for more details, zero is default
        level:
            int, decomposition level, by default (level < 0) return all
        kwargs:
            in1:
                np.ndarray, input array
            shape:
                tuple, shape of the input array
            implementation:
                int, 0 or anything


    Returns:
        The DWT LazyLinearOperator.

    Raises:
        ValueError
            function expects in1 or shape argument but not both.
        ValueError
            function expects in1 or shape argument.
        ValueError
            first dimension of the input is not a power of two.
        ValueError
            second dimension of the input is not a power of two.
    """
    if 'in1' in kwargs.keys() and 'shape' in kwargs.keys():
        raise ValueError("function expects in1 or shape argument but not both.")
    if not ('in1' in kwargs.keys() or 'shape' in kwargs.keys()):
        raise ValueError("function expects in1 or shape argument.")
    use_1d, use_2d, implementation = False, False, 1
    for key, value in kwargs.items():
        if key == 'in1':
            shape = value.shape
            use_1d = bool(in1.ndim == 1)
            use_2d = bool(in1.ndim == 2)
        elif key == 'shape':
            shape = value
            use_1d = bool(not shape[0] is None and shape[1] is None)
            use_2d = bool(not shape[0] is None and not shape[1] is None)
        elif key == 'implementation':
            implementation = value
        else:
            pass
    N = shape[0]
    if not _is_power_of_two(N):
        raise ValueError("first dimension of the input is not a power of two.")
    if not shape[1] is None:
        if not _is_power_of_two(shape[1]):
            raise ValueError("second dimension of the input is not a power of two.")
    if use_1d:
        # because of the decomposition the size
        # of the input has to be a power of 2^k
        K = int(np.log2(N))
        # first iteration of hih-pass and low-pass filters + decimation
        # return vertical stack of high-pass and low-pass filters lazy linear operator
        D = K if level < 1 else min(K, level)
        A = eye(N, n=N, k = 0)
        M = [N]
        for i in range(D):
            # low-pass filter
            G = convolveND((M[i], ), lfilter, mode='same', boundary='fill', method='lazy.scipy.signal.convolve')
            # high-pass filter
            H = convolveND((M[i], ), hfilter, mode='same', boundary='fill', method='lazy.scipy.signal.convolve')
            # decimation and vertical stack (pywavelet starts from 1)
            if False:
                GH = vstack((G[1::2, :], H[1::2, :]))
            else:
                GH = vstack((decimation(G.shape, 1, None, 2) @ G, decimation(H.shape, 1, None, 2) @ H))
            if i == 0:
                # first level of decomposition
                # apply low and high-pass filters to the signal
                A = GH @ A
            else:
                # second and higher levels of decomposition
                # do not apply to the result of the high-pass filter
                tmp_eye = eye(N - M[i], n=N - M[i], k=0)
                # low-pass filter output goes through low-pass and high-pass filters
                # it corresponds to a lazy linear operator (second level of decomposition):
                # (GH 0) @ (G) @ input
                # (0 Id)   (H)
                A = block_diag(*[GH, tmp_eye], mt=True) @ A
            M.append(M[i] // 2)
        return A
    if use_2d:
        # TODO: does not work for decomposition level > 1.
        if implementation == 0:
            # image has been flattened (with img.flatten(order='C'))
            # the result is vec = (row1, row2, ..., rowR) with size = R * C
            # number of rows, columns
            R, C = shape[0], shape[1]
            # low-pass filter for each row + decimation
            # result is vec = (gdrow1, gdrow2, ..., gdrowR)
            G = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "low"), use_pylops=True)
            # high-pass filter for each row + decimation
            # result is vec = (hdrow1, hdrow2, ..., hdrowR)
            H = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "high"), use_pylops=True)
            # now we work on the columns
            # from 'C' order to 'F' order
            G = C_to_F_flatten((R, C // 2)) @ G
            H = C_to_F_flatten((R, C // 2)) @ H
            # low-pass for each column of the result of the previous low-pass filter
            GG = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "low"), use_pylops=True) @ G
            # high-pass for each column of the result of the previous low-pass filter
            HG = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "high"), use_pylops=True) @ G
            # low-pass for each column of the result of the previous high-pass filter
            GH = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "low"), use_pylops=True) @ H
            # high-pass for each column of the result of the previous high-pass filter
            HH = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "high"), use_pylops=True) @ H
            # from 'F' order to 'C' order
            GG = C_to_F_flatten((C // 2, R // 2)) @ GG
            HG = C_to_F_flatten((C // 2, R // 2)) @ HG
            GH = C_to_F_flatten((C // 2, R // 2)) @ GH
            HH = C_to_F_flatten((C // 2, R // 2)) @ HH
        else:
            # image has been flattened (with img.flatten(order='C'))
            # the result is vec = (row1, row2, ..., rowR) with size = R * C
            # number of rows, columns
            R, C = shape[0], shape[1]
            # low-pass filter for each row + decimation
            # high-pass filter for each row + decimation
            # first work on the row ...
            G = _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "low")
            H = _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "high")
            GH = vstack((G, H))
            A = kron(GH, GH, use_pylops=True)
            print(A, R, C)
            # ... and then work on the column
            
        # do we need to do from 'F' order to 'C' order ?
        # return -------
        #        |GG|HG|
        #        -------
        #        |GH|HH|
        #        -------
        # return vstack((hstack((GG, HG)), hstack((GH, HH))))
        # return ----
        #        |GG|
        #        |HG|
        #        |GH|
        #        |HH|
        #        ----
        return vstack((vstack((GG, HG)), vstack((GH, HH))))


def dwt(in1, hfilter: np.ndarray, lfilter: np.ndarray, mode: str = 'zero', level: int = 1) -> list:
    """multiple levels DWT, see _dwt function for more details.
    If in1 is a tuple the function returns a lazy linear operator.
    If in1 is a Numpy array the function returns the result of the DWT.

    Args:
        in1:
            tuple or np.ndarray, shape or array of the input
        hfilter:
            np.ndarray, quadratic mirror high-pass filter
        lfilter:
            np.ndarray, quadratic mirror low-pass filter
        mode:
            str, optional, see pywavelet documentation for more details, zero is default
        level:
            int, optional, decomposition level >= 1, 1 is the default value
            consider only decomposition level <= log2(in1.shape[0])

    Returns:
        [cAn, cDn, cDn-1, ..., cD2, cD1]: list, approximation and detail coefficients

    Raises:
        ValueError
            decomposition level must greater or equal to 1.
        Exception
            in1 expects tuple or np.ndarray.
    """
    if level < 1:
        raise ValueError("decomposition level must be greater or equal to 1.")
    if type(in1) is tuple:
        return _dwt(hfilter, lfilter, mode, 1, shape=in1)
    elif type(in1) is np.ndarray:
        if in1.ndim == 1:
            N = in1.shape[0]
            if level == 1:
                cAcD = _dwt(hfilter, lfilter, mode, 1, N=N) @ in1
                return [cAcD[:(N // 2)], cAcD[(N // 2):]]
            else:
                cAD = _dwt(hfilter, lfilter, mode, level, N=N) @ in1
                # max decomposition level
                K = int(np.log2(N))
                # build list of approximaton and details coefficients
                M = N // np.power(2, level)
                list_cAD = [cAD[:M], cAD[M:(2 * M)]]
                start = 2 * M
                for k in range(min(K, level) - 1 - 1, -1, -1):
                    M *= 2
                    list_cAD.append(cAD[start:(start + M)])
                    start += M
                return list_cAD
        if in1.ndim == 2:
            X, Y = in1.shape
            F = X * Y
            result = _dwt(hfilter, lfilter, mode, 1, shape=in1.shape) @ in1.flatten()
            return (result[:(F // 4)], (result[(F // 4):(2 * F // 4)], result[(2 * F // 4):(3 * F // 4)], result[(3 * F // 4):]))
    else:
        raise Exception("in1 expects tuple or np.ndarray.")


def C_to_F_flatten(shape: tuple, F_to_C: bool = False):
    """Constructs a lazy linear operator LOP such that LOP @ x
    is F order flattened from C order flattened x array.
    C and F order definition comes from Numpy flatten function.
    If F order to C order is True swap shape[0] and shape[1].

    Args:
        shape:
            tuple, shape of the image
        F_to_C:
            bool, optional
            if True F order to C order, if False (default) C order to F order.
            if C order to F order swap shape[0] and shape[1].

    Returns:
        LazyLinearOperator

    Raises:
        Exception
            shape expects a tuple (X, Y).

    Examples:
        >>> from lazylinop.wip.lsignal import C_to_F_flatten
        >>> import numpy as np
        >>> img = np.reshape(np.arange(16), newshape=(4, 4))
        >>> LOP = C_to_F_flatten(img.shape)
        >>> np.allclose(LOP @ img.flatten(order='C'), img.flatten(order='F'))
        True
        >>> img = np.reshape(np.arange(12), newshape=(3, 4))
        >>> LOP = C_to_F_flatten(img.shape)
        >>> np.allclose(LOP @ img.flatten(order='C'), img.flatten(order='F'))
        True
        >>> img = np.reshape(np.arange(12), newshape=(4, 3))
        >>> LOP = C_to_F_flatten(img.shape)
        >>> np.allclose(LOP @ img.flatten(order='C'), img.flatten(order='F'))
        True
    """
    if shape[0] is None or shape[1] is None:
        raise Exception("shape expects a tuple (X, Y).")
    if F_to_C:
        newshape = (shape[1], shape[0])
    else:
        newshape = (shape[0], shape[1])
    def _matvec(x, shape):
        X, Y = shape[0], shape[1]
        mv = np.zeros(X * Y, dtype=x.dtype)
        # get column c=0
        # P[r, r * Y] = 1 where r = 0 to X - 1
        # get column c=1
        # P[c * X + r, c + r * Y] = 1 where r = 0 to X - 1
        # ...
        for c in range(Y):
            mv[c * X + np.arange(X)] = x[np.arange(X) * Y + c]
        return mv
    def _rmatvec(x, shape):
        Y, X = shape[0], shape[1]
        mv = np.zeros(X * Y, dtype=x.dtype)
        for c in range(Y):
            mv[c * X + np.arange(X)] = x[np.arange(X) * Y + c]
        return mv
    X, Y = shape[0], shape[1]
    return LazyLinearOperator(
        (shape[0] * shape[1], shape[0] * shape[1]),
        matvec=lambda x: _matvec(x, newshape),
        rmatvec=lambda x: _rmatvec(x, newshape)
    )


def _ttoeplitz(c1: np.ndarray, r1: np.ndarray, K: int = None):
    """Constructs triangular Toeplitz matrix as lazy linear operator
    that will be used in the computation of the convolution.
    Shape of the lazy linear operator is computed from c1 and r1.

    Args:
        :c1: np.ndarray, first column of the Toeplitz matrix, shape is (R, )
        :r1: np.ndarray, first row of the Toeplitz matrix, shape is (C, )
             if r1 is not zero considers c1 to be zero except first element c1[0] = r1[0]
        :K: int, size of the kernel, if None (default) size is c1.shape[0]

    Returns:
        The triangular Toeplitz LazyLinearOperator
    """
    # matrix-vector product
    def _matvec(x, c1: np.ndarray, r1: np.ndarray) -> np.ndarray:
        # number of rows and columns (shape of Toeplitz matrix)
        R, C = c1.shape[0], r1.shape[0]
        nzr = np.count_nonzero(r1)
        if nzr > int(r1[0] != 0.0):
            # find the index 'sz' such that c1[i >= sz] = 0
            # all the elements with index greater or equal to 'sz' are zero
            if not K is None and K > 0:
                sz = K
            else:
                sz = 0
                for r in range(R):
                    nzr -= int(r1[r] != 0.0)
                    if nzr == 0:
                        sz = r + 1
                        break
            # print(r1[sz - 1], r1[sz], r1[sz + 1])
            if x.dtype == r1.dtype:
                vtype = r1.dtype
            else:
                if 'complex' in [x.dtype, r1.dtype]:
                    vtype = 'complex128'
                elif 'float' in [x.dtype, r1.dtype]:
                    vtype = 'float64'
                else:
                    pass
            mv = np.zeros(R, dtype=vtype)
            fr1 = r1[:sz]
            rmax = min(R, C - sz)
            # broadcasting
            mv[:rmax] = x[np.arange(0, rmax, 1)[:, None] + np.arange(0, sz, 1)] @ fr1
            # no broadcasting
            for r in range(rmax, min(R, C), 1):
                start = 0
                end = start + sz - min(0, (C - sz) - r)
                xstart = r
                xend = min(x.shape[0], xstart + end - start)
                mv[r] = fr1[start:end] @ x[xstart:xend]
        else:
            # find the index 'sz' such that c1[i >= sz] = 0
            # all the elements with index greater or equal to 'sz' are zero
            if not K is None and K > 0:
                sz = K
            else:
                nzc = np.count_nonzero(c1)
                sz = 0
                for r in range(R):
                    nzc -= int(c1[r] != 0.0)
                    if nzc == 0:
                        sz = r + 1
                        break
            # print(R, sz, c1[sz - 1], c1[sz], c1[sz + 1])
            if x.dtype == c1.dtype:
                vtype = c1.dtype
            else:
                if 'complex' in [x.dtype, c1.dtype]:
                    vtype = 'complex128'
                elif 'float' in [x.dtype, c1.dtype]:
                    vtype = 'float64'
                else:
                    pass
            import time
            tt = time.time()
            mv = np.zeros(R, dtype=vtype)
            txy = tt - time.time()
            fc1 = np.flip(c1[:sz])
            broadcasting = True
            if not broadcasting:
                for r in range(R):
                    start = max(0, (sz - 1) - r)
                    end = sz + min(0, C - (r + 1))
                    xend = min(C, r + 1)
                    xstart = max(0, xend - (end - start))
                    # t0 = time.time()
                    mv[r] = np.dot(fc1[start:end], x[xstart:xend])
                    # t0 = time.time() - t0
                    # t1 = time.time()
                    # mv[r] = np.sum(fc1[start:end] * x[xstart:xend])
                    # t1 = time.time() - t1
                    # print(t0, t1)
            if broadcasting:
                # tt = time.time()
                # no numpy broadcasting
                for r in range(sz):
                    start = max(0, (sz - 1) - r)
                    end = sz + min(0, C - (r + 1))#min(sz, start + C)
                    xend = min(C, r + 1)
                    xstart = max(0, xend - (end - start))
                    mv[r] = np.dot(fc1[start:end], x[xstart:xend])
                # print(sz, time.time() - tt)
                # numpy broadcasting
                step = sz
                middle = (C - sz) - (C - sz) % step
                if True:
                    tt = time.time()
                    mv[sz:(sz + middle)] = x[np.arange(0, middle, 1)[:, None] + np.arange(1, step + 1, 1)] @ fc1
                    # mv[sz:(sz + middle)] = np.sum(fc1 * x[np.arange(0, middle, 1)[:, None] + np.arange(1, step + 1, 1)], axis=1)
                    t1 = time.time() - tt
                else:
                    tt = time.time()
                    astep = np.arange(1, step + 1, 1)
                    vstep = np.arange(0, step, 1)[:, None]
                    for r in range(sz, sz + middle, step):
                        mv[r:(r + step)] = x[(vstep + (r - sz)) + astep] @ fc1
                    print(time.time() - tt)
                # no numpy broadcasting
                for r in range(middle, R, 1):
                    start = max(0, (sz - 1) - r)
                    end = sz + min(0, C - (r + 1))#min(sz, start + C)
                    xend = min(C, r + 1)
                    xstart = max(0, xend - (end - start))
                    mv[r] = np.dot(fc1[start:end], x[xstart:xend])
        return mv
    # matrix-matrix product
    def _matmat(x, c1: np.ndarray, r1: np.ndarray) -> np.ndarray:
        # number of rows and columns (shape of Toeplitz matrix)
        R, C = c1.shape[0], r1.shape[0]
        nzr = int(r1[0] != 0.0)
        nzr = np.count_nonzero(r1)
        if nzr > 0:
            # find the index 'sz' such that c1[i >= sz] = 0
            # all the elements with index greater or equal to 'sz' are zero
            if not K is None and K > 0:
                sz = K
            else:
                sz = 0
                for r in range(R):
                    nzr -= int(r1[r] != 0.0)
                    if nzr == 0:
                        sz = r + 1
                        break
            # print(r1[sz - 1], r1[sz], r1[sz + 1])
            if x.dtype == r1.dtype:
                vtype = r1.dtype
            else:
                if 'complex' in [x.dtype, r1.dtype]:
                    vtype = 'complex128'
                elif 'float' in [x.dtype, r1.dtype]:
                    vtype = 'float64'
                else:
                    pass
            mv = np.zeros((R, x.shape[0]), dtype=vtype)
            fr1 = r1[:sz]
            for r in range(min(R, C)):
                start = 0
                end = start + sz - min(0, (C - sz) - r)
                xstart = r
                xend = min(x.shape[0], xstart + end - start)
                mv[r, :] = fr1[start:end] @ x[xstart:xend, :]
        else:
            # find the index 'sz' such that c1[i >= sz] = 0
            # all the elements with index greater or equal to 'sz' are zero
            if not K is None and K > 0:
                sz = K
            else:
                nzc = np.count_nonzero(c1)
                sz = 0
                for r in range(R):
                    nzc -= int(c1[r] != 0.0)
                    if nzc == 0:
                        sz = r + 1
                        break
            # print(R, sz, c1[sz - 1], c1[sz], c1[sz + 1])
            if x.dtype == c1.dtype:
                vtype = c1.dtype
            else:
                if 'complex' in [x.dtype, c1.dtype]:
                    vtype = 'complex128'
                elif 'float' in [x.dtype, c1.dtype]:
                    vtype = 'float64'
                else:
                    pass
            mv = np.zeros((R, x.shape[0]), dtype=vtype)
            fc1 = np.flip(c1[:sz])
            # print(x.ndim, x.shape, x)
            for r in range(R):
                start = max(0, (sz - 1) - r)
                end = sz + min(0, C - (r + 1))
                xend = min(C, r + 1)
                xstart = max(0, xend - (end - start))
                mv[r, :] = fc1[start:end] @ x[xstart:xend, :]
        return mv
    return LazyLinearOperator(
        (c1.shape[0], r1.shape[0]),
        matvec=lambda x: _matvec(x, c1, r1),
        rmatvec=lambda x: _matvec(x, r1, c1)# ,
        # matmat=lambda X: _matmat(X, c1, r1),
        # rmatmat=lambda X: _matmat(X, r1, c1)
    )


def convolveND(in1, in2: np.ndarray, mode: str = 'full', boundary: str = 'fill', method: str = 'scipy.signal.convolve'):
    """return the lazy linear operator of convolution.

    Args:
        in1:
            tuple or np.ndarray, shape or input array of the input signal/image
        in2:
            np.ndarray, kernel to use for the convolution, shape is (K, ) for 1D and (K, L) for 2D
        mode:
            str, optional
            'full' computes convolution (input + padding)
            'valid' computes 'full' mode and extract centered output that does not depend on the padding. 
            'same' computes 'full' mode and extract centered output that has the same shape that the input.
            refer to Scipy documentation of scipy.signal.convolve function for more details
        boundary:
            str, optional, refer to Scipy documentation of scipy.signal.convolve2d function
        method:
            str, optional
             'auto' benchmark in progress
             'direct' direct computation
             'scipy.signal.convolve' (default) to use lazy encapsulation of Scipy.signal convolve function
             'scipy.linalg.toeplitz' to use lazy encapsulation of Scipy implementation of Toeplitz matrix
             'pyfaust.toeplitz' to use pyfaust implementation
             'lazylinop.toeplitz_for_convolution' to use Toeplitz for convolution
             'oa' to use lazylinop implementation of overlap-add method
             circular convolution methods:
             'circ.direct' direct computation
             'circ.scipy.linalg.circulant' use Scipy implementation of circulant matrix
             'circ.scipy.fft.fft' use Scipy implementation of FFT
             'circ.pyfaust.circ' use pyfaust implementation of circulant matrix
             'circ.pyfaust.dft' use pyfaust implementation of DFT

    Returns:
        LazyLinearOperator or np.ndarray

    Raises:
        Exception
        in1 expects tuple or np.ndarray.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.lsignal import convolveND
        >>> from scipy.signal import convolve, convolve2d
        >>> signal = np.random.rand(1024)
        >>> kernel = np.random.rand(32)
        >>> c1 = convolveND(signal.shape, kernel, mode='same', method='lazylinop.toeplitz_for_convolution') @ signal
        >>> c2 = convolveND(signal.shape, kernel, mode='same', method='pyfaust.toeplitz') @ signal
        >>> c3 = convolve(signal, kernel, mode='same', method='auto')
        >>> np.allclose(c1, c3)
        True
        >>> np.allclose(c2, c3)
        True
        >>> image = np.random.rand(6, 6)
        >>> kernel = np.random.rand(3, 3)
        >>> c1 = convolveND(image, kernel, mode='same', boundary='fill', method='scipy.linalg.toeplitz')
        >>> c2 = convolveND(image, kernel, mode='same', boundary='fill', method='pyfaust.toeplitz')
        >>> c3 = convolve2d(image, kernel, mode='same', boundary='fill')
        >>> np.allclose(c1, c3)
        True
        >>> np.allclose(c2, c3)
        True
        >>> signal = np.random.rand(32768)
        >>> kernel = np.random.rand(48)
        >>> c1 = convolveND(signal.shape, kernel, mode='same', method='circ.scipy.fft.fft') @ signal
        >>> c2 = convolveND(signal.shape, kernel, mode='same', method='circ.pyfaust.dft') @ signal
        >>> c3 = convolveND(signal, kernel, mode='same', method='circ.scipy.fft.fft')
        >>> c4 = convolveND(signal, kernel, mode='same', method='circ.pyfaust.dft')
        >>> np.allclose(c1, c2)
        True
        >>> np.allclose(c1, c3)
        True
        >>> np.allclose(c1, c4)
        True
    """
    if type(in1) is tuple:
        return _convolve(in2, mode=mode, boundary='fill', method=method, shape=in1)
    elif type(in1) is np.ndarray:
        shape = in1.shape
        if in1.ndim == 1:
            if mode == 'valid':
                X = shape[0] - in2.shape[0] + 1
            elif mode == 'same':
                X = shape[0]
            else:
                # full mode is default
                X = shape[0] + in2.shape[0] - 1
        elif in1.ndim == 2:
            if mode == 'valid':
                X, Y = shape[0] - in2.shape[0] + 1, shape[1] - in2.shape[1] + 1
            elif mode == 'same':
                X, Y = shape[0], shape[1]
            else:
                # full mode is default
                X, Y = shape[0] + in2.shape[0] - 1, shape[1] + in2.shape[1] - 1
        else:
            pass
        # apply lazy linear operator to flatten input
        if in1.ndim == 1:
            # no need to reshape
            return _convolve(in2, mode=mode, method=method, shape=in1.shape) @ in1.flatten()
        elif in1.ndim == 2:
            fconvolution = _convolve(in2, mode=mode, boundary='fill', method='lazylinop.toeplitz_for_convolution', shape=in1.shape) @ in1.flatten()
            # reshape the image to the input.ndim and return
            return fconvolution.reshape(X, Y)
        else:
            pass
    else:
        raise Exception("in1 expects tuple or np.ndarray.")


def _convolve(kernel: np.ndarray, mode: str = 'full', boundary: str = 'fill', method: str = 'scipy.signal.convolve', **kwargs):
    """If shape of the signal has been passed return Lazy Linear Operator that corresponds
    to the convolution with the kernel. If signal has been passed return the convolution result.
    The function determines if it is 1D or 2D convolution based on the number of dimensions of the kernel.

    Args:
        :kernel: np.ndarray, kernel to use for the convolution, shape is (K, ) for 1D and (K, L) for 2D
        :mode: str, optional
            'full' computes convolution (input + padding)
            'valid' computes 'full' mode and extract centered output that does not depend on the padding. 
            'same' computes 'full' mode and extract centered output that has the same shape that the input.
            refer to Scipy documentation of scipy.signal.convolve function for more details
        :boundary: str, optional,
            refer to Scipy documentation of scipy.signal.convolve2d function
        :method: str, optional
             'auto' benchmark in progress
             'direct' direct computation
             'scipy.signal.convolve' (default) to use lazy encapsulation of Scipy.signal convolve function
             'scipy.linalg.toeplitz' to use lazy encapsulation of Scipy implementation of Toeplitz matrix
             'pyfaust.toeplitz' to use pyfaust implementation
             'lazylinop.toeplitz_for_convolution' to use Toeplitz for convolution
             'oa' to use lazylinop implementation of overlap-add method
             circular convolution methods:
             'circ.direct' direct computation
             'circ.scipy.linalg.circulant' use Scipy implementation of circulant matrix
             'circ.scipy.fft.fft' use Scipy implementation of FFT
             'circ.pyfaust.circ' use pyfaust implementation of circulant matrix
             'circ.pyfaust.dft' use pyfaust implementation of DFT
        :kwargs:
            shape (tuple) of the signal to convolve with kernel.
            input_array (np.ndarray) to convolve with kernel, shape is (S, ) or (S, T)

    Returns:
        LazyLinearOperator or np.ndarray

    Raises:
        ValueError
        number of dimensions of the signal and/or the kernel is greater than one.
        ValueError
        mode is either 'full' (default), 'valid' or 'same'
        ValueError
        boundary is either 'fill' (default), 'wrap' or 'symm'
        ValueError
        shape or input_array are expected
        ValueError
        expect shape or input_array not both.
        ValueError
        size of the kernel is greater than the size of signal.
        ValueError
        method 'scipy.linalg.toepliz' expects input_array for 2d kernel.
        ValueError
        method is not in:
             'direct',
             'lazy.scipy.signal.convolve',
             'scipy.linalg.toeplitz',
             'pyfaust.toeplitz',
             'lazylinop.toeplitz_for_convolution',
             'oa',
             'circ.direct',
             'circ.scipy.linalg.circulant',
             'circ.scipy.fft.fft',
             'circ.pyfaust.circ',
             'circ.pyfaust.dft'
        Exception
        circular convolution method expects mode='same'.
    """
    if not mode in ['full', 'valid', 'same']:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'")
    if not boundary in ['fill', 'wrap', 'symm']:
        raise ValueError("boundary is either 'fill' (default), 'wrap' or 'symm'")
    if not 'shape' in kwargs.keys() and not 'input_array' in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if 'shape' in kwargs.keys() and 'input_array' in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both.")
    if method == 'scipy.linalg.toeplitz' and kernel.ndim == 2 and not 'input_array' in kwargs.keys():
        raise ValueError("method 'scipy.linalg.toepliz' expects input_array for 2d kernel.")
    if not method in ['direct', 'lazy.scipy.signal.convolve', 'scipy.linalg.toeplitz', 'pyfaust.toeplitz', 'lazylinop.toeplitz_for_convolution', 'oa', 'circ.direct', 'circ.scipy.linalg.circulant', 'circ.scipy.fft.fft', 'circ.pyfaust.circ', 'circ.pyfaust.dft']:
        raise ValueError("method is not in ['direct', 'lazy.scipy.signal.convolve', 'scipy.linalg.toeplitz', 'pyfaust.toeplitz', 'lazylinop.toeplitz_for_convolution', 'oa', 'circ.direct', 'circ.scipy.linalg.circulant', 'circ.scipy.fft.fft', 'circ.pyfaust.circ', 'circ.pyfaust.dft'].")
    if 'circ.' in method and mode != 'same':
        raise Exception("circular convolution method expects mode='same'.")

    # check if signal/image has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop = True
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            if kernel.ndim == 1:
                # signal
                signal = np.copy(value)
                shape = signal.shape
            elif kernel.ndim == 2:
                # image
                image = np.copy(value)
                shape = image.shape
            else:
                pass
        else:
            pass        

    # convolution
    if kernel.ndim == 1:
        kernel_is_complex = bool('complex' in kernel.dtype.str)
        # 1D convolution
        if shape[0] <= 0 or kernel.ndim != 1:
            raise ValueError("number of dimensions of the signal and/or the kernel is not equal to 1.")
        K = kernel.shape[0]
        S = shape[0]
        if K > S:
            raise ValueError("size of the kernel is greater than the size of the signal.")
        # lazy linear operator
        # check which method is asked for
        if method == 'direct':
            def _matvec(kernel, signal):
                K = kernel.shape[0]
                S = signal.shape[0]
                O = S + K - 1
                output = np.full(O, 0.0)
                pkernel = np.pad(kernel, (0, O - K), mode='constant', constant_values=0.0)
                psignal = np.pad(signal, (0, O - S), mode='constant', constant_values=0.0)
                # y[n] = sum(h[k] * s[n - k], k, 0, n)
                for i in range(O):
                    # print(i, O, pkernel.shape, psignal.shape, pkernel[:(i + 1)].shape, psignal[np.subtract(i, np.arange(i + 1))].shape)
                    output[i] = np.dot(pkernel[:(i + 1)], psignal[np.subtract(i, np.arange(i + 1))])
                return output
            def _rmatvec(kernel, signal):
                K = kernel.shape[0]
                S = signal.shape[0]
                O = S + K - 1
                output = np.full(O, 0.0)
                pkernel = np.pad(kernel, (0, O - K), mode='constant', constant_values=0.0)
                psignal = np.pad(signal, (0, O - S), mode='constant', constant_values=0.0)
                # y[n] = sum(h[k] * s[k + n], k, 0, K - 1)
                for i in range(O):
                    output[i] = np.dot(pkernel[:(i + 1)], psignal[np.add(i, np.arange(i + 1))])
                return output
            LO = LazyLinearOperator(
                (S + K - 1, S),
                matvec=lambda x: _matvec(kernel, x),
                rmatvec=lambda x: _rmatvec(kernel, x)
            )
        elif method == 'lazy.scipy.signal.convolve':
            LO = LazyLinearOperator(
                (S + K - 1, S),
                matvec=lambda x: sp.signal.convolve(x, kernel, mode='full', method='auto'),
                rmatvec=lambda x: sp.signal.correlate(x, kernel, mode='full', method='auto')
            )
        elif method == 'scipy.linalg.toeplitz':
            LO = LazyLinearOperator(
                (S + K - 1, S),
                matvec=lambda x: sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1))) @ x,
                rmatvec=lambda x: sp.linalg.toeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1))).T.conj() @ x
            )
        elif method == 'pyfaust.toeplitz':
            from pyfaust import toeplitz
            LO = LazyLinearOperator(
                (S + K - 1, S),
                matvec=lambda x: toeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1)), diag_opt=False) @ x if kernel_is_complex or 'complex' in x.dtype.str else np.real(toeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1)), diag_opt=False) @ x),
                rmatvec=lambda x: toeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1)), diag_opt=False).T.conj() @ x if kernel_is_complex or 'complex' in x.dtype.str else np.real(toeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1)), diag_opt=False).T.conj() @ x)
            )
        elif method == 'lazylinop.toeplitz_for_convolution':
            LO = _ttoeplitz(np.pad(kernel, (0, S - 1)), np.pad([kernel[0]], (0, S - 1)), K)
        elif method == 'oa':
            LO = LazyLinearOperator(
                (S + K - 1, S),
                matvec=lambda x: _oaconvolve(kernel, 'full', shape=shape) @ x if kernel_is_complex or 'complex' in x.dtype.str else np.real(_oaconvolve(kernel, 'full', shape=shape) @ x),
                rmatvec=lambda x: _oaconvolve(kernel, 'full', shape=shape).T.conj() @ x if kernel_is_complex or 'complex' in x.dtype.str else np.real(_oaconvolve(kernel, 'full', shape=shape).T.conj() @ x)
            )
        elif 'circ.' in method:
            tmp_method = method.replace('circ.', '')
            LO = LazyLinearOperator(
                (S, S),
                matvec=lambda x: _circconvolve(kernel, tmp_method, shape=shape) @ x if kernel_is_complex or 'complex' in x.dtype.str else np.real(_circconvolve(kernel, tmp_method, shape=shape) @ x),
                rmatvec=lambda x: _circconvolve(kernel, tmp_method, shape=shape).T.conj() @ x if kernel_is_complex or 'complex' in x.dtype.str else np.real(_circconvolve(kernel, tmp_method, shape=shape).T.conj() @ x)
            )
        else:
            pass
        # compute full mode and extract what we need
        dim = {}
        dim['full'] = S + K - 1
        dim['valid'] = S - K + 1
        dim['same'] = S
        if mode == 'valid' or mode == 'same':
            start = (S + K - 1) // 2 - dim[mode] // 2
            if return_lazylinop:
                return LO[start:(start + dim[mode]), :S]
            else:
                return LO[start:(start + dim[mode]), :S] @ signal
        else:
            if return_lazylinop:
                return LO
            else:
                return LO @ signal
    elif kernel.ndim == 2:
        # 2D convolution
        if shape[1] <= 0:
            raise ValueError("number of dimensions of the image is not equal to 2.")
        M, N = shape[0], shape[1]
        K, L = kernel.shape
        if K > M or L > N:
            raise ValueError("size of the kernel is greater than the size of the image.")
        # shape of the output image (full mode)
        X, Y = M + K - 1, N + L - 1
        # write 2d convolution as a sum of Kronecker products:
        # convolution(kernel, image) = sum(kron(A_i, B_i), i, 1, M)
        # A_i is a Toeplitz matrix.
        # first column is 0 except for element i that is 1
        # first row is 0
        # B_i is a Toeplitz matrix build from the kernel.
        # first column is the i-th row of the kernel
        # first row is 0
        lops = [None] * K
        for i in range(K):
            # does it need Toeplitz construction because it looks like an eye matrix ?
            if method == 'scipy.linalg.toeplitz':
                lops[i] = kron(eye(M + K - 1, n=M, k=-i), sp.linalg.toeplitz(pad_kernel[i, :], np.full(N, 0.0)), use_pylops=True)
            elif method == 'pyfaust.toeplitz':
                from pyfaust import toeplitz
                lops[i] = kron(eye(M + K - 1, n=M, k=-i), toeplitz(np.pad(kernel[i, :], (0, N - 1), mode='constant', constant_values=0.0), np.pad([kernel[i, 0]], (0, N - 1)), diag_opt=True), use_pylops=True)
            elif method == 'lazylinop.toeplitz_for_convolution':
                lops[i] = kron(eye(M + K - 1, n=M, k=-i), _ttoeplitz(np.pad(kernel[i, :], (0, N - 1), mode='constant', constant_values=0.0), np.full(N, 0.0), K), use_pylops=True)
            else:
                lops[i] = kron(eye(M + K - 1, n=M, k=-i), sp.linalg.toeplitz(np.pad(kernel[i, :], (0, N - 1), mode='constant', constant_values=0.0), np.full(N, 0.0)), use_pylops=True)
        # return lazy linear operator or the convolution result
        mt, af = False, False
        if return_lazylinop:
            # if backend == 'scipy':
            #     if mode == 'valid':
            #         i1 = M - K + 1
            #         i2 = N - L + 1
            #     elif mode == 'same':
            #         i1 = M
            #         i2 = N
            #     else:
            #         i1 = M + K - 1
            #         i2 = N + L - 1
            #     return LazyLinearOperator(
            #         (i1 * i2, M * N),
            #         matvec=lambda x: sp.signal.convolve2d(x, kernel, mode=mode, boundary='fill'),
            #         rmatvec=lambda x: sp.signal.correlate2d(x, kernel, mode=mode, boundary='fill')
            #     )
            # A = [[], []]
            # for i in range(len(lops)):
            #     A[i % 2].append(lops[i])
            if mode == 'valid' or mode == 'same':
                if mode == 'valid':
                    # compute full mode and extract what we need
                    # number of rows to extract is M - K + 1 (centered)
                    # number of columns to extract is N - L + 1 (centered)
                    i1 = (X - (M - K + 1)) // 2
                    s1 = i1 + M - K + 1
                    i2 = (Y - (N - L + 1)) // 2
                    s2 = i2 + N - L + 1
                    # indices = np.add(np.outer(np.multiply(Y, np.arange(i1, s1)), np.full(M - K + 1, 1)), np.outer(np.full(M - K + 1, 1), np.arange(i1, s1))).flatten()
                    indices = ((np.arange(X * Y).reshape(X, Y))[i1:s1, i2:s2]).ravel()
                else:
                    # keep middle of the full mode
                    # number of rows to extract is M (centered)
                    # number of columns to extract is N (centered)
                    i1 = (X - M) // 2
                    s1 = i1 + M
                    i2 = (Y - N) // 2
                    s2 = i2 + N
                    # indices = np.add(np.outer(np.multiply(Y, np.arange(i1, s1)), np.full(M, 1)), np.outer(np.full(M, 1), np.arange(i1, s1))).flatten()
                    indices = ((np.arange(X * Y).reshape(X, Y))[i1:s1, i2:s2]).ravel()
                if K <= 128:
                    return sum(*lops, mt=mt, af=af)[indices, :]
                elif K <= 256:
                    return sum(sum(*lops[:(K // 2)], mt=mt, af=af), sum(*lops[(K // 2):K], mt=mt, af=af))[indices, :]
                else:
                    return sum(sum(sum(*lops[:(K // 4)], mt=mt, af=af), sum(*lops[(K // 4):(2 * (K // 4))], mt=mt, af=af)), sum(sum(*lops[(2 * (K // 4)):(3 * (K // 4))], mt=mt, af=af), sum(*lops[(3 * (K // 4)):K], mt=mt, af=af)))[indices, :]
                # return sum(*[sum(*A[0], mt=False, af=False), sum(*A[1], mt=False, af=False)], mt=True, af=False)[indices, :]
            else:
                # return full mode
                if K <= 128:
                    return sum(*lops, mt=mt, af=af)
                elif K <= 256:
                    return sum(sum(*lops[:(K // 2)], mt=mt, af=af), sum(*lops[(K // 2):K], mt=mt, af=af))
                else:
                    return sum(sum(sum(*lops[:(K // 4)], mt=mt, af=af), sum(*lops[(K // 4):(2 * (K // 4))], mt=mt, af=af)), sum(sum(*lops[(2 * (K // 4)):(3 * (K // 4))], mt=mt, af=af), sum(*lops[(3 * (K // 4)):K], mt=mt, af=af)))
                # print(A)
                # print(A[0])
                # print(A[1])
                # print(sum(*A[0], mt=False, af=False))
                # return sum(*[sum(*A[0], mt=False, af=False), sum(*A[1], mt=False, af=False)], mt=True, af=False)
        else:
            # return result of the 2D convolution
            if mode == 'valid' or mode == 'same':
                if mode == 'valid':
                    # compute full mode result and extract what we need
                    # number of rows to extract is M - K + 1
                    i1 = (X - (M - K + 1)) // 2
                    s1 = i1 + M - K + 1
                    i2 = (Y - (N - L + 1)) // 2
                    s2 = i2 + N - L + 1
                elif mode == 'same':
                    # keep middle of the full mode result
                    # number of rows to extract is M
                    # centered
                    i1 = (X - M) // 2
                    s1 = i1 + M
                    i2 = (Y - N) // 2
                    s2 = i2 + N
                return ((sum(*lops) @ image.flatten()).reshape(X, Y))[i1: s1, i2: s2]
            else:
                # compute full mode
                return (sum(*lops) @ image.flatten()).reshape(X, Y)


def _circconvolve(kernel: np.ndarray, method: str = 'auto', **kwargs):
    """This function returns circular convolution.
    Length of the signal and length of the kernel must be the same.
    If shape of the signal has been passed return Lazy Linear Operator
    that corresponds to the convolution with the kernel.
    If signal has been passed return the convolution result.
    The function only considers the first dimension of both kernel and signal.

    Args:
        :kernel: np.ndarray, kernel to use for the convolution
        :method: str, optional
            'auto' benchmark in progress
            'direct' direct computation
            'scipy.linalg.circulant' use Scipy implementation of the circulant matrix
            'scipy.fft.fft' use Scipy implementation of the FFT
            'pyfaust.circ' use pyfaust implementation of circulant matrix
            'pyfaust.dft' use pyfaust implementation of DFT
        :kwargs:
            shape (tuple) of the signal to convolve with kernel
            input_array (np.ndarray) to convolve with kernel, shape is (S, )

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        Exception
        kernel number of dimensions < 1.
        ValueError
        shape or input_array are expected.
        ValueError
        expect shape or input_array not both.
        ValueError
        method is not in ['auto', 'direct', 'scipy.linalg.circulant', 'scipy.fft.fft', 'pyfaust.circ', 'pyfaust.dft'].
        ValueError
        'scipy.fft.fft' and 'pyfaust.dft' methods expect the size of the signal to be a power of 2.
    """
    if not "shape" in kwargs.keys() and not "input_array" in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if "shape" in kwargs.keys() and "input_array" in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both")
    if not method in ['auto', 'direct', 'scipy.linalg.circulant', 'scipy.fft.fft', 'pyfaust.circ', 'pyfaust.dft']:
        raise ValueError("method is not in ['auto', 'direct', 'scipy.linalg.circulant', 'scipy.fft.fft', 'pyfaust.circ', 'pyfaust.dft']")

    # check if signal has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop, B = True, 2
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            if value.ndim == 1:
                # signal
                signal1d = np.copy(value)
                shape = signal1d.shape
            elif value.ndim > 1:
                # keep only the first dimension of the signal
                signal1d = np.copy(value[:1])
                shape = signal1d.shape
            else:
                pass
        else:
            pass

    # keep only the first dimension of the kernel
    if kernel.ndim == 1:
        kernel1d = np.copy(kernel)
    elif kernel.ndim > 1:
        kernel1d = np.copy(kernel[:1])
    else:
        raise Exception("kernel number of dimensions < 1.")

    # size of the kernel
    K = kernel1d.size
    # size of the signal
    S = shape[0]
    # if K != S:
    #     raise ValueError("size of the kernel differs from the size of the signal.")
    if not _is_power_of_two(S) and (method == 'scipy.fft.fft' or method == 'pyfaust.dft'):
        raise ValueError("'scipy.fft.fft' and 'pyfaust.dft' methods expect the size of the signal to be a power of 2.")
    # size of the output (full mode)
    O = S# + K - 1
    # pad the kernel
    if method == 'pyfaust.dft':
        P = O
        while not _is_power_of_two(P):
            P += 1
        pkernel = np.pad(kernel, (0, P - K), mode='constant', constant_values=0.0)
    else:
        pkernel = np.pad(kernel, (0, O - K), mode='constant', constant_values=0.0)

    if method == 'direct':
        def _matvec(kernel, signal):
            K = kernel.shape[0]
            S = signal.shape[0]
            O = S# + K - 1
            seq = np.arange(K)
            # output = np.full(O, 0.0)
            # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
            output = np.array([np.dot(kernel, signal[np.mod(np.subtract(i, seq), S)]) for i in range(O)])
            return output
        def _rmatvec(kernel, signal):
            K = kernel.shape[0]
            S = signal.shape[0]
            O = S# + K - 1
            seq = np.arange(K)
            # output = np.full(O, 0.0)
            # y[n] = sum(h[k] * s[k + n mod N], k, 0, K - 1)
            output = np.array([np.dot(kernel, signal[np.mod(np.add(seq, i), S)]) for i in range(O)])
            return output
        LO = LazyLinearOperator(
            (O, S),
            matvec=lambda x: _matvec(kernel1d, x),
            rmatvec=lambda x: _rmatvec(kernel1d, x)
        )
    elif method == 'scipy.linalg.circulant':
        LO = LazyLinearOperator(
            (O, S),
            # matvec=lambda x: sp.linalg.circulant(pkernel) @ np.pad(x, (0, K - 1)),
            # rmatvec=lambda x: sp.linalg.circulant(pkernel).T.conj() @ np.pad(x, (0, K - 1))
            matvec=lambda x: sp.linalg.circulant(np.pad(kernel, (0, O - K))) @ x,
            rmatvec=lambda x: sp.linalg.circulant(np.pad(kernel, (0, O - K))).T.conj() @ x
            # matvec=lambda x: np.pad(sp.linalg.circulant(kernel), ((0, S - 1), (0, K - 1))) @ np.pad(x, (0, K - 1)),
            # rmatvec=lambda x: np.pad(sp.linalg.circulant(kernel), ((0, S - 1), (0, K - 1))).T.conj() @ np.pad(x, (0, K - 1))
        )
    elif method == 'scipy.fft.fft':
        # Op @ signal
        # Op = FFT^-1 @ diag(FFT(kernel)) @ FFT
        # Op^H = FFT^H @ diag(FFT(kernel))^H @ (FFT^-1)^H
        # FFT^H equiv FFT^-1
        fft_kernel = sp.fft.fft(pkernel)
        ifft_kernel = sp.fft.ifft(pkernel)
        LO = LazyLinearOperator(
            (O, S),
            # matvec=lambda x: sp.fft.ifft(fft_kernel * sp.fft.fft(np.pad(x, (0, K - 1)))) if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(sp.fft.ifft(fft_kernel * sp.fft.fft(np.pad(x, (0, K - 1))))),
            # rmatvec=lambda x: sp.fft.ifft(ifft_kernel * sp.fft.fft(np.pad(x, (0, K - 1)))) if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(sp.fft.ifft(ifft_kernel * sp.fft.fft(np.pad(x, (0, K - 1)))))
            matvec=lambda x: sp.fft.ifft(fft_kernel * sp.fft.fft(x)) if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(sp.fft.ifft(fft_kernel * sp.fft.fft(x))),
            rmatvec=lambda x: sp.fft.ifft(ifft_kernel * sp.fft.fft(x)) if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(sp.fft.ifft(ifft_kernel * sp.fft.fft(x)))
        )
    elif method == 'pyfaust.circ':
        from pyfaust import circ
        LO = LazyLinearOperator(
            (O, S),
            # matvec=lambda x: circ(pkernel) @ np.pad(x, (K - 1)) if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(circ(pkernel) @ np.pad(x, (0, K - 1))),
            # rmatvec=lambda x: circ(pkernel).T.conj() @ np.pad(x, (0, K - 1)) if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(circ(pkernel).T.conj() @ np.pad(x, (0, K - 1))),
            matvec=lambda x: circ(pkernel) @ x if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(circ(pkernel) @ x),
            rmatvec=lambda x: circ(pkernel).T.conj() @ x if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(circ(pkernel).T.conj() @ x),
        )
    elif method == 'pyfaust.dft':
        from pyfaust import dft
        norm = False
        fft_kernel = dft(P, normed=norm) @ np.multiply(1.0 / P, pkernel)
        ifft_kernel = dft(P, normed=norm).T.conj() @ np.multiply(1.0 / P, pkernel)
        LO = LazyLinearOperator(
            (P, S),
            # matvec=lambda x: aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(fft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ zpad(((0, P - S)), x.shape) @ x if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(fft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ zpad(((0, P - S)), x.shape) @ x),
            # rmatvec=lambda x: aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(ifft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ zpad(((0, P - S)), x.shape) @ x if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(ifft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ zpad(((0, P - S)), x.shape) @ x)
            matvec=lambda x: aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(fft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ eye(P, n=S, k=0) @ x if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(fft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ eye(P, n=S, k=0) @ x),
            rmatvec=lambda x: aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(ifft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ eye(P, n=S, k=0) @ x if 'complex' in pkernel.dtype.str or 'complex' in x.dtype.str else np.real(aslazylinearoperator(dft(P, normed=norm).T.conj()) @ diag(ifft_kernel) @ aslazylinearoperator(dft(P, normed=norm)) @ eye(P, n=S, k=0) @ x)
        )[:O, :]
    else:
        # TODO: auto
        pass

    # convolution
    if return_lazylinop:
        # return lazy linear operator
        # keep the middle of full mode (centered)
        start = O // 2 - S // 2
        return LO[start:(start + S), :]
    else:
        # return result of the convolution
        # keep the middle of full mode (centered)
        start = O // 2 - S // 2
        return (LO @ signal1d)[start:(start + S)]


def _oaconvolve(kernel: np.ndarray, mode: str = 'full', **kwargs):
    """This function implements overlap-add method for convolution.
    If shape of the signal has been passed return Lazy Linear Operator
    that corresponds to the convolution with the kernel.
    If signal has been passed return the convolution result.
    The function only considers the first dimension of both kernel and signal.

    Args:
        :kernel: np.ndarray, kernel to use for the convolution
        :mode: str, optional
            'full' computes convolution (input + padding)
            'valid' computes 'full' mode and extract centered output that does not depend on the padding
            'same' computes 'full' mode and extract centered output that has the same shape that the input
            refer to Scipy documentation of scipy.signal.convolve function for more details
        :kwargs:
            shape (tuple) of the signal to convolve with kernel
            input_array (np.ndarray) to convolve with kernel, shape is (S, )
            block_size (int) size of the block unit (a power of two)

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        Exception
        kernel number of dimensions < 1.
        ValueError
        mode is either 'full' (default), 'valid' or 'same'
        ValueError
        shape or input_array are expected
        ValueError
        expect shape or input_array not both.
        ValueError
        block_size argument expects a value that is a power of two.
        ValueError
        block_size must be greater than the kernel size.
        ValueError
        size of the kernel is greater than the size of the signal.
    """
    if not mode in ['full', 'valid', 'same']:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'")
    if not "shape" in kwargs.keys() and not "input_array" in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if "shape" in kwargs.keys() and "input_array" in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both.")

    # check if signal has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop, B = True, 2
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            if value.ndim == 1:
                # signal
                signal1d = np.copy(value)
                shape = signal1d.shape
            elif value.ndim > 1:
                # keep only the first dimension of the signal
                signal1d = np.copy(value[:1])
                shape = signal1d.shape
            else:
                pass
        elif key == "block_size":
            B = value
            if B <= 0 or not _is_power_of_two(B):
                raise ValueError("block_size argument expects a value that is a power of two.")
        else:
            pass

    # keep only the first dimension of the kernel
    if kernel.ndim == 1:
        kernel1d = np.copy(kernel)
    elif kernel.ndim > 1:
        kernel1d = np.copy(kernel[:1])
    else:
        raise Exception("kernel number of dimensions < 1.")

    # size of the kernel
    K = kernel1d.size
    # size of the signal
    S = shape[0]
    if K > S:
        raise ValueError("size of the kernel is greater than the size of the signal.")
    # size of the output (full mode)
    O = S + K - 1

    # block size B, number of blocks X=S/B
    if not "block_size" in kwargs.keys():
        # no input for the block size: compute a value
        B = K
        while B < min(S, 2 * K) or not _is_power_of_two(B):
            B += 1
    else:
        if B < K:
            raise ValueError("block_size must be greater or equal to the kernel size.")
    # number of blocks
    R = S % B
    X = (S + R) // B

    # create linear operator LO that will be applied to all the blocks
    # LO = ifft(np.diag(fft(kernel)) @ fft(signal))
    # use Kronecker product between identity matrix and LO to apply to all the blocks
    # use pyfaust_multi_pad to pad each block
    # if the size of the signal is S the size of the result is 2*S
    norm = False
    from pyfaust import dft
    fft_kernel = dft(2 * B, normed=norm) @ np.multiply(1.0 if norm else 1.0 / (2 * B), np.pad(kernel1d, ((0, 2 * B - K))))
    LO = overlap_add(B, 2 * X) @ kron(
        eye(X, n=X, k=0),
        aslazylinearoperator(dft(2 * B, normed=norm).T.conj()) @ diag(
            fft_kernel, k=0
        ) @ aslazylinearoperator(
            dft(2 * B, normed=norm)
        ) @ multi_pad(B, 1),
        use_pylops=True
    )

    is_complex = 'complex' in kernel1d.dtype.str or (not return_lazylinop and 'complex' in signal1d.dtype.str)

    # convolution
    if return_lazylinop:
        # return lazy linear operator
        if mode == 'valid' or mode == 'same':
            if mode == 'valid':
                # compute full mode and extract what we need
                extract = S - K + 1
                start = O // 2 - extract // 2
            else:
                # keep the middle of full mode (centered)
                extract = S
                start = O // 2 - extract // 2
            return LazyLinearOperator(
                (extract, S),
                matvec=lambda x: LO[start:(start + extract), :] @ x if is_complex else np.real(LO[start:(start + extract), :] @ x),
                rmatvec=lambda x: LO[start:(start + extract), :].T.conj() @ x if is_complex else np.real(LO[start:(start + extract), :].T.conj() @ x)
            )
        else:
            # compute full mode
            return LazyLinearOperator(
                (O, S),
                matvec=lambda x: LO[:O, :] @ x if is_complex else np.real(LO[:O, :] @ x),
                rmatvec=lambda x: LO[:O, :].T.conj() @ x if is_complex else np.real(LO[:O, :].T.conj() @ x)
            )
    else:
        # return result of the convolution
        psignal = np.pad(signal1d, ((0, R)))
        if mode == 'valid' or mode == 'same':
            if mode == 'valid':
                # compute full mode and extract what we need
                extract = S - K + 1
                start = O // 2 - extract // 2
            else:
                # keep the middle of full mode (centered)
                extract = S
                start = O // 2 - extract // 2
            return (LO @ psignal)[start:(start + extract)] if is_complex else np.real((LO @ psignal)[start:(start + extract)])
        else:
            # compute full mode
            return (LO @ psignal)[:O] if is_complex else np.real((LO @ psignal)[:O])


def multi_pad(L: int, X: int, signal = None):
    """return a lazy linear operator or np.ndarray mp to pad each block of a signal.
    If you apply this operator to a vector of length L * X the output
    will be of length 2 * L * X. The operator looks like:
    mp = (1 0 0 0 ... 0)
    (0 0 0 0 ... 0)
    (0 1 0 0 ... 0)
    (0 0 0 0 ... 0)
    (0 0 1 0 ... 0)
    (.           .)
    (.           .)
    (.           .)
    (.           1)
    (0 0 0 0 ... 0)

    Args:
        L:
            int, block size
        X:
            int, number of blocks
        signal:
            np.ndarray, optional
            if signal is numpy array apply overlap-add linear operator (default is None).

    Returns:
        LazyLinearOp or np.ndarray

    Examples:
        >>> from lazylinop.wip.lsignal import multi_pad
        >>> import numpy as np
        >>> signal = np.full(5, 1.0)
        >>> signal
        array([1., 1., 1., 1., 1.])
        >>> y = multi_pad(1, 5) @ signal
        >>> y
        array([1., 0., 1., 0., 1., 0., 1., 0., 1., 0.])
    """
    mp = np.zeros((2 * X, X))
    indices = np.arange(0, 2 * X, 2)
    mp[indices, np.floor_divide(indices, 2)] = 1
    if type(signal) is np.ndarray:
        return kron(mp, eye(L, n=L, k=0), use_pylops=True) @ signal
    else:
        return kron(mp, eye(L, n=L, k=0), use_pylops=True)


def overlap_add(L: int, X: int, signal = None):
    """return overlap-add linear operator or result of the overlap-add.
    If signal is a numpy array return the result of the matrix-vector product.
    The overlap-add linear operator adds block i > 0 (of size L) with
    block i + 1 (of size L). Of note, block i = 0 (of size L) does not change.

    Args:
        L:
            int, block size
        X:
            int, number of blocks
        signal:
            np.ndarray, optional
            if signal is numpy array apply overlap-add linear operator (default is None).

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        ValueError
        L is strictly positive.
        ValueError
        X is strictly positive.
        ValueError
        number of columns of the linear operator is not equal to the size of the signal.

    Examples:
        >>> from lazylinop.wip.lsignal import overlap_add
        >>> import numpy as np
        >>> signal = np.full(16, 1.0)
        >>> oa1 = overlap_add(1, 16, None) @ signal
        >>> oa2 = overlap_add(1, 16, signal)
        >>> np.allclose(oa1, oa2)
        True
        >>> oa1
        array([1., 2., 2., 2., 2., 2., 2., 2., 1., 0., 0., 0., 0., 0., 0., 0.])
        >>> oa1 = overlap_add(2, 8, None) @ signal
        >>> oa2 = overlap_add(2, 8, signal)
        >>> np.allclose(oa1, oa2)
        True
        >>> oa1
        array([1., 1., 2., 2., 2., 2., 2., 2., 1., 1., 0., 0., 0., 0., 0., 0.])
    """
    if L <= 0:
        raise ValueError("L is strictly positive.")
    if X <= 0:
        raise ValueError("X is strictly positive.")
    if (X % 2) != 0:
        raise ValueError("number of blocks is not a multiple of 2.")
    if type(signal) is np.ndarray and (X * L) != signal.size:
        raise ValueError("L * X is not equal to the size of the signal.")
    def _matmat(x, L, X):
        rnz = X // 2 + 1
        if x.ndim == 1:
            x_is_1d = True
            y = np.reshape(x, newshape=(x.size, 1))
        else:
            x_is_1d = False
            y = np.copy(x)
        mv = np.full((X, y.shape[1]), 0.0, dtype=y.dtype)
        mv[0, :] = y[0, :]
        # for i in range(1, rnz - 1):
        #     mv[i, :] = y[2 * (i - 1) + 1, :] + y[2 * (i - 1) + 2, :]
        indices = np.arange(1, rnz - 1, 1)
        mv[indices, :] = y[2 * indices - 1, :] + y[2 * indices, :]
        mv[rnz - 1, :] = y[2 * ((rnz - 1) - 1) + 1, :]
        if x_is_1d:
            return mv.ravel()
        else:
            return mv
    if type(signal) is np.ndarray:
        rnz = X // 2 + 1
        oa = np.full((X, X), 0.0)
        oa[0, 0] = 1
        indices = np.arange(1, rnz - 1, 1)
        oa[indices, 2 * indices - 1] = 1
        oa[indices, 2 * indices] = 1
        oa[rnz - 1, 2 * ((rnz - 1) - 1) + 1] = 1
        return aslazylinearoperator(
            kron(
                oa,
                eye(L, n=L, k=0),
                use_pylops=True
            )
        ) @ signal
    else:
        return aslazylinearoperator(
            kron(
                LazyLinearOperator(
                    (X, X),
                    matmat=lambda x: _matmat(x, L, X),
                    rmatmat=lambda x: _matmat(x, L, X).T.conj()
                ),
                eye(L, n=L, k=0),
                use_pylops=True
            )
        )
