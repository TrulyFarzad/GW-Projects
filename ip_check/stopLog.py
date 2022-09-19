import time

if __name__ == '__main__':
    with open('/home/farzad/Documents/CheckIP-logs.txt', 'a') as f:
        f.write(f'CheckIP service stopped at {time.ctime()}')
        f.close()
