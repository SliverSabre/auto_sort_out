# auto_sort_out

## 功能

自动整理文件目录

+ 这个模块是用来获取指定目录文件的文件信息，包括名称、大小、创建时间、最后访问时间以及最后修改时间。
+ info，是一个字典变量，里面有文件名File、大小Size、以及mat三个时间数组
+ 为了方便，时间数组用的还是那些，自己用time.localtime调用获取数据组，按照表格自己做去，为什么我不做？因为我累了！
+ path是可访问变量，用来确定路径的，在定义好类之后最好要定义path
+ total是目录下所有文件的总数，我实在是觉得每一次for都要用range(leng(self.info["File"]))这样子太蠢了，虽说那么搞会不占用什么内存空间，但是老娘都用上Python了还管这些？！而且一个整型变量也不占用多少空间吧，不然代码可读性差，自己也没法修改，反正默认大家2GB内存起步……
+ class的名字想起一个霸气点的，所以直白点——file_sort

## 注意！！！

无论那种类型的分类，都是破坏原有的目录结构，请慎用。后悔药功能暂未上线哦！即便是有后悔药功能，也不见得很有用，所以还是请慎重分类。

## 使用

建立一个demo,或者一个main的py脚本，然后：


    import file_data 
    f=file_data.file_sort()
    f.path=("/home/xxx/Documents")
    f.sort_out_by_mtime("normal") #将/home/xxx/Documents中的文件按照最后修改时间的年/月目录分类
    f.path="/home/xxx/Pictures"
    f.sort_out_by_filetype() #根据文件类型将/home/xxx/Picturesde文件分类，暂时为分类图片类

## class的内容

### 变量

+ path：要处理的目录路径

+ info：字典文件，包含所有文件的名称、大小、修改时间、最后访问时间、创建时间以及。。。文件类型

+ total：文件的总数

### 函数调用

+ __get(file_name)：获取文件的信息，存储到info文件，作为数组的一部分

+ Get_Info()：调用了__get()，把目录下所有的文件信息都拿到手，存储到info字典中，是一个超级大的数组，数组的长度就是total——文件的数量

+ sort_out_by_mtime(Type)：根据修改时间把文件分类，选择normal则是按照年月划分文件夹，选项all是按照年月日划分，推荐每天修改的文件太多了这么干，毕竟每个文件夹里文件高达上百也是可以了，按照月的划分怕太多你看不过来

+ sort_out_by_filetype()：根据文件类型分类，分出的类别不多，更多的是玩票的性质

+ sort_out_by_key(Key)：根据关键字分类，暂未测试，使用时要慎重

## 准备添加的功能：

+ 加入日志系统，知道你自己都改了些什么

+ 一键还原，按照日志系统还原回原来的样子

+ 一键清理——把目录里的文件全拿到当前目录里，不依靠日志，可以设置成私有调用，免得用户干坏事，嘿嘿

+ 剩下的就是日志记录更改，最好是……改成隐藏属性

+ 添加更多的filetype
