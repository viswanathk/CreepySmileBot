#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2



import praw
import time
import logging
from google.appengine.ext import db


frown = u"ಠ_ಠ"
smile = u"ಠ◡ಠ"

readlist = []

r = praw.Reddit(user_agent='CreepySmileBot v0.1 by /u/packsracks')
r.login('CreepySmileBot', 'password')


class ReadList(db.Model):
	readListStorage = db.StringListProperty()
	
class CreepySmileBot(webapp2.RequestHandler):
	def get(self):
	
		try:
			logging.info("Getting the next batch")
			all_comments = r.get_comments("all", limit=None)

			for comment in all_comments:
				#logging.info(comment.body)
				if unicode(comment.body) == frown and comment.id not in readlist:
					comment.reply(smile)
					readlist.append(comment.id)
					logging.info("Found "+comment.id)
			
		
		except Exception, e:
			logging.info(e)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Home of CreepySmileBot')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/CreepySmileBot',CreepySmileBot)
], debug=True)
