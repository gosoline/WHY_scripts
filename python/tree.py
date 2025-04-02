import argparse
from pathlib import Path
from typing import Callable


class Tree:
    """
    目录树
    """

    # ANSI颜色代码
    BLUE = "\033[34m"
    WHITE = "\033[0m"
    YELLOW = "\033[33m"
    # 图标
    root_icon = '📦'
    dir_icon = '📁'
    file_icon = '📜'
    # 分支
    branch = ['│', '└─', '├─']
    branch_bold = ['┃', '┗━', '┣━']

    def __init__(self) -> None: ...

    def _print_tree(
        self,
        path: Path = None,
        depth: int = None,
        indent: str = " ",
        is_last: bool = True,
        filter_: Callable[[Path], bool] = None,
    ):
        '''
        ~:递归打印目录树方法
        '''
        entries: list[Path] = list(filter(filter_, Path(path).iterdir()))
        dirs = [e for e in entries if e.is_dir()]
        files = [e for e in entries if e.is_file()]
        # 合并目录和文件，目录在前，文件在后
        entries = dirs + files
        total_entries = len(entries)
        total_entries = len(entries)
        for i, entry in enumerate(entries):
            is_dir = entry.is_dir()
            entry_name = entry.name

            if i == total_entries - 1:
                pre_branch = f"{self.branch[1]} "
                new_indent = (
                    indent + "    " if is_last else indent + f"{self.branch[0]}   "
                )
            else:
                pre_branch = f"{self.branch[2]} "
                new_indent = indent + f"{self.branch[0]}   "

            if is_dir:
                print(
                    f"{indent}{pre_branch}{self.dir_icon}{self.BLUE}{entry_name}{self.WHITE}"
                )
                if depth is None or (depth and depth > 1):
                    self._print_tree(
                        path=entry,
                        depth=None if depth is None else depth - 1,
                        indent=new_indent,
                        is_last=(i == total_entries - 1),
                        filter_=filter_,
                    )
            else:
                print(f"{indent}{pre_branch}{self.file_icon}{entry_name}")

    def print_tree(
        self,
        path: str = None,
        depth: int = None,
        bold: bool = True,
        filter_: Callable[[Path], bool] = None,
    ) -> None:
        """
        ~:打印树结构

        Parameters
        ----------
        - path: str = None, 树的路径,为None表示当前路径
        - depth: int = None, 树的深度,为None表示不限制深度
        - bold: bool = True, 是否加粗显示
        - filter_: Callable[[Path], bool] = None, 过滤器函数,为None表示不执行过滤

        Returns
        -------
        - None
        """

        if path is None:
            path = './'
        self.path = Path(path)
        if bold:
            self.branch = Tree.branch_bold
        else:
            self.branch = Tree.branch

        print(f'{self.root_icon}{self.YELLOW}{self.path.absolute().name}{self.WHITE}')

        self._print_tree(
            path=self.path,
            depth=depth,
            indent=' ',
            is_last=True,
            filter_=filter_,
        )


def shell():
    parser = argparse.ArgumentParser(description="Python实现tree命令")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=None,
        help="要遍历的目录路径",
    )
    parser.add_argument("-d", "--depth", type=int, help="限制显示的层数")
    parser.add_argument("--bold_off", action="store_false", help="关闭粗体分支")
    args = parser.parse_args()
    tree = Tree()
    tree.print_tree(
        path=args.path,
        depth=args.depth,
        bold=args.bold_off,
    )


if __name__ == '__main__':
    tree = Tree()
    tree.print_tree(
        path='./',
        depth=3,
        bold=True,
        filter_=lambda path: not str(path).endswith('.git'),
    )

    ...

    # shell()
