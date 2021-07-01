#!/bin/env python
#-*- encoding: utf-8 -*-

'''
convert the markdown symbol to html
'''
import time, os
import re, hashlib
from parseFunctions import *

def getHtmlHeadInfo(head_file):
    res = []

    try:
        with open(head_file, "r", encoding="utf8") as fp:
            for line in fp.readlines():
                line = line.strip()

                if line == "":
                    continue

                res.append(line)
    except:
        pass

    if head_file.split(".")[1] == "css":
        res.insert(0, '''<style type="text/css">''')
        res.append('''</style>''')
    
    return "\n".join(res)

def getMd(md_file):
    res = []

    try:
        with open(md_file, "r", encoding="utf8") as fp:
                text = fp.read()
    except:
        pass

    for line in text.split("\n\n"):
        if line == "":
            continue
        res.append(line)

    return res

def getMdInfo(md_file, *pub_info):
    res = []
    c_time = time.localtime(os.stat(md_file).st_ctime)
    pub_date = time.strftime("%Y-%m-%d", c_time)
    
    if pub_info == ():
        pub_info = ["others"]

    res.append('''{0:}<br>tag:'''.format(pub_date))
    for tag in pub_info:
        res.append('''<span><a class="md-tag-link" 
        href="../index.html?tag={0:}">#{0:}</a></span>'''.format(tag))
    
    res.insert(0, '''<p class="md-info-font">''')
    res.append('''</p>''')

    res.insert(0, '''<div class="md-article-info">''')
    res.append('''</div>''')

    return res

def getToc(toc):
    if len(toc) < 3:
        return 0
    
    res = []
    for markup,header in toc:
        str_md5 = hashlib.md5(header.encode("utf8"))
        str_md5_short = str_md5.hexdigest()[0:5]

        # item = '''<a class="md-toc" href="#{0:}"><div class="md-toc">{1:}{2:}</div></a>'''.format(str_md5_short, "&nbsp"*2*len(markup), header)
        item = '''<a class="md-toc" href="javascript:void(0);" onclick="javascript:document.getElementById('{0:}').scrollIntoView()"><div class="md-toc">{1:}{2:}</div></a>'''.format(str_md5_short, "&nbsp"*4*len(markup), header)
        
        res.append(item)
    
    res.insert(0, '''<div class="md-toc-box">''')
    res.append('''</div>''')

    return res


def parseHead(meta_file, css_file):
    meta_txt = getHtmlHeadInfo(meta_file)
    css_txt = getHtmlHeadInfo(css_file)

    res = []
    res.append(meta_txt)
    res.append(css_txt)

    res.insert(0, '''<head>''')
    res.append('''</head>''')

    return "\n".join(res)

def generateHtml(meta_file, css_file, md_file, *pub_info):
    res = []
    res.append(parseHead(meta_file, css_file))
    res.append(parseMd(md_file, *pub_info))

    res.insert(0, '''<html lang="en">''')
    res.append('''</html>''')

    res.insert(0, '''<!DOCTYPE html>''')

    html_file = md_file.split(".")[0] + ".html"
    with open(html_file, "w", encoding="utf8") as fp:
            fp.write("\n".join(res))

            
def parseMd(md_file, *pub_info):
    md_txt = getMd(md_file)

    toc = []
    res = []
    for md in md_txt:
        # check fo heading
        if "#" == md[0]:
            markup = md[0:md.index(" ")]
            sentence = md[md.index(" "):].strip()
            res.append(heading(markup, sentence))

            if len(markup) < 4:
                toc.append((markup,sentence))

            if markup == "#":
                res += getMdInfo(md_file, *pub_info)
            
            continue
        
        # check code block ```xxxx```
        matched_str = block(md)
        if matched_str != 0:
            md = matched_str
            res.append(md)
            continue

        # check for [xx](yy) link
        matched_str = a(md)
        if matched_str != 0:
           md = matched_str
            
        # check for ![xx](yy) img
        matched_str = img(md)
        if matched_str != 0:
           md = matched_str

        # check for ==xx== highlight
        matched_str = highlight(md)
        if matched_str != 0:
           md = matched_str
            
        # check for __xx__ underline
        matched_str = underline(md)
        if matched_str != 0:
           md = matched_str

        # check for **xx** bold
        matched_str = bold(md)
        if matched_str != 0:
           md = matched_str
            

        res.append(p(md))




    res.insert(0, '''<div class="md-article-box">''')
    res.append('''</div>''')

    # toc
    left_toc = getToc(toc)
    if left_toc != 0:
        res += left_toc

    res.insert(0, '''<body>''')
    res.append('''</body>''')

    return "\n".join(res)



    

if __name__ == "__main__":
    # res = []
    # res.append(parseHead("meta.txt", "style.css"))

    # print(getHtmlHeadInfo("style.css"))
    generateHtml("meta.txt", "style.css", "Hello-GitHub-Pages.md", "github")

    generateHtml("meta.txt", "style.css", "md2html.md", "github")