import SortOutFiles as SOF
Dirs=SOF.file_sort("/home/xxx/Documents")
#Dirs.path="/home/xxx/Music" #If you want to change path,do this
Dirs.sort_out_by_time("ctime","all")
Dirs.sort_out_by_key("report")
#Dirs.sort_out_by_filetype() #Is not completed.
