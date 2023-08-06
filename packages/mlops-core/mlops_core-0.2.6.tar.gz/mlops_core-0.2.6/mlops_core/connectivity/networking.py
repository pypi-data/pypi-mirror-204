import os
import socket

import dns.resolver

from typing import List
from functools import partial
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor, as_completed

CONNECTIVITY_CHECK_TIMEOUT = 5

MIN_PORT = 0
MAX_PORT = 65535


class QueryResult():
    def __init__(self, host: str, port: int, s_type, result: bool) -> None:
        self.host = host
        self.port = port
        self.open = result
        self.s_type = s_type

    def __str__(self) -> str:
        return f"{self.host}:{self.port} is {'open' if self.open else 'closed'}"


def resolve_ip_address(hostname: str) -> List[str]:
    """Resolve IP address given a hostname

    Args:
        hostname (str): Hostname to resolve

    Returns:
        List[str]: IP address(es) of the hostname
    """
    answer = dns.resolver.resolve(hostname, "A")
    return [a.to_text() for a in answer.rrset]


def attempt_connection(host: str, port: int, timeout: int = CONNECTIVITY_CHECK_TIMEOUT, use_tcp: bool = True) -> bool:
    """Attempt connection to a host

    Args:
        host (str): Host to connect to
        port (int): Port to connect to
        timeout (int, optional): Timeout for connection attempt. Defaults to CONNECTIVITY_CHECK_TIMEOUT
        use_tcp (bool, optional): Use TCP connection. Defaults to True (UDP otherwise)

    Returns:
        bool: True if connection was successful, otherwise False
    """
    s_type = socket.SOCK_STREAM if use_tcp else socket.SOCK_DGRAM

    with closing(socket.socket(socket.AF_INET, s_type)) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except Exception as e:
            return False


def is_port_open(host: str, port: int, timeout: int = CONNECTIVITY_CHECK_TIMEOUT, use_tcp: bool = True) -> bool:
    """
    Check if a port is open on a host

    Args:
        host (str): Host to check
        port (int): Port to check
        timeout (int, optional): Timeout for connection attempt. Defaults to CONNECTIVITY_CHECK_TIMEOUT
        use_tcp (bool, optional): Use TCP connection. Defaults to True (UDP otherwise)

    Returns:
        query_result (QueryResult): Result of the query
    """
    s_type = socket.SOCK_STREAM if use_tcp else socket.SOCK_DGRAM
    with closing(socket.socket(socket.AF_INET, s_type)) as sock:
        sock.settimeout(timeout)
        try:
            if sock.connect_ex((host, port)) == 0:
                return QueryResult(host, port, s_type, True)
            else:
                return QueryResult(host, port, s_type, False)
        except socket.error as e:
            return QueryResult(host, port, s_type, False)


def scan_ports(host: str, start: int = MIN_PORT, end: int = MAX_PORT, show_open: bool = True, timeout: int = CONNECTIVITY_CHECK_TIMEOUT - 3) -> List[QueryResult]:
    """
    Scan a range of ports on a host

    Args:
        host (str): Host to scan
        start (int, optional): Start of the port range. Defaults to MIN_PORT
        end (int, optional): End of the port range. Defaults to MAX_PORT
        show_open (bool, optional): Only show accessible ports. Defaults to True
        timeout (int, optional): Timeout for connection attempt. Defaults to CONNECTIVITY_CHECK_TIMEOUT

    Returns:
        List[QueryResult]: List of QueryResult objects
    """
    # Create a partial function to pass to the thread pool
    fn = partial(is_port_open, host)

    # Create a thread pool executor to run the thread pool
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 50) as executor:
        # Create a list of threads to run. Each thread will run the is_port_open function
        # with the given host and the port in the range.
        result = [executor.submit(fn, port, timeout)
                  for port in range(start, end)]

        # Wait for all threads to finish
        searches = [r.result() for r in as_completed(result)]

        # Filter out inaccessible ports if only accessible ports are requested
        def do_filter_or_not(search):
            return search.open == show_open if show_open else True

        # Create a list of the results that match the filter
        status = list(filter(do_filter_or_not, searches))
        return status


def scan_common_ports(host: str, show_open: bool = True, timeout: int = CONNECTIVITY_CHECK_TIMEOUT - 3) -> List[QueryResult]:
    """
        Scan a range of common ports on a host

        Args:
            host (str): Host to scan
            show_open (bool, optional): Only show accessible ports. Defaults to True
            timeout (int, optional): Timeout for connection attempt. Defaults to CONNECTIVITY_CHECK_TIMEOUT

        Returns:
            List[QueryResult]: List of QueryResult objects
    """
    common_ports = [7, 20, 21, 22, 23, 25, 69, 88, 53, 80, 110, 119, 123,
                    143, 161, 179, 194, 443, 465, 500, 587, 636, 2483, 3306, 3389, 5432]
    fn = partial(is_port_open, host)
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 50) as executor:
        result = [executor.submit(fn, port, timeout) for port in common_ports]

        searches = [r.result() for r in result]

        # Filter out inaccessible ports if only accessible ports are requested
        def do_filter_or_not(search):
            return search.open == show_open if show_open else True

        status = list(filter(do_filter_or_not, searches))
        return status
