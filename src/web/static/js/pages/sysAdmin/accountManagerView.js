/**
 * Created by panchengyin on 16/1/5.
 */
var dialogWindow;
var sel_account_id = null;

$(function() {
    $('#accountList').datagrid({
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
            {field:'name',title:'账号名称',width:$(this).width() * 0.2,align:'center',
                formatter:function(value,row){
                    var str = '';
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="openAccDetail(\'{0}\');">{1}</a>', row.id,value);
                    return str;
                }
            },
            {field:'app_name',title:'应用名称',width:$(this).width() * 0.2,align:'center'},
            {field:'create_time',title:'帐号创建时间',width:$(this).width() * 0.2,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            },
            {field:'file_size',title:'文件容量',width:$(this).width() * 0.1,align:'center'},
            {field:'status',title:'账号状态',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    if(value==1){
                        return '启用';
                    }else if(value==2){
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
                    str += sy.formatString("<a href='#' style='color:#007fae' onclick='changePassword(\"{0}\")'>{1}</a>",row.id,'修改密码');
                    return str;
                }
            }
        ]],
        toolbar : '#toolbar',
        onLoadSuccess:function(data){
            //$(".loan_ct_view_button").linkbutton();
        }
    });

    var pager = $('#accountList').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getData(pageNumber, pageSize);
        }
    });

    searchAcountList();

});

$(window).resize(function(){
    $('#accountList').datagrid('resize');
});

function searchAcountList(){
    var pager = $('#accountList').datagrid('getPager');
    var gridOpts = pager.pagination('options');
    getData(gridOpts.pageNumber,gridOpts.pageSize);
}

var getData = function (pageNumber, pageSize) {
    var pgctl = {
        "page_size": pageSize,
        "page_num":pageNumber
    };
    var name = $('#name').textbox('getValue');
    var app_name = $('#app_name').textbox('getValue');
    var status = $("#status").combobox("getValue");
    if(name==null||sy.trim(name)==""){
        name = null;
    }
    if(app_name==null||sy.trim(app_name)==""){
        app_name = null;
    }
    if(status==null||sy.trim(status)==""){
        status = null;
    }

    var query_parameters = {};

    query_parameters.pgctl= pgctl;
    query_parameters.case= {
        "name":name,
        "app_name":app_name,
        "status":status
    };

    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/admin/getAccountList/",
        data: {query_parameters:JSON.stringify(query_parameters)},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#accountList").datagrid('loadData', {total:data.pgctl.total,rows:data.result});
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
        url: sy.data.url+"/webapi/admin/changeAccountStatus/",
        data: {
            "ids":JSON.stringify(ids),
            "status":status
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                searchAcountList();
                $.messager.alert('提示', '修改成功!', 'info');
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}


function openAccEditWindow(){
    dialogWindow = parent.sy.modalDialog({
        title : '账号信息维护',
        url : "pages/sysAdmin/accountEditWindow.html",
        width : 640,
        height : 260
    });
};

function openAccDetail(id){
    dialogWindow = parent.sy.modalDialog({
        title : '账号信息维护',
        url : "pages/sysAdmin/accountEditWindow.html?id="+id,
        width : 640,
        height : 260
    });
}

function changePassword(id){
    dialogWindow = parent.sy.modalDialog({
        title : '修改密码',
        url : "pages/sysAdmin/passwordEditWindow.html?id="+id,
        width : 540,
        height : 220
    });
}



