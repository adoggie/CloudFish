/**
 * Created by panchengyin on 16/1/5.
 */
var account_id = "";//账号ID
var parentSy = {};//总的SY

$(function(){
    $.ajax({
        type:"post",
        url:sy.data.url+"/webapi/admin/getAllApp/",
        dataType: "json",
        success: function (data) {
            if(data.status == 0){
                $("#app_name").combobox('loadData',data.result);
            }else{
                var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                $.messager.alert('查询错误',message,'error');
            }
        }
    });

    account_id = sy.getUrlParam('id');//发送时如果有 就说明已经保存过
    if(account_id&&account_id!=''){
        $.ajax({
            type: "post",
            url: sy.data.url+"/webapi/admin/getAccountDetail/",
            data: {id: account_id},
            dataType: "json",
            success: function (data) {
                if (data.status == 0) {
                    var result = data.result;
                    $("#name").textbox('setValue',result.name);
                    $("#phone").textbox('setValue',result.phone);
                    $("#address").textbox('setValue',result.address);
                    $("#username").textbox('setValue',result.username);
                    $("#app_name").combobox("setValue",result.app_id);
                    $("#newpasswd").textbox('setValue','000000');//修改时不提交密码
                    $("#newpasswdAgain").textbox('setValue','000000');
                    $("#file_size").html(result.file_size);
                    $("#changePassword").hide();

                    var status = result.status;
                    if(status == 1){
                        $("input[name='acc_status'][value='1']").attr("checked",true);
                    }else{
                        $("input[name='acc_status'][value='2']").attr("checked",true);
                    }
                } else {
                    var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                    $.messager.alert('查询错误', message, 'error');
                }
            }
        });
    }
    else {
        $("#th_file_size").html("");
        $("#file_size").hide();
        $("input[name='app_status'][value='1']").attr("checked", true);
    }
    parentSy = window.parent.sy;
});

function saveAccount(){
    if(!($("#accForm").form('validate'))){
       return;
    }
    var name = $("#name").val();
    var phone = $("#phone").val();
    var address = $("#address").val();
    var username = $("#username").val();
    var stauts = $('input[name="acc_status"]:checked').val()==null?0:parseInt($('input[name="acc_status"]:checked').val());
    var app_id = $("#app_name").combobox("getValue");

    if(account_id&&account_id!=''){
        $.ajax({
            type:"post",
            url:sy.data.url+"/webapi/admin/updateAccount/",
            data: {
                id:account_id,
                name:name,
                app_id:app_id,
                phone:phone,
                address:address,
                status:stauts,
                username:username,
            },
            dataType: "json",
            success: function(data){
                if(data.status == 0){
                    $.messager.alert('提示','保存成功!','info',function(){
                        closeWindow()
                    });
                }else{
                    var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                    $.messager.alert('查询错误',message,'error');
                }
            }
        });
    }else{
        var passwd =$("#newpasswd").textbox('getValue');
        $.ajax({
            type:"post",
            url:sy.data.url+"/webapi/admin/createAccount/",
            data: {
                name:name,
                app_id:app_id,
                phone:phone,
                address:address,
                status:stauts,
                passwd:passwd,
                username:username,
            },
            dataType: "json",
            success: function(data){
                if(data.status == 0){
                    $.messager.alert('提示','保存成功!','info',function(){
                        closeWindow()
                    });
                }else{
                    var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                    $.messager.alert('查询错误',message,'error');
                }
            }
        });
    }
}


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
