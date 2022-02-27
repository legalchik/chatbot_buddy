# -*- coding: utf-8 -*-
from flask import Flask, request

import buddy


app = Flask(__name__)

@app.route('/buddy/texttotext/', methods=['GET'])
def api():
	query_text = request.args.get('text')

	return dict(text = buddy.response(buddy.pipe, question=query_text))



if __name__ == '__main__':
     app.run(threaded=True, port=5000)






