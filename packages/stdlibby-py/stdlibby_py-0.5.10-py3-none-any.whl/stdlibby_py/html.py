"""
Opinonated server-side html generation
Integrates with htmx and

Assumes the server producing html is trustworthy
XOR
If it isn't secure, I am more fucked
"""

from functools import partial

def escape_attr(key: str, val: str):
    if '\'' in key:
        key = key.replace('\'', '&#39')
    if '\'' in val:
        val = val.replace('\'', '&#39')
    return key, val

def get_attr_str(attrs: dict)->str:
    """
    Converts a dictionary to an HTML formated attr string, ie 'key='value''
    """
    l = []
    for i in attrs.items():
        key, val = escape_attr(i[0], i[1])
        l.append(f"{key}='{val}'")
    return " ".join(l)

def to_table(lst: list[tuple|dict|list])->str:
    if isinstance(lst[0], tuple):
        pass
    elif isinstance(lst[0], dict):
        pass
    elif isinstance(lst[0], list):
        pass
    else:
        raise Exception(f"{type(lst[0])} is not a valid sub collection")

def to_tag(text: str="", tag: str="div", attrs: dict={}, required_attrs: None|dict=None)->str:
    if required_attrs is not None:
        pass

    if len(attrs) >= 1:
        attr_str = get_attr_str(attrs)
        return f"<{tag} {attr_str}>{text}</{tag}>"
    else:
        return f"<{tag}>{text}</{tag}>"

def to_unclosed(tag: str, attrs: dict={}):
    if len(attrs) >= 1:
        attr_str = get_attr_str(attrs)
        return f"<{tag} {attr_str}/>"
    else:
        return f"<{tag} />"

meta = partial(to_unclosed, "meta")

def from_dict(d: dict, s: list=[])->str:
    if "tag" in d:
        tag_name = d["tag"]
    else:
        tag_name = "div"

    if "content" in d:
        content = d["content"]
    else:
        content = ""

    if "attrs" in d:
        attrs = d["attrs"]
    else:
        attrs = {}

    if isinstance(content, dict):
        s.append(to_tag(tag=tag_name, attrs=attrs))
        return from_dict(content, s=s)
    else:
        s.append(to_tag(content, tag=tag_name, attrs=attrs))
        return "\n".join(s)

div = partial(to_tag, tag="div")
span = partial(to_tag, tag="span")
section = partial(to_tag, tag="section")
article = partial(to_tag, tag="article")
a = partial(to_tag, tag="a")
aside = partial(to_tag, tag="aside")
head = partial(to_tag, tag="head")
body = partial(to_tag, tag="body")
script = partial(to_tag, tag="script")
header = partial(to_tag, tag="header")
footer = partial(to_tag, tag="footer")
p = partial(to_tag, tag="p")
img = partial(to_tag, tag="img")
code = partial(to_tag, tag="code")
html = partial(to_tag, tag="html")

def default_head(title: str):
    title = meta({"title": title})
    resp = meta({"name": "viewport", "content": "width=device-width"})
    return head(" ".join([title, resp]))

def post():
    _head = default_head("tivlet was wrong")
    _body = body()
    return html(_head+_body)

if __name__ == "__main__":
    print(post())
