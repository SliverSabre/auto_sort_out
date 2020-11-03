import file_data as fs
import time,logging,os
types={"Pic":["gif","png"],"Mov":["mov","avi"]}
files=["gif","xls","avi","png","mp4"]
for i in range(len(files)):
    for j in types.keys():
        if files[i] in types[str(j)]:
           files[i]=0
for i in range(len(files)):
    if files[i] != 0:
        files[i]=1024
print(files)
dirs=os.listdir(".")
for i in dirs:
    if os.path.isfile(i):
        print("It is a file")
    else:
        print("Get off!")
