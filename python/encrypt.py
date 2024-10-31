# -*- coding: utf-8 -*-
"""
@File    : encrypt.py
@Time    : 2024/05/07 11:43:09
@Author  : WHY
@Version : 1.0
@Desc    : python项目代码加密脚本
"""

from __future__ import annotations

import ast
import os
import shutil
import sys
from pathlib import Path
from time import sleep


class RemoveAnnotationsTransformer(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        # 移除函数返回值的类型注解
        node.returns = None

        # 移除函数参数的类型注解
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None

        # 继续遍历函数体内的语句
        return self.generic_visit(node)

    def visit_AnnAssign(self, node):
        # 如果是纯类型注解语句(没有赋值),则移除
        if node.value is None:
            return None
        else:
            # 创建新的Assign节点,并设置正确的行号信息
            new_node = ast.Assign(targets=[node.target], value=node.value)
            # 从原AnnAssign节点复制行号信息
            new_node.lineno = node.lineno
            new_node.col_offset = node.col_offset
            # 返回新的Assign节点,effectively移除了类型注解但保留了赋值
            return new_node


class Encrypt:
    '''
    利用cython实现python项目代码加密,保留`'main.py','manage.py'`为入口文件
    '''

    # setup.py文件的源码格式
    setup_fmt = r'''
try:
    from distutils.core import setup
    from traceback import print_exc

    from Cython.Build import cythonize
    if __name__ == '__main__':
        setup(ext_modules=cythonize('{pyfile_name}', compiler_directives={{'language_level': 3}}))
except:
    print('\n\033[31m', end='')
    print_exc()
    print('\033[0m', end='')
        '''

    def __init__(
        self,
        src_path: Path | str,
        dst_path: Path | str = None,
        interpreter_path: Path | str = None,
        pylist: list[str | Path] = None,
    ) -> None:
        """
        ~:利用cython实现python项目代码加密,保留`'main.py','manage.py'`为入口文件

        Parameters
        ----------
        - src_path: Path | str, 项目源文件路径
        - dst_path: Path | str = None, 目的路径,默认为项目根目录同级路径下 `${项目文件夹名称}.encrypt`
        - interpreter_path: Path | str = None, 项目所用python解释器路径,默认为当前解释器
        - pylist: list[str | Path] = None, 指定项目内要加密的文件,只能使用相对于项目文件夹的相对路径, \
            默认不指定,即加密整个项目
        """
        # 源码路径
        self.src_path = Path(src_path).absolute()
        # 目的路径,默认为源码根目录下 ${源码目录名}.encrypt
        if dst_path is None:
            self.dst_path = Path(
                self.src_path.parent / (self.src_path.name + '.encrypt')
            ).absolute()
        else:
            self.dst_path = Path(dst_path).absolute()
        # 目的路径不能与源路径相同
        if self.dst_path.resolve() == self.src_path.resolve():
            raise Exception('为了防止源码被加密后丢失,目的路径不能与源路径相同!')
        # 源码所用python解释器路径,默认为当前解释器
        if interpreter_path is None:
            self.interpreter_path = Path(sys.executable).absolute()
        else:
            self.interpreter_path = Path(interpreter_path).absolute()
        # 不加密的文件列表
        self.exclude = ['__init__.py', 'setup.py', 'main.py', 'manage.py']
        # python文件列表
        self.pylist: list[Path] = []
        # __init__文件列表,存在__init__.py文件时无法使用cython加密
        self.init_file_list: list[Path] = []
        if pylist is None:
            self.not_specified_pylist()
        else:
            self.specified_pylist(pylist)
        # 开始加密
        self.start_encrypt()

    @staticmethod
    def remove_annotation(path_src: Path, path_dst: Path):
        # 读取python源码
        code_str = path_src.read_text(encoding='utf8')
        # 解析代码字符串,得到AST
        tree = ast.parse(code_str)
        # 创建RemoveAnnotationsTransformer实例
        transformer = RemoveAnnotationsTransformer()
        # 遍历并修改AST
        modified_tree = transformer.visit(tree)
        # 将修改后的AST转换回代码字符串
        cleaned_code = ast.unparse(modified_tree)
        # 重新写入无注解的源码
        path_dst.write_text(cleaned_code, encoding='utf8')

    def specified_pylist(self, pylist: list[Path | str]):
        """
        ~:指定项目内要加密的文件,只能使用相对于项目文件夹的相对路径

        Parameters
        ----------
        - pylist: list[str | Path], 指定项目内要加密的文件,只能使用相对于项目文件夹的相对路径
        """
        for item_relative in pylist:
            item_src = self.src_path / item_relative
            item = self.dst_path / item_relative
            # 处理文件
            if item_src.is_file():
                # 如果文件父目录不存在则创建
                if not item.parent.exists():
                    item.parent.mkdir(parents=True)
                # 复制文件并移除注解
                shutil.copyfile(item_src, item)
                Encrypt.remove_annotation(item, item)
                # 将__init__.py文件重命名为__init__.py.not_encrypt,后续恢复原名
                if '__init__.py' in item.parent.iterdir():
                    new_name = item.parent / '__init__.py.not_encrypt'
                    item.rename(new_name)
                    self.init_file_list.append(new_name)
                else:
                    self.pylist.append(item)
            else:
                if item.exists():
                    shutil.rmtree(item)
                # 等待删除结束
                sleep(1)
                shutil.copytree(item_src, item)
                self.search_py(item)

    def not_specified_pylist(self):
        # 如果目的路径存在则删除
        if self.dst_path.exists():
            shutil.rmtree(self.dst_path)
        # 等待删除结束
        sleep(1)
        # 拷贝源码,后续处理在此拷贝的文件夹中进行
        shutil.copytree(self.src_path, self.dst_path)
        # 检索python文件
        self.search_py(self.dst_path)

    def start_encrypt(self):
        pyfile_count = len(self.pylist)
        print(f'\n\033[33m{"-*-"*30}\033[0m', f'开始加密 {pyfile_count} 个文件')
        for i, pyfile in enumerate(self.pylist, start=1):
            setup_str = self.setup_fmt.format_map(
                {
                    'pyfile_name': pyfile.name,
                }
            )
            setup_file = pyfile.parent / 'setup.py'
            setup_file.write_text(setup_str, encoding='utf8')
            # 切换到要加密文件的根目录
            os.chdir(setup_file.parent)
            # 执行加密
            os.system(fr"{self.interpreter_path} setup.py build_ext --inplace")
            # 清理中间文件及源码文件
            self.clean(pyfile)
            # 每个文件加密输出的分界线
            print(f'\033[36m{"-*-"*30}\033[0m', f'{i}/{pyfile_count} 已完成')
            # 将__init__.py文件恢复原名
        print(f'\n\033[36m处理中...\033[0m')
        for init_file in self.init_file_list:
            init_file.rename(init_file.parent / '__init__.py')
        print(f'\n\033[32m加密完成!\033[0m')

    def search_py(self, folder: Path):
        """
        ~:递归搜索python文件,并处理

        Parameters
        ----------
        """

        for item in folder.iterdir():
            if item.is_file():
                # 存在__init__.py文件时windows下无法正常加密,linux下加密后导入会出现问题, \
                # 所以先重命名,后续会改回来
                if item.name == '__init__.py':
                    new_name = item.parent / '__init__.py.not_encrypt'
                    item.rename(new_name)
                    self.init_file_list.append(new_name)
                elif item.name in self.exclude:
                    continue
                elif item.suffix == '.py':
                    # cython加密最好移除类型注解,因为如果如果实际类型与类型注解不同,加密后代码运行时会报错
                    Encrypt.remove_annotation(item, item)
                    self.pylist.append(item)
            # 删除缓存的字节码,.pyc文件可以很轻易反编译为源码,如果要加密,该字节码文件一定要删除
            elif item.name == '__pycache__':
                shutil.rmtree(item)
            # 递归查找
            else:
                self.search_py(item)

    def clean(self, pyfile: Path):
        """
        ~:清理中间文件及源码文件

        Parameters
        ----------
        """
        for path in [
            'build',
            pyfile.stem + '.c',
            pyfile.stem + '.py',
            'setup.py',
        ]:
            path = pyfile.parent / path
            if path.exists():
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)


if __name__ == '__main__':

    Encrypt(r'./')
