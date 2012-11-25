from markupsafe import Markup

def striptags(html,n=80):
    return Markup(html).striptags()[:n]
