var fs = require('fs');
var os = require('os');
var ip = require("ip");
var WebSocketClient = require('websocket').client;

var wdt = require('./wdt');


var WS_SUBSCRIPTION_ENABLE = 0;

var usebtswshost = '';    //  테스트베드 IP입니다.
var usebtswsport = '';    //  테스트베드 port입니다.
var usebtswslocaluserid = '';    //  테스트베드에 등록된 사용자입니다.

sh_state = 'connect';

var ifaces = os.networkInterfaces();
for (var dev in ifaces) {
    var iface = ifaces[dev].filter(function (details) {
        return details.family === 'IPv4' && details.internal === false;
    });
    //console.log(iface)
    //if (iface.length > 0) 
    //usebtswslocalip = ifaces.en0[1].address
    //= iface[0].address;

    usebtswslocalip = '10.12.87.160'

    console.log('local ip address : ' + usebtswslocalip);
}

function ws_watchdog() {
    if (sh_state == 'connect') {
        ws_connect(usebtswshost);
    } else if (sh_state == 'connecting') {
        var req_message = {};
        req_message['m2m:rqp'] = {};
        req_message['m2m:rqp'] = {};
        req_message['m2m:rqp'].op = 'CONNECT';
        req_message['m2m:rqp'].userid = usebtswslocaluserid;

        sh_state = 'ready'

        ws_connection.sendUTF(JSON.stringify(req_message['m2m:rqp']));
        console.log('websocket (json) ' + JSON.stringify(req_message['m2m:rqp']) + ' ---->');
    }
}

var ws_client = null;
global.ws_connection = null;
wdt.set_wdt(require('shortid').generate(), 1, ws_watchdog);

function ws_connect(ws_ip) {
    ws_client = new WebSocketClient();

    protocol = 'onem2m.r2.0.json';

    ws_client.connect('ws://' + ws_ip + ':' + usebtswsport, protocol);

    ws_client.on('connectFailed', function (error) {
        console.log('Connect Error: ' + error.toString());
        ws_client.removeAllListeners();

        sh_state = 'connect';
    });

    ws_client.on('connect', function (connection) {
        console.log('WebSocket Client Connected');
        ws_connection = connection;
        sh_state = 'connecting';

        connection.on('error', function (error) {
            console.log("Connection Error: " + error.toString());
            sh_state = 'connect';
        });
        connection.on('close', function () {
            console.log('echo-protocol Connection Closed');
            sh_state = 'connect';
        });

        connection.on('message', ws_message_handler)
    });
}

function ws_message_handler(message) {

    if (message.type === 'utf8') {

        var protocol_arr = this.protocol.split('.');
        var bodytype = protocol_arr[protocol_arr.length - 1];

        var jsonObj = JSON.parse(message.utf8Data.toString());

        if (jsonObj['m2m:dbg'] == null) {
            jsonObj['m2m:dbg'] = jsonObj;
        }

        if (jsonObj['m2m:dbg'].status === 'ERROR') {
            console.log(jsonObj);
            sh_state = 'connect';
        }
        else
            if (jsonObj['m2m:dbg'].status === 'SUCCESS' &&
                jsonObj['m2m:dbg'].message === 'CONNECT') {
                console.log('Socket server connect OK');
                sh_state = 'ready';
            }
            else
                if (jsonObj['m2m:dbg'].status === 'SUCCESS') {
                    ws_message_action(jsonObj);
                }
    }
    else if (message.type === 'binary') {

    }
}

const spawn = require('child_process').spawn;


function ws_message_action(jsonObj) {

    /////////////////////////////////////////////////////////////////////////
    // 수신된 데이터 처리부분.
    /////////////////////////////////////////////////////////////////////////
    console.log('================================================================');
    const result_01 = spawn('python', ['storeData.py', JSON.stringify(jsonObj)]);
    result_01.stdout.on('data', (result) => {
        console.log(result.toString());
    });
}




