/**
 * Created by panchengyin on 16/1/5.
 */
var id = "";//应用ID
var parentSy = {};//总的SY
$(function(){
    id = sy.getUrlParam('id');//发送时如果有 就说明已经保存过
    if(id&&id!=''){
        $('#app_id').textbox('readonly',true);;
        $.ajax({
            type: "post",
            url: sy.data.url+"/webapi/admin/getAppDetail/",
            data: {id: id},
            dataType: "json",
            success: function (data) {
                if (data.status == 0) {
                    var result = data.result;
                    $("#name").textbox('setValue',result.name);
                    $("#app_id").textbox('setValue',result.app_id);
                    $("#comment").textbox('setValue',result.comment);
                    $("#access_token").html(result.access_token);
                    $("#file_size").html(result.file_size);
                    $("#hidden").val(result.secret_key);
                    var status = result.status;
                    if(status == 1){
                        $("input[name='app_status'][value='1']").attr("checked",true);
                    }else{
                        $("input[name='app_status'][value='2']").attr("checked",true);
                    }
                } else {
                    var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                    $.messager.alert('查询错误', message, 'error');
                }
            }
        });
    }else {
        $("#secret_key").html("");
        $("#th_file_size").html("");
        $("#file_size").hide();
        $("input[name='app_status'][value='1']").attr("checked", true);
    }
    parentSy = window.parent.sy;
});

function saveApp(){
    if(!($("#appForm").form('validate'))){
        return;
    }
    var name = $("#name").val();
    var app_id = $("#app_id").val();
    var comment = $("#comment").val();
    var stauts = $('input[name="app_status"]:checked').val()==null?0:parseInt($('input[name="app_status"]:checked').val());
    if(id&&id!=''){
        $.ajax({
            type:"post",
            url:sy.data.url+"/webapi/admin/updateApp/",
            data: {
                id:id,
                name:name,
                app_id:app_id,
                comment:comment,
                status:stauts
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
        $.ajax({
            type:"post",
            url:sy.data.url+"/webapi/admin/createApp/",
            data: {
                name:name,
                app_id:app_id,
                comment:comment,
                status:stauts
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
                frames[i].searchAppList();
                dialogWindow.dialog('destroy');
                break;
            }
        }
    }

}

function viewsecret_key(){
    var secret_key = '访问口令:'+ $("#hidden").val();
     $.messager.alert('查看口令',secret_key,'info');

}