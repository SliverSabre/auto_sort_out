import sort_out as SOF

path=input("Where the directory you want to sort out?")
f=SOF.Sort_Out(str(path))
print("-----------------\n1：根据文件最后访问时间整理分类\n2：根据文件类型分类整理\n3：根据文件名中关键字分类整理\nr:恢复\n----------------------\n输入'q'后回车退出")
cm=input("请选择：")
while True:
  if cm == '1':
    f.sort_out_by_time("mtime","normal")
    break
  elif cm == '2':
    f.sort_out_by_filetype()
    break
  elif cm =='3':
    Keys=input("请输入分类使用的关键词：")
    f.sort_out_by_key(Keys)
    break
  elif cm == 'r':
    f.recover();
    break
  elif cm=='q':
    break
  else:
    print("错误！未发现指令，可以输入q后回车退出。")
    continue
print("分类完成，目录下的sort_out_log文件请勿删除，以便日后恢复。")
f.close()
