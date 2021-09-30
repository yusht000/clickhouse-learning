#!/usr/bin/env python3
# coding: utf-8

__version__ = "1.0.0"
__date__ = "20210930"
__welcome__ = '''
  .--,       .--,
 ( (  \.---./  ) )
  '.__/o   o\__.'
     {=  ^  =}
      >  -  <
     /       \
    //       \\
   //|   .   |\\
   "'\       /'"_.-~^`'-.
      \  _  /--'         `
    ___)( )(___
   (((__) (__)))   不积小流，无以成江海!
'''

from mclib.utils.models import UserDataProducer
from mclib.utils.models import ItemDataProducer
from mclib.utils.models import  DB

UserDataProducer = UserDataProducer()
ItemDataProducer = ItemDataProducer()
DB = DB()