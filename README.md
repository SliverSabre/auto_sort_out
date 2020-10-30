# auto_sort_out

## 功能

自动整理文件目录

## 使用
建立一个demo,或者一个main的py脚本，然后：


    import file_data 
    f=file_data.file_sort()
    f.path=(".") #Current directory in example
    f.sort_out_by_mtime("normal") #Sorting out files,will create directories with name is year and sub directories name with month
    f.sort_out_by_filetype() #Sorting out files depends on their file type,for example:source code,MS Word,MS Excel and balabala


