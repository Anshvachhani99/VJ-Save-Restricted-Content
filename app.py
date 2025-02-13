#--> Standard module & library
import json

#--> Flask
from flask import Flask, Response, request
from flask_cors import CORS

#--> Initialize Flask App
app = Flask(__name__)
CORS(app=app)

#--> Local module
from python.terabox1 import TeraboxFile as TF1, TeraboxLink as TL1
from python.terabox2 import TeraboxFile as TF2, TeraboxLink as TL2, TeraboxSession as TS

#--> Global Variable
config = {
    'status': 'success',  
    'message': 'Cookie added successfully',
    'mode': 2,
    'user_id': 'oV3yVUBAotSkMW8ADJymPYDbtqG15hRwCCcrBl3CORYIWatFbhQeOPV6Z_Q',
    'cookie': 'lang=id; ndus=8B58AEF11A9105323E995AB093E368AE22EC55FDB6EA507BE0A3FA87E3AE5F9D;'
}


#--> Home Route (For Koyeb)
@app.route('/')
def home():
    return 'Tech VJ - TeraDL Backend Running Successfully!'

#--> Get Config App
@app.route('/get_config', methods=['GET'])
def getConfig() -> Response:
    global config
    try:
        x = TS()
        x.generateCookie()
        x.generateAuth()
        log = x.isLogin
        config = {'status': 'success', **x.data} if log else {
            'status': 'failed',
            'message': 'cookie terabox nya invalid bos, coba lapor ke dapunta',
            'mode': 1,
            'cookie': ''
        }
    except Exception as e:
        config = {'status': 'failed', 'message': f'Error in config.json: {str(e)}', 'mode': 1, 'cookie': ''}
    return Response(response=json.dumps(config, sort_keys=False), mimetype='application/json')

#--> Get file
@app.route('/generate_file', methods=['POST'])
def getFile() -> Response:
    global config
    try:
        data: dict = request.get_json()
        result = {'status': 'failed', 'message': 'invalid params'}
        mode = config.get('mode', 1)
        cookie = config.get('cookie', '')

        if data.get('url') and mode:
            if mode == 1 or cookie == '':
                TF = TF1()
            elif mode == 2:
                TF = TF2(cookie)
            TF.search(data.get('url'))
            result = TF.result
    except Exception as e:
        result = {'status': 'failed', 'message': f'Error in terabox app: {str(e)}'}
    
    return Response(response=json.dumps(result, sort_keys=False), mimetype='application/json')

@app.route('/generate_link', methods=['POST'])
def getLink() -> Response:
    global config
    try:
        data : dict = request.get_json()
        result = {'status':'failed', 'message':'invalid params'}
        mode = config.get('mode', 1)
        if mode == 1:
            required_keys = {'fs_id', 'uk', 'shareid', 'timestamp', 'sign', 'js_token', 'cookie'}
            if all(key in data for key in required_keys):
                TL = TL1(**{key: data[key] for key in required_keys})
                TL.generate()
        elif mode == 2:
            required_keys = {'url'}
            if all(key in data for key in required_keys):
                TL = TL2(**{key: data[key] for key in required_keys})
            pass
        else : result = {'status':'failed', 'message':'gaada mode nya'}
        result = TL.result
    except: result = {'status':'failed', 'message':'wrong payload'}
    return Response(response=json.dumps(result, sort_keys=False), mimetype='application/json')





#--> Run Flask App on Koyeb
if __name__ == "__main__":
    app.run()
