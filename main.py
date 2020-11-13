import sort_out as SOF

path=input("Where the directory you want to sort out?")
f=SOF.Sort_Out(str(path))
cm=input("What kind of type do you want to use?")
print("-----------------\n1:Sort out by file's time infomation.\n2:Sort out by file's type.\n3:Sort out by keywords.\n----------------------\nCommand 'q' to quit.")
while true:
  if cm == '1':
    f.sort_out_by_time("mtime","normal")
  elif cm == '2':
    f.sort_out_by_filetype()
  elif cm =='3':
    Keys=input("Input your keywords:")
    f.sort_out_by_key(Keys)
  elif cm=='q':
    break
  else:
    print("Error,you input an wrong command!")
    continue
f.close()
