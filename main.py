import mistune
import re
import argparse
import os
from pygments import highlight,lexers,formatters
from bs4 import BeautifulSoup
from mistune.directives import DirectiveToc,DirectiveInclude
from mistune.plugins import plugin_footnotes,\
plugin_strikethrough,plugin_table,plugin_url,\
plugin_task_lists,plugin_def_list,plugin_abbr

class RendererwithCSS(mistune.HTMLRenderer):
    table_color = False
    table_caption = ''
    def __init__(self):
        super().__init__(escape=False)
    def block_code(self, code, lang=None):
        if lang:
            lexer = lexers.get_lexer_by_name(lang, stripall=True)
            formatter = formatters.HtmlFormatter(noclasses=True, style='github-dark', linenos='inline')
            return highlight(code, lexer, formatter)


    def heading(self, text, level):
        text = text.replace('<BR>', '<br/>')
        cl = re.search(r'^([\s\S]+){(\..+)}$', text)
        clStr = ''
        if cl is not None:
            clStr = cl.group(2)
            clStr = f' class="{' '.join([i[1:] for i in clStr.split()])}"'
            text = cl.group(1)
        idStr = f' id="{level}_{text.replace('<br/>', ' ').replace('<br>', ' ').replace(' ', '_')}"'
        return f'<h{level}{idStr}{clStr}>{text}</h{level}>'

    def paragraph(self, text):
        cl = re.search(r'^([\s\S]+){(\..+)}$', text)
        if cl is not None:
            clStr = cl.group(2)
            clStr = ' '.join([i[1:] for i in clStr.split()])
            return f'<p class="{clStr}">{cl.group(1)}</p>\n'
        return f'<p>{text}</p>\n'


    def block_quote(self, text):
        cl = re.search(r'^([\s\S]*)<(.*)>{(\..+)}</(\2)>$', text)
        if cl is not None:
            clStr = cl.group(3)
            clStr = ' '.join([i[1:] for i in clStr.split()])
            return f'<blockquote class="{clStr}">\n{cl.group(1)}</blockquote>\n'
        return f'<blockquote>\n{text}</blockquote>\n'


    def codespan(self, text):
        if text.startswith('%') and text.endswith('%'):
            self.table_caption = text[1:-1]
            return ''
        return '<code>' + mistune.escape(text) + '</code>'

    def table(self, text):
        caption = ''
        if self.table_caption:
            caption = f'<caption>{self.table_caption}</caption>\n'
        self.table_caption = ''
        return f'<table>\n{caption}{text}\n</table>'

    def table_head(self, text):
        self.table_color = False
        return f'<thead><tr class="light">\n{text}</tr></thead>\n'

    def table_row(self, text):
        self.table_color = not self.table_color
        clColor = 'colored' if self.table_color else 'light'
        cl = re.search(r'^([\s\S]+){(\..+)}$', text)
        if cl is not None:
            clStr = cl.group(2)+' .'+clColor
            clStr = ' '.join([i[1:] for i in clStr.split()])
            return f'<tr class="{clStr}">\n{cl.group(1)}</tr>\n'
        return f'<tr class="{'colored' if self.table_color else 'light'}">\n{text}</tr>\n'

    def table_cell(self, text, align=None, is_head=False):
        label = ''
        headStr = ''
        if is_head:
            label = 'th'
            headStr = ' nowarp'
            if re.search(r'^d\d{1,3}$', text) is not None:
                headStr = f' width={15*len(text)+10}{headStr}'
        else:
            label = 'td'

        cl = re.search(r'^([\s\S]*){(\..+)}$', text)
        alignStr = 'aligned_'+align if align is not None else ''
        clStr = ''
        if cl is not None:
            if not cl.group(1):
                return text
            else:
                clStr = cl.group(2)+(' .'+alignStr if alignStr else '')
                clStr = ' '.join([i[1:] for i in clStr.split()])
                text = cl.group(1)
        if clStr or alignStr:
            clStr = f' class="{clStr}{' ' if clStr and alignStr else ''}{alignStr}"'

        return f'<{label}{clStr}{headStr}>{text}</{label}>\n'

    def link(self, link, text=None, title=None):
        clStr = ''
        titleStr = ''
        if text is not None:
            cl = re.search(r'^([\s\S]*){(\..+)}$', text)
            if cl is not None:
                clStr = cl.group(2)
                clStr = ' class="' +' '.join([i[1:] for i in clStr.split()]) + '"'
                text = cl.group(1)
        if text is None or not text:
            text = link
        if title is not None:
            titleStr = f' title="{title}"'
        return f'<a href="{link}"{clStr}{titleStr}>{text}</a>'


markdown = mistune.create_markdown(renderer=RendererwithCSS(), plugins=[plugin_table, plugin_def_list, plugin_strikethrough,plugin_footnotes])
parser = argparse.ArgumentParser(description='Convert markdown with css-labe into html')
parser.add_argument('-f', '--filename', type=str, metavar='xxx.md', help='The name(or path) of markdown file.', required=True)
parser.add_argument('-c', '--cssfile', type=str, metavar='xxx.css', help='The .css file name to be used in label <link>.', default='style.css')
parser.add_argument('-e', '--encoding', type=str, help='As if you need this option in reading file. The default is utf-8, while the outputs are always in gbk.', default='utf-8')
parser.add_argument('-t', '--title', type=str, help='As if you need this option to set file title.', default='')
args = parser.parse_args()

mdText = ''
with open(args.filename ,"r+",encoding=args.encoding) as f:
    mdText = f.read()

filename = os.path.split(args.filename)[1][0:-3]
fileHead = f"""
<head>
    <title>{args.title}</title>
    <meta name="generator" content="MarkdownWithCSS">
    <meta http-equiv="Content-Type" content="text/html; charset=gbk">
    <link rel="stylesheet" type="text/css" href="{args.cssfile}">
</head>
"""
githubAnnounce = '<!--coding: gbk-->\n'

md_HTML = githubAnnounce+fileHead+markdown(mdText)

bs = BeautifulSoup(md_HTML, 'lxml')
if bs.title.string is None:
    if bs.h1 is not None and bs.h1.string is not None:
        bs.title.string = str(bs.h1.string)
    elif filename is not None:
        bs.title.string = str(filename)

with open(filename+'.html',"wb+") as f:
    f.write(bs.encode('gbk'))
    # f.write(bs.prettify(encoding='gbk', formatter='minimal'))