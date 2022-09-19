import time

if __name__ == '__main__':
    with open('/home/farzad/Documents/CheckUpdate-logs.txt', 'w') as f:
        f.write(f'CheckUpdate get_update_check_data service started at {time.ctime()}')
        f.close()
