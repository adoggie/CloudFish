/**
 * Created by 董键 on 2014/12/05.
 */

$(function() {
    $('#adminLog').datagrid({
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
            //{field: 'act_name', title: '操作名称', width: $(this).width() * 0.15, align: 'center'},
            {field: 'user_role', title: '操作人角色', width: $(this).width() * 0.15, align: 'center'},
            {field: 'issue_time', title: '操作时间', width: $(this).width() * 0.15, align: 'center',
                formatter: function (value) {
                    var str = '';
                    str += sy.setStringByDateTime(value,'YYYY-MM-DD hh:mm:ss');
                    return str;
                }},
            {field: 'act_name', title: '日志类型', width: $(this).width() * 0.15, align: 'center'},
            {field: 'target', title: '操作对象', width: $(this).width() * 0.15, align: 'center'},
            {field: 'result', title: '操作结果', width: $(this).width() * 0.1, align: 'center' },
            {field: 'detail', title: '日志内容', width: $(this).width() * 0.15, align: 'center'}

        ]],
        toolbar: '#adminLog_toolbar'
    });

    $('#importCertWindow').window('close');

    var pager = $('#adminLog').datagrid('getPager');
    $(pager).pagination({
        onSelectPage: function (pageNumber, pageSize) {
            getData(pageNumber, pageSize);
        }
    });
});

//获取管理员日志
var getData = function (pageNumber, pageSize) {

    var adminLog = $("input[name='adminLog']:checked");
    var start_time= sy.getDateTime($('#start_time').datebox('getValue'));
    if(start_time==null){
        start_time = 0;
    }
    var end_time = sy.getDateTimeEnd($('#end_time').datebox('getValue'));
    if(end_time==null){
        end_time =  sy.getDateTimeEndFromDate(new Date());
    }

    if(start_time > end_time ){
        $.messager.alert('提示',"开始时间不能大于结束时间",'info');
        return;
    }
    if(adminLog.length==0)
    {
        $.messager.alert('提示','日志类型不能为空，请选择后再进行查询操作!','info');
        return;
    }
    var target = $('#target').textbox('getValue');
    var user_role = $('#user_role').combobox('getValue');
    var result = $('#result').combobox('getValue');
    var action_ids = new Array();
    for(var i=0;i<adminLog.length;i++){
        action_ids.push(adminLog[i].value);
    }
    var detail = $('#detail').textbox('getValue');

    if(target==null||sy.trim(target)==""){
        target = null;
    }
    if(user_role==null||sy.trim(user_role)==""){
        user_role = null;
    }
    if(result==null||sy.trim(result)==""){
        result = null;
    }

    var data = {};

    var pgctl = {
        "page_size": pageSize,
        "page_num":pageNumber
    };


    data['case']= JSON.stringify({
        "start_time":start_time,
        "end_time":end_time,
        "target":target,
        "user_role":user_role,
        "action_ids":action_ids,
        "result":result,
        "detail":detail
    });

    data['pgctl']= JSON.stringify(pgctl);

    $.ajax({
        type: "post",
        url:'/webapi/admin/getAdminLog/',
        data:data,
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                $('#adminLog').datagrid('loadData', {total:data.pgctl.total,rows:data.result});
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
};

//打开日志类型窗口
function showAdminLogTypeWindow(){
    $('#adminLogTypeWindow').window('open');
}

//关闭日志类型窗口
function closeAdminLogTypeWindow(){
    $('#adminLogTypeWindow').window('close');
}

function clearAdminLogType(){
    $("[name='adminLog']").removeAttr("checked");//取消全选
}

//全选
function selectAdminLogType(){

    $("[name='adminLog']").attr("checked",true);//取消全选
}


//查询用户日志
function searchAdminLog(){
    var pager = $('#adminLog').datagrid('getPager');
    var gridOpts = pager.pagination('options');
    getData(gridOpts.pageNumber,gridOpts.pageSize);

}

//导出管理员操作日志
function exportAdminOperationLog(){

    var adminLog = $("input[name='adminLog']:checked");
    var start_time= sy.getDateTime($('#start_time').datebox('getValue'));
    if(start_time==null){
        start_time = 0;
    }
    var end_time = sy.getDateTimeEnd($('#end_time').datebox('getValue'));
    if(end_time==null){
        end_time =  sy.getDateTimeEndFromDate(new Date());
    }

    if(start_time > end_time ){
        $.messager.alert('提示',"开始时间不能大于结束时间",'info');
        return;
    }
    if(adminLog.length==0)
    {
        $.messager.alert('提示','日志类型不能为空，请选择后再进行导出操作!','info');
        return;
    }
    var target = $('#target').textbox('getValue');
    var user_role = $('#user_role').combobox('getValue');
    var result = $('#result').combobox('getValue');
    var action_ids = new Array();
    for(var i=0;i<adminLog.length;i++){
        action_ids.push(adminLog[i].value);
    }
    var detail = $('#detail').textbox('getValue');

    if(target==null||sy.trim(target)==""){
        target = null;
    }
    if(user_role==null||sy.trim(user_role)==""){
        user_role = null;
    }
    if(result==null||sy.trim(result)==""){
        result = null;
    }
    
    var export_case = encodeURI(JSON.stringify({
        "start_time":start_time,
        "end_time":end_time,
        "target":target,
        "user_role":user_role,
        "action_ids":action_ids,
        "result":result,
        "detail":detail
    }));


    window.open(sy.data.url+'/webapi/admin/exportAdminLog/?case='+export_case);

}
