from __future__ import annotations

import re
from pathlib import Path
from typing import Literal


def replace_images_link(
    file_path: str | Path,
    owner: str,
    repo: str,
    proxy: Literal['jsdelivr'] = None,
    html_link: bool = False,
):
    """
    ~:替换 Markdown 文件中的图片链接为指定的服务器链接。

    Parameters:
    ----------
    - file_path: str | Path, 文件路径
    - owner: str, 仓库所有者
    - repo: str, 仓库名
    - proxy: Literal['jsdelivr'] = None, 代理
    - html_link: bool = False, 是否生成 HTML 链接

    Returns:
    -------
    None: 该函数会将修改后的内容写入一个新文件。
    """
    file_path = Path(file_path)
    markdown_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    if proxy is None:
        base_url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/'
    elif proxy == 'jsdelivr':
        base_url = f'https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/'
    else:
        raise ValueError("不支持的代理选项")

    # 替换图片链接
    markdown_text_new = re.sub(
        markdown_image_pattern, fr'![\1]({base_url}\2)', markdown_text
    )
    # 生成 HTML 链接
    if html_link:
        html_text = re.sub(
            markdown_image_pattern, fr'<img src="{base_url}\2" alt="\1">', markdown_text
        )
        markdown_text_new = html_text

    # 将修改后的内容写回文件
    output_file_path = file_path.parent / (file_path.stem + '.new' + file_path.suffix)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(markdown_text_new)


if __name__ == '__main__':
    # 示例用法
    file_path = r'vscode扩展推荐.md'
    replace_images_link(
        file_path,
        'gosoline',
        'WHY_docs',
        'jsdelivr',
        True,
    )
