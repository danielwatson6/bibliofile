"""Model and Property classes and associated stuff."""

__author__ = 'watsondaniel6@gmail.com (Daniel Watson)'

import re
import logging

from lib import utils
from google.appengine.ext import ndb, blobstore


__all__ = ['Model', 'BlobModel', 'get_blob_extension',
           'not_empty', 'length_between', 'valid_blob_extension',
           'generic', 'string', 'integer', 'boolean', 'double',
           'text', 'date', 'user', 'key', 'pickle', 'json']

# NOTE: This method is for validation, and thus the
# expected argument is the user's input, not any sort
# of existing/stored/etc blob object.
def get_blob_extension(blob):
    """Get the submitted blob's extension."""
    try:
        filename = blob.split('filename="')[1]
        filename = filename.split('"')[0]
        return filename.split('.')[-1]
    except IndexError: pass


class Model(ndb.Model):
    """Custom Model class.
    
    The custom Model class includes more
    features for all models and their support
    (controllers, templates, etc.)
    
    """
    
    @classmethod
    def all(cls, max = None):
        """Get all the entities from the model."""
        if max:
            return cls.query().fetch(20)
        return cls.query()
    
    def destroy(self):
        """Destroy the entity from the database."""
        self.key.delete()
    
    def uri(self):
        """Get the entity's show page URL."""
        return '/%ss/%s' % (utils.lowercase(self.__module__[7:]), self.key.id())
    
    def edit_uri(self):
        """Get the entity's edit page URL."""
        logging.info(self.uri())
        return self.uri() + '/edit'


class BlobModel(Model):
    """Model class that supports blobs.
    
    The BlobModel class adds the default `blob_key` property
    and methods that support it.
    
    """
    blob_key = ndb.StringProperty(required = True)
    
    def filename(self):
        """Get the blob's filename."""
        obj = blobstore.BlobInfo.get(self.blob_key)
        return obj.filename
    
    def size(self):
        """Get the blob's size in bytes."""
        obj = blobstore.BlobInfo.get(self.blob_key)
        return obj.size
    
    def serve_uri(self):
        """Get the blob's download page."""
        return '/%ss/serve/%s' % (utils.lowercase(self.__module__[7:]), self.key.id())


### Validators:

def not_empty(s):
    return s and s != ''

def length_between(a, b):
    return lambda s: a <= len(s) <= b

def valid_blob_extension(extensions):
    return lambda b: get_blob_extension(b) in extensions


### NDB Property shortcuts:

class generic(ndb.GenericProperty): pass
class string(ndb.StringProperty): pass
class integer(ndb.IntegerProperty): pass
class boolean(ndb.BooleanProperty): pass
class double(ndb.FloatProperty): pass
class text(ndb.TextProperty): pass
class date(ndb.DateProperty): pass
class user(ndb.UserProperty): pass
class key(ndb.KeyProperty): pass
class pickle(ndb.PickleProperty): pass
class json(ndb.JsonProperty): pass

