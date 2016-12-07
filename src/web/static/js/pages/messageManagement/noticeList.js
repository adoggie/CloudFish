/**
 * Created by 董键 on 2014/12/05.
 */

$(function() {
    $('#noticeList').datagrid({
        url: '',
        rownumbers: true,
        singleSelect: true,
        idField: 'id',
        nowrap: false,//不折行
        fitColumns: true,
        pagination: true,
        pageSize: 10,
        pageList: [10, 20, 30],
        fit:true,
        columns: [[
            {field: 'title', title: '标题', width: $(this).width() * 0.15, align: 'center',
                formatter:function(value,row){
                    var str = '';
                    str += sy.formatString('<a href="#" onclick="getNoticeDetailWindow(\'{0}\');">{1}</a>', row.id,value);
                    return str;
                }
            },
            {field: 'create_time', title: '创建时间', width: $(this).width() * 0.15, align: 'center',
                formatter: function (value) {

                    var str = '';
                    str += sy.setStringByDateTime(value,'YYYY-MM-DD hh:mm:ss');
                    return str;
                }
            }
        ]]
    });
    //点击分页控件触发分页
    var pager = $('#noticeList').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getNoticeData(pageNumber, pageSize);
        }
    });
    var gridOpts = pager.pagination('options');
    getNoticeData(gridOpts.pageNumber,gridOpts.pageSize);
});


var getNoticeData = function (pageNumber, pageSize) {
    var pgctl = {
        "page_size": pageSize,
        "page_num": pageNumber
    };
    var data = {};
    data['pgctl'] = JSON.stringify(pgctl);

    //请求通知列表
    $.ajax({
        type: "post",
        //正式url
        url:sy.data.url+" /webapi/common/getNoticeList/",
        data: data,
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#noticeList").datagrid('loadData', {total:data.pgctl.total,rows:data.result});
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
};

//点击通知标题查看详情
function getNoticeDetailWindow(id){
    var dialog = parent.sy.modalDialog({
        title : '通知详情信息',
        width: 600,
        height: 300,
        url : 'pages/sysAdmin/noticeView.html?id='+id,
        buttons : [ {
            text : '关闭',
            handler : function() {
                dialog.dialog('destroy');
            }}
        ]
    });
}


