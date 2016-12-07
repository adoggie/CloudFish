/**
 * Created by machao on 16/1/12.
 */
var dialogWindow;

$(function() {
    $('#appServerList').datagrid({
        url: '',
        //url:'http://localhost:63342/cloudfish/src/web/static/js/test/secAdmin/getAppServerList.json',
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
            {field:'name',title:'服务器名称',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    var str = '';
                    str += sy.formatString('<a href="#" onclick="openAppServerDetail(\'{0}\');">{1}</a>', row.id,value);
                    return str;
                }
            },
            {field:'ip_addr',title:'服务器IP',width:$(this).width() * 0.1,align:'center'
            },
            {field:'app_name',title:'关联应用',width:$(this).width() * 0.1,align:'center'},
            {field:'create_time',title:'创建时间',width:$(this).width() * 0.3,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            },
            {field:'status',title:'服务器状态',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    if(value==1){
                        return '启用';
                    }else{
                        return '禁用';
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
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="changeStatus(\'{0}\',1);">{1}</a>&nbsp;&nbsp;', row.id,'启用 ');
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="changeStatus(\'{0}\',2);">{1}</a>', row.id,'禁用 ');
                    return str;
                }
            }
        ]],
        toolbar : '#toolbar'
    });
    var pager = $('#appServerList').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getData(pageNumber, pageSize);
        }
    });
    searchAppServerList();
});

$(window).resize(function(){
    $('#appServerList').datagrid('resize');
});

function searchAppServerList(){
    var pager = $('#appServerList').datagrid('getPager');
    var gridOpts = pager.pagination('options');
    getData(gridOpts.pageNumber,gridOpts.pageSize);
}

var getData = function (pageNumber, pageSize) {
    var pgctl = {
        "page_size": pageSize,
        "page_num":pageNumber
    };
    var name = $('#name').textbox('getValue');
    if(name==null||sy.trim(name)==""){
        name = null;
    }

    var query_parameters = {};

    query_parameters.pgctl= pgctl;
    query_parameters.case= {
        "name":name
    };
    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/admin/getAppServerList/",
        //url:"http://localhost:63342/cloudfish/src/web/static/js/test/secAdmin/getAppServerList.json",
        data: {query_parameters:JSON.stringify(query_parameters)},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#appServerList").datagrid('loadData', {total:data.pgctl.total,rows:data.result});
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
        url: sy.data.url+"/webapi/admin/changeAppServerStatus/",
        data: {
            "ids":JSON.stringify(ids),
            "status":status
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                searchAppServerList();
                $.messager.alert('提示', '修改成功!', 'info');
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}


function openAddAppServerWindow(){
    dialogWindow = parent.sy.modalDialog({
        title : '应用服务器信息',
        width : 640,
        height : 240,
        url : "pages/secAdmin/addAppServer.html"
        //url:"http://localhost:63342/cloudfish/src/web/pages/secAdmin/addAppServer.html#"
    });
};

function openAppServerDetail(id){
    dialogWindow = parent.sy.modalDialog({
        title : '服务器信息维护',
        width : 640,
        height : 300,
        url : "pages/secAdmin/editAppServer.html?id="+id
        //url:"http://localhost:63342/cloudfish/src/web/pages/secAdmin/editAppServer.html#"
    });
}
