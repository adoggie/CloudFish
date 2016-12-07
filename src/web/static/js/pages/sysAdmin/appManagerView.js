/**
 * Created by panchengyin on 16/1/5.
 */
var dialogWindow;
var sel_app_id=null;

$(function() {
    $('#appList').datagrid({
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
            {field:'name',title:'应用名称',width:$(this).width() * 0.2,align:'center',
                formatter:function(value,row){
                    var str = '';
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="openAppDetail(\'{0}\');">{1}</a>', row.id,value);
                    return str;
                }
            },
            {field:'create_time',title:'应用创建时间',width:$(this).width() * 0.15,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            },
            {field:'app_id',title:'应用标识',width:$(this).width() * 0.15,align:'center'},
            {field:'file_size',title:'文件容量',width:$(this).width() * 0.15,align:'center'},
            {field:'status',title:'应用状态',width:$(this).width() * 0.15,align:'center',
                formatter:function(value,row){
                    if(value==1){
                        return '启用';
                    }else if(value=2){
                        return '禁用';
                    }else{
                        return '未知';
                    }
                }
            },
            {
                title: '操作',
                field: 'action',
                width:$(this).width() * 0.2,
                align:'center',
                formatter: function (value, row) {
                    var str = '';
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="changeStatus(\'{0}\',1);">{1}</a>&nbsp;&nbsp;', row.id,'启用');
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="changeStatus(\'{0}\',2);">{1}</a>&nbsp;&nbsp;', row.id,'禁用');

                    return str;
                }
            }
        ]],
        toolbar : '#toolbar'
    });

    var pager = $('#appList').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getData(pageNumber, pageSize);
        }
    });

    $('#importCertWindow').window({
        onBeforeClose:function(){
            searchAppList();
        }
    });
    searchAppList();
});

$(window).resize(function(){
    $('#appList').datagrid('resize');
});

function searchAppList(){
    var pager = $('#appList').datagrid('getPager');
    var gridOpts = pager.pagination('options');
    getData(gridOpts.pageNumber,gridOpts.pageSize);
}

var getData = function (pageNumber, pageSize) {
    var pgctl = {
        "page_size": pageSize,
        "page_num":pageNumber
    };
    var name = $('#name').textbox('getValue');
    var status = $("#status").combobox("getValue");
    if(status==null||sy.trim(status)==""){
        status = null;
    }
    if(name==null||sy.trim(name)==""){
        name = null;
    }

    var query_parameters = {};

    query_parameters.pgctl= pgctl;
    query_parameters.case= {
        "name":name,
        "status":status
    };

    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/admin/getAppList/",
        data: {query_parameters:JSON.stringify(query_parameters)},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#appList").datagrid('loadData', {total:data.pgctl.total,rows:data.result});
                //$("#appList").datagrid('clearChecked');
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
};

function changeStatus(id,status){
    var ids = new Array([id]);
    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/admin/changeAppStatus/",
        data: {
           "ids":JSON.stringify(ids),
           "status":status
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                searchAppList();
                $.messager.alert('提示', '修改成功!', 'info');
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}

function openAppEditWindow(){
    dialogWindow = parent.sy.modalDialog({
        title : '应用信息维护',
        url : "pages/sysAdmin/appEditWindow.html",
        width : 640,
        height : 300
    });
};

function openAppDetail(id){
    dialogWindow = parent.sy.modalDialog({
        title : '应用信息维护',
        url : "pages/sysAdmin/appEditWindow.html?id="+id,
        width : 640,
        height : 300
    });
}

function exportApp(id){
    window.open('/webapi/admin/exportAppCert/?id='+id);
}
