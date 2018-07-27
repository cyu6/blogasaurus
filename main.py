import webapp2
import os
import jinja2
from models import *

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("my_blog.html")
        self.response.write(template.render())

class AboutMeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("about_me.html")
        self.response.write(template.render())

class PostsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_current_dir.get_template("posts.html")
        self.response.write(template.render())
    def post(self):
        # get user responses
        title = self.request.get("title")
        content = self.request.get("content")
        user = self.request.get("user")
        tags = str(self.request.get("tags"))
        tags = tags.split(', ')
        # store the Post and enter into database
        basic_post = Post(title = title, content = content, tags = tags)
        basic_post.put()
        # retrieve the author if they already exist,
        # otherwise enter them into database
        if Author.query(Author.username == user).fetch():
            author = Author.query(Author.username == user).get()
            author.posts.append(basic_post.key)
        else:
            author = Author(username = user, posts = [basic_post.key])
            author.put()
        # blog_posts = []
        # for blog_post_key in author.posts:
            # blog_posts.append(blog_post_key.get())
        template_vars = {
            # "post_title": basic_post.title,
            # "post_content": basic_post.content,
            # "post_tags": basic_post.tags,
            "user": author.username,
            "posts": author.posts # blog_posts
        }

        template = jinja_current_dir.get_template("show_post.html")
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler), #can't be /static.. because it will look in the static folder
    ('/aboutme', AboutMeHandler),
    ('/posts', PostsHandler)
], debug=True)
