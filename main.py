import webapp2
import urllib2
import jinja2
import datetime
import os
import re
import HTMLParser
import random

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=True)

        
class Main(webapp2.RequestHandler):
    def get(self):
        tag_list = []
        html = urllib2.urlopen("""http://www.reddit.com/r/Music+ListenToThis""").read().split("""<a class="title may-blank""")[1:]
        for tag in html:
            data = tag.split("&#32")[0]
            if "youtube" in data or "youtu.be" in data:
                tag_list.append(data)
        music = {}
        for a in tag_list:
            if "[" in a and "]" in a:
                music[str(re.split("""href="|" tabindex="1"|>|</a>""",a)[1][-11:])] = re.split("\[|\]| - | -- ",str(re.split("""href="|" tabindex="1"|>|</a>""",a)[3]).decode("utf-8"))

        template_values = {
            "music":music.items(),
            "play":random.choice(music.keys())
            }
        template = jinja_environment.get_template('Main.html')
        self.response.write(template.render(template_values))

class Search(webapp2.RequestHandler):
    def get(self):
        query = re.sub(" ", "+", self.request.get("query"))
        if "+" in query:
            url = """http://www.reddit.com/r/Music+ListenToThis/search?q=""" + query + """+self%3Ano&restrict_sr=on&sort=relevance&t=all"""
        else:
            url = """http://www.reddit.com/r/Music+ListenToThis/search?q=""" + query + """+self%3Ano&restrict_sr=on&sort=top&t=all"""
        tag_list = []
        html = urllib2.urlopen(url).read().split("""<a class="title may-blank""")[1:]
        for tag in html:
            data = tag.split("&#32")[0]
            if "youtube" in data or "youtu.be" in data:
                tag_list.append(data)
        music = {}
        for a in tag_list:
            if "[" in a and "]" in a:
                music[str(re.split("""href="|" tabindex="1"|>|</a>""",a)[1][-11:])] = re.split("\[|\]| - | -- ",str(re.split("""href="|" tabindex="1"|>|</a>""",a)[3]).decode("utf-8"))

        template_values = {
            "music":music.items(),
            "play":random.choice(music.keys())
            }
        template = jinja_environment.get_template('Main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', Main),
    ('/search', Search)
], debug=True)
