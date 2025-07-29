# imghdr.py – handmatig toegevoegd omdat Python 3.13 het niet meer bevat

tests = []

def test_jpeg(h, f):
    if h[6:10] == b'JFIF' or h[6:10] == b'Exif':
        return 'jpeg'

def test_png(h, f):
    if h[:8] == b'\211PNG\r\n\032\n':
        return 'png'

def test_gif(h, f):
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

def test_tiff(h, f):
    if h[:2] in (b'MM', b'II'):
        return 'tiff'

def test_bmp(h, f):
    if h[:2] == b'BM':
        return 'bmp'

def test_webp(h, f):
    if h[:4] == b'RIFF' and h[8:12] == b'WEBP':
        return 'webp'

tests.extend([
    test_jpeg,
    test_png,
    test_gif,
    test_tiff,
    test_bmp,
    test_webp
])

def what(file, h=None):
    if h is None:
        with open(file, 'rb') as f:
            h = f.read(32)
    for test in tests:
        res = test(h, file)
        if res:
            return res
    return None
