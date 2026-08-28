# Installation

## From PyPI

```console
pip install pypodlib                          # core (device + library read/write)
pip install 'pypodlib[artwork]'               # + embedded-art extraction/encoding
```

## Runtime dependencies

| Dependency | Required for |
|---|---|
| `pyusb>=1.3.1` / `libusb-package>=1.0.30` | USB device identification |
| `pycryptodome>=3.20.0` | HASH72 checksum signing (Nano 5G) |
| `wasmtime>=30.0.0` | HASHAB checksum signing (Nano 6G/7G) |
| `numpy>=2.0.0`, `pillow>=10.0.0`, `mutagen>=1.47.0` | Artwork support (`[artwork]` extra) |

## From source

```console
git clone https://github.com/TheRealSavi/pyPodLib.git
cd pyPodLib
pip install -e .          # core
pip install -e '.[artwork]'   # with artwork support
```
