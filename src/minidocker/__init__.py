"""
minidocker
"""

__version__ = '0.1.0'

__all__ = [
    'make_date_version',
    'make_datetime_version',
]

from ._make_version import make_date_version, make_datetime_version