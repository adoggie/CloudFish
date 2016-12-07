/**
 * Created by panchengyin on 8/27/15.
 */


    
//应用注册 消息类型:0x0001
//应用名 + 是否强制上传标识(0/1) + 心跳间隔时间 + 应用id + 用户证书集合
//用户证书集合 = (加密证书 + 加密证书 + 加密口令 + 签名口令 + key口令)
function MsgAppReg(appName,upType,heartBeat,appId,userId,userList){
    this.appname = appName;
    this.uptype = upType;
    this.heartbeat = heartBeat;
    this.appid = appId;
    this.userid = userId;
    this.usercert = userList//用户证书集合

    this.getBufferViewArray=function(){
        return null;
    }
}

//用户证书集合
function UserCert(cert,signCart,passwd,signPassword,key){
    //(用户1证书)
    //用户证书集合 = 加密证书 + 加密证书 + 加密口令 + 签名口令 + key口令
    this.cert = cert;
    this.signcart = signCart;
    this.passwd = passwd;
    this.signpassword = signPassword;
    this.key = key;

}

//取消应用注册 

//心跳

//http加密并上传接口
//属性 + 权限数组
//属性 = 文件id + 文件大小 + 文件密级 + 文件名 +文件标题 + 文件过期时间 + 属性数组 (属性类型+属性id+属性值)
//权限数组 = 读权限 + 写权限 + 打印权限 + 可读次数 + 可打印次数 + 已打印次数 + 证书内容
function MsgEncrypt(attriList,priArray,attriFlag,priarrayFlag){
	this.attri = attriList;  //属性
	this.priarray = priArray;   //权限数组
    this.attriflag = attriFlag;
    this.priarrayflag = priarrayFlag;
	
	this.getBufferViewArray=function(){
        return null;
	}
}

//属性
function AttriList(fileId, fileSize, fileLevel, fileTitle, fileExpiredTime, AttrArray){
	this.fileid = fileId;
	this.filesize = fileSize;
	this.filelevel = fileLevel;
	this.filetitle = fileTitle;
	this.fileexpiredtime = fileExpiredTime;
	this.attrarray = attrArray;  //属性数组
	
}

//属性数组
function AttrArray(attrType, attrId, attrValue){
	this.attrtype = attrType;
	this.attrid = attrId;
	this.attrvalue = attrValue;
	
}

//权限数组
function PriArray(readPri,writePri,printPri,readCount,printCount,printedCount,cert){
	this.readpri = readPri;
	this.writepri = writePri;
	this.printpri = printPri;
	this.readcount = readCount;
	this.printcount = printCount;
	this.printedcount = printedCount;
	this.cert = cert;
	
}

function msgAppDate(appName,upType,heartBeat,appId,userId,cert,signCart,passwd,signPassword,key){
    var data = {};
    //data.json = Json.string();

    var userCert = new UserCert(cert,signCart,passwd,signPassword,key);
    var userCertList = new Array();
    userCertList.push(userCert);

    var msgAppReg = new MsgAppReg(appName,upType,heartBeat,appId,userId,userCertList);
    data.json = JSON.stringify(msgAppReg);

    return data;
}

//注册取消，传入注册时获取的data.result.id
function msgAppUnreg(id){
    var data = {};
    data.id = id;
    return data;
}

//心跳，传入注册时获取的data.result.id
function msgHeartbeat(id){
    var data = {};
    data.id = id;
    return data;
}

//http加密上传
function msgEncryptUpload(id,token,attriFlag,priarrayFlag,cert){
    var data = {};

    var priarrayList =  new Array();
    var priArray = new PriArray(1,1,1,0,0,0,cert);
    priarrayList.push(priArray);
    var msgEncrypt = new MsgEncrypt(null,priarrayList,attriFlag,priarrayFlag);
    data.json = JSON.stringify(msgEncrypt);
    data.id = id;
    data.token = token;
    return data;
}

//http下载解密
function msgDecryptDownload(id,token,fileId){
    var data = {};
    data.id = id;
    data.token = token;
    data.fileId = fileId;

    return data;
}