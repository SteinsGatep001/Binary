
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" ================ Mine Plugin ============
" NERDTree
Bundle 'scrooloose/nerdtree' 
" display button infomation
Plugin 'bling/vim-airline'
" indent lines
Plugin 'Yggdroot/indentLine'
" ranbow parentheses
Plugin 'luochen1990/rainbow'
" icon
Plugin 'ryanoasis/vim-devicons'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
"

" --------------------- plugin 设置 ---------------------------
let g:vim_markdown_folding_disabled = 1
" 在 vim 启动的时候默认开启 NERDTree（autocmd 可以缩写为 au）
autocmd VimEnter * NERDTree
" 设置 NERDTree宽度
let NERDTreeWinSize=25
" 自动关闭tree
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
" 是否显示隐藏文件
let NERDTreeShowHidden=1
" 显示Bookmark
"let NERDTreeShowBookmarks=1
" rigth tree
let NERDTreeWinPos="right"
" indent
let g:indentLine_enabled = 1
let g:indentLine_setColors = 0
let g:indentLine_color_term = 239
let g:indentLine_char = ' '
" vim-dev icon
set encoding=utf8
let g:airline_powerline_fonts = 1
" ranbow
let g:rainbow_active = 1 "0 if you want to enable it later via :RainbowToggle

" --------------------- 个人基本设置 ---------------------------
" delete key set for brew install vim in mac
set backspace=indent,eol,start
" 设置行标
set number
" 设置空格折叠快捷键
nnoremap <space> za
" 开启语法高亮
syntax on
" 允许指定语法高亮方案替换默认的高亮方案
syntax on
" 自动适应不同语言的缩进
filetype on
filetype plugin on
filetype indent on
" 制表符转换为空格
set expandtab
" 设置编辑时制表符占空格数
set tabstop=4
" 设置格式化时制表符占空格数
set shiftwidth=4
" 突出显示当前行
"set cursorline
" 突出显示当前列
"set cursorcolumn


