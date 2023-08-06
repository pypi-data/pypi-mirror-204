Usage

  python -m minolz [options] <URL>

  options:
    -o --output FILE|DIR   output filename or directory


API Usage

  >>> import minolz
  >>> url = 'https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe'
  >>> filename = minolz.download(url)
  100% [................................................] 3841532 / 3841532>
  >> filename
  'python-3.11.3-amd64.exe'

The skew that you see above is a documented side effect.
Alternative progress bar:

  >>> minolz.download(url, bar=bar_thermometer)


ChangeLog

0.5 (2023-04-21)
 * release

