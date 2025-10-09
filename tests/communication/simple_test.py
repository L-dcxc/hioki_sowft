#!/usr/bin/env python3
# Simple LR8450 connection test

import socket
import sys

def test_connection(ip="192.168.1.14", port=8800):
    """Test connection to LR8450"""
    try:
        print("Connecting to device: {}:{}".format(ip, port))

        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((ip, port))

        # Send IDN query
        command = "*IDN?"
        print("Sending command: {}".format(command))
        sock.sendall((command + "\r\n").encode("ascii"))

        # Receive response
        response = sock.recv(1024).decode("ascii", errors="ignore").strip()
        print("Received response: {}".format(response))

        sock.close()

        if response:
            print("SUCCESS: Connection successful!")
            return True
        else:
            print("FAIL: Connection failed - no response")
            return False

    except Exception as e:
        print("FAIL: Connection failed - {}".format(e))
        return False

def main():
    """Main function"""
    print("LR8450 Simple Connection Test")
    print("=" * 40)

    # Default IP address
    default_ip = "192.168.1.14"
    default_port = 8800

    # Check command line arguments
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = default_ip

    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = default_port

    success = test_connection(ip, port)

    if success:
        print("\nTest successful! Device can communicate normally.")
    else:
        print("\nTest failed! Please check:")
        print("  1. Device IP address is correct")
        print("  2. Device port number is correct (default 8800)")
        print("  3. Device is powered on and connected to network")
        print("  4. Firewall is not blocking the connection")

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
