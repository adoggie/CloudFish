/**
 * Created by 丞寅 on 2014/11/19.
 */
var dialog;
var target_ids = [];

$(function() {
    $('#sendDept').panel('close');
    $('#deptSelectWindow').window('close');
    //加载发送单位
    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/ras/getUserRASUnitList/",
        dataType: "json",
        success: function(data){
            if(data.status == 0){
                $("#issue_id").combobox('loadData',data.result);
            }else{
                var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                $.messager.alert('查询错误',message,'error');
            }
        }
    });

    //加载发文单
    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/ras/getReceiverListArraySimple/",
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#receiverSel").combobox('loadData', data.result);
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
});

function showDeptWindow(){
    var url = '../../pages/common/deptSelect.html';
    $('#deptSelectWindow').window('clear');
    $('#deptSelectWindow').append(sy.formatString('<iframe src="{0}" allowTransparency="true" style="border:0;width:100%;height:99%;" frameBorder="0"></iframe>', url));
    $('#deptSelectWindow').window('open');
}

function getReceiverDetail(rec) {
    var receiver_list_id = rec.receiver_list_id;
    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/ras/getMembersInReceiverList/",
        data: {receiver_list_id:receiver_list_id},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                var recieverList = data.result.receivers;
                for(var i=0;i<recieverList.length;i++){
                    var row = recieverList[i]
                    var hasSame = false;
                    for(var j=0;j<target_ids.length;j++){
                        var id = target_ids[j];
                        if(id==row.unit_id){
                            hasSame = true
                            break;
                        }
                    }
                    if(hasSame){
                        continue;
                    }else{
                        $('#sendDept').panel('body').append(
                            '<div id="'+'div_'+row.unit_id+'"><span onclick="removeDept('+row.unit_id+')" style="cursor:pointer;" class="icon-remove" title="删除">&nbsp;&nbsp;&nbsp;&nbsp;</span>'+
                            row.unit_name+'</div>');
                        target_ids.push(row.unit_id);
                    }
                }
                $('#sendDept').panel('open');
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}

function sendMessage(){
    if($("#form").form('validate')){
        if(target_ids==null||target_ids==""||target_ids.length==0){
            $.messager.alert('提示','请选择接收单位!','info');
            return;
        }
        var title = $('#title').textbox('getValue');
        var content = $('#content').textbox('getValue');
        var issue_id = $("#issue_id").combobox("getValue");
        var data = {
            title:title,
            content:content,
            issue_id : issue_id,
            target_ids : JSON.stringify(target_ids)
        };
        $.ajax({
            type: "post",
            url: sy.data.url+"/webapi/ras/createAndSendMessage/",
            data: data,
            dataType: "json",
            success: function(data){
                if(data.status == 0){
                    parent.$.messager.alert('提示','发送成功!','info');
                    closeWindow();
                }else{
                    var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                    $.messager.alert('查询错误',message,'error');
                }
            }
        });
    }
}

function closeWindow(){
    window.parent.$('#sendMessageWindow').window('close');
}

function doSendDept(rows){
    for(var i=0;i<rows.length;i++){
        var row = rows[i]
        var hasSame = false;
        for(var j=0;j<target_ids.length;j++){
            var id = target_ids[j];
            if(id==row.unit_id){
                hasSame = true;
                break;
            }
        }
        if(hasSame){
            continue;
        }else{
            $('#sendDept').panel('body').append(
                '<div id="'+'div_'+row.unit_id+'"><span onclick="removeDept('+row.unit_id+')" style="cursor:pointer;" class="icon-remove" title="删除">&nbsp;&nbsp;&nbsp;&nbsp;</span>'+
                row.dept_name+'</div>');
            target_ids.push(row.unit_id);
        }
    }
    $('#sendDept').panel('open');
    cloaseDeptSelect();
}

function removeDept(unit_id){
    var new_ids = [];
    for(var j=0;j<target_ids.length;j++){
        var id = target_ids[j];
        if(id==unit_id){
            continue;
        }else{
            new_ids.push(id);
        }
    }
    target_ids = new_ids;
    $('#div_'+unit_id).remove();
}

function cloaseDeptSelect(){
    $('#deptSelectWindow').window('close');
}