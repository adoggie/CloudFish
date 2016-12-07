/**
 * Created by panchengyin on 16/1/5.
 */
/**
 * Created by panchengyin on 16/1/5.
 */
$(function() {
    $('#certList').datagrid({
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
            {field:'name',title:'证书名称',width:$(this).width() * 0.1,align:'center'},
            {field:'cert_rel_name',title:'证书关联名称',width:$(this).width() * 0.3,align:'center'},
            //{field:'expire_time',title:'证书有效期',width:$(this).width() * 0.2,align:'center',
            //    formatter:function(value,row){
            //        if(value){
            //            return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
            //        }else{
            //            return "";
            //        }
            //    }
            //},
            {field:'create_time',title:'证书创建时间',width:$(this).width() * 0.2,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            },
            {field:'status',title:'证书状态',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    if(value==1){
                        return '可用';
                    }else if(value==2){
                        return '禁用';
                    }else if(value==3){
                        return '已用';
                    }else{
                        return '未知';
                    }
                }
            },
            {field:'type',title:'证书类型',width:$(this).width() * 0.1,align:'center',
                formatter:function(value,row){
                    if(value==1){
                        return 'RSA';
                    }else if(value==2){
                        return 'IBC';
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
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="changeStatus(\'{0}\',3);">{1}</a>&nbsp;&nbsp;', row.id,'启用');
                    str += sy.formatString('<a href="#" style="color:#007fae" onclick="changeStatus(\'{0}\',2);">{1}</a>', row.id,'禁用');

                    return str;
                }
            }
        ]],
        toolbar : '#toolbar'
    });

    var pager = $('#certList').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getData(pageNumber, pageSize);
        }
    });
    $('#importCertWindow').window({
        onBeforeClose:function(){
            searchCertList();
        }
    });
    searchCertList();
});

$(window).resize(function(){
    $('#certList').datagrid('resize');
});

function searchCertList(){
    var pager = $('#certList').datagrid('getPager');
    var gridOpts = pager.pagination('options');
    getData(gridOpts.pageNumber,gridOpts.pageSize);
}

var getData = function (pageNumber, pageSize) {
    var pgctl = {
        "page_size": pageSize,
        "page_num":pageNumber
    };
    var cert_rel_name = $('#cert_rel_name').textbox('getValue');
    var status = $("#status").combobox("getValue");
    if(cert_rel_name==null||sy.trim(cert_rel_name)==""){
        cert_rel_name = null;
    }
    if(status==null||sy.trim(status)==""){
        status = null;
    }

    var query_parameters = {};

    query_parameters.pgctl= pgctl;
    query_parameters.case= {
        "cert_rel_name":cert_rel_name,
        "status":status
    };

    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/admin/getCertList/",
        data: {query_parameters:JSON.stringify(query_parameters)},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $("#certList").datagrid('loadData', {total:data.pgctl.total,rows:data.result});
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
        url: sy.data.url+"/webapi/admin/changeCertStauts/",
        data: {
            "ids":JSON.stringify(ids),
            "status":status
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                searchCertList();
                $.messager.alert('提示', '修改成功!', 'info');
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}

function importCert(){
    var file = $("#file");
    file.after(file.clone().val(""));
    file.remove();
    $('#importCertWindow').window('open');
}

function uploadCert(){
    var file = $("#file");
    var files = file.prop('files');
    var length = files.length;
    if(length==0){
        $.messager.alert('证书错误', '请选择证书!', 'error');
        return;
    }
    if(!chk(length)){
        $.messager.alert('证书错误', '请选择一一对应的证书!', 'error');
        return;
    }

    $("#addForm").ajaxSubmit({
        url : '/webapi/admin/importCert/',
        type : 'POST',
        dataType : 'json',
        success : function(data) {
            if (data.status == 0) {
                $.messager.alert('提示', '导入证书成功!', 'info',function(){
                    $('#importCertWindow').window('close');
                });
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}

function chk(num){//是否是偶数
    return num?num%2?false:true:false
}

function closeWindow(){
    $('#importCertWindow').window('close');
}