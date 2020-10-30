import os,shutil,time,re

'''
+ 这个模块是用来获取指定目录文件的文件信息，包括名称、大小、创建时间、最后访问时间以及最后修改时间。
+ info。。。改成隐藏属性
+ Demo
import file_data
f=file_data.file_sort("/home/xxzx/Downloads") #二者互斥，否则你的字典文件会很乱的
#f.path="/home/xxzx/Downloads"
f.sort_out_by_filetype()
'''

class file_sort:

    path="";
    info={"File":[],"Size":[],"mtime":[],"atime":[],"ctime":[],"FileType":[]}
    total=0;#文件数量统计，默认是0
    __file_type={"MS-Word":["doc","docx"],"MS-Excel":["xls","xlsx"],"Picture":["jpg","jpeg","png","gif","tiff"],"Photo-Raw":["NEF","nef","drw"],"PPT":["ppt","pptx"],"Program":["exe"],"Package":["rar","zip","tar.gz","tar.bz"]}
    #私有变量file_type,是包含了可以分类的文件，不需要更改，用于文件按照类型分类
    
    def __init__(self,path): #必选，要不然怕你出错
        self.path=os.path.abspath(path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        self.Get_Info()#来来来，我先帮你们搞到信息，怎么排序就是你们的问题了

    def __get(self,file_name):
        #获取文件的信息，内置函数
        data=os.stat(file_name);
        self.info["atime"].append(data[7]);
        self.info["mtime"].append(data[8]);
        self.info["Size"].append(data[6])
        self.info["ctime"].append(data[9]);
        self.total=len(self.info["File"]); #目录下所有的文件数量，反正这里使用的太频繁了，我也烦了，直接给一个变量好了
        for i in range(self.total): #反正为了方便，改成total
            s=re.findall(r'\w+\.(\w+$)',self.info["File"][i])#这里因为表达是太长了 所以懒惰的我就重新赋值给变量s
            if len(s)==0: #为了数据统一,不然怕出现out of range什么的错误
                s=[None]
            self.info["FileType"].append(s)

    def Get_Info(self):
        #获取目录下的所有文件信息赋值给字典info里，每个内容都是一个数组
        if self.total != 0: #如果之前对于初始化获取了内容那么info所有内容都需要清空，包括total,不过有了self.path这个做引导就没问题了
            for i in self.info.keys():
                self.info[i]=[]
             self.total=0 #这里需要把总数重置成0
        #然后接下来就是获取数据
        self.path=os.path.abspath(self.path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        os.chdir(self.path)
        self.info["File"]=os.listdir(self.path)#
        for name in self.info["File"]:
            name=os.path.abspath(name) #还是为了windows兼容，防止之前我忘了获取绝对路径
            self.__get(name)

    def sort_out_by_mtime(self,Type):
        #根据文件最后修改时间进行分类
        self.Get_Info();
        t=time.localtime(sefl.info["mtime"]);
        os.chdir(self.path)
        if Type == "normal": #这个就是按照年/月的目录分类
            for i in range(self.total):
                dirs=str(t[i][0])
                if os.path.isdir(dirs):
                    shutil.move(self.info["File"][i],dirs)
                else:
                    os.makedirs(dirs)
                    shutil.move(self.info["File"][i],dirs)
            return True
        elif Type == "all": #这个更详细，按照年月日的目录细分
            for i in range(self.total):
                dirs=str(t[i][0])+"/"+str(t[i][1])+"/"+str(t[i][2])
                if os.path.isdir(dirs):
                    shutil.move(self.info["File"][i],dirs)
                else:
                    os.makedirs(dirs)
                    shutil.move(self.info["File"][i],dirs)
            return True;
        else:
            return False #回复False就是失败了

    def sort_out_by_filetype(self):
        #根据文件的后缀分类，如果你的文件过于复杂最好别用，其实整个项目都建议慎用
        self.Get_Info();
        os.chdir(self.path)
        for i in range(self.total):
            for j in self.__file_type.keys():
                if self.info["FileType"][i] in self.__file_type[j]:
                    if os.path.isdir(str(j)):
                        shutil.move(self.info["File"][i],str(j))
                    else:
                        os.mkdir(str(j))
                        shutil.move(self.info["File"][i],str(j))
                        
                else:
                    if os.path.isdir("Unknow"):
                        shutil.move(self.info["File"][i],"Unknow")
                    else:
                        os.mkdir("Unknow")
                        shutil.move(self.info["File"][i],"Unknow")
        return True
                        
        '''for i in range( self.total ):#太复杂繁琐，没有意义，准备重写
            if self.info["FileType"][i] in ["doc","docx"]:
                if os.path.isdir("word文档"):
                    shutil.move(self.info["File"][i],"word文档")
                else:
                    os.mkdir("word文档")
                    shutil.move(self.info["File"][i],"word文档")

            elif self.info["FileType"][i] in ["xls","xlsx"]:
                if os.path.isdir("电子表格"):
                    shutil.move(self.info["File"][i],"电子表格")
                else:
                    os.mkdir("电子表格")
                    shutil.move(self.info["File"][i],"电子表格")

            elif self.info["FileType"][i] in ["ppt","pptx"]:
                if os.path.isdir("演讲文稿"):
                    shutil.move(self.info["File"][i],"演讲文稿")
                else:
                    os.mkdir("演讲文稿")
                    shutil.move(self.info["File"][i],"演讲文稿")

            elif self.info["FileType"][i] in ["c","cpp","py","java"]:
                if os.path.isdir("源代码"):
                    shutil.move(self.info["File"][i],"源代码")
                else:
                    os.mkdir("源代码")
                    shutil.move(self.info["File"][i],"源代码")
            else:
                if os.path.isdir("未闻其名"):
                    shutil.move(self.info["File"][i],"未闻其名")
                else:
                    os.mkdir("未闻其名")
                    shutil.move(self.info["File"][i],"未闻其名")'''
         return True

    def sort_out_by_key(self,Key):
        self.Get_Info()
        os.chdir(self.path)
        if not os.path.isdir(str(key)):
            os.mkdir(str(key))
        for i in range(self.total):
            pattern="r"+"\""+str(key)+"\""
            if re.search(pattern,self.info["File"][i]) != None:
                shutil.move(self.info["File"][i],str(key))
        return True
    
    def __get_out(self):#算是后悔药的设计设定吧，一键把所有目录下的内容都弄出来，同样慎用，这里给设置成私有函数了，哈哈
        pass
    
    def back(self): #回复原来的东西，但是需要日志
        pass
    
    def log(self):记录日志——你都干了些什么，都记录下来，方便吃后悔药的啊，哈哈！
        pass
    
   # End of Class file_sort
