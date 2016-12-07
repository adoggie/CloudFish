/**
 * Created by 董键 on 2014/11/19.
 */
var account_id = "";//账号ID

$(function(){
    account_id = sy.getUrlParam('id');//发送时如果有 就说明已经保存过

})

function closeWindow(){
    var frames = window.parent.frames;
    if(frames){
        for(var i=0;i<frames.length;i++){
            var dialogWindow =frames[i].dialogWindow;
            if(dialogWindow!=null){
                frames[i].searchAcountList();
                dialogWindow.dialog('destroy');
                break;
            }
        }
    }
}

function updatePassword(){
    if(account_id==null||account_id==""){
        $.messager.alert('添加错误', '缺少账户Id', 'error');
        return;
    }
    if($("#from").form('validate')){
        var data = {
            oldpasswd:$("#oldpasswd").textbox('getValue'),
            newpasswd:$("#newpasswd").textbox('getValue'),
            id:account_id
        };
        $.ajax({
            type: "post",
            //正式url
            url:"/webapi/admin/changeAccountPassword/",
            data: data,
            dataType: "json",
            success: function (data) {
                if (data.status == 0) {
                    parent.$.messager.alert('提示','修改成功','info');
                   closeWindow();
                } else {
                    var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                    $.messager.alert('查询错误', message, 'error');
                }
            }
        });
    }
}