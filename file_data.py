import os
import time

'''
这个模块是用来获取指定目录文件的文件信息，包括名称、大小、创建时间、最后访问时间以及最后修改时间。

类里有两个变量，Path，是要获取的目录的地址
info，是一个字典变量，里面有文件名File、大小Size、以及mat三个时间数组
为了方便，时间数组用的还是那些，就是time.localtime获取的类型，你想要什么都有，按照表格自己做去——因为我累了

'''
if __name__ == '__main__':
    print("By itself")
else:
    print("From other module\n")

#mode ino dev nlink uid gid size atime mtime ctime
class File_Info: #目前只能获取某一个文件的详细信息
    info={"File":[],"Size":[],"mtime":[],"atime":[],"ctime":[],"Location":[]}

    def __get(self,file_name):#获取文件的信息，内置函数
        data=os.stat(file_name);
        self.info["atime"].append(data[7]);
        self.info["mtime"].append(data[8]);
        self.info["Size"].append(data[6])
        self.info["ctime"].append(data[9]);
        self.info["Location"].append(len(self.info["Size"])-1);
        #tm_year,tm_mon,tm_mday,h/m/s,wday,yday,tm_isdst

    def Get_Info(self,path):#获取目录下的所有文件信息赋值给字典info里，每个内容都是一个数组
        os.chdir(path)
        self.info["File"]=os.listdir(path)
        for name in self.info["File"]:
            name=os.path.abspath(name)
            self.__get(name)

    def Sort_Out(self,Type):#整理文件，按照要求创建文件夹什么的
        pass

    def __sorted_by_time(self): #按照时间排序，默认从早到晚 准备采取归并法
        pass

    def __location_trans(self):#根据列表里的location的改变来改变其他所有数据的顺序，以期望内容一一对应，可能会有用处的啊
        i=0;
        i=int(i);
        for l in self.info["Location"]:#这里l是需要变动到的位置，i作为地址指针
            if l == i:
                i=i+1;
            else:
                self.__swap(i,l);
                i=i+1;

    def __swap(self,i,j):
        #用来数据交换,key是File、Size等字典里的关键字，i、j是位置，没有顺序，i推荐是原生从0到len（字典）-1,j就是Location的数据
        for key in self.info.key():#获取info字典里的所有关键字
            swap_tmp=self.info[key][j] #这里先把第J个位置内容提取
            self.info[key][j]=self.info[key][i]; #因为J的位置内容已经备份，所以可以无所畏惧地交给要交换的i内容
            self.info[key][i]=swap_tmp; #哈哈，苍天绕过谁阿i号元素，你也要被替换，最终变成原来j的形状
        #就这样，i和j互相变成对方的形状，交换完成

    def func_demo(self):#用来测试各个函数用的，完成后别忘了删除了哈
        self.__location_trans();


    #End of Class File_Info

