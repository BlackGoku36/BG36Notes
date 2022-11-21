import json
import os
from subprocess import Popen, PIPE
import shutil
import sys
import shutil

# UTIL functions ------

def create_dir(file_path):
    try:
        os.mkdir(file_path)
    except:
        x = 0

def remove_dir(file_path):
    try:
        shutil.rmtree(file_path)
    except:
        x = 0

# UTIL functions ------

path_to_pandoc = 'pandoc'
try:
    path_to_pandoc = sys.argv[1]
except:
    print('Trying installed pandoc at PATH')

profile = {}
blogs = []
contacts = []

mailSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-mail">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
            </svg>'''
twitterSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-twitter">
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z">
                </path>
            </svg>'''
githubSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-github">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22">
                </path>
            </svg>'''

# Make button
switch_theme_btn_html = '''
<button id="btn" onclick="setTheme()">THEME</button>
'''
switch_theme_btn_js = ""

with open('js/theming.js', 'r') as file:
    switch_theme_btn_js += "<script>"
    switch_theme_btn_js += ''.join(file.readlines())
    switch_theme_btn_js += "</script>"

with open('profile.json', 'r') as file:
    profile = json.loads(''.join(file.readlines()))

for blog in profile["blogs"]:
    isSeries = False
    try:
        series = blog["series"]
        isSeries = True
        blogs.append("<details>")
        blogs.append("<summary>"+blog["name"]+"</summary>")
        for chapter in series:
            name = chapter["name"]
            link = chapter["link"]
            isDisabled = False
            try:
                isDisabled = chapter["disabled"]
            except:
                x = 0
            if isDisabled == True:
                blogs.append("<a class='disabled' href='"+link[:-3]+".html"+"'> <li>"+"<s>"+name+"</s>"+"</li></a>")
            else:
                blogs.append("<a href='"+link[:-3]+".html"+"'> <li>"+name+"</li></a>")
        blogs.append("</details>")
    except:
        x = 0

    if isSeries == False:
        name = blog["name"]
        link = blog["link"]
        isDisabled = False
        try:
            isDisabled = blog["disabled"]
        except:
            x = 0
        if isDisabled == True:
            blogs.append("<a class='disabled' href='"+link[:-3]+".html"+"'> <li>"+"<s>"+name+"</s>"+"</li></a>")
        else:
            blogs.append("<a href='"+link[:-3]+".html"+"'> <li>"+name+"</li></a>")

try:
    contacts.append("<a href='"+profile["github"]+"'>"+githubSVG+"</a>")
except:
    print("-> Github account skipped")

try:
    contacts.append("<a href='"+profile["twitter"]+"'>"+twitterSVG+"</a>")
except:
    print("-> Twitter account skipped")

try:
    contacts.append("<a href='mailto: "+profile["mail"]+"'>"+mailSVG+"</a>")
except:
    print("-> Mail skipped")

contact = ""
if(len(contacts)!=0):
    contact = '<br><h2>CONTACTS</h2><hr><div class="contact">'+''.join(contacts) + '</div>'

copyright = ""
try:
    copyright = "<footer>"+profile["copyright"]+"</footer>"
except:
    print("-> copyright skipped")

indexHTML = [
    '''<!DOCTYPE html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="index.css"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>''', profile["name"], '''</title></head>
    <body>
    <div class="contents">
    <h1 style="display: inline-block; padding-right: 20px;">''', profile["name"], '''</h1>''',
    switch_theme_btn_html,
    '''<hr>
    <div class="profile">
        <img src="''', profile["profile_picture"], '''"
            width="150" height="150" style="float:left; margin-right: 15px; margin-top: 5px;">
        <p>''',profile["description"],'''</p>
        <br>
    </div>
    <h2>BLOGS</h2><hr>
    <div class="project">
        <ul>''', ''.join(blogs), '''</ul>
    </div>''', 
    contact, 
    '''</div>''', 
    copyright, switch_theme_btn_js,'''
    </body>
    </html>
    '''
]

# Clean build docs
remove_dir("docs")
create_dir("docs")

with open('docs/index.html', 'w') as file:
    file.writelines(indexHTML)


def get_home_button(file_name):
    return "<a class='home' href="+((len(file_name.split('/')) - 1) * '../')+"index.html"+">HOME</a>"+switch_theme_btn_html+'''
---

'''

# Copy resources
shutil.copy(profile["profile_picture"], 'docs/'+profile["profile_picture"])
shutil.copy('css/blog.css', 'docs/blog.css')
shutil.copy('css/index.css', 'docs/index.css')
shutil.copy('js/highlight.min.js', 'docs/highlight.min.js')

# Clean build assets
remove_dir("docs/assets")
create_dir("docs/assets")

with os.scandir('blogs/assets/') as assets:
    for asset in assets:
        if (".png" or ".jpeg" or ".mp4" or ".mov") in asset.name:
            shutil.copy('blogs/assets/'+asset.name, 'docs/assets/'+asset.name)

def md_to_html(title, file_name):
    process = Popen([
            path_to_pandoc, 
            '--metadata', 'title='+title,
            '-s', '--no-highlight', 
            '-c', ((len(file_name.split('/')) - 1) * '../') + 'blog.css', 
            'docs/'+file_name, 
            '-o', 'docs/'+file_name[:-3]+'.html'
        ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    error = bytes.decode(stderr)
    if(error == ""):
        print('\033[32m '+file_name+' successfully translated to html'+' \033[0m')
    else:
        print("\033[31m '"+error+"' \033[0m")

def create_blog(title, file_name, dir_name):
    blogContents = []
    blogContents.append('<h1>' + profile["name"] + "</h1>")
    blogContents.append('<div class="contents">')
    blogContents.append(get_home_button(file_name))
    with open('blogs/' + file_name, 'r') as file:
        blogContents.append(''.join(file.readlines()))
    blogContents.append("\n")
    blogContents.append('\n<script src="' + ((len(file_name.split('/')) - 1) * '../') +'highlight.min.js"></script><script>hljs.highlightAll();</script>')
    blogContents.append(switch_theme_btn_js)
    blogContents.append('</div>')
    blogContents.append(copyright)
    if(dir_name != ""):
        create_dir('docs/'+dir_name)
    with open('docs/' + file_name, 'w') as file:
        file.writelines(blogContents)
    md_to_html(title, file_name)
    os.remove('docs/' + file_name)

for blog in profile["blogs"]:
    isSeries = False
    try:
        series = blog["series"]
        isSeries = True
        for chapter in series:
            title = chapter["name"]
            file_name = chapter["link"]
            create_blog(title, file_name, file_name.split('/')[0])
    except:
        x = 0

    if isSeries == False:
        title = blog["name"]
        file_name = blog["link"]
        create_blog(title, file_name, "")
