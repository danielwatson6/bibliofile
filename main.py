import controllers

from lib.server import Application


app = Application(*controllers.all_classes())
