/**
 * Created by 董键 on 2014/11/19.
 */

function closeWindow(){
    window.parent.$('#passwordEditWindow').window('close');
}

function updatePassword(){
    if($("#from").form('validate')){
        var data = {
            oldpasswd:$("#oldpasswd").textbox('getValue'),
            newpasswd:$("#newpasswd").textbox('getValue')
        };
        $.ajax({
            type: "post",
            //正式url
            url:"/webapi/admin/changePassword/",
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