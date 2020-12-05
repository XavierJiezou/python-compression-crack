'''依赖模块
pip install unrar
'''

# 环境变量 UNRAR_LIB_PATH: D:\Program Files (x86)\UnrarDLL\x64\UnRAR64.dll

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
            with open('res.txt','w') as f:
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
            with open('res.txt','w') as f:
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
