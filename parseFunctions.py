import re
import hashlib

def heading(markup, string):
    str_md5 = hashlib.md5(string.encode("utf8"))
    str_md5_short = str_md5.hexdigest()[0:5]

    if len(markup) < 5:
        return '''<h{0:} id="{1:}">{2:}</h{0:}>'''.format(len(markup), str_md5_short, string)
    
    return '''<h5>''' + string + '''</h5>'''

def p(string):
    return '''<p class="md-content-font">''' + string + '''</p>'''


def a(string):
    pattern = r"[^!]\[(?P<text>.+?)\]\((?P<link>.+?)\)"
    replaced = r'<a href="\2">\1</a>'
    
    res = re.sub(pattern, replaced, string)

    if res == string:
        return 0

    return res


def img(string):
    pattern = r"!\[(?P<text>.+?)\]\((?P<link>.+?)\)"
    replaced = r'<img src="\2" alt="\1"/>'
    
    res = re.sub(pattern, replaced, string)

    if res == string:
        return 0

    return res


def highlight(string):
    pattern = r"==(?P<text>.+?)=="
    replaced = r'<span class="md-highlight">\1</span>'

    res = re.sub(pattern, replaced, string)

    if res == string:
        return 0

    return res

# def md_match_ul(matched):
#     text = matched.group("text")
#     res = '''<span class="md-underline">{0:}</span>'''.format(text)
#     return res
# def underline(string):
#     pattern = r"__(?P<text>.+?)__"
#     res = re.sub(pattern, md_match_ul, string)
#     if res == string:
#         return 0
#     return res
def underline(string):
    pattern = r"__(?P<text>.+?)__"
    replaced = r'<span class="md-underline">\1</span>'

    res = re.sub(pattern, replaced, string)

    if res == string:
        return 0

    return res

def bold(string):
    pattern = r"\*\*(?P<text>.+?)\*\*"
    replaced = r'<b class="md-bold">\1</b>'

    res = re.sub(pattern, replaced, string)

    if res == string:
        return 0

    return res

def block(string):
    pattern = r"```.*\n(?P<text>.+?)\n```"
    replaced = r'''<div class="md-block">\1</div>'''
    
    res = re.sub(pattern, replaced, string)

    if res == string:
        return 0

    return res