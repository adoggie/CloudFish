/**
 * Created by 丞寅 on 2015/1/22.
 */


function init_message_server(userToken){
    var gwsprx = null;
    var ws_url =  'wss://'+window.location.host+'/mexs/';
//var api_url = 'http://192.168.10.100:8088/webapi/';


    function TerminalImpl(){
        this.onNotifyMessage = function(msg,ctx){
            //$('#result').html( new Date().toLocaleString() +' issue_user:'+ msg.issue_user +
            //', issue_unit:'+msg.issue_unit+
            //', issue_time:'+msg.issue_time+
            //' , type:'+msg.type );
            var message = "";
            switch (msg.type)
            {
                case 201://新建消息
                    message="您有一条新的消息！";
                    break;
                case 202://回复消息
                    message="您有一条新的回复消息！";
                    break;
                case 203://发送公文（重发公文）
                    message="您有一封新的公文到达，请注意查收！";
                    break;
                case 204://转发公文
                    message="您有一封新的转发公文，请注意查收！";
                    break;
                case 205://催办消息
                    message="您有一条催办公文，请及时处理！";
                    break;
                case 206://撤销发文
                    message="您有一条发文被撤销。";
                    break;
                case 207://重打印申请
                    message="您有一条打印申请,请审批！";
                    break;
                case 208://重打印审批
                    message="您有一条打印申请已审批！";
                    break;
                case 209://转发申请
                    message="您有一条转发申请,请审批！";
                    break;
                case 210://转发审批
                    message="您有一条转发申请已审批！";
                    break;
                default:
                    message = '您有一条未知类型的消息!';
            }
            $.messager.show({
                msg:message,
                timeout:6000,
                showType:'slide'
            });
        };

    }

    TerminalImpl.prototype = new ITerminal();

    var servant = new TerminalImpl();
    RpcCommunicator.instance().init();
    gwsprx = ITerminalGatewayServerProxy.create(ws_url);
    var adapter = RpcCommunicator.instance().createAdapter("test");
    adapter.addServant(servant);
    gwsprx.conn.attachAdapter(adapter);

    gwsprx.conn.setToken(userToken);
    gwsprx.ping_oneway();
    setInterval(function(){
        gwsprx.ping_oneway();
    },1000*50);
}