/**
 * Created by machao on 16/1/26.
 */
var appServer_id = "";// 服务ID

$(function(){

    $.ajax({
        type:"post",
        url:sy.data.url+"/webapi/admin/getAllApp/",
        dataType: "json",
        success: function (data) {
            if(data.status == 0){
                $("#app_id").combobox('loadData',data.result);
            }else{
                var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                $.messager.alert('查询错误',message,'error');
            }
        }
    });

    appServer_id = sy.getUrlParam('id');//发送时如果有 就说明已经保存过
    if(appServer_id&&appServer_id!=''){
        $.ajax({
            type: "post",
            url: sy.data.url+"/webapi/admin/getAppServerDetail/",
            data: {id: appServer_id},
            dataType: "json",
            success: function (data) {
                if (data.status == 0) {
                    var result = data.result;

                  /*  var name = $("#name").val();
                    var ip_addr = $("#ip_addr").val();
                    //var app_id = $("#ip_addr").val();
                    // var app_name = $("#app_id").val();
                    var is_addr_restricted = $('input[name="is_addr_restricted"]:checked').val()==null?0:parseInt($('input[name="is_addr_restricted"]:checked').val());
                    var status = $('input[name="status"]:checked').val()==null?0:parseInt($('input[name="status"]:checked').val());
                    var app_id = $("#app_id").combobox("getValue");*/

                    $("#name").textbox('setValue',result.name);
                    $("#ip_addr").textbox('setValue',result.ip_addr);
                    $("#app_id").combobox("setValue",result.app_id);


                    var is_addr_restricted = result.is_addr_restricted;
                    if(is_addr_restricted == 1){
                        $("input[name='is_addr_restricted'][value='1']").attr("checked",true);
                    }else{
                        $("input[name='is_addr_restricted'][value='2']").attr("checked",true);
                    }
                    var status = result.status;
                    if(status == 1){
                        $("input[name='status'][value='1']").attr("checked",true);
                    }else{
                        $("input[name='status'][value='2']").attr("checked",true);
                    }

                    $("#access_token").html(result.access_token);

                    $("#secret_key").html(result.secret_key);

                } else {
                    var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                    $.messager.alert('查询错误', message, 'error');
                }
            }
        });
    }
    parentSy = window.parent.sy;
});

function saveApp(){
    if(!($("#addLogAdmin").form('validate'))){
        return;
    }
    var name = $("#name").val();
    var ip_addr = $("#ip_addr").val();

    var is_addr_restricted = $('input[name="is_addr_restricted"]:checked').val()==null?0:parseInt($('input[name="is_addr_restricted"]:checked').val());
    var status = $('input[name="status"]:checked').val()==null?0:parseInt($('input[name="status"]:checked').val());
    var app_id = $("#app_id").combobox("getValue");

    $.ajax({
            type:"post",
            url:sy.data.url+"/webapi/admin/updateAppServer/",
            data: {
                id:appServer_id,
                name:name,
                ip_addr:ip_addr,
                app_id:app_id,
                is_addr_restricted:is_addr_restricted,
                status:status
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


function closeWindow(){
    var frames = window.parent.frames;
    if(frames){
        for(var i=0;i<frames.length;i++){
            var dialogWindow =frames[i].dialogWindow;
            if(dialogWindow!=null){
                frames[i].searchAppServerList();
                dialogWindow.dialog('destroy');
                break;
            }
        }
    }


}
