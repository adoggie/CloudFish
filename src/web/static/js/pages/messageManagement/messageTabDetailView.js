/**
 * Created by 丞寅 on 2015/1/20.
 */
var id = "";
var rootId = "";
$(function() {

    id = sy.getUrlParam('id');
    rootId= sy.getUrlParam('rootId');
    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/ras/getMessageDetail/",
        data: {msg_id:id},
        dataType: "json",
        success: function(data){
            if(data.status == 0){
                var result = data.result;
                $('#issue_user_name').html(result.issue_user_name);
                $("#title").html(result.title);
                $("#issue_time").html(sy.setStringByDateTime(result.issue_time,'YYYY-MM-DD hh:mm:ss'));
                $("#issue_unit").html(result.issue_unit);
                $("#content").html(result.content);
            }else{
                var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                $.messager.alert('查询错误',message,'error');
            }
        }
    });
});

function replyMessage(){
    if($("#form").form('validate')){
        if(id==null||sy.isEmpty(id)){
            $.messager.alert('系统异常','消息ID不存在!','error');
            return;
        }
        var title = $('#re_title').textbox('getValue');
        var content = $('#re_content').textbox('getValue');
        var data = {
            title:title,
            content:content,
            from_id : id,
            root_id : rootId
        };
        $.ajax({
            type: "post",
            url: sy.data.url+"/webapi/ras/replyMessage/",
            data: data,
            dataType: "json",
            success: function(data){
                if(data.status == 0){
                    parent.$.messager.alert('提示','回复成功!','info');
                    window.parent.refushTabs();
                }else{
                    var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                    $.messager.alert('查询错误',message,'error');
                }
            }
        });
    }
}