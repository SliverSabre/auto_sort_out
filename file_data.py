import os,shutil,time,re

'''
+ 这个模块是用来获取指定目录文件的文件信息，包括名称、大小、创建时间、最后访问时间以及最后修改时间。
+ info，是一个字典变量，里面有文件名File、大小Size、以及mat三个时间数组
+ 为了方便，时间数组用的还是那些，自己用time.localtime调用获取数据组，按照表格自己做去，为什么我不做？因为我累了！
+ path是可访问变量，用来确定路径的，在定义好类之后最好要定义path
+ total是目录下所有文件的总数，我实在是觉得每一次for都要用range(leng(self.info["File"]))这样子太蠢了，虽说那么搞会不占用什么内存空间，但是老娘都用上Python了还管这些？！而且一个整型变量也不占用多少空间吧，不然代码可读性差，自己也没法修改，反正默认大家2GB内存起步……
+ class的名字想起一个霸气点的，所以直白点——file_sort
----
# class的内容
+ 变量
-- path：要处理的目录路径
-- info：字典文件，包含所有文件的名称、大小、修改时间、最后访问时间、创建时间以及。。。文件类型
-- total：文件的总数
+ 函数调用
-- __get(file_name)：获取文件的信息，存储到info文件，作为数组的一部分
-- Get_Info()：调用了__get()，把目录下所有的文件信息都拿到手，存储到info字典中，是一个超级大的数组，数组的长度就是total——文件的数量
-- sort_out_by_mtime(Type)：根据修改时间把文件分类，选择normal则是按照年月划分文件夹，选项all是按照年月日划分，推荐每天修改的文件太多了这么干，毕竟每个文件夹里文件高达上百也是可以了，按照月的划分怕太多你看不出来
-- 剩下的就是按照关键字分类以及按照文件类型分类了，建议不要用——特别是你是程序员工程师，文件类型分类绝对不是好办法，会把你的工程文件搞的一团糟！关键字最好按照单位或者项目名字分类，再次警告，请确定路径里的文件都是人类可阅读的文件——例如报表什么的，否则不要使用，不然一个一个目录嵌套想还原都难
-- sort_out_by_filetype()：根据文件类型分类
-- sort_out_by_key(Key)：根据关键字分类
+ 准备添加的功能：
-- 加入日志系统，知道你自己都改了些什么
-- 一键还原，按照日志系统还原回原来的样子
-- 一键清理——把目录里的文件全拿到当前目录里，不依靠日志，可以设置成私有调用，免得用户干坏事，嘿嘿
-- 剩下的就是日志记录更改，最好是。。。改成隐藏属性
+ Demo
import file_data
f=file_data.file_sort("/home/xxzx/Downloads") #二者互斥，否则你的字典文件会很乱的
#f.path="/home/xxzx/Downloads"
f.sort_out_by_filetype()
'''

class file_sort:

    path="";
    info={"File":[],"Size":[],"mtime":[],"atime":[],"ctime":[],"FileType":[]}
    total="";#文件数量统计

    def __init__(self,path="."):
        self.path=os.path.abspath(path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        self.Get_Info()#来来来，我先帮你们搞到信息，怎么排序就是你们的问题了

    def __get(self,file_name):
        #获取文件的信息，内置函数
        data=os.stat(file_name);
        self.info["atime"].append(data[7]);
        self.info["mtime"].append(data[8]);
        self.info["Size"].append(data[6])
        self.info["ctime"].append(data[9]);
        self.total=len(self.info["File"]);#目录下所有的文件数量，反正这里使用的太频繁了，我也烦了，直接给一个变量好了
        for i in range(self.total): #反正为了方便，改成total
            s=re.findall(r'\w+\.(\w+$)',self.info["File"][i])#这里因为表达是太长了 所以懒惰的我就重新赋值给变量s
            if len(s)==0:#为了数据统一
                s=[None]
            self.info["FileType"].append(s)

    def Get_Info(self):
        #获取目录下的所有文件信息赋值给字典info里，每个内容都是一个数组


        self.path=os.path.abspath(self.path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        os.chdir(self.path)
        self.info["File"]=os.listdir(self.path)#
        for name in self.info["File"]:
            name=os.path.abspath(name)
            self.__get(name)

    def sort_out_by_mtime(self,Type):
        #根据文件最后修改时间进行分类
        self.Get_Info();
        t=time.localtime(sefl.info["mtime"]);
        os.chdir(self.path)
        if Type == "normal":
            for i in range(self.total):
                dirs=str(t[i][0])
                if os.path.isdir(dirs):
                    shutil.move(self.info["File"][i],dirs)
                else:
                    os.makedirs(dirs)
                    shutil.move(self.info["File"][i],dirs)
            return True
        elif Type == "all":
            for i in range(self.total):
                dirs=str(t[i][0])+"/"+str(t[i][1])+"/"+str(t[i][2])
                if os.path.isdir(dirs):
                    shutil.move(self.info["File"][i],dirs)
                else:
                    os.makedirs(dirs)
                    shutil.move(self.info["File"][i],dirs)
            return True;
        else:
            return False

    def sort_out_by_filetype(self):
        #根据文件的后缀分类，如果你的文件过于复杂最好别用
        self.Get_Info();
        os.chdir(self.path)
        for i in range( self.total ):
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
                    shutil.move(self.info["File"][i],"未闻其名")

    def sort_out_by_key(self,Key):
        self.Get_Info()
        os.chdir(self.path)
        if not os.path.isdir(str(key)):
            os.mkdir(str(key))
        for i in range(self.total):
            pattern="r"+"\""+str(key)+"\""
            if re.search(pattern,self.info["File"][i]) != None:
                shutil.move(self.info["File"][i],str(key))
