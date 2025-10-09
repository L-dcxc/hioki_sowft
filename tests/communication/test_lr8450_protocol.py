#!/usr/bin/env python3
import socket
import time

def test_protocol():
    ip = '192.168.1.14'
    port = 8800
    
    print('Testing LR8450 protocol on {}:{}'.format(ip, port))
    print('=' * 50)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((ip, port))
        
        commands = [
            ('*IDN?', 'Device identification'),
            ('*ESR?', 'Event status register'),
            (':ERRor?', 'Error query'),
            (':MEMory:MAXPoint?', 'Memory capacity'),
            (':MEMory:UNIT?', 'Unit information'),
        ]
        
        results = []
        for cmd, desc in commands:
            try:
                command = cmd + '

'
                print('
Testing: {} - {}'.format(cmd, desc))
                sock.sendall(command.encode('ascii'))
                
                response = ''
                start_time = time.time()
                while time.time() - start_time < 2.0:
                    try:
                        data = sock.recv(1024)
                        if not data:
                            break
                        response += data.decode('ascii', errors='ignore')
                        if '
' in response:
                            break
                    except socket.timeout:
                        break
                
                response = response.strip()
                print('Response: {}'.format(response))
                results.append((cmd, True, response))
                
            except Exception as e:
                print('Error: {}'.format(e))
                results.append((cmd, False, str(e)))
        
        sock.close()
        
        print('
' + '=' * 50)
        print('Test Summary:')
        print('=' * 50)
        
        successful = sum(1 for _, success, _ in results if success)
        total = len(results)
        
        for cmd, success, response in results:
            status = 'OK' if success else 'FAIL'
            print('{} {}: {}'.format(status, cmd, response[:50] + '...' if len(response) > 50 else response))
        
        print('
Overall: {}/{} tests passed ({:.1f}%)'.format(successful, total, successful/total*100))
        
        return successful > 0
        
    except Exception as e:
        print('Connection failed: {}'.format(e))
        return False

if __name__ == '__main__':
    test_protocol()
