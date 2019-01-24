import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

from flask import Flask
from flask import request
from flask import Response
from pathlib import Path
import subprocess


app = Flask(__name__)

def cmd(cmd_str):
    return subprocess.Popen([cmd_str], stdout=subprocess.PIPE).communicate()[0]

def resContent(xcresult_path):

    if Path(xcresult_path).exists():
        index_path = xcresult_path + '/index.html'
        if not Path(index_path).exists():
            command = 'xchtmlreport -r "{}"'.format(xcresult_path)
            print("Report generation: {}".format(command))
            res = subprocess.Popen(['xchtmlreport', '-r', '"{}"'.format(xcresult_path)], stdout=subprocess.PIPE).communicate()[0]
            print(res)
            print("Report generation done")
        return Path(index_path).read_text()
    else:
        return "no xcresult"



@app.route('/')
def index():
    # link = "http://0.0.0.0:5244/report?xcresult_path=/Users/bogdan/xcode/jibral/testReports/Test-JWTestsUI-2018.12.07_11-45-06-0300.xcresult"
    link = "server-mini.local:5244/report?xcresult_path=/Library/Developer/XcodeServer/IntegrationAssets/69a4014569ed0e3c579b0695930de236-JWI-R17%20Sim%20iPhone%206%2012.1/11/xcodebuild_result.xcresult"
    return "xcreportService <a href='{}'>Using example</a>".format(link)

@app.route('/report', methods=['GET'])
def get_status():
    xcresult_path = request.args.get("xcresult_path")
    contents = resContent(xcresult_path)

    resp = Response(response=contents,
                    status=200,
                    mimetype='text/html')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5244, debug=False)
