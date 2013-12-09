# Built-in libs
import os
import re
import cgi
import json
import urllib
import logging

# External GAE libs
import webapp2
import jinja2

# Project libs
from lib import utils
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers

# 3rd party libs
from lib.xml import dicttoxml as xml



# Initialize global variables
template_dir = os.path.join(os.path.dirname(__file__), '..', "views")
jinja_env    = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
default_error_message = "Oops! An error has occured."


# Return a string with the processed template
def render_str(filename, **params):
	filename = os.path.join(*filename.split('/'))
	return jinja_env.get_template(filename).render(params)


# Custom request object used by controllers
class Request(webapp2.Request):
	
	# Add request header
	def add_head(self, head, value):
		self.headers[head] = value
	
	# (Overriden) Get a specified argument from the request
	def get(self, arg, escape = False, **kw):
		r = webapp2.Request.get(self, arg, **kw)
		if escape and r:
			return cgi.escape(r, quote = True)
		return r
	
	# Get a specified cookie's value
	def get_cookie(self, name, default = None):
		return self.cookies.get(name, default)
	
	# Get a list of all cookies
	def get_cookies(self):
		cookies = []
		for i in self.cookies.items():
			cookies.append((i[0], i[1]))
		return cookies
	
	# Get the path's extension
	def get_extension(self):
		separation = self.path.split('.')
		if len(separation) > 1:
			return separation[-1]


# Custom response object used by controllers
class Response(webapp2.Response):
	
	# Add response header
	def add_head(self, head, value):
		self.headers[head] = value
	
	# Render an html template
	def render(self, filename, **params):
		html = render_str(filename, ** params)
		self.out.write(html)
		
	# Delete a cooie from the client
	def del_cookie(self, *a, **kw):
		self.delete_cookie(*a, **kw)
	
	# Set the output content type
	def set_content(self, t):
		self.headers["Content-Type"] = t


# Application class
class Application(webapp2.WSGIApplication):
	
	# Initialize the custom request/response classes
	request_class = Request
	response_class = Response
	
	# Application initializing
	def __init__(self, controllers):
		self._tuples = []
		
		for c in controllers:
			
			# Check if routhing path exists
			if c._path:
				current = c._path
			elif c.__doc__:
				current = c.__doc__
			else:
				raise MissingPathError("No path was found for class `%s`!" % c.__name__)
			
			# Add maps for classes that support models
			if c._supports_model and not c._blob_class:
				self._tuples.append((current + r'/new', c))
				self._tuples.append((current + r'/([0-9]+)(?:\.(.+))?', c))
			self._tuples.append((current, c))
	
	# Update jinja options
	def set_jinja_options(self, **kw):
		global jinja_env
		jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), **kw)
	
	def set_default_error_msg(self, msg):
		global default_error_message
		default_error_message = msg
	
	# Running script
	def initialize(self, **kw):
		webapp2.WSGIApplication.__init__(self, self._tuples, **kw)


# Base request handler
class BaseController(webapp2.RequestHandler):
	
	# Handler path. Override or set as class doc (regex).
	_path = None
	
	# Variable to identify if the class supports a model
	_supports_model = False
	
	# Variable to identify if the class supports blob serving
	_blob_class = False
	
	
	### Methods child classes may override:
	
	# If not authorized, throw a 401 error
	def authorized(self):
		return True
	
	# When showing the index.html page
	def index(self, *a):
		pass
	
	# Before any request
	def init(self, *a):
		pass
	
	### RESTful methods:
	def get(self, *a):
		self.init(*a)
	def post(self, *a):
		self.init(*a)
	def put(self, *a):
		self.init(*a)
	def delete(self, *a):
		self.init(*a)
	def head(self, *a):
		self.init(*a)
	def options(self, *a):
		self.init(*a)
	def trace(self, *a):
		self.init(*a)
	
	
	# Default actions
	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		
		# Extension detector
		self.format = self.request.get_extension()
		
		# Set the variable-like name for the class
		self._name = utils.lowercase(self.__class__.__name__)
		
		# Arguments to consider when rendering templates
		self._params = {}
		
		# Miscellaneous flags
		self._flags = {
			"render": True,
		}
	
	# Get a flag's value
	def get_flag(self, f):
		try:
			return self._flags[f]
		except KeyError:
			raise UnknownFlagError("Flag not found: `%s`" % f)
	
	# Set a flag's value
	def set_flag(self, f, value):
		self._flags[f] = value
		return value
	
	# Return a dict with results from all arguments in the page
	def get_data(self, *a):
		return {i: self.request.get(i) for i in list(a)}
	
	# Add arguments to consider when rendering the page	
	def send_data(self, data = {}, **kw):
		self._params = dict(dict(kw).items() + data.items())
	
	# Render dict as json
	def render_json(self, d):
		self.set_flag("render", False)
		self.response.headers["Content-Type"] = "application/json"
		json_txt = json.dumps(d)
		self.response.out.write(json_txt)
	
	# Render dict as xml
	def render_xml(self, d):
		self.set_flag("render", False)
		self.response.headers["Content-Type"] = "application/xml"
		xml_txt = xml.dicttoxml(d)
		self.response.out.write(xml_txt)
	
	# Overriden method to handle errors.
	# This allows custom error pages.
	def handle_exception(self, exception, debug):
		logging.exception(exception)
		if isinstance(exception, webapp2.HTTPException):
			error_code = exception.code
		else:
			error_code = 500
		try:
			error_msg = self._params["error_msg"]
			self.response.render('error/default_error.html',
		                         status = error_code,
		                         message = error_msg)
		except KeyError:
			self.response.render('error/default_error.html',
		                         status = error_code,
		                         message = default_error_message)
		
		self.response.set_status(error_code)
	
	# Overriden method to raise the error
	# instead of just setting status.
	# This fixes a bug where the error page won't display.
	def error(self, code, message = default_error_message):
		self.send_data(error_msg = message)
		webapp2.abort(code)

# Class for simple pages
class Controller(BaseController):
	
	# Handle GET requests
	def get(self, *a):
		BaseController.get(self, *a)
		if not self.authorized():
			self.error(401, message="Oops! Access has been denied to this page.")
		
		# Actions from index method
		self.index(*a)
		
		# Check if render is on
		if self._flags["render"]:
			self.response.render(self._name + '/index.html', ** self._params)
	
	# Handle POST requests
	def post(self, *a):
		BaseController.post(self, *a)
		self.custom_post(*a)
	
	# Implementable
	def custom_post(self, *a):
		pass


# Class for model-supporting pages
class ModelController(BaseController):
	
	# Model-supporting verification
	_supports_model = True
	
	# Model that the class supports
	model = None
	
	# Handle GET requests
	def get(self, *a):
		
		# Super
		BaseController.get(self, *a)
		
		# Do appropriate actions
		mode = self.get_mode()
		if mode == "index":
			self.index()
			self.get_resources()
		elif mode == "new":
			self.new()
		elif mode == "show":
			self.show(*a)
		
		# Display the correct page
		self.render_appropriate(** self._params)
	
	def post(self, *a):
		BaseController.post(self, *a)
		
		# Check if successful
		c = self.create()
		if c:
			new_entity = self.model(** c)
			new_entity.put()
			self.redirect('/%ss/%s' % (self._name, new_entity.key.id()))
		else:
			self.new()
			self.render_appropriate(** self._params)
	
	# Render appropriate template
	def render_appropriate(self, **params):
		
		# Check if render is on
		if not self._flags["render"]:
			return
		
		# Index page
		if self.get_mode() == "index":
			self.response.render(self._name + '/index.html', ** params)
		
		# Resource page
		elif self.get_mode() == "show":
			
			resource = self.get_resource()
			self.response.render(self._name + '/show.html', resource = resource, ** params)
		
		# Other pages
		else:
			self.response.render(self._name + '/' + self.get_mode() + '.html', ** params)
	
	# In "show" mode
	def get_resource(self):
		path_cut = self.request.path.split('/')[-1].split('.')[0]
		return ndb.Key(self.model.__name__, int(path_cut)).get()
	
	### Methods child classes may override:
	
	# When displaying new.html
	def new(self):
		pass
	
	# When displaying show.html
	def show(self, *a):
		pass
	
	# When doing a POST request
	def create(self):
		pass
	
	# When doing a PUT request
	def edit(self, *a):
		pass
	
	# When getting the resources on index mode
	def get_resources(self, *a):
		r = self.model.all()
		self.send_data(resources = r)
	
	### End
	
	
	# Get the correct page
	def get_mode(self):
		path = self.request.path
		if path[:-1] == '/' + self._name or path[:-1] == '/' + self._name + 's':
			return "index"
		elif re.match(r'([0-9]+)(?:\.(.+))?', path.split('/')[-1]):
			return "show"
		else:
			return path.split('/')[-1]

# Regular class for blob-serving controllers
class BlobController(ModelController):
	
	def get(self, *a):
		upload_url = blobstore.create_upload_url('/%s/upload' % self._name)
		self.send_data(upload_url = upload_url)
		ModelController.get(self, *a)
	
	# Overriden: only do default stuff
	# The UploadController class takes care of the procedure.
	def post(self, *a):
		BaseController.post(self, *a)


# Upload class for blob-serving controllers
class UploadController(blobstore_handlers.BlobstoreUploadHandler, ModelController):
	
	_blob_class = True
	default_class = None
	
	def upload(self):
		try:
			return self.get_uploads()[0]
		except IndexError: pass
	
	def init(self):
		self.model = self.default_class.model
	
	# On GET request
	def get(self, *a):
		self.error(405)
	
	# On POST request
	def post(self, *a):
		BaseController.post(self, *a)
		
		# Check if successful
		c = self.create()
		if c:
			
			# Try to upload
			upload = self.upload()
			if upload:
				
				# Get blob reference
				c['blob_key'] = str(upload.key())
				
				# Delete useless blob argument
				del c['blob']
				
				# Use current arguments left to create the model
				new_entity = self.model(** c)
				new_entity.put()
				self.redirect('/%s/%s' % (self._name, new_entity.key.id()))
			else:
				self.redirect('/%s/new' % self._name)
		
		# Bounce back if form did not pass
		else:
			self.redirect('/%s/new' % self._name)


# Upload class for blob-serving controllers
class DownloadController(blobstore_handlers.BlobstoreDownloadHandler, ModelController):
	
	_blob_class = True
	default_class = None
	
	# Download files from blobstore
	def download(self):
		pass
	
	def init(self, *a):
		self.model = self.default_class.model
	
	def get(self, resource):
		BaseController.get(self, resource)
		entity = self.model.get_by_id(long(resource))
		resource = str(urllib.unquote(entity.blob_key))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)


# Controller for asynchronous requests
class AJAXController(BaseController):
	def initialize(self, *a, **kw):
		BaseController.initialize(self, *a, **kw)
		self._flags["render"] = False
	
	# Shortcut for output
	def puts(self, s):
		self.response.out.write(s)
	
	# Overridables
	def GET(self, *a): pass
	def POST(self, *a): pass
	def PUT(self, *a): pass
	def DELETE(self, *a): pass
	
	# Call overridables
	def get(self, *a):
		BaseController.get(self, *a)
		self.GET(*a)
	def post(self, *a):
		BaseController.post(self, *a)
		self.POST(*a)
	def put(self, *a):
		BaseController.put(self, *a)
		self.PUT(*a)
	def delete(self, *a):
		BaseController.delete(self, *a)
		self.DELETE(*a)

# Error thrown by controllers when no routing path is found
class MissingPathError(Exception): pass

# Error thrown by controllers when a requested flag is not found
class UnknownFlagError(Exception): pass

