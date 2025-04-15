from .docker import parse_size_to_bytes, format_size

def test_parse_size_to_bytes():
    # Test different units
    assert parse_size_to_bytes('1B') == 1
    assert parse_size_to_bytes('1K') == 1024
    assert parse_size_to_bytes('1M') == 1024**2
    assert parse_size_to_bytes('1G') == 1024**3
    assert parse_size_to_bytes('1T') == 1024**4

    # Test decimal values
    assert parse_size_to_bytes('1.5K') == int(1.5 * 1024)
    assert parse_size_to_bytes('2.75M') == int(2.75 * 1024**2)

    # Test case insensitivity
    assert parse_size_to_bytes('1k') == parse_size_to_bytes('1K')
    assert parse_size_to_bytes('1m') == parse_size_to_bytes('1M')

    # Test invalid inputs
    assert parse_size_to_bytes('') == 0
    assert parse_size_to_bytes('invalid') == 0
    assert parse_size_to_bytes('123') == 0
    assert parse_size_to_bytes('1X') == 0

def test_format_size():
    # Test basic conversions
    assert format_size(0) == '0 B'
    assert format_size(1) == '1.00 B'
    assert format_size(1024) == '1.00 KB'
    assert format_size(1024**2) == '1.00 MB'
    assert format_size(1024**3) == '1.00 GB'
    assert format_size(1024**4) == '1.00 TB'

    # Test decimal values
    assert format_size(1536) == '1.50 KB'  # 1.5 KB
    assert format_size(int(2.75 * 1024**2)) == '2.75 MB'

    # Test values just under next unit
    assert format_size(1023) == '1023.00 B'
    assert format_size(1024**2 - 1) == '1024.00 KB'
