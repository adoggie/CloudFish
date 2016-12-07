/**
 * Created by 丞寅 on 2014/11/19.
 */
$(function() {
    $('#sendMessageWindow').window('close');
    $('#receiveList').datagrid({
        url:'',
        rownumbers : true,
        singleSelect : true,
        idField : 'id',
        nowrap:false,//不折行
        fitColumns:true,
        pagination : true,
        pageSize : 10,
        pageList : [ 10, 20, 30],
        border:false,
        columns:[[
            {field:'status',title:'状态',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    var str = '';
                    if(value==1){
                        str = '未读';
                    }else{
                        str = '已读';
                    }
                    return str;
                }
            },
            {field:'title',title:'标题',width:$(this).width() * 0.3,align:'center',
                formatter:function(value,row){
                    var str = '';
                    str += sy.formatString('<a href="#" onclick="messageDetail(\'{0}\');">{1}</a>', row.id,value);
                    return str;
                }
            },
            {field:'target_unit',title:'接收单位',width:$(this).width() * 0.15,align:'center'},
            {field:'issue_unit',title:'发送单位',width:$(this).width() * 0.15,align:'center'},
            {field:'issue_time',title:'发送时间',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            }

        ]],
        toolbar : '#toolbar'
    });
    var pager = $('#receiveList').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getData(pageNumber, pageSize);
        }
    });
    getData(1, 10);
})

var getData = function (pageNumber, pageSize) {
    var pgctl = {
        "page_size": pageSize,
        "page_num":pageNumber
    };
    var title = $('#title').textbox('getValue');
    var status = $('#status').combobox('getValue');
    //alert(status);
    var content = $('#content').textbox('getValue');
    if(title==null||sy.isEmpty(title)){
        title = null;
    }
    if(status==null||sy.isEmpty(status)){
        status = null;
    }
    if(content==null||sy.isEmpty(content)){
        content = null;
    }
    var start_time = sy.getDateTime($('#start_time').datebox('getValue'));
    if(start_time==null){
        start_time = 0;
    }
    var end_time = sy.getDateTimeEnd($('#end_time').datebox('getValue'));
    if(end_time==null){
        end_time =  sy.getDateTimeEndFromDate(new Date());
    }
    if(start_time>end_time){
        $.messager.alert('提示','开始时间不能大于结束时间','info');
        return;
    }
    var data = {};
    data['case']= JSON.stringify({
        "title":title,
        "start_time":start_time,
        "end_time":end_time,
        "status":status,
        "issuer":content
    });
    data['pgctl']= JSON.stringify(pgctl);


    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/ras/getMessageList/",
        data: data,
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#receiveList").datagrid('loadData', {total:data.pgctl.total,rows:data.result});
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
};

function searchList(){
    var pager = $('#receiveList').datagrid('getPager');
    var gridOpts = pager.pagination('options');
    getData(gridOpts.pageNumber,gridOpts.pageSize);
}

function openSendMessage(){
    window.parent.openMessageWindow('新建消息','pages/messageManagement/sendMessageWindow.html');
}

function messageDetail(id){
    var rowIndex = $('#receiveList').datagrid('getRowIndex',id);
    $('#receiveList').datagrid('updateRow',{index:rowIndex,row:{
        status:2
    }});
    var dialog = parent.sy.modalDialog({
        title : '消息详情',
        url : 'pages/messageManagement/messageDetailWindow.html?id='+id
    });
}

$(window).resize(function(){
    $('#sendList').datagrid('resize');
});