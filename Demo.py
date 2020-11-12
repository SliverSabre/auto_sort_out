import sort_out as SOF
Dirs=SOF.Sort_Out("/home/xxzx/Pictures")
#Dirs.path="/home/xxzx" #If you want to change path,do this
Dirs.sort_out_by_time("ctime","all")
#Dirs.sort_out_by_key("")
#Dirs.sort_out_by_filetype()
#Dirs.path="/home/xxzx/Pictures/图片"
#Dirs.sort_out_by_filetype()
#Dirs.recover()
