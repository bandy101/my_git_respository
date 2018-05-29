
#-------------------------#_-------------
os.path.splitext()可以直接让你得到文件扩展名
>>> os.path.splitext('/path/to/file.txt')
('/path/to/file', '.txt')
os.path.split
>>> os.path.split('/Users/michael/testdir/file.txt')
('/Users/michael/testdir', 'file.txt')

#文件重命名
>>> os.rename('test.txt', 'test.py')
#删除文件
>>>os.remove('filename')
#列出当前目录下的所有目录    
>>> [x for x in os.listdir('.') if os.path.isdir(x)]
['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Applications', 'Desktop', ...]
#要列出所有的.py文件，也只需一行代码：
 [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']
#复制文件
    import os,shutil
    shutil.copyfile(srcfile_path_name,dstfile_path_name) 
    shutil.copytree(sourceSrcDir, dstSrcDir) #复制文件夹

# 创建多级目录：os.makedirs（"/Users/ximi/version"）
# 创建单个目录：os.mkdir（"project"）
#shutil.move(srcfile,dstfile)          #移动文件
#shutil.rmtree("dir")    空目录、有内容的目录都可以删
