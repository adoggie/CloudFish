/**
 * Created by 董键 on 2014/12/15.
 */
var id = "";

$(function(){
    id = sy.getUrlParam('id');//获取ID
});

function changeLogAdminUserPasswordSure(dialog){
    if($("#from").form('validate')){
        var data = {
            user_id:id,
            password:$("#newpasswdAgain").textbox('getValue')
        };
        $.ajax({
            type: "post",
            //正式url
            url:"/webapi/admin/changeAdminUserPassword/",
            data: data,
            dataType: "json",
            success: function (data) {
                if (data.status == 0) {
                    $.messager.alert('提示','修改成功!','info',function(){
                        dialog.dialog('destroy');
                    });

                } else {
                    var message = '错误代码:' + data.errcode + ',错误信息' + data.errmsg + '!';
                    $.messager.alert('查询错误', message, 'error');
                }
            }
        });
    }
}