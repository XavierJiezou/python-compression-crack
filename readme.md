【python】80行代码实现压缩包密码破解软件，支持zip和rar（多线程高速撞库）
# 软件下载
> win64：[https://ghgxj.lanzous.com/iEpZUj3998d](https://ghgxj.lanzous.com/iEpZUj3998d)

`mac`、`linux`和`win32`用户请参考打包教程使用源代码打包。
# 破解测试
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020120519515547.gif#pic_center)
# 文件说明
- `run.exe`：压缩包密码破解软件，支持`zip`和`rar`格式
- `pwd.txt`：包含所有`3`位数的密码字典，从`000`到`999`
- `res.txt`：破解成功后保存密码的文件
- `999.rar`：加密的`rar`压缩包，加密密码是：`999`，里面的内容是一张图片
- `999.zip`：加密的`zip`压缩包，加密密码是：`999`，里面的内容是个`txt`文件
- `run.py`：`python`源码
- `UnRAR64.dll`：`rar`解压依赖库文件
- `app.ico`：软件图标
- `gan.py`：生成密码字典的代码
- `readme.md`：项目说明文件
# 项目简介
这是一个基于`python`开发的压缩包密码破解软件，利用多线程技术高速地读取密码字典并对压缩包尝试破解。
# 项目地址
> github: [https://github.com/XavierJiezou/python-compression-crack](https://github.com/XavierJiezou/python-compression-crack)

# 破解思路
压缩包加密算法基本上都是不可逆的，即我们不能在算法层面上推理出它的明文。所以我们只能用穷举法不断的碰撞，大白话就是随机生成很多密码，然后一个一个的试。具体思路如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201205231055763.png#pic_center)

# 开发环境
我们用到的模块有：
```python
from unrar.rarfile import RarFile
import concurrent.futures as cf
from zipfile import ZipFile
import time
import os
```
`os`、`time`、`zipfile`和`concurrent.futures`都是`python`内置模块，无需安装。

----
`unrar`是第三方模块，可以通过`pip`指令安装：
```bash
pip install unrar
```
根据[pypi](https://pypi.org/project/unrar/)官网可知，安装后还需要配置一下库文件才能正常使用：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201205200355465.png)

**具体配置教程如下：（windows）**

1、下载库文件的压缩包
> [http://www.rarlab.com/rar/UnRARDLL.exe](http://www.rarlab.com/rar/UnRARDLL.exe)

2、选择解压路径`D:\Program Files (x86)\UnrarDLL`，点击`Install`解压
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201205200645767.png)

3、解压后的主要**目录结构**如下：
```
D:\Program Files (x86)\UnrarDLL
├─Documentation
├─Examples
├─NoCrypt
├─Examples
└─x64
│  └─UnRAR64.lib
├─UnRAR.lib
```
4、配置系统环境变量。变量名必须是：`UNRAR_LIB_PATH`，变量值：`D:\Program Files (x86)\UnrarDLL\x64\UnRAR64.dll`（如果你是win32系统，变量值：`D:\Program Files (x86)\UnrarDLL\UnRAR.dll`)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20201205201912575.png)
5、配置完成后，记得点击**确定**保存，然后重启代码编辑器`vscode`或`pycharm`，不重启不会生效的！

**顺便一提：**

解压`rar`文件时，我们用的模块是`unrar`里面的`rarfile`，其实还有个直接叫`rarfile`的包，但是那个`rarfile`包依赖`unrar`环境，配置还很复杂，所以我直接放弃了，用`unrar`即可。
# 生成字典
这里我生成了一个包含所有三位数的字典，并按行保存到`pwd.txt`文件中。
```python
f = open('pwd.txt', 'w')
l = [str(i) for i in range(10)]
for i in l:
    for j in l:
        for k in l:
            f.write(i+j+k+'\n')
f.close()
```
当然，实际情况是很复杂的。密码可能不止三位，并且不仅包含数字，还有字母和特殊字符等。你可以在我的代码基础上做些修改，生成更为复杂的密码字典。如果你不想自己写代码，我这里也为大家准备好了一个[43G的大字典](https://blog.csdn.net/qq_42554007/article/details/108271757)（你下载的是压缩过的只有80MB，下载后请解压）：
> 43G大字典：[https://ghgxj.lanzous.com/i8JR0j33r3a](https://ghgxj.lanzous.com/i8JR0j33r3a)

这里再推荐一个提供密码字典下载的网站：
> [https://wiki.skullsecurity.org/Passwords](https://wiki.skullsecurity.org/Passwords)

# 读取密码
密码字典一般都很大，假如你用的密码字典是`43GB`，直接读整个文件的话可能会导致内存溢出，所以我们一般是按行读，读一行处理一行，处理完成后指针会自动帮你定位到下一行，往复循环即可，具体`python`实现如下：
```python
def crack(self, funcname):
    book = open(self.bookname)
    with cf.ThreadPoolExecutor(12) as tp:
        while True:
            pwd = book.readline().strip()
            tp.submit(funcname, pwd)
```
# 尝试破解
## 尝试破解zip格式的压缩包
```python
def zip_crack(self, pwd):
    runtime = self.show()
    print(f'破解已用时: {runtime} 当前密码: {pwd}', end='\r')
    try:
        zip_file = ZipFile(self.filename)
        zip_file.pwd = pwd.encode()
        zip_file.extractall()
        print(f'破解已完成: {runtime} 压缩密码: {pwd}')
        with open('res.txt','w') as f:
            f.write(pwd)
        os._exit(0)
    except:
        pass
```
## 尝试破解rar格式的压缩包
```python
def rar_crack(self, pwd):
    runtime = self.show()
    print(f'破解已用时: {runtime} 当前密码: {pwd}', end='\r')
    try:
        rar_file = RarFile(self.filename, pwd=pwd)
        rar_file.extractall()
        print(f'破解已完成: {runtime} 压缩密码: {pwd}')
        with open('res.txt','w') as f:
            f.write(pwd)
        os._exit(0)
    except:
        pass
```
# 完整代码
```python
# run.py
from unrar.rarfile import RarFile
import concurrent.futures as cf
from zipfile import ZipFile
import time
import os


class CompressionCrack(object):
    def __init__(self):
        self.filename = input('请输入压缩文件的绝对路径: ')
        self.bookname = input('请输入密码字典的绝对路径: ')
        self.startTime = time.time()

    def show(self):
        runtime = round(time.time()-self.startTime)
        if runtime > 3600:
            h = int(runtime/3600)
            m = int(runtime % 3600/60)
            s = runtime % 3600 % 60
            runtime = f'{h}h{m}m{s}s'
        elif runtime > 60:
            m = int(runtime/60)
            s = runtime % 60
            runtime = f'{m}m{s}s'
        else:
            runtime = f'{runtime}s'
        return runtime

    def zip_crack(self, pwd):
        runtime = self.show()
        print(f'破解已用时: {runtime} 当前密码: {pwd}', end='\r')
        try:
            zip_file = ZipFile(self.filename)
            zip_file.pwd = pwd.encode()
            zip_file.extractall()
            print(f'破解已完成: {runtime} 压缩密码: {pwd}')
            with open('res.txt', 'w') as f:
                f.write(pwd)
            os._exit(0)
        except:
            pass

    def rar_crack(self, pwd):
        runtime = self.show()
        print(f'破解已用时: {runtime} 当前密码: {pwd}', end='\r')
        try:
            rar_file = RarFile(self.filename, pwd=pwd)
            rar_file.extractall()
            print(f'破解已完成: {runtime} 压缩密码: {pwd}')
            with open('res.txt', 'w') as f:
                f.write(pwd)
            os._exit(0)
        except:
            pass

    def crack(self, funcname):
        book = open(self.bookname)
        with cf.ThreadPoolExecutor(12) as tp:
            while True:
                pwd = book.readline().strip()
                tp.submit(funcname, pwd)

    def main(self):
        if self.filename.endswith('.zip'):
            filetype = 1
        elif self.filename.endswith('.rar'):
            filetype = 0
        else:
            print('不支持的压缩格式，必须是rar或zip')
            os._exit(0)
        if filetype:
            self.crack(self.zip_crack)
        else:
            self.crack(self.rar_crack)


if __name__ == "__main__":
    CompressionCrack().main()
```
# 软件打包
推荐在`pipenv`创建的虚拟环境下打包，这样打包的体积会很小，具体打包教程如下：
1. 执行命令`pip install pipenv`安装`pipenv`
2. `cd`到项目路径，运行命令`pipenv install`创建虚拟环境
3. 运行命令`pipenv shell`激活虚拟环境
4. 安装项目开发中用到的第三方模块：`pip install unrar`
5. 安装打包工具：`pip install pyinstaller`
6. 执行打包命令：`pyinstaller -F -i app.ico run.py`

**第6步执行打包命令前先停一下。**

`unrar`模块依赖库文件`UnRAR64.dll`，所以先把`UnRAR64.dll`复制到项目路径下（`win32`复制`UnRAR.dll`）。

然后修改pipenv创建的虚拟环境里面的unrar的代码，具体是修改`C:\Users\xxx\.virtualenvs\python-compression-crack-ZMK49n5q\Lib\site-packages\unrar`路径下的`unrarlib.py`文件，将第33行代码由`lib_path = os.environ.get('UNRAR_LIB_PATH', None)`改为`lib_path = 'UnRAR64.dll'`。

好了，可以执行打包命令了：`pyinstaller -F -i app.ico run.py`。
# 引用参考
> [https://blog.csdn.net/qq_42951560/article/details/110097655](https://blog.csdn.net/qq_42951560/article/details/110097655)
