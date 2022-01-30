# coding: utf-8


from  flask import Flask

from contoller.dd import dd_bp



class Intranet_Server(object) :

    def __init__(self):

        self.app = self.create_app

    @property
    def create_app(self):

         app = Flask(__name__ + "_Intranet_Server")
         app.register_blueprint(dd_bp)
         return  app
