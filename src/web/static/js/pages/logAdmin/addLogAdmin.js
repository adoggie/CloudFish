/**
 * Created by 董键 on 2014/12/03.
 */


var id = "";
var unit_id;//组织节点ID
var unit_name;

$(function(){
    id = sy.getUrlParam('id');//发送时如果有 就说明已经保存过
    unit_id = sy.getUrlParam('unit_id');
    unit_name = decodeURI(sy.getUrlParam('unit_name'));
    if(id&&id!=''){
        $('#loginName').textbox('disable');
        $('#passWord').textbox('disable');
        $('#unitName').textbox('disable');
        getAdminUserDetail();
    }else{
        $("#unitName").textbox('setValue',unit_name);
        $('#unitName').textbox('disable');
    }
});


//获取管理员记录详情
function getAdminUserDetail() {
    $.ajax({
        type: "post",
        //正式url
        url:"/webapi/admin/getAdminUserDetail/",
        //测试url testurl
        //url: "../../js/test/sysAdmin/getAdminUserDetail.json",
        data: {id: id},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                var result = data.result;
                $("#unitName").textbox('setValue',result.unit_name);
                $("#userName").textbox('setValue',result.name);
                $("#loginName").textbox('setValue',result.user);
                $("#passWord").textbox('setValue','******');
            } else {
                var message = data.errmsg+'('+data.errcode+')';
                $.messager.alert('提示', message, 'error');
            }
        }
    });
}

//点击保存
function addLogAdminSure(dialog, window){
    if($("#addLogAdmin").form('validate')){
        var user = $("#loginName").textbox('getValue');
        var password = $("#passWord").textbox('getValue');
        var name = $("#userName").textbox('getValue');
        var saveData = {
            unit_id:unit_id,
            user :user,
            password : password,
            name:name
        };
        if(id!=null&&id!=""){
            var url ="/webapi/admin/updateAdminUser/";//修改安全审计管理员
            //saveData.id = id;
            $.ajax({
                type: "post",
                url:url,
                data: {id:id,name:name},
                dataType: "json",
                success: function(data){
                    if(data.status == 0){
                        parent.$.messager.alert('提示','修改成功!','info',function(){
                            window.getAdminUserList();
                            dialog.dialog('destroy');
                        });
                        closeDialog();
                    }else{
                        var message = data.errmsg+'('+data.errcode+')';
                        parent.$.messager.alert('提示',message,'error');
                    }
                }
            });
        }else{
            var url ="/webapi/admin/createAdminUser/";//创建安全审计管理员
            $.ajax({
                type: "post",
                url:url,
                data: saveData,
                dataType: "json",
                success: function(data){
                    if(data.status == 0){
                        id = data.result;
                        parent.$.messager.alert('提示','保存成功!','info',function(){
                            window.getAdminUserList();
                            dialog.dialog('destroy');
                        });
                    }else{
                        var message = data.errmsg+'('+data.errcode+')';
                        parent.$.messager.alert('提示',message,'error');
                    }
                }
            });
        }
    }
}