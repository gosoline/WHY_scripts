# Clean, simple, compatible and meaningful.
# Tested on Linux, Unix and Windows under ANSI colors.
# It is recommended to use with a dark background.
# Colors: black, red, green, yellow, *blue, magenta, cyan, and white.
#
# Mar 2013 Yad Smood

# VCS
YS_VCS_PROMPT_PREFIX1=" %{$reset_color%}on%{$fg[blue]%} "
YS_VCS_PROMPT_PREFIX2=":%{$fg[cyan]%}"
YS_VCS_PROMPT_SUFFIX="%{$reset_color%}"
YS_VCS_PROMPT_DIRTY=" %{$fg[red]%}x"
YS_VCS_PROMPT_CLEAN=" %{$fg[green]%}o"

# Git info
local git_info='$(git_prompt_info)'
ZSH_THEME_GIT_PROMPT_PREFIX="${YS_VCS_PROMPT_PREFIX1}git${YS_VCS_PROMPT_PREFIX2}"
ZSH_THEME_GIT_PROMPT_SUFFIX="$YS_VCS_PROMPT_SUFFIX"
ZSH_THEME_GIT_PROMPT_DIRTY="$YS_VCS_PROMPT_DIRTY"
ZSH_THEME_GIT_PROMPT_CLEAN="$YS_VCS_PROMPT_CLEAN"

# SVN info
local svn_info='$(svn_prompt_info)'
ZSH_THEME_SVN_PROMPT_PREFIX="${YS_VCS_PROMPT_PREFIX1}svn${YS_VCS_PROMPT_PREFIX2}"
ZSH_THEME_SVN_PROMPT_SUFFIX="$YS_VCS_PROMPT_SUFFIX"
ZSH_THEME_SVN_PROMPT_DIRTY="$YS_VCS_PROMPT_DIRTY"
ZSH_THEME_SVN_PROMPT_CLEAN="$YS_VCS_PROMPT_CLEAN"

# HG info
local hg_info='$(ys_hg_prompt_info)'
ys_hg_prompt_info() {
    # make sure this is a hg dir
    if [ -d '.hg' ]; then
        echo -n "${YS_VCS_PROMPT_PREFIX1}hg${YS_VCS_PROMPT_PREFIX2}"
        echo -n $(hg branch 2>/dev/null)
        if [[ "$(hg config oh-my-zsh.hide-dirty 2>/dev/null)" != "1" ]]; then
            if [ -n "$(hg status 2>/dev/null)" ]; then
                echo -n "$YS_VCS_PROMPT_DIRTY"
            else
                echo -n "$YS_VCS_PROMPT_CLEAN"
            fi
        fi
        echo -n "$YS_VCS_PROMPT_SUFFIX"
    fi
}

# 添加环境变量在 ohmyzsh的zshrc中:
# export ZSH=${ohmyzsh根目录}.oh-my-zsh
# export ZSH_COMPDUMP=$HOME/.zcompdump  # 否则会[出现`rm: 无法删除 xxx`]
# export XDG_CONFIG_HOME=$HOME/.config  # 否则会出现权限问题
# export CONDARC=$HOME/.condarc  # 否则会出现权限问题
# ZSH_THEME="why_ys"  设置主题

# 在`/etc/zshrc`中:
# source ${zsh.d根目录}/ohmyzsh.zshrc
# source ${zsh.d根目录}/conda.zshrc

# 在`/etc/zshrc`中:先source ohmyzsh的zshrc,再source conda的zshrc,否则会[出现PYTHON_VERSION显示不正确]

# Conda info
local conda_info='$(conda_prompt_info)'
conda_prompt_info(){
    # 当前python路径
    export CURRENT_PYTHON_PATH=$(which python)
    # 检查当前python路径是否以$CONDA_PREFIX开头,$CONDA_PREFIX是conda安装路径
    if [ -n "$CONDA_DEFAULT_ENV" ]&&[[ $CURRENT_PYTHON_PATH == $CONDA_PREFIX* ]]; then
        echo -n "$CONDA_DEFAULT_ENV "
    else
        echo -n ""
    fi
}

# Python info
local python_info='$(python_prompt_info)'
python_prompt_info(){
    # 显示python版本号
    export PYTHON_VERSION=$(python --version 2>/dev/null | awk '{print $2}')
    if [ -n "$PYTHON_VERSION" ]; then
        echo -n "$PYTHON_VERSION"
    else
        echo -n ""
    fi
}

# Bracket info
local bracket_info='$(bracket_prompt_info)'
local left='${bracket_info: 1:1}'
local right='${bracket_info: -1}'
bracket_prompt_info(){
    if [[ -n "$CONDA_DEFAULT_ENV" || -n "$PYTHON_VERSION" ]]; then
        echo -n "()"
    else
        echo -n "%{$reset_color%}"
    fi
}


# Virtualenv
local venv_info='$(virtenv_prompt)'
YS_THEME_VIRTUALENV_PROMPT_PREFIX=" %{$fg[green]%}"
YS_THEME_VIRTUALENV_PROMPT_SUFFIX=" %{$reset_color%}%"
virtenv_prompt() {
    [[ -n "${VIRTUAL_ENV:-}" ]] || return
    echo "${YS_THEME_VIRTUALENV_PROMPT_PREFIX}${VIRTUAL_ENV:t}${YS_THEME_VIRTUALENV_PROMPT_SUFFIX}"
}

local exit_code="%(?,,C:%{$fg[red]%}%?%{$reset_color%})"

# Prompt format:
#
# PRIVILEGES USER @ MACHINE in DIRECTORY on git:BRANCH STATE [TIME] C:LAST_EXIT_CODE
# $ COMMAND
#
# For example:
#
# % ys @ ys-mbp in ~/.oh-my-zsh on git:master x [21:47:42] C:0
# $

PROMPT="
%{$fg[magenta]%}\
${left}\
${conda_info}\
${python_info}\
${right}\
%{$reset_color%}\
%{$terminfo[bold]$fg[blue]%}#%{$reset_color%} \
%(#,%{$bg[yellow]%}%{$fg[black]%}%n%{$reset_color%},%{$fg[cyan]%}%n) \
%{$reset_color%}@ \
%{$fg[green]%}%m \
%{$reset_color%}in \
%{$terminfo[bold]$fg[yellow]%}%~%{$reset_color%}\
${hg_info}\
${git_info}\
${svn_info}\
${venv_info}\
 \
[%*] $exit_code
%{$terminfo[bold]$fg[red]%}$ %{$reset_color%}"
