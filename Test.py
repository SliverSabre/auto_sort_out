import sort_out
import os

#path=input("请输入路径")
path="/home/xxzx/Pictures"
path=os.path.abspath(path)
f=sort_out.Sort_Out(path)
#f.sort_out_by_key("a")
#f.sort_out_by_time("mtime","easy") #普通的按照年/月分类
#f.sort_out_by_filetype()
#f.recover()#后悔药功能
f.close()#清空该类中的各种公共、私有的内容
