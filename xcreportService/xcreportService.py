import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

from flask import Flask
from flask import request
from flask import Response
from pathlib import Path
import subprocess
import glob


app = Flask(__name__)

def cmd(cmd_str):
    return subprocess.Popen([cmd_str], stdout=subprocess.PIPE).communicate()[0]

def resContent(xcresult_path):

    if Path(xcresult_path).exists():
        index_path = xcresult_path + '/index.html'
        if not Path(index_path).exists():
            command = 'xchtmlreport -r "{}"'.format(xcresult_path)
            print("Report generation: {}".format(command))
            res = subprocess.Popen(['/usr/local/bin/xchtmlreport', '-r', '{}'.format(xcresult_path)], stdout=subprocess.PIPE).communicate()[0]
            print(res)
            print("Report generation done")
            if Path(index_path).exists():
                return Path(index_path).read_text()
            else:
                return "Report generation fail: {}".format(res)
        else:
            return Path(index_path).read_text()
    else:
        return "no xcresult on: {}".format(xcresult_path)

@app.route('/1_Test/Attachments/<screenshotPath>')
def screenshotForReport(screenshotPath):
    #http://0.0.0.0:5244/1_Test/Attachments/Screenshot%20of%20main%20screen%20(ID%201)_1_5BE71AF9-B68E-4A3A-9196-8C20E5AAA0EF.png
    #http://192.168.7.57:5244/1_Test/Attachments/JWI-T84_1_66AD4AAE-E08B-4E8D-8835-67CA6C4A0764.png
    # screenshotPathPart = "{}_{}*".format(screenshotPath.split("_")[0], screenshotPath.split("_")[1])
    # /Library/Developer/XcodeServer/IntegrationAssets/1d3cf83551620b4254fde68e36cbd7ef-Simulator iPhone 6 10.3.1/30/xcodebuild_result.xcresult/1_Test/Attachments
    findPath = '/Library/Developer/XcodeServer/IntegrationAssets/**/1_Test/Attachments/{}*'.format(screenshotPath)
    # findPath = '/Users/bogdan/xcode/jibral/testReports/**/1_Test/Attachments/{}'.format(screenshotPath)
    for filename in glob.iglob(findPath, recursive=True):
        filename
        break

    if Path(filename).exists():
        return Path(filename).read_bytes()
    else:
        return "No screenshot"

@app.route('/screenshot/<XCS_BOT_ID>/<XCS_BOT_NAME>/<XCS_INTEGRATION_NUMBER>/<SCR_NAME>')
def screenshot(XCS_BOT_ID, XCS_BOT_NAME, XCS_INTEGRATION_NUMBER, SCR_NAME):
    # /Library/Developer/XcodeServer/IntegrationAssets/1d3cf83551620b4254fde68e36cbd7ef-Simulator iPhone 6 10.3.1/30/xcodebuild_result.xcresult/1_Test/Attachments

    findPath = '/Library/Developer/XcodeServer/IntegrationAssets/{}-{}/{}/xcodebuild_result.xcresult/1_Test/Attachments/{}*'.format(XCS_BOT_ID, XCS_BOT_NAME, XCS_INTEGRATION_NUMBER, SCR_NAME)
    for filename in glob.iglob(findPath, recursive=True):
        if Path(filename).exists():
            return Path(filename).read_bytes()

    return "No screenshot for: {} {} {} {}".format(XCS_BOT_ID, XCS_BOT_NAME, XCS_INTEGRATION_NUMBER, SCR_NAME)



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
    app.run(host='0.0.0.0', port=5244, debug=True)
