import os,shutil,time,re,json,sys

class Sort_Out:
    path="";
    info={"File":[],"Size":[],"mtime":[],"atime":[],"ctime":[],"FileType":[]}
    total=0; #文件数量统计，默认是0
    __file_type={};#config.json中定义
    __forbidden_file=[];#config.json中定义
    __forbidden_dir =[];#config.json中定义

    def __init__(self,path): #必选，要不然怕你出错
        '''
        来来来，我先帮你们搞到信息，怎么排序就是你们的问题了
        当然，每一次调用获取函数Get_Info（）都会重置info和total里的内容，而且是调用path变量获取，后续也可以更改的，为了方便和安全最好强制您进行初始化
        '''
        self.path=os.path.abspath(path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        self.Get_Info()

    def __config(self): #这个是用来检测配置文件的，丢失了就禁止使用了哦～
        os.chdir(os.path.abspath(sys.path[0]))#获取脚本所在的目录，需要sys模块
        if not os.path.isfile("config.json"):
            print("错误！config.json文件丢失！")
            return False
        with open("config.json","r") as f:
            con=f.read()
        con=json.loads(con)
        self.__forbidden_file=list(con["Forbidden_Files"])
        self.__forbidden_dir =list(con["Forbidden_Dirs"])
        self.__file_type=dict(con["File_Type"])
        return True

    def close(self):#清理内存
        for i in self.info.keys():
            self.info[i]=[]
        self.total=0
        self.__forbidden_dir=[]
        self.__forbidden_file=[]
        self.__file_type={}
        self.path="";
        return True

    def __get(self,file_name):
        #获取文件的信息，内置函数
        data=os.stat(file_name);
        self.info["atime"].append(data[7]);
        self.info["mtime"].append(data[8]);
        #self.info["Size"].append(data[6]); #这个暂时无用，不需要为了省空间可以注释掉
        self.info["ctime"].append(data[9]);
        self.total=len(self.info["File"]);  #目录下所有的文件数量，反正这里使用的太频繁了，我也烦了，直接给一个变量好了，如果喜欢也可以单独拿出来看看多少个文件
        for i in range(self.total):  #反正为了方便，改成total
            s=re.findall(r'\w+\.(\w+$)',self.info["File"][i])#这里因为表达是太长了 所以懒惰的我就重新赋值给变量s
            if len(s)==0: #为了数据统一,不然怕出现out of range什么的错误
                s=[None]
            self.info["FileType"].append(s)

    def Get_Info(self):
        if not self.__config(): #没有配置文件还搞什么文件分类啊！
            return False
        if self.__is_log_exist():
            return False
        #先检查，出错直接跳出，这样免得每一次都要调用检查
        #获取目录下的所有文件信息赋值给字典info里，每个内容都是一个数组
        if self.total != 0:
            #如果之前对于初始化获取了内容那么info所有内容都需要清空，包括total,不过有了self.path这个做引导就没问题了——反正都离不开Get_Info获取，这里处理好就好了
            for i in self.info.keys():
                self.info[i]=[]
            self.total=0 #这里需要把总数重置成0
        #然后接下来就是获取数据
        self.path=os.path.abspath(self.path) #因为Windows下读取文件的特性，这里必须使用绝对路径
        os.chdir(self.path)
        self.info["File"]=os.listdir(self.path)
        for name in self.info["File"]:
            name=os.path.abspath(name) #还是为了windows兼容，防止之前我忘了获取绝对路径
            self.__get(name)
        if not self.__check():#进行可行性检查，不可行则弹出警告后退出
            return False;
        return True

    def sort_out_by_time(self,T_type="mtime",Type="normal"):
        '''
        T_type:是指的是创建时间还是访问时间还是修改时间，参数为mtime、ctime、atime，默认是mtime
        Type:easy、normal、all三种，分别是按照年作为目录以及年/月目录以及年/月/日目录结构，默认是normal
        '''
        '''不需要检查'''
        self.Get_Info();
        os.chdir(self.path)
        t=[];
        for i in self.info[str(T_type)]:
            t.append(time.localtime(i));
        os.chdir(self.path)
        if Type == "easy":
            for i in range(self.total):
                dirs=str(t[i][0])
                self.__move(dirs,i)
            return True

        elif Type == "normal": #这个就是按照年/月的目录分类
            for i in range(self.total):
                dirs=str(t[i][0])+"/"+str(t[i][1])
                self.__move(dirs,i)
            return True

        elif Type == "all": #这个更详细，按照年月日的目录细分
            for i in range(self.total):
                dirs=str(t[i][0])+"/"+str(t[i][1])+"/"+str(t[i][2])
                self.__move(dirs,i)
            return True;
        else:
            return False #回复False就是失败了

    def sort_out_by_filetype(self):
        #根据文件的后缀分类，如果你的文件过于复杂最好别用，其实整个项目都建议慎用
        self.Get_Info();
        os.chdir(self.path)
        for i in range(self.total):
            for j in self.__file_type.keys():
                if self.info["FileType"][i][0] in self.__file_type[j]:
                    self.__move(str(j),i)
                    #可以使用了
                    break;#找到了就不要再搞了，尽量跳出循环
        for i in range(self.total):
            if os.path.isfile(self.info["File"][i]):#剩下的文件如果还在，那就是未知的类别
                self.__move("Unknown",i)
                print(str(self.info["File"][i])+"has been moved to [Unknown]")
        return True

    def sort_out_by_key(self,Key=[]):#现在是数组了键词
        self.Get_Info()
        os.chdir(self.path)
        for i in range(self.total):
            for k in Key:
                if re.search(r""+str(k),self.info["File"][i]) != None:
                    k=os.path.abspath(k)
                    self.__move(str(k),a)
                    message=str(name)+" "+str(k)#记录日志
                    self.__mk_log(message)
        return True;

    def __check(self):
            '''
            安全检查，只要你的目录在禁止的目录里，那就禁止分类;目录中含有特殊文件也禁止分类;
            Type
            '''
            os.chdir(self.path)
            self.path=os.path.abspath(self.path)
            if self.total==0:
                print("当前目录下没有文件可供分类整理^_^")
                return False
            else:
                return True
            for i in self.__forbidden_dir : #__forbidden_dir里全是敏感词，碰到了就直接不允许
                if re.search(r""+str(i),self.path) != None:
                    print("禁止在包含"+str(i)+"类型的文件的目录中进行分类整理！")
                    return False
                else:
                    return True
            for i in range(self.total):
                if str(self.info["FileType"][i][0]) in self.__forbidden_file:#只要文件类型在禁止的范围内就禁止使用了！
                    print("禁止在包含目录["+str(i)+"]的目录中进行分类整理！")
                    return False
                else:
                    return True

    def __move(self,dirs,num):
            #受够了，直接写一个文件移动的函数，dirs就是目标目录，而num是文件编号，不是文件名
            if self.info["File"][num]=="sort_out_log":
                print("sort_out_log文件无需处理")
                return True
            if os.path.isdir(dirs):
                shutil.move(str(self.info["File"][num]),str(dirs))
                print(str(self.info["File"][num])+"has been moved to "+str(dirs))
            else:
                os.makedirs(str(dirs))
                shutil.move(str(self.info["File"][num]),str(dirs))
                print(str(self.info["File"][num])+"has been moved to "+str(dirs))
            dirs=os.path.abspath(dirs)
            name=self.info["File"][num]
            message=str(name)+";"+str(dirs)#记录日志
            self.__mk_log(message)
            return True

    def __mk_log(self,message):
        '''
        记录日志，名称为sort_out_log
        每条日志格式为：
            [日期  时间];源文件;移动到的文件夹;[回车]
            当然，这是修改后的情况了。
        '''
        os.chdir(self.path)
        t=time.localtime(time.time())
        s_t="["+str(t[0])+"-"+str(t[1])+"-"+str(t[2])+"  "+str(t[3])+":"+str(t[4])+":"+str(t[5])+"];"
        message=s_t+message+";\n"
        with open("sort_out_log","a") as f:
            f.writelines(message)
        return True

    def __log_path(self): #返回log所在的目录地址 不是ture or false游戏
        url=[]
        for path,dirs,files in os.walk(self.path):
            if "sort_out_log" in files:
                path=os.path.abspath(path)
                #path=os.path.join(path,"sort_out_log")#我个憨憨，当时记录的是有sor_out_log文件的目录啊！！
                url.insert(0,path) #最后发现的内容恰恰是最前面的,这样还原的话就是有内而外
        return url

    def __is_log_exist(self):
        for path,dirs,files in os.walk(self.path):
            if "sort_out_log" in files:
                print("--------------------\n**警告！！！**\n哎呀，目录下可是曾经分类过的，除非您想恢复否则将禁止文件整理分类。\n--------------------")
                return True #找到就退出，毕竟就是为了检测，不要浪费太多性能去找到每一个文件
        return False

    def recover(self):#恢复每一个目录下包含sort_out_log的文件夹恢复
        '''
        + 由于日志文件变更了，原来的四个数组变成了三个，所以要更改。和原来边界比来看都减去1。
        + lines数组最大编号应该为2
        + lines[0]:时间 lines[1]:文件名称 lines[2]:复制到的目录
        '''
        os.chdir(self.path)  
        msg=[]
        path=self.__log_path() #不要废话，使用recover了应该是有需要的
        if not len(path): #如果path长度为0，那就是说根本没有文件，不可以执行recover的功能。当然，会浪费运算力，所以要确定自己是否需要执行这个操作。
            print("对不起，这里没有需要恢复的日志")
            return Flase
            
        '''
        问题在下面的部分：lines数组更改为三个，最大边界是2。
        '''
        for u in path:
            os.chdir(u) #u的变量的作用除了确定当前目录外，还是文件恢复制定移动到的位置
            with open("sort_out_log","r") as f:
                for lines in f.readlines():
                    lines=lines.split(";")
                    name=os.path.join(str(lines[2]),str(lines[1])) #我当时就是在偷懒，所以省略lines[x]的写法改成了name
                    if os.path.isfile(name): #如果这个目录下有这个文件则移动，否则就不要管它了
                        shutil.move(str(name),str(u))
                        print(str(name)+"has been moved to "+str(u))
                    else:
                        print("文件"+str(name)+"可能被移动或者删除了。")
                        cm=input("继续恢复么？（n：中止任务，其余均为继续）")
                       
                        if cm='n':
                            print("恢复任务被用户中止")
                            msg.append(name)
                            break
                            exit()    
                        else:
                            continue
            #到这里移动了所有日志里存在的文件
            
            with open("sort_out_log","r") as f:
                for lines in f.readlines():
                    lines=lines.split(";")
                    name=str(lines[2])
                    if os.path.isdir(name):#如果有这个目录就删除，没有就不要管它了
                        os.removedirs(name)
                        print("目录 "+str(name)+" 被删除。")
            if os.path.isfile("sort_out_log"): #删除sort_out_log文件，恢复
                os.remove("sort_out_log")
                print("日志 "+str(lines[2])+"/"+"sort_out_log 被删除。")
             #到这里，清理了不想要目录与日志文件
        
        if not len(msg):
            print()"以下文件可能被删除或者移动而未能恢复")
            print("---------------------------------------------------")
            for i in msg:
                print("文件：" +str(i))
        print("恢 复 完 成")
        return True

      # End of Class Sort_Out.
