from src.ip_converter import ip_to_cidr

def test_single_ip():
    """Test converting a single IP address."""
    result = ip_to_cidr("192.168.1.100")
    assert result == ["192.168.1.0/24"]

def test_multiple_ips():
    """Test converting multiple IP addresses."""
    result = ip_to_cidr("192.168.1.100,10.0.0.1,172.16.5.200")
    assert result == ["10.0.0.0/24", "172.16.5.0/24", "192.168.1.0/24"]

def test_duplicate_network():
    """Test that duplicate networks are removed."""
    result = ip_to_cidr("192.168.1.100,192.168.1.200")
    assert result == ["192.168.1.0/24"]

def test_invalid_ip():
    """Test handling of invalid IP addresses."""
    result = ip_to_cidr("192.168.1.100,invalid.ip,10.0.0.1")
    assert result == ["10.0.0.0/24", "192.168.1.0/24"]

def test_empty_input():
    """Test handling of empty input."""
    result = ip_to_cidr("")
    assert result == []

def test_whitespace():
    """Test handling of whitespace in input."""
    result = ip_to_cidr(" 192.168.1.100 , 10.0.0.1 ")
    assert result == ["10.0.0.0/24", "192.168.1.0/24"]

def test_partial_ip():
    """Test handling of partial IP addresses."""
    result = ip_to_cidr("192.168.1,10.0.0.1")
    assert result == ["10.0.0.0/24"]

def test_special_ips():
    """Test handling of special IP addresses."""
    result = ip_to_cidr("127.0.0.1,0.0.0.0,255.255.255.255")
    assert result == ["0.0.0.0/24", "127.0.0.0/24", "255.255.255.0/24"] 