# import requests
import time

# with open('/home/farzad/Documents/lists.txt', 'r') as output:
#     inputs = output.readlines()
#     output.close()
#
# for index, r in enumerate(inputs):
#     if r == '\n':
#         print(index, r'\n')
#     else:
#         print(index, r)
#
# results = []
# add = []
#
#
# while True:
#     try:
#         package = input()
#         if package.split(' ')[0].lower() == 'latest':
#             pckg = package.split(' ')
#             add.append(pckg[3][0:-1].strip())
#             add.append(pckg[-1].strip())
#         elif package.split(' ')[0].lower() == 'installed':
#             pckg = package.split(' ')
#             add.append(pckg[-1].strip())
#             print(f'add is: {add[1]}')
#             results.append(add)
#             add = []
#         else:
#             continue
#     except:
#         break

while True:
    with open('/home/farzad/Documents/unit.txt', 'w') as f:
        f.write(f'ctime is: {time.ctime()}\n')
        f.close()
    time.sleep(10)
