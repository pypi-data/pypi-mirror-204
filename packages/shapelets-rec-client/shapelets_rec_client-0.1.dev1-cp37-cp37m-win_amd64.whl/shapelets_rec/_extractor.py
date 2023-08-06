from typing import Optional, List, Dict, Union, Any
from typing_extensions import Literal

import datetime as dt

from .services import (RawExtractor, StringExtractor, IntegerExtractor, FloatExtractor,
                       TimeExtractor, DateExtractor, TimestampExtractor, DurationExtractor,
                       FlattenIteratorExtractor, ListIteratorExtractor,
                       ListExtractor, RecordExtractor, ExtractorOp, Extractor)

# all types for _is_data_type
_all_types = (RawExtractor, StringExtractor, IntegerExtractor, FloatExtractor,
              TimeExtractor, DateExtractor, TimestampExtractor, DurationExtractor,
              FlattenIteratorExtractor, ListIteratorExtractor,
              ListExtractor, RecordExtractor, ExtractorOp, Extractor)


def _is_data_type(obj: Any) -> bool:
    """
    Checks if obj is an instance of a ExtractorOp
    """
    return isinstance(obj, _all_types)


def _check_pointer(pointer: str) -> str:
    """
    Checks the validity of the json pointer before sending it to the server.
    """
    if pointer is None:
        raise ValueError("Pointer is None")
    
    result = pointer.strip()
    if len(result) == 0:
        raise ValueError("Pointer is an empty string")
    
    if not result.startswith('/'):
        raise ValueError("Pointers should start with a '/' character")

    if '*' in result:
        raise ValueError(f'Pointer {pointer} should not contain wildcard expressions')
    
    return result

def raw(pointer: str) -> ExtractorOp:
    """
    Constructs a data extractor that performs no data conversion.

    Since there is no conversion, the actual data type will be 
    either a 64 bits number (signed int or float), a boolean or 
    a string.

    Parameters
    ----------
    pointer : str
        JSON Pointer to the data.

    Returns
    -------
    ExtractorOp
    """
    return RawExtractor(pointer=_check_pointer(pointer))


def string(pointer: str, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a data extractor that performs a string conversion 
    to the data referenced by `pointer`.

    If the data referenced by `pointer` is already a string, no 
    conversion will be executed.  

    If the data is a float or an int, the values will be converted 
    using the locale conventions.

    Boolean values will be translated to either 'True' or 'False' 
    values.

    Parameters
    ----------
    pointer : str
        JSON Pointer to the data
    loc_id: optional str, defaults to None
        When set, number and float conventions will be based on 
        this locale identifier.  When not set, the default 
        locale active on the server will be used to perform the 
        string conversions.

    Returns
    -------
    ExtractorOp
    """
    return StringExtractor(pointer=_check_pointer(pointer))


def integer(pointer: str, signed: bool = True, size: Literal[8, 16, 32, 64] = 64, 
            null_value: Optional[int] = None, 
            format: Optional[str] = None, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a data extractor that performs an integer conversion 
    of the data referenced by pointer.

    If the data is already an integer, the value will be used as it 
    is, respecting the signed and size parameters given in the 
    parameters.  If the value overflows, the output should be set 
    to `null_value`.

    If the data is a float, it should be rounded.  The resulting integer
    will be set to the same size, signed and overflow checks as 
    if it was an integer.

    If the data is boolean, True values will be converted to 1 whilst 
    False values will be converted to 0.

    When the data is a string, it should be converted using the locale 
    and formatting rules.  The resulting number should be finally adapted 
    using size, signed and overflow checks as any other integer.

    Parameters
    ----------
    pointer : str, required
        JSON Pointer to de data
    signed : bool, optional, defaults to True
        Indicates if the output should be a signed or unsigned integer.
    size : Literal[8, 16, 32, 64], optional, defaults to 64
        Indicates the desired width of the output.
    null_value : Optional[int], defaults to None 
        Indicates the value to used with either the pointer is not found or 
        the actual value is null. If left unset, the output may contain 
        null values.
    format : Optional[str], defaults to None
        Format string to drive the conversion from string to integer.
    loc_id : Optional[str], defaults to None 
        Locale identifier to driver the conversion from string to integer. 

    Returns
    -------
    ExtractorOp
    """
    return IntegerExtractor(pointer=_check_pointer(pointer), signed=signed, size=size, nullValue=null_value, format=format, locale=loc_id)


def float(pointer: str, size: Literal[16, 32, 64] = 64, 
          null_value: Optional[float] = None, 
          format: Optional[str] = None, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a data extractor that performs an float conversion 
    of the data referenced by pointer.

    Integer values will be converted to float 64 bits before 
    conversion.

    Floating values will be adjusted to the closest representation 
    using the size constrains.

    If the data is boolean, True values will be converted to 1.0 whilst 
    False values will be converted to 0.0

    When the data is a string, it should be converted using the locale 
    and formatting rules.  The resulting floating point number should 
    be finally adapted to the size constrains.

    Parameters
    ----------
    pointer : str
        JSON Pointer to de data
    size : Literal[16, 32, 64], optional, defaults to 64
        Indicates the desired width of the output.
    null_value : Optional[float], optional, defaults to None 
        Indicates the value to used with either the pointer is not found or 
        the actual value is null. If left unset, the output may contain 
        null values.
    format : Optional[str], optional, defaults to None 
        Format string to drive the conversion from string.
    loc_id : Optional[str], optional, defaults to None
        Locale identifier to driver the conversion from string. 

    Returns
    -------
    ExtractorOp
    """

    return FloatExtractor(pointer=_check_pointer(pointer), size=size, nullValue=null_value, format=format, locale=loc_id)


def time(pointer: str, resolution: Literal['us', 'ns', 's', 'ms'] = 'ms', 
         null_value: Optional[dt.time] = None,
         format: Optional[str] = None, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a data extractor that performs a time of day conversion 
    of the data referenced by pointer.

    Time of day column should be represented as a integer column, whose 
    width will be set to 64 bits for 'us' and 'ns' resolutions and 
    to 32 bits to 's' and 'ms'.

    If the underlying data is a boolean, the conversion operation should 
    fail with an error.

    If the underlying data is an integer, it will be interpreted as the number 
    of seconds ('s'), milliseconds ('ms'), microseconds ('us') or nanoseconds 
    ('ns', as per resolution parameter) from the beginning of the day.

    If the underlying data is a float, the integral part of the number will be 
    considered as seconds from midnight, whilst the fractional part of the 
    value will be considered as fractions of a second. 

    If the data referenced by pointer is a string, it will be converted to a
    valid time representation using the locale and format parameters.  If 
    no locale and format strings are provided, the conversion will default to 
    ISO 8601 formats; if the conversion fails, null values will be used.

    Parameters
    ----------
    pointer : str
        JSON Pointer to de data
    resolution : Literal['us', 'ns', 's', 'ms'], optional, defaults to 'ms'
        Units of the resulting time of day column.
    null_value : Optional[datetime.time], optional, defaults to None 
        Indicates the value to used with either the pointer is not found or 
        the actual value is null. If left unset, the output may contain 
        null values.
    format : Optional[str], optional, defaults to None 
        Format string to drive the conversion from string.
    loc_id : Optional[str], optional, defaults to None
        Locale identifier to driver the conversion from string. 

    Returns
    -------
    ExtractorOp
    """
    return TimeExtractor(pointer=_check_pointer(pointer), resolution=resolution, nullValue=null_value, format=format, locale=loc_id)


def date(pointer: str, 
         resolution: Literal['d', 'ms'] = 'd', 
         null_value: Optional[dt.date] = None, 
         format: Optional[str] = None, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a data extractor that performs a date conversion 
    of the data referenced by pointer.

    Date column should be represented as a signed integer column, whose 
    width will be set to 64 bits for 'ms' and 32 bits for 'd'; the value 
    of this column will represent the amount of days ('d') or milliseconds 
    ('ms') since Unix Epoch .

    If the underlying data is a boolean, the conversion operation should 
    fail with an error.

    If the underlying data is an integer, it will be interpreted as the number 
    of seconds ('s') or milliseconds ('ms') since Unix Epoch.

    If the underlying data is a float, the integral part of the number will be 
    considered as seconds since Unix Epoch.

    If the data referenced by pointer is a string, it will be converted to a
    valid time representation using the locale and format parameters.  If 
    no locale and format strings are provided, the conversion will default to 
    ISO 8601 formats; if the conversion fails, null values will be used.    

    Parameters
    ----------
    pointer : str
        JSON Pointer to de data
    resolution : Literal['d', 'ms'], optional, defaults to 'd'
        When set to 'd' (days since Unix Epoch) the integer 
        column will be 32 bits; however, when set to 'ms' (milliseconds 
        since Unix Epoch), the output column will be set to 
        64 bits.
    null_value : Optional[datetime.date], optional, defaults to None 
        Indicates the value to used with either the pointer is not found or 
        the actual value is null. If left unset, the output may contain 
        null values.
    format : Optional[str], optional, defaults to None 
        Format string to drive the conversion from string.
    loc_id : Optional[str], optional, defaults to None
        Locale identifier to driver the conversion from string.

    Returns
    -------
    ExtractorOp
    """
    return DateExtractor(pointer=_check_pointer(pointer), resolution=resolution, nullValue=null_value, format=format, locale=loc_id)


def timestamp(pointer: str, 
              resolution: Literal['us', 'ns', 's', 'ms'] = 'ms', 
              assume_tz: Optional[str] = 'UTC', 
              null_value: Optional[dt.datetime] = None, 
              format: Optional[str] = None, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a timestamp extractor.

    Timestamp columns are represented by signed 64 integers, representing 
    the amount of seconds, milliseconds, microseconds or nanoseconds since 
    Unix Epoch time, without leap seconds.

    All timestamps are stored in shapelets as UTC timestamps.

    If the underlying data is a boolean, the conversion operation should 
    fail with an error.

    If the underlying data is an integer, it will be interpreted as the number 
    of units of time, as described by resolution.

    If the underlying data is a float, the integral part of the number will be 
    considered as seconds since Unix Epoch.

    If the data referenced by pointer is a string, it will be converted to a
    valid time representation using the locale and format parameters.  If 
    no locale and format strings are provided, the conversion will default to 
    ISO 8601 formats; if the conversion fails, null values will be used.    

    Parameters
    ----------
    pointer : str
        JSON Pointer to de data
    resolution : Literal['us', 'ns', 's', 'ms'], optional, defaults to 'ms'
        Units of time
    assume_tz: Optional[str], defaults to 'UTC'
        Default timezone when it is not explicitly given.  The transformed 
        data will be *always* stored as UTC.
    null_value : Optional[datetime.datetime], optional, defaults to None 
        Indicates the value to used with either the pointer is not found or 
        the actual value is null. If left unset, the output may contain 
        null values.
    format : Optional[str], optional, defaults to None 
        Format string to drive the conversion from string.
    loc_id : Optional[str], optional, defaults to None
        Locale identifier to driver the conversion from string.

    Returns
    -------
    ExtractorOp
    """
    return TimestampExtractor(pointer=_check_pointer(pointer), resolution=resolution, assumeTimeZone=assume_tz, nullValue=null_value, format=format, locale=loc_id)


def duration(pointer: str, 
             resolution: Literal['us', 'ns', 's', 'ms'] = 'ms', 
             null_value: Optional[dt.timedelta] = None, 
             format: Optional[str] = None, loc_id: Optional[str] = None) -> ExtractorOp:
    """
    Constructs a data extractor that performs a duration conversion
    of the data referenced by pointer.

    Durations are exact intervals of time, and they shouldn't be 
    confused with periods, which are calendar based time intervals.

    Durations will be represented as signed integer column of 64 bits.

    If the underlying data is a boolean, the conversion operation should 
    fail with an error.

    If the underlying data an integer, it should be interpreted as the 
    as a duration of `resolution` units.

    If the underlying data is a float, it should be interpreted as the 
    number of seconds and converted to the desired resolution.

    If the data referenced by pointer is a string, it will be converted to a
    valid time representation using the locale and format parameters.  If 
    no locale and format strings are provided, the conversion will default to 
    ISO 8601 formats; if the conversion fails, null values will be used.   

    Parameters
    ----------
    pointer : str
        JSON Pointer to de data
    resolution : Literal['us', 'ns', 's', 'ms'], optional, defaults to 'ms'
        Units of the time interval
    null_value : Optional[datetime.timedelta], optional, defaults to None 
        Indicates the value to used with either the pointer is not found or 
        the actual value is null. If left unset, the output may contain 
        null values.
    format : Optional[str], optional, defaults to None 
        Format string to drive the conversion from string.
    loc_id : Optional[str], optional, defaults to None
        Locale identifier to driver the conversion from string.

    Returns
    -------
    ExtractorOp
    """
    return DurationExtractor(pointer=_check_pointer(pointer), resolution=resolution, nullValue=null_value, format=format, locale=loc_id)


def _parse_spec(spec: Dict[str, Any], path: List[str] = []) -> RecordExtractor:
    """
    Builds the spec, considering all the idioms.

    Parameters
    ----------
    spec : Dict[str, Any]
        Top level dictionary.  The values in the spec may be strings, 
        ExtractorOp instances created through the helper methods, lists 
        and other dictionaries (for inner records).
    path : List[str], optional
        Accumulated path as the specification is traversed.

    Returns
    -------
    RecordType
        An instance of a RecordType representing the specification.

    Raises
    ------
    ValueError
        - In case of empty top level dictionaries
        - In case of empty or null values
        - If empty lists are found 
        - Non recognised parameters
    """
    if spec is None or len(spec) == 0:
        raise ValueError(f'spec must contain at least one entry {".".join(path)}')

    converted: Dict[str, ExtractorOp] = {}

    for (k, v) in spec.items():
        if v is None:
            raise ValueError(f'{k} entry is none {".".join(path + [k])}')

        if isinstance(v, str):
            # raw access
            if '*' not in v:
                converted[k] = RawExtractor(pointer=v)
            else:
                # do flatten
                # '/store/book/*/isbn'
                sections = v.split('*')
                base = flatten(sections[0], '/' if len(sections[1]) == 0 else sections[1])
                for i in range(2, len(sections)):
                    base = flatten(base, '/' if len(sections[i]) == 0 else sections[i])
                converted[k] = base

                pass

        elif _is_data_type(v):
            # direct definition
            converted[k] = v

        elif isinstance(v, dict):
            # recurse
            converted[k] = _parse_spec(v, path + [k])

        elif isinstance(v, list):
            if len(v) == 0:
                raise ValueError(f'Empty lists are not permitted {".".join(path + [k])}')

            if len(v) == 1 and isinstance(v[0], str) and '*' in v[0]:
                # do iterate /store/book/*/isbn /store/book/*/*/isbn /store/book/* /store/book/*/
                sections = v[0].split('*')
                base = iterate(sections[0], '/' if len(sections[1]) == 0 else sections[1])
                for i in range(2, len(sections)):
                    base = iterate(base, '/' if len(sections[i]) == 0 else sections[i])
                converted[k] = base
            else:
                inner = []
                for (pos, entry) in enumerate(v):
                    if isinstance(entry, str):
                        inner.append(RawExtractor(pointer=entry))
                    elif _is_data_type(entry):
                        inner.append(entry)
                    elif isinstance(entry, dict):
                        inner.append(_parse_spec(entry, path + [f'_{pos}']))
                    else:
                        key = ".".join(path + [f'{k}_{pos}'])
                        raise ValueError(f'Unsupported value at {key}')

                converted[k] = ListExtractor(of=inner)

        else:
            raise ValueError(f'Unsupported value at {".".join(path + [k])}')

    return RecordExtractor(fields=converted)


def iterate(source: Union[str, ExtractorOp], selector: Union[str, dict, ExtractorOp]) -> ExtractorOp:
    """
    Represents an algorithm to extract values from a list of values, by applying 
    a selector to each element of the list.

    Parameters
    ----------
    source : Union[str, ExtractorOp]
        Source of the iteration; it may be a JSON Pointer or another iterator 
        construct.

    selector : Union[str, dict, ExtractorOp]
        Extraction to be applied to the each element of the list.

    Returns
    -------
    ExtractorOp

    Raises
    ------
    ValueError
        - When the source cannot be interpreted as another iterator.
        - When the selector cannot be applied as a valid transformation.
    """
    if isinstance(selector, str):
        converted = RawExtractor(pointer=selector)
    elif _is_data_type(selector):
        converted = selector
    elif isinstance(selector, dict):
        converted = _parse_spec(selector)
    else:
        raise ValueError(f'Unable to process selector {selector}')

    if not isinstance(source, (str, ListIteratorExtractor)):
        raise ValueError(f'Incorrect list source {source}')

    return ListIteratorExtractor(iterator=source, of=converted)


def flatten(source: Union[str, ExtractorOp], selector: Union[str, dict, ExtractorOp]) -> ExtractorOp:
    """
    Represents an algorithms that flattens the results by emitting as many 
    rows as elements in the list.

    Parameters
    ----------
    source : Union[str, ExtractorOp]
        Source of the iteration; it may be a JSON Pointer or another iterator 
        construct.
    selector : Union[str, dict, ExtractorOp]
        Extraction to be applied to the each element of the list.

    Returns
    -------
    ExtractorOp

    Raises
    ------
    ValueError
        - When the source cannot be interpreted as another iterator.
        - When the selector cannot be applied as a valid transformation.
    """
    if isinstance(selector, str):
        converted = RawExtractor(pointer=selector)
    elif _is_data_type(selector):
        converted = selector
    elif isinstance(selector, dict):
        converted = _parse_spec(selector)
    else:
        raise ValueError(f'Unable to process selector {selector}')

    if not isinstance(source, (str, FlattenIteratorExtractor)):
        raise ValueError(f'Incorrect list source {source}')

    return FlattenIteratorExtractor(iterator=source, of=converted)

def extractor(spec: Dict[str, Any]) -> Extractor:
    return Extractor(record = _parse_spec(spec))

__all__ = [
    'Extractor', 'extractor',
    'flatten', 'iterate', 'duration', 'timestamp', 
    'date', 'time', 'float', 'integer', 'string', 
    'raw'
]
