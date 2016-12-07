/**
 * Created by panchengyin on 15/6/4.
 * 与标签平台对接
 */

//webscoket通信地址
var url ='ws://127.0.0.1:8000';//'ws://192.168.10.193:8080/WebSocketTest/websocket'; //ws://192.168.4.89:8000   //ws://127.0.0.1:9999 ws://localhost:8080/WebSocketTest/websocket

var labelSockert = new Object();
//初始化
labelSockert.init = function(){
    labelSockert.labelWs = new WebSocket(url);
    labelSockert.labelWs.binaryType = "arraybuffer" ;

    labelSockert.callBackFun = null;//回调函数
    labelSockert.maxheartbeatTime = 120;//心跳间隔 单位：秒 最大检测间隔 用于给标签标识平台设置时间
    labelSockert.realheartbeatTime = 60;//实际心跳间隔 必须比最大检测间隔小 否则 将会取消注册
    labelSockert.errorMeassger = '';
    labelSockert.versionType = 1;

//如果为 false 或未定义，则应写入 big-endian 值；否则应写入 little-endian 值。
//big endian是指低地址存放最高有效字节（MSB），而little endian则是低地址存放最低有效字节
    labelSockert.littleEndian = true;

    // 打开Socket
    labelSockert.labelWs.onopen = function(event) {
        console.log('Client received a open', event);
    };

// 监听消息
    labelSockert.labelWs.onmessage = function(event) {
        console.log('Client received a message',event);
        console.log('Client received a data',event.data);
        if(event.data){
            var reMessageHead = new ReMessageHead();
            var bufferViewArray= reMessageHead.getBufferViewArray();
            var reBufferArray = event.data;
            console.log('reBufferArray:',reBufferArray.byteLength);
            var dataview = new DataView(reBufferArray,0);
            var byteOffset = 0;

            for(var i=0;i<bufferViewArray.length;i++){
                var dataBufferView = bufferViewArray[i];
                switch(dataBufferView.dataType){
                    case DATATYPE.INT8:
                        dataBufferView.value = dataview.getInt8(byteOffset);
                        break;
                    case DATATYPE.INT32:
                        dataBufferView.value = dataview.getInt32(byteOffset,labelSockert.littleEndian);
                        break;
                    case DATATYPE.UINT8:
                        var value = "";
                        for (var y=0, strLen=dataBufferView.length; y<strLen; y++) {
                            value = value +dataview.getUint8(byteOffset+y);
                        }
                        dataBufferView.value = value;
                        break;
                    default:

                }
                byteOffset = setByteoffset(byteOffset,dataBufferView);
                console.log('byteOffset:',byteOffset);
            }

            console.log('version:',reMessageHead.version.value);
            console.log('type:',reMessageHead.type.value);
            console.log('result:',reMessageHead.result.value);
            console.log('errcode:',reMessageHead.errcode.value);

            if(reMessageHead.errcode.value!=null&&reMessageHead.errcode.value==0){//成功接收
                switch(reMessageHead.type.value){
                    case 1:    //应用注册
                        var id = "";
                        for (var y = 0, strLen = 36; y < strLen; y++) {
                            id = id + String.fromCharCode(dataview.getUint8(byteOffset + y));
                        }
                        labelSockert.callBackFun(id);
                        break;
                    case 2:    //取消注册
                        var result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 3:    //心跳
                        var result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 5:    //文件加密
                        var result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 6:    //文件解密
                        var result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 9:    //增加权限
                        var result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 12:   //是否拥有权限
                        var result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 16:   //判断是否加密0-未加密，1-加密
                        var errcode = "";
                        var result = "";
                        errcode = reMessageHead.errcode.value;
                        if (errcode == 0){
                            result = reMessageHead.result.value;
                            labelSockert.callBackFun(result);
                        }
                        else
                        {
                            result = "11";
                            labelSockert.callBackFun(result);  
                        }
                        break;
                    case 17:    //上传文件消息
                        var result = "";
                        result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 20:    //判断是否授权0-未授权，1-已授权
                        var result = "";
                        result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 21:     //进行授权
                        var result = "";
                        result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 22:     //获取目录
                        var result = "";
                        result = reMessageHead.errcode.value;
                        var jsonDate = [];
                        if(result == "0"){
                            var totalSize =dataview.getInt32(byteOffset,labelSockert.littleEndian);
                            byteOffset = byteOffset +4;
                            var contentSize = dataview.getInt32(byteOffset,labelSockert.littleEndian);
                            byteOffset = byteOffset +4;
                            if(totalSize>0){
                                for (var y = 0; y < totalSize; y++) {
                                    var fileObject = {};
                                    var fileNameLength = dataview.getInt32(byteOffset,labelSockert.littleEndian);
                                    byteOffset = byteOffset +4;
                                    var fileName = "";
                               
                                    for (var i = 0; i < fileNameLength; i++) {
                                        fileName = fileName + String.fromCharCode(dataview.getUint8(byteOffset));
                                        byteOffset = byteOffset + 1;
                                    }
                                    var isDir = dataview.getInt8(byteOffset);
                                    byteOffset = byteOffset +1;
                                    fileObject.text= fileName;
                                    fileObject.state = isDir==1?'closed':'open';
                                    fileObject.isDir = isDir;
                                    jsonDate.push(fileObject);
                                }
                            }
                        
                        }
                        labelSockert.callBackFun(result,jsonDate);
                        break;
                    case 23:   //下载文件消息
                        var result = "";
                        result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                    case 24:    //web预览文件消息
                        var result = "";
                        result = reMessageHead.errcode.value;
                        labelSockert.callBackFun(result);
                        break;
                }
/*
                if(reMessageHead.type.value==1) { //应用注册
                    var id = "";
                    for (var y = 0, strLen = 36; y < strLen; y++) {
                        id = id + String.fromCharCode(dataview.getUint8(byteOffset + y));
                    }
                    labelSockert.callBackFun(id);
                }else if(reMessageHead.type.value==2){ //取消注册
                    var result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==3){ //心跳
                    var result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==5){ //文件加密
                    var result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==6){ //文件解密
                    var result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==9){ //增加权限
                    var result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==12){ //是否拥有权限
                    var result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }                
                else if(reMessageHead.type.value==16){ //判断是否加密0-未加密，1-加密
                    var errcode = "";
                    var result = "";
                    errcode = reMessageHead.errcode.value;
                    if (errcode == 0){
                        result = reMessageHead.result.value;
                        labelSockert.callBackFun(result);
                    }
                    else
                    {
                        result = "11";
                        labelSockert.callBackFun(result);  
                    }
                    
                }
                else if(reMessageHead.type.value==17){ //上传文件消息
                    var result = "";
                    result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==20){ //判断是否授权0-未授权，1-已授权
                    var result = "";
                    result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==21){ //进行授权
                    var result = "";
                    result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==22){ //获取目录
                    var result = "";
                    result = reMessageHead.errcode.value;
                    var jsonDate = [];
                    if(result == "0"){
                        var totalSize =dataview.getInt32(byteOffset,labelSockert.littleEndian);
                        byteOffset = byteOffset +4;
                        var contentSize = dataview.getInt32(byteOffset,labelSockert.littleEndian);
                        byteOffset = byteOffset +4;
                        if(totalSize>0){
                            for (var y = 0; y < totalSize; y++) {
                                var fileObject = {};
                                var fileNameLength = dataview.getInt32(byteOffset,labelSockert.littleEndian);
                                byteOffset = byteOffset +4;
                                var fileName = "";
                               
                                for (var i = 0; i < fileNameLength; i++) {
                                    fileName = fileName + String.fromCharCode(dataview.getUint8(byteOffset));
                                    byteOffset = byteOffset + 1;
                                }
                                var isDir = dataview.getInt8(byteOffset);
                                byteOffset = byteOffset +1;
                                fileObject.text= fileName;
                                fileObject.state = isDir==1?'closed':'open';
                                fileObject.isDir = isDir;
                                jsonDate.push(fileObject);
                            }
                        }
                        
                    }
                    labelSockert.callBackFun(result,jsonDate);
                }
                else if(reMessageHead.type.value==23){ //下载文件消息
                    var result = "";
                    result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
                else if(reMessageHead.type.value==24){ //web预览文件消息
                    var result = "";
                    result = reMessageHead.errcode.value;
                    labelSockert.callBackFun(result);
                }
*/
            }else{//失败
                if(reMessageHead.type.value==20){ //未授权
                    var result = "";
                    result = reMessageHead.errcode.value;
                    var codelength = dataview.getInt32(byteOffset,labelSockert.littleEndian);
                    var code = "";
                    for (var y = 0, strLen = codelength; y < codelength; y++) {
                        code = code + String.fromCharCode(dataview.getUint8(byteOffset+4 + y));
                    }
                    labelSockert.callBackFun(result,code);
                }
            }
        }
    };

// 监听Socket的关闭
    labelSockert.labelWs.onclose = function(event) {
        console.log('Client notified socket has closed',event);
    };


    labelSockert.labelWs.onerror = function(evt)
    {
        console.log("error");
    };

}


var DATALENGTH = {
    ONE:1,
    FOUR:4,
    EIGHT:8,
    THIRTYTWO:32,
    THIRTYSIX:36
};

var DATATYPE = {
    INT32:"INT32",
    UINT8:"UINT8",
    INT8:"INT8",
    ARRAYBUFFER:"ARRAYBUFFER"
};

var BufferView = (function(){
    var BufferView = function(value,length,dataType){
        this.value = value;
        this.length = length;
        this.dataType = dataType;
    };

    return function(value,length,dataType){
        return new BufferView(value,length,dataType);
    }
})();

//消息头 固定每次都要发送 消息类型  “0001”---  “9999”
//版本号 + 消息类型 + 标识码 + 预留1 +  预留2 + 预留3 + 预留4 + 结束标志(是否是最后一个包 1是最后一个包 0是非最后一个包) +  数据长度 + 数据
// 1    +  4  +   36  +   ４    +  4    +  4     +  4  +   1  +                     4 + len
function MessagerHead (version,type,id,temp1,temp2,temp3,temp4,endType,dataLength,dataBufferViewArray){
    this.version = new BufferView(version,DATALENGTH.ONE,DATATYPE.INT8);
    this.type =new BufferView(type,DATALENGTH.FOUR,DATATYPE.INT32);
    this.id = new BufferView(id,DATALENGTH.THIRTYSIX,DATATYPE.UINT8);
    this.temp1 = new BufferView(temp1,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp2 = new BufferView(temp2,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp3 = new BufferView(temp3,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp4 = new BufferView(temp4,DATALENGTH.FOUR,DATATYPE.INT32);
    this.endType = new BufferView(endType,DATALENGTH.ONE,DATATYPE.INT8);
    this.dataLength = new BufferView(dataLength,DATALENGTH.FOUR,DATATYPE.INT32);
    this.dataBufferViewArray = dataBufferViewArray;
    this.totalLength = this.version.length + this.type.length+this.id.length+this.temp1.length+this.temp2.length+this.temp3.length+this.temp4.length+this.endType.length
    + this.dataLength.length+dataLength;
    this.getBuffer=function(){
        var bufferArray = new ArrayBuffer(this.totalLength);
        var dataview = new DataView(bufferArray,0);
        var byteOffset = 0;
        //版本号占1个字符8位
        dataview.setInt8(byteOffset,this.version.value);
        byteOffset = setByteoffset(byteOffset,this.version);
        dataview.setInt32(byteOffset,this.type.value,labelSockert.littleEndian);
        byteOffset = setByteoffset(byteOffset,this.type);
        for (var i=0, strLen=this.id.value.length; i<strLen; i++) {
            dataview.setUint8(byteOffset+i,this.id.value.charCodeAt(i));
        }
        byteOffset = setByteoffset(byteOffset,this.id);
        dataview.setInt32(byteOffset,this.temp1.value,labelSockert.littleEndian);
        byteOffset = setByteoffset(byteOffset,this.temp1);
        dataview.setInt32(byteOffset,this.temp2.value,labelSockert.littleEndian);
        byteOffset = setByteoffset(byteOffset,this.temp2);
        dataview.setInt32(byteOffset,this.temp3.value,labelSockert.littleEndian);
        byteOffset = setByteoffset(byteOffset,this.temp3);
        dataview.setInt32(byteOffset,this.temp4.value,labelSockert.littleEndian);
        byteOffset = setByteoffset(byteOffset,this.temp4);
        dataview.setInt8(byteOffset,this.endType.value);
        byteOffset = setByteoffset(byteOffset,this.endType);
        dataview.setInt32(byteOffset,this.dataLength.value,labelSockert.littleEndian);
        byteOffset = setByteoffset(byteOffset,this.dataLength);
        if(dataBufferViewArray!=null&&dataBufferViewArray.length>0&&dataLength!=null&&dataLength>0){
            for(var i=0;i<dataBufferViewArray.length;i++){
                var dataBufferView = dataBufferViewArray[i];
                console.log("byteOffset:"+byteOffset+";i:"+i);
                switch(dataBufferView.dataType){
                    case DATATYPE.INT8:
                        dataview.setInt8(byteOffset,dataBufferView.value);
                        break;
                    case DATATYPE.INT32:
                        dataview.setInt32(byteOffset,dataBufferView.value,labelSockert.littleEndian);
                        break;
                    case DATATYPE.UINT8:
                        for (var y=0, strLen=dataBufferView.length; y<strLen; y++) {
                            dataview.setUint8(byteOffset+y,dataBufferView.value.charCodeAt(y));
                        }
                        break;
                    case DATATYPE.ARRAYBUFFER:
                        for (var y=0, strLen=dataBufferView.length; y<strLen; y++) {
                            dataview.setUint8(byteOffset+y,dataBufferView.value[y]);
                        }
                        break;
                    default:

                }
                byteOffset = setByteoffset(byteOffset,dataBufferView);
            }
        }


        return bufferArray;
    };
};

//服务器向客户端发送的消息格式:
//BUF  结构
//版本号 + 类型 +  处理结果 + 错误码+ 预留1 +  预留2 + 预留3 + 预留4 + 结束标志(是否是最后一个包) + 数据长度 
//   1  +  4  +   4        +       4      +     ４    +      4      +     4     +     4      +    1   +  4 
function ReMessageHead(){
    this.version = new BufferView(null,DATALENGTH.ONE,DATATYPE.INT8);
    this.type =new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.result = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.errcode = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp1 = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp2 = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp3 = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.temp4 = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.endType = new BufferView(null,DATALENGTH.ONE,DATATYPE.INT8);
    this.dataLength = new BufferView(null,DATALENGTH.FOUR,DATATYPE.INT32);
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.version);
        bufferViewArray.push(this.type);
        bufferViewArray.push(this.result);
        bufferViewArray.push(this.errcode);
        bufferViewArray.push(this.temp1);
        bufferViewArray.push(this.temp2);
        bufferViewArray.push(this.temp3);
        bufferViewArray.push(this.temp4);
        bufferViewArray.push(this.endType);
        bufferViewArray.push(this.dataLength);
        return bufferViewArray;
    }
}

//应用注册 消息类型:0x0001
//应用名长度 + 应用名 + 是否强制上传标识 + 心跳间隔时间 + 应用id + 用户id长度 + 用户id + 用户证书大小 + 用户个数 + 用户1证书长度 + 加密证书长度 + 加密证书 + 签名证书长度 + 签名证书+ 加密口令长度 + 加密口令 + 签名口令长度 ＋ 签名口令 + key口令长度 + key口令
// 4         +  len   +      1           +   4 (秒)     +    8   +     4      +  len   +      4       + 4 (1个)  +       4       +      4       +     len  +    4         +   len   +      4       +   len    +    4          +    len   +  4          +    len
function MsgAppReg(appName,upType,heartBeat,appId,userId,userNum,cert,signCart,passwd,signPassword,key){
    this.appLen = new BufferView(appName.length,DATALENGTH.FOUR,DATATYPE.INT32);
    this.appName =new BufferView(appName,appName.length,DATATYPE.UINT8);
    this.upType = new BufferView(upType,DATALENGTH.ONE,DATATYPE.INT8);

    this.heartBeat = new BufferView(heartBeat,DATALENGTH.FOUR,DATATYPE.INT32);
    this.appId = new BufferView(appId,DATALENGTH.EIGHT,DATATYPE.UINT8);
    this.userIdLen = new BufferView(userId.length,DATALENGTH.FOUR,DATATYPE.INT32);
    this.userId = new BufferView(userId,userId.length,DATATYPE.UINT8);
    this.userNum = new BufferView(userNum,DATALENGTH.FOUR,DATATYPE.INT32);
    //用户证书结构格式(用户1证书)
    //加密证书长度 + 加密证书 + 签名证书长度 + 签名证书+ 加密口令长度 + 加密口令 + 签名口令长度 ＋ 签名口令 + key口令长度 + key口令
    this.certLen = new BufferView(cert.byteLength,DATALENGTH.FOUR,DATATYPE.INT32);
    this.cert = new BufferView(cert,cert.byteLength,DATATYPE.ARRAYBUFFER);
    this.signLen = new BufferView(signCart.byteLength,DATALENGTH.FOUR,DATATYPE.INT32);
    this.signCart = new BufferView(signCart,signCart.byteLength,DATATYPE.ARRAYBUFFER);
    this.passwdLen = new BufferView(passwd.length,DATALENGTH.FOUR,DATATYPE.INT32);
    this.passwd = new BufferView(passwd,passwd.length,DATATYPE.UINT8);
    this.signPasswordLen = new BufferView(signPassword.length,DATALENGTH.FOUR,DATATYPE.INT32);
    this.signPassword = new BufferView(signPassword,signPassword.length,DATATYPE.UINT8);
    this.keyLen = new BufferView(key.length,DATALENGTH.FOUR,DATATYPE.INT32);
    this.key = new BufferView(key,key.length,DATATYPE.UINT8);
    
    //用户个数 = 1, 用户证书大小(userCertSize) = 用户1证书长度(usr1CertLen)
    this.usr1CertLen = this.certLen.length+this.cert.length+this.signLen.length+this.signCart.length+this.passwdLen.length
    + this.passwd.length+ this.signPasswordLen.length+ this.signPassword.length+ this.keyLen.length+ this.key.length;    
    this.userCertSize = new BufferView(this.usr1CertLen,DATALENGTH.FOUR,DATATYPE.INT32);
    this.userCertlenView = new BufferView( this.usr1CertLen,DATALENGTH.FOUR,DATATYPE.INT32);

    this.byteLength = this.appLen.length + this.appName.length+this.upType.length
    + this.heartBeat.length+this.appId.length+this.userIdLen.length+this.userId.length
    + this.userCertSize.length+this.userNum.length+this.userCertlenView.length
    + this.certLen.length+this.cert.length+this.signLen.length+this.signCart.length+this.passwdLen.length
    + this.passwd.length+ this.signPasswordLen.length+ this.signPassword.length+ this.keyLen.length+ this.key.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.appLen);
        bufferViewArray.push(this.appName);
        bufferViewArray.push(this.upType);
        bufferViewArray.push(this.heartBeat);
        bufferViewArray.push(this.appId);
        bufferViewArray.push(this.userIdLen);
        bufferViewArray.push(this.userId);
        bufferViewArray.push(this.userCertSize);
        bufferViewArray.push(this.userNum);
        bufferViewArray.push(this.userCertlenView);
        bufferViewArray.push(this.certLen);
        bufferViewArray.push(this.cert);
        bufferViewArray.push(this.signLen);
        bufferViewArray.push(this.signCart);
        bufferViewArray.push(this.passwdLen);
        bufferViewArray.push(this.passwd);
        bufferViewArray.push(this.signPasswordLen);
        bufferViewArray.push(this.signPassword);
        bufferViewArray.push(this.keyLen);
        bufferViewArray.push(this.key);
        return bufferViewArray;
    }
}

function setByteoffset(byteOffset,bufferView){
    byteOffset = byteOffset +bufferView.length;
    return byteOffset
}

//加密文件形式 消息类型:0x0005
//源全路径长度 + 源全路径 + 标签全路径长度 + 标签全路径 +密文全路径长度 + 密文全路径 +替换标志 +属性设置类型 + 属性信息长度 + 属性信息
// 4         +  len      +          4      +     len    +     4        +     len     +    1    +  1         +       4      +    len
function MsgEncryptFile(srcPath,labelPath,ciphertextPath,alterMark,attrType,attrInfo){
    this.srcPathLen = new BufferView(srcPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.srcPath =new BufferView(srcPath, srcPath.length, DATATYPE.UINT8);
    this.labelPathLen= new BufferView(labelPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.labelPath =new BufferView(labelPath, labelPath.length, DATATYPE.UINT8);
    this.ciphertextPathLen= new BufferView(ciphertextPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.ciphertextPath =new BufferView(ciphertextPath, ciphertextPath.length, DATATYPE.UINT8);
    this.alterMark = new BufferView(alterMark, DATALENGTH.ONE,DATATYPE.INT8);
    this.attrType = new BufferView(attrType, DATALENGTH.ONE,DATATYPE.INT8);
    this.attrLen = new BufferView(attrInfo.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.attrInfo =new BufferView(attrInfo,attrInfo.length,DATATYPE.UINT8);
    this.byteLength = this.srcPathLen.length+ this.srcPath.length+ this.labelPathLen.length
    + this.labelPath.length+ this.ciphertextPathLen.length+ this.ciphertextPath.length
    + this.alterMark.length+ this.attrType.length+ this.attrLen.length+ this.attrInfo.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.srcPathLen);
        bufferViewArray.push(this.srcPath);
        bufferViewArray.push(this.labelPathLen);
        bufferViewArray.push(this.labelPath);
        bufferViewArray.push(this.ciphertextPathLen);
        bufferViewArray.push(this.ciphertextPath);
        bufferViewArray.push(this.alterMark);
        bufferViewArray.push(this.attrType);
        bufferViewArray.push(this.attrLen);
        bufferViewArray.push(this.attrInfo);
        return bufferViewArray;
    }
}

//加密 0x0007
//数据类型 + 属性设置类型  + 属性信息长度 + 属性信息  + 结束标识
//        1        +             1             +             4             +        len       +        1
function MsgEncryptMem(dataType,propertyType,dataLen,arrayData,endType){
    this.dataType = new BufferView(dataType, DATALENGTH.ONE, DATATYPE.INT8);
    this.propertyType =new BufferView(propertyType, DATALENGTH.ONE, DATATYPE.INT8);
    this.dataLen= new BufferView(arrayData.bytelength, DATALENGTH.FOUR, DATATYPE.INT32);
    this.arrayData =new BufferView(arrayData, arrayData.bytelength, DATATYPE.UINT8);
    this.endType= new BufferView(endType, DATALENGTH.ONE, DATATYPE.INT8);

    this.byteLength = this.dataType.length+ this.propertyType.length+ this.arrayData.length
    + this.dataLen.length+ this.arrayData.length+ this.endType.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.dataType);
        bufferViewArray.push(this.propertyType);
        bufferViewArray.push(this.dataLen);
        bufferViewArray.push(this.arrayData);
        bufferViewArray.push(this.endType);
        return bufferViewArray;
    }
}


//解密文件形式 消息类型:0x0006
//源全路径长度 + 源全路径 + 标签全路径长度 + 标签全路径 +密文全路径长度 + 密文全路径 +替换标志 +属性设置类型 + 属性信息长度 + 属性信息
// 4         +  len      +          4      +     len    +     4        +     len     +    1    +  1         +       4      +    len
function MsgDecryptFile(srcPath,labelPath,ciphertextPath,alterMark,attrType,attrInfo){
    this.srcPathLen = new BufferView(srcPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.srcPath =new BufferView(srcPath, srcPath.length, DATATYPE.UINT8);
    this.labelPathLen= new BufferView(labelPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.labelPath =new BufferView(labelPath, labelPath.length, DATATYPE.UINT8);
    this.ciphertextPathLen= new BufferView(ciphertextPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.ciphertextPath =new BufferView(ciphertextPath, ciphertextPath.length, DATATYPE.UINT8);
    this.alterMark = new BufferView(alterMark, DATALENGTH.ONE,DATATYPE.INT8);
    this.attrType = new BufferView(attrType, DATALENGTH.ONE,DATATYPE.INT8);
    this.attrLen = new BufferView(attrInfo.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.attrInfo =new BufferView(attrInfo,attrInfo.length,DATATYPE.UINT8);
    this.byteLength = this.srcPathLen.length+ this.srcPath.length+ this.labelPathLen.length
    + this.labelPath.length+ this.ciphertextPathLen.length+ this.ciphertextPath.length
    + this.alterMark.length+ this.attrType.length+ this.attrLen.length+ this.attrInfo.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.srcPathLen);
        bufferViewArray.push(this.srcPath);
        bufferViewArray.push(this.labelPathLen);
        bufferViewArray.push(this.labelPath);
        bufferViewArray.push(this.ciphertextPathLen);
        bufferViewArray.push(this.ciphertextPath);
        bufferViewArray.push(this.alterMark);
        bufferViewArray.push(this.attrType);
        bufferViewArray.push(this.attrLen);
        bufferViewArray.push(this.attrInfo);
        return bufferViewArray;
    }
}

//解密 0x0008
//数据类型 + 属性设置类型  + 属性信息长度 + 属性信息  + 结束标识
//        1        +             1             +             4             +        len       +        1
function MsgDecryptMem(dataType,propertyType,dataLen,arrayData,endType){
    this.dataType = new BufferView(dataType, DATALENGTH.ONE, DATATYPE.INT8);
    this.propertyType =new BufferView(propertyType, DATALENGTH.ONE, DATATYPE.INT8);
    this.dataLen= new BufferView(arrayData.bytelength, DATALENGTH.FOUR, DATATYPE.INT32);
    this.arrayData =new BufferView(arrayData, arrayData.bytelength, DATATYPE.UINT8);
    this.endType= new BufferView(endType, DATALENGTH.ONE, DATATYPE.INT8);

    this.byteLength = this.dataType.length+ this.propertyType.length+ this.arrayData.length
    + this.dataLen.length+ this.arrayData.length+ this.endType.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.dataType);
        bufferViewArray.push(this.propertyType);
        bufferViewArray.push(this.dataLen);
        bufferViewArray.push(this.arrayData);
        bufferViewArray.push(this.endType);
        return bufferViewArray;
    }
}

//增加权限 消息类型::0x0009
//全路径长度 + 全路径 + 权限列表大小 + 权限个数 + 权限1长度 + 权限1信息
//    4      +  len   +      4       +    4     +     4     +    len
//权限格式：读权限 + 写权限 + 打印权限 + 可度次数 + 可打印次数 + 已打印次数 + 证书长度 + 证书内容
//   1   +   1    +     1    +     4    +     4      +      4     +     4    +   len
//权限个数 = 1, 权限列表大小= 权限1长度 + 权限1信息, 权限信息= 权限1信息
function MsgAddPrivilege(fullPath,priNum,readPri,writePri,printPri,readableTime,printableTime,printedTime,certContent){
    this.fullPathLen = new BufferView(fullPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.fullPath = new BufferView(fullPath, fullPath.length, DATATYPE.UINT8);
    this.priNum = new BufferView(priNum, DATALENGTH.FOUR, DATATYPE.INT32);
    //权限1信息，权限格式：读权限 + 写权限 + 打印权限 + 可度次数 + 可打印次数 + 已打印次数 + 证书长度 + 证书内容
    this.readPri = new BufferView(readPri, DATALENGTH.ONE, DATATYPE.INT8);
    this.writePri = new BufferView(writePri, DATALENGTH.ONE, DATATYPE.INT8);
    this.printPri = new BufferView(printPri, DATALENGTH.ONE, DATATYPE.INT8);
    this.readableTime = new BufferView(readableTime.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.printableTime = new BufferView(printableTime.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.printedTime = new BufferView(printedTime.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.certLen = new BufferView(certContent.byteLength, DATALENGTH.FOUR, DATATYPE.INT32);
    this.certContent = new BufferView(certContent,certContent.byteLength,DATATYPE.ARRAYBUFFER);
    //权限1信息长度
    this.pri1Info = this.readPri.length + this.writePri.length + this.printPri.length + 
    this.readableTime.length + this.printableTime.length + this.printedTime.length +
    this.printedTime.length +  this.certLen.length + this.certContent.length;
    this.pri1Len = new BufferView(this.pri1Info, DATALENGTH.FOUR, DATATYPE.INT32);
    //权限列表大小 = 权限1长度 + 权限1信息
    this.priListLen = this.pri1Len.length +this.readPri.length + this.writePri.length + this.printPri.length +
    this.readableTime.length + this.printableTime.length + this.printedTime.length +  this.certLen.length +
    this.certContent.length;
    this.priListSize = new BufferView(this.priListLen, DATALENGTH.FOUR, DATATYPE.INT32);

    this.byteLength = this.fullPathLen.length + this.fullPath.length + this.priListSize.length 
    + this.priNum.length + this.pri1Len.length +  this.pri1Info;

    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.fullPathLen);
        bufferViewArray.push(this.fullPath);
        bufferViewArray.push(this.priListSize);
        bufferViewArray.push(this.priNum);
        bufferViewArray.push(this.pri1Len);
        bufferViewArray.push(this.readPri);
        bufferViewArray.push(this.writePri);
        bufferViewArray.push(this.printPri);
        bufferViewArray.push(this.readableTime);
        bufferViewArray.push(this.printableTime);
        bufferViewArray.push(this.printedTime);
        bufferViewArray.push(this.certLen);
        bufferViewArray.push(this.certContent);   
        return bufferViewArray;
    }
}

//获取权限 消息类型::0x000A
//读权限 + 写权限 + 打印权限 + 可度次数 + 可打印次数 + 已打印次数 + 证书长度 + 证书内容
//   1   +   1    +     1    +     4    +     4      +      4     +     4    +   len
function MsgGetPrivilege(readPri,writePri,printPri,readableTime,printableTime,printedTime,certContent){
    this.readPri = new BufferView(readPri, DATALENGTH.ONE, DATATYPE.INT8);
    this.writePri = new BufferView(writePri, DATALENGTH.ONE, DATATYPE.INT8);
    this.printPri = new BufferView(printPri, DATALENGTH.ONE, DATATYPE.INT8);
    this.readableTime = new BufferView(readableTime.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.printableTime = new BufferView(printableTime.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.printedTime = new BufferView(printedTime.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.certLen = new BufferView(certContent.bytelength, DATALENGTH.FOUR, DATATYPE.INT32);
    this.certContent = new BufferView(certContent,certContent.bytelength,DATATYPE.ARRAYBUFFER);

    this.byteLength = this.readPri.length + this.writePri.length + this.printPri.length +
    this.readableTime.length + this.printableTime.length + this.printedTime.length +
    this.printedTime.length +  this.certLen.length + this.certContent.length;

    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.readPri);
        bufferViewArray.push(this.writePri);
        bufferViewArray.push(this.printPri);
        bufferViewArray.push(this.readableTime);
        bufferViewArray.push(this.printableTime);
        bufferViewArray.push(this.printedTime);
        bufferViewArray.push(this.certLen);
        bufferViewArray.push(this.certContent);   
        return bufferViewArray;
    }
}

//是否拥有权限消息  12
//全路径长度 + 全路径 + 证书长度 +  证书内容
//    4   +   len     +     4    +   len
function MsgIsOwner(path,certContent){
    this.pathLen = new BufferView(path.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.path =new BufferView(path, path.length, DATATYPE.UINT8);
    this.certLen = new BufferView(certContent.byteLength, DATALENGTH.FOUR, DATATYPE.INT32);
    this.certContent = new BufferView(certContent,certContent.byteLength,DATATYPE.ARRAYBUFFER);

    this.byteLength = this.pathLen.length+ this.path.length + this.certLen.length + this.certContent.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.pathLen);
        bufferViewArray.push(this.path);
        bufferViewArray.push(this.certLen);
        bufferViewArray.push(this.certContent);  
        return bufferViewArray;
    }
}

//是否加密 16
//全路径长度 + 全路径
//    4   +   len
function MsgIsCrypt(path){
    this.pathLen = new BufferView(path.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.path =new BufferView(path, path.length, DATATYPE.UINT8);
    this.byteLength = this.pathLen.length+ this.path.length;
    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.pathLen);
        bufferViewArray.push(this.path);
        return bufferViewArray;
    }
}

//授权 21
//长度  +  授权文件内容
//  4    +  len
function MsgAuth(authCode) {
    this.authCodeLen = new BufferView(authCode.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.authCode = new BufferView(authCode, authCode.length, DATATYPE.UINT8);
    this.byteLength = this.authCodeLen.length + this.authCode.length;
    this.getBufferViewArray = function () {
        var bufferViewArray = new Array();
        bufferViewArray.push(this.authCodeLen);
        bufferViewArray.push(this.authCode);
        return bufferViewArray;
    }
}

//获取目录 22   base64 to binrary
//长度  +  目录路径
//  4    +  len
function MsgDir(dirPath){
    this.dirPathLen = new BufferView(dirPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.dirPath = new BufferView(dirPath, dirPath.length, DATATYPE.UINT8);
    this.byteLength = this.dirPathLen.length +  this.dirPath.length;
    this.getBufferViewArray = function () {
        var bufferViewArray = new Array();
        bufferViewArray.push(this.dirPathLen);
        bufferViewArray.push(this.dirPath);
        return bufferViewArray;
    }
}

//上传文件消息  17
//服务器地址长度 + 服务器地址 + 上传文件全路径长度 + 上传全路径 + 文件名长度 + 文件名 + 用户令牌长度 + 用户令牌 + 上传文件删除标识 + 文件ID长度 + 文件ID
//     4         +     len    +       ４           +    len     +     4      +  len   +      4       +    len   +        1         +    4       +    len            
function MsgUpload(serverIp,upLoadPath,fileName,userToken,delSign){
    this.serverIpLen = new BufferView(serverIp.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.serverIp = new BufferView(serverIp, serverIp.length, DATATYPE.UINT8);
    this.upLoadPathLen = new BufferView(upLoadPath.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.upLoadPath = new BufferView(upLoadPath, upLoadPath.length, DATATYPE.UINT8);
    this.fileNameLen = new BufferView(fileName.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.fileName = new BufferView(fileName,fileName.length,DATATYPE.UINT8);
    this.userTokenLen = new BufferView(userToken.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.userToken = new BufferView(userToken, userToken.length, DATATYPE.UINT8);
    this.delSign = new BufferView(delSign, DATALENGTH.ONE, DATATYPE.INT8);

    this.byteLength = this.serverIpLen.length + this.serverIp.length + this.upLoadPathLen.length
    + this.upLoadPath.length + this.fileNameLen.length + this.fileName.length + this.userTokenLen.length
    + this.userToken.length + this.delSign.length;

    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.serverIpLen);
        bufferViewArray.push(this.serverIp);
        bufferViewArray.push(this.upLoadPathLen);
        bufferViewArray.push(this.upLoadPath);  
        bufferViewArray.push(this.fileNameLen);
        bufferViewArray.push(this.fileName);
        bufferViewArray.push(this.userTokenLen);
        bufferViewArray.push(this.userToken);  
        bufferViewArray.push(this.delSign);        
        return bufferViewArray;
    }
}

//下载文件消息.  23
//服务器地址长度 + 服务器地址 + 文件全路径长度 + 文件全路径 + 用户令牌长度 + 用户令牌 + 是否解密标识
//      4        +     len    +      ４        +     len    +      4       +   len    +       1         
function MsgDownload(serverIp,fileName,userToken,decSign){
    this.serverIpLen = new BufferView(serverIp.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.serverIp = new BufferView(serverIp, serverIp.length, DATATYPE.UINT8);
    this.fileNameLen = new BufferView(fileName.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.fileName = new BufferView(fileName,fileName.length,DATATYPE.UINT8);
    this.userTokenLen = new BufferView(userToken.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.userToken = new BufferView(userToken, userToken.length, DATATYPE.UINT8);
    this.delSign = new BufferView(delSign, DATALENGTH.ONE, DATATYPE.INT8);

    this.byteLength = this.serverIpLen.length + this.serverIp.length + this.fileNameLen.length 
    + this.fileName.length + this.userTokenLen.length + this.userToken.length + this.delSign.length;

    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.serverIpLen);
        bufferViewArray.push(this.serverIp);
        bufferViewArray.push(this.fileNameLen);
        bufferViewArray.push(this.fileName);
        bufferViewArray.push(this.userTokenLen);
        bufferViewArray.push(this.userToken);  
        bufferViewArray.push(this.delSign);        
        return bufferViewArray;
    } 
}

//web预览文件消息  24
//服务器地址长度 + 服务器地址 +  用户令牌长度 + 用户令牌
//      4        +    len     +      4        +   len    
function MsgWebFilePreview(serverIp,userToken){
    this.serverIpLen = new BufferView(serverIp.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.serverIp = new BufferView(serverIp, serverIp.length, DATATYPE.UINT8);
    this.userTokenLen = new BufferView(userToken.length, DATALENGTH.FOUR, DATATYPE.INT32);
    this.userToken = new BufferView(userToken, userToken.length, DATATYPE.UINT8);

    this.byteLength = this.serverIpLen.length + this.serverIp.length + this.userTokenLen.length
    + this.userToken.length;

    this.getBufferViewArray=function(){
        var bufferViewArray = new Array();
        bufferViewArray.push(this.serverIpLen);
        bufferViewArray.push(this.serverIp);
        bufferViewArray.push(this.userTokenLen);
        bufferViewArray.push(this.userToken);        
        return bufferViewArray;
    } 
}

//应用注册  消息类型 0x0001
function msg_app_reg(appName,upType,heartBeat,appId,userId,userNum,cert,signCart,passwd,signPassword,key,callBack){
    var msgAppReg = new MsgAppReg(appName,upType,heartBeat,appId,userId,userNum,cert,signCart,passwd,signPassword,key);
    var bufferViewArray = msgAppReg.getBufferViewArray();
    var id = "000000000000000000000000000000000000";  //36位标识码，注册时传0
    var endMark = 0;  //结束标志
    var messagerHead= new MessagerHead(labelSockert.versionType,1,id,null,null,null,null,endMark,msgAppReg.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());

}

//应用取消注册
function msg_app_unreg(id,callBack){
    var endMark = 1;  //结束标志 =1, 数据长度 = 0 
    var messagerHead = new MessagerHead(labelSockert.versionType,2,id,null,null,null,null,endMark,0,null);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());
    console.log("do msg_app_unreg:" + id);
}

//心跳，没有返回消息
function msg_app_heartbeat(id){
    var endMark = 0;  //结束标志 =0, 数据长度 = 0 
    var messagerHead = new MessagerHead(labelSockert.versionType,3,id,null,null,null,null,endMark,0,null);
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());
    console.log("do msg_app_heartbeat:"+id);
}

//加密文件形式
function msg_encrypt_file(id,srcPath,labelpath,ciphertextPath,alterMark,attrtype,attrInfo,callBack){
    var msgEncryptFile = new MsgEncryptFile(srcPath,labelpath,ciphertextPath,alterMark,attrtype,attrInfo);
    var bufferViewArray = msgEncryptFile.getBufferViewArray();
    var endMark = 0;  //结束标志 =0, 数据长度 = 0 
    var messagerHead= new MessagerHead(labelSockert.versionType,5,id,null,null,null,null,endMark,msgEncryptFile.byteLength,bufferViewArray);
    // 发送一个初始化消息
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//加密内存形式
function msg_encrypt_mem(id,dataType,propertyType,dataLen,arrayData,endType,callBack){
    var msgEncryptMem = MsgEncryptMem(dataType,propertyType,dataLen,arrayData,endType);
    var bufferViewArray = msgEncryptMem.getBufferViewArray();
    var messagerHead= new MessagerHead(labelSockert.versionType,7,id,null,null,null,null,0,msgEncryptMem.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//解密文件形式
function msg_decrypt_file(id,srcPath,labelpath,ciphertextPath,alterMark,attrtype,attrInfo,callBack){    
    var msgDecryptFile = new MsgDecryptFile(srcPath,labelpath,ciphertextPath, alterMark,attrtype,attrInfo);
    var bufferViewArray = msgDecryptFile.getBufferViewArray();
    var endMark = 0;  //结束标志 =0, 数据长度 = 0 
    var messagerHead= new MessagerHead(labelSockert.versionType,6,id,null,null,null,null,endMark,msgDecryptFile.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//解密内存形式
function msg_decrypt_mem(id,dataType,propertyType,dataLen,arrayData,endType,callBack){
    var msgDencryptMem = new MsgDecryptMem(dataType,propertyType,dataLen,arrayData,endType);
    var bufferViewArray = msgDencryptMem.getBufferViewArray();
    var messagerHead= new MessagerHead(labelSockert.versionType,8,id,null,null,null,null,1,msgDencryptMem.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//增加权限
function msg_add_privilege(id,fullPath,priNum,readPri,writePri,printPri,readableTime,printableTime,printedTime,certContent,callBack){
    var count = countSubstr(certContent, "=");
    var serCertArray = Base64Binary.decodeArrayBuffer(certContent);
    if(count > 0){
        var serArray = new ArrayBuffer(serCertArray.byteLength-count);
        for(var i=0;i<serArray.byteLength;i++){
            serArray[i]=serCertArray[i];
        }
        serCertArray= serArray;
    }

    var msgAddPrivilege = new MsgAddPrivilege(fullPath,priNum,readPri,writePri,printPri,readableTime,printableTime,printedTime,serCertArray);
    var bufferViewArray = msgAddPrivilege.getBufferViewArray();
    var endMark = 0;  //结束标志 =0, 数据长度 = 0 
    var messagerHead = new MessagerHead(labelSockert.versionType,9,id,null,null,null,null,endMark,msgAddPrivilege.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//获取权限
function msg_get_privilege(id,readPri,writePri,printPri,readableTime,printableTime,printedTime,certLen,certContent,callback){
    var msgGetPrivilege = MsgGetPrivilege(readPri,writePri,printPri,readableTime,printableTime,printedTime,certContent);
    var bufferViewArray = msgGetPrivilege.getBufferViewArray();
    var messagerHead = new MessagerHead(labelSockert.versionType,10,id,null,null,null,null,0,msgGetPrivilege.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//删除权限
function msg_del_privilege(id,callBack){
    var messagerHead = new MessagerHead(labelSockert.versionType,11,id,null,null,null,null,0,0,null);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    // 发送一个初始化消息
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//是否拥有权限 
function msg_is_owner(id,path,certContent,callBack){
    var count = countSubstr(certContent, "=");
    var serCertArray = Base64Binary.decodeArrayBuffer(certContent);
    if(count > 0){
        var serArray = new ArrayBuffer(serCertArray.byteLength-count);
        for(var i=0;i<serArray.byteLength;i++){
            serArray[i]=serCertArray[i];
        }
        serCertArray= serArray;
    }

    var msgIsOwner = new MsgIsOwner(path,serCertArray);
    var bufferViewArray = msgIsOwner.getBufferViewArray();
    var endMark = 0;  //结束标志 =0, 数据长度 = 0 
    var messagerHead= new MessagerHead(labelSockert.versionType,12,id,null,null,null,null,endMark,msgIsOwner.byteLength,bufferViewArray);
    if(callBack){msg_is_crypt_back
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//是否加密
function msg_is_crypt(id,path,callBack){
    var msgIsCrypt = new MsgIsCrypt(path);
    var bufferViewArray = msgIsCrypt.getBufferViewArray();
    var endMark = 0;  //结束标志 =0, 数据长度 = 0 
    var messagerHead= new MessagerHead(labelSockert.versionType,16,id,null,null,null,null,endMark,msgIsCrypt.byteLength,bufferViewArray);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//是否授权  20
function msg_check_auth(callBack){
    console.log("msg_check_auth");
    var id = "000000000000000000000000000000000000";  //36位标识码，判断授权时传0
    var endMark = 0;  //结束标志
    var messagerHead= new MessagerHead(labelSockert.versionType,20,id,null,null,null,null,endMark,0,null);
    if(callBack){
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//授权
function msg_auth(authcode,callBack) {
    console.log("msg_auth:" + authcode);
    var msgAuth = new MsgAuth(authcode);
    var bufferViewArray = msgAuth.getBufferViewArray();
    var messagerHead = new MessagerHead(labelSockert.versionType, 21, "000000000000000000000000000000000000", null, null, null, null, 0, msgAuth.byteLength, bufferViewArray);
    if (callBack) {
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

function msg_dir(id,filePath,callBack){
    var msgDir = new MsgDir(filePath);
    var bufferViewArray = msgDir.getBufferViewArray();
    var messagerHead = new MessagerHead(labelSockert.versionType, 22, id, null, null, null, null, 0, msgDir.byteLength, bufferViewArray);
    if (callBack) {
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());
}

//上传文件消息  17
function msg_upload(id,serverIp,upLoadPath,fileName,userToken,delSign,callBack){
    var msgUpload = new MsgUpload(serverIp,upLoadPath,fileName,userToken,delSign,fileID);
    var bufferViewArray = msgUpload.getBufferViewArray();
    var messagerHead = new MessagerHead(labelSockert.versionType, 17, id, null, null, null, null, 0, msgUpload.byteLength, bufferViewArray);
    if (callBack) {
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());    
}

//下载文件消息  23
function msg_downlaod(id,serverIp,fileName,userToken,decSign,callBack){
    var msgDownload = new MsgDownload(serverIp,fileName,userToken,delSign);
    var bufferViewArray = msgDownload.getBufferViewArray();
    var messagerHead = new MessagerHead(labelSockert.versionType, 23, id, null, null, null, null, 0, msgDownload.byteLength, bufferViewArray);
    if (callBack) {
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());    
}

//web预览文件消息  24
function msg_web_file_preview(id,serverIp,userToken,callBack){
    var msgWebFilePreview = new MsgWebFilePreview(serverIp,userToken);
    var bufferViewArray = msgWebFilePreview.getBufferViewArray();
    var messagerHead = new MessagerHead(labelSockert.versionType, 24, id, null, null, null, null, 0, msgWebFilePreview.byteLength, bufferViewArray);
    if (callBack) {
        labelSockert.callBackFun = callBack;
    }
    labelSockert.labelWs.send(messagerHead.getBuffer());    
}

var Base64Binary = {
    _keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

    /* will return a  Uint8Array type */
    decodeArrayBuffer: function(input) {
        var bytes = (input.length/4) * 3;
        var ab = new ArrayBuffer(bytes);
        var result = this.decode(input, ab);
        //return ab;
        return result;
    },

    removePaddingChars: function(input){
        var lkey = this._keyStr.indexOf(input.charAt(input.length - 1));
        if(lkey == 64){
            return input.substring(0,input.length - 1);
        }
        return input;
    },

    decode: function (input, arrayBuffer) {
        //get last chars to see if are valid
        input = this.removePaddingChars(input);
        input = this.removePaddingChars(input);

        var bytes = parseInt((input.length / 4) * 3, 10);

        var uarray;
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        var j = 0;

        if (arrayBuffer)
            uarray = new Uint8Array(arrayBuffer);
        else
            uarray = new Uint8Array(bytes);

        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

        for (i=0; i<bytes; i+=3) {
            //get the 3 octects in 4 ascii chars
            enc1 = this._keyStr.indexOf(input.charAt(j++));
            enc2 = this._keyStr.indexOf(input.charAt(j++));
            enc3 = this._keyStr.indexOf(input.charAt(j++));
            enc4 = this._keyStr.indexOf(input.charAt(j++));

            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;

            uarray[i] = chr1;
            if (enc3 != 64) uarray[i+1] = chr2;
            if (enc4 != 64) uarray[i+2] = chr3;
        }

        return uarray;
    }
}

//str:在这个字符串里面找    substr:要找的字符或字符串
function countSubstr(str,substr){
    var count;
    var reg="/"+substr+"/gi";    //查找时忽略大小写
    reg=eval(reg);
    if(str.match(reg)==null){
            count=0;
    }else{
            count=str.match(reg).length;
    }
    return count;
    //返回找到的次数
}

