import time

if __name__ == '__main__':
    with open('/home/farzad/Documents/CheckIP-logs.txt', 'w') as f:
        f.write(f'CheckIP service started at {time.ctime()}')
        f.close()
