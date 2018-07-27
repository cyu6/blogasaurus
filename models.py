from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty();
    content = ndb.StringProperty();
    tags = ndb.StringProperty(repeated = True);


class Author(ndb.Model):
    username = ndb.StringProperty();
    posts = ndb.KeyProperty(kind = Post, repeated = True)
