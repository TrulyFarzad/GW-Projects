import time

if __name__ == '__main__':
    with open('/home/farzad/Documents/CheckUpdate-logs.txt', 'a') as f:
        f.write(f'CheckUpdate get_update_check_data service stopped at {time.ctime()}')
        f.close()
