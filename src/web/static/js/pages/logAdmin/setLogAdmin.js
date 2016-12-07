/**
 * Created by 董键 on 2014/12/03.
 */

var unit_id;//组织节点ID
var flag =false;
var unit_name;
var login_name;

$(function() {

    $.ajax({
        type: "post",
        url: sy.data.url+"/webapi/admin/getCurrentUserInfo/",
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                login_name = data.result.user;
            }
        }
    });

    $('#setLogAdmin').datagrid({
        url: '',
        rownumbers: true,
        singleSelect: true,
        idField: 'id',
        nowrap: false,//不折行
        fitColumns: true,
        fit:true,
        columns: [[
            {field: 'user', title: '用户名', width: $(this).width() * 0.15, align: 'center',
                formatter:function(value,row){
                    var str = '';
                    str += sy.formatString('<a href="#" onclick="getAdminUserDetailWindow(\'{0}\');">{1}</a>', row.id,value);
                    return str;
                }},
            {field: 'name', title: '姓名', width: $(this).width() * 0.15, align: 'center'},
            {field: 'unit_fullname', title: '权限范围', width: $(this).width() * 0.15, align: 'center'},
            { title: '修改密码',
                field: 'changeAdminUserPassword',
                width: '110',
                align:'center',
                formatter: function (value, row) {
                    var str = '';
                    str = str + sy.formatString('<input type="button" title="修改密码" class="update-mouse-on" onmouseover="sy.addOrRemoveClass(this,[\'update-mouse-over\'],[\'update-mouse-on\'])" ' +
                    'onmouseout="sy.addOrRemoveClass(this,[\'update-mouse-on\'],[\'update-mouse-over\'])" onclick="changeAdminUserPassword(\'{0}\');" />', row.id);
                    return str;
                }
            },
            {
                title: '操作',
                field: 'action',
                width: '200',
                align:'center',
                formatter: function (value, row) {
                    var str = '';
                    if (row.user != login_name) {
                        str = str + sy.formatString('<input type="button" title="删除" class="delete-mouse-on" onmouseover="sy.addOrRemoveClass(this,[\'delete-mouse-over\'],[\'delete-mouse-on\'])" ' +
                        'onmouseout="sy.addOrRemoveClass(this,[\'delete-mouse-on\'],[\'delete-mouse-over\'])" onclick="removeLogAdmin(\'{0}\');" />', row.id);
                        return str;
                    }
                }
            }
        ]],
        toolbar: '#setLogAdmin_toolbar'

    });

    $('#deptTree').tree({
        method:'post',
        animate:true,
        loadFilter:myLoadFilter,
        onBeforeExpand:expandTree,
        cascadeCheck:false,
        //checkbox:true,
        //url:'/webapi/ras/getOrgNodeChildren?parent=&depth=2&flag=1'
        url:sy.data.url+'/webapi/ras/getOrgNodeChildren/?parent=&depth=2&flag=1',
        onLoadSuccess:function(){
            if(flag==false) {
                //选中根节点
                var nodes = $('#deptTree').tree('getRoots'), i;
                for (i = 0; i < nodes.length; i++) {
                    if ($('#deptTree').tree('getParent', nodes[i]) == null) {
                        $('#deptTree').tree('select', nodes[i].target);
                        break;
                    }
                }
                unit_id = nodes[0].id;
                unit_name = nodes[0].text;
                flag=true;
                getAdminUserList();
            }
        },

        onClick:function(node){
            unit_name=node.text;
            unit_id=node.id;
            getAdminUserList();
        }
    });

});

//添加管理员
function addLogAdmin(){
    var dialog = parent.sy.modalDialog({
        title : '添加安全审计管理员',
        width: 600,
        height: 200,
        url : 'pages/logAdmin/addLogAdmin.html?unit_id='+unit_id+'&unit_name='+encodeURI(encodeURI(unit_name)),
        buttons : [ {
            text : '保存',
            width :58,
            handler : function() {
                dialog.find('iframe').get(0).contentWindow.addLogAdminSure(dialog, window);
            }},{
            text : '关闭',
            width :58,
            handler : function() {
                dialog.dialog('destroy');
            }}
        ]
    });
}

//获取组织单位管理员列表
function getAdminUserList() {
    $.ajax({
        type: "post",
        url:'/webapi/admin/getAdminUserList/',
        //test
        //url: "../../js/test/sysAdmin/getAdminUserList.json",
        dataType: "json",
        data:{unit_id:unit_id},
        success: function (data) {
            if (data.status == 0) {
                $('#setLogAdmin').datagrid('loadData', {total:data.result.length,rows:data.result});
            } else {
                var message = '错误代码:' + data.errcode + ',错误信息' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
}

//点击管理员名称查看详情
function getAdminUserDetailWindow(id){
    var dialog = parent.sy.modalDialog({
        title : '系统管理员信息',
        width: 600,
        height: 200,
        url : 'pages/logAdmin/addLogAdmin.html?id='+id,
        buttons : [ {
            text : '保存',
            width :58,
            handler : function() {
                dialog.find('iframe').get(0).contentWindow.addLogAdminSure(dialog, window);
            }},{
            text : '关闭',
            width :58,
            handler : function() {
                dialog.dialog('destroy');
            }}
        ]
    });
}

//删除管理员列表选中表格行数据
var removeLogAdmin = function(id) {
    parent.$.messager.confirm('询问', '您确定要删除此记录？', function(r) {
        if (r) {
            $.post('/webapi/admin/removeAdminUser/', {
                user_id : id
            }, function() {
                getAdminUserList();
            }, 'json');
        }
    });
};

//过滤树节点增加额外属性
function myLoadFilter(data,parent){
    var result=[];
    if(data.status == 0){
        result = data.result;
        for(var i=0; i<result.length; i++){
            var subunit_num = result[i].subunit_num;
            var children = result[i].children;
            if(children&&children.length>0&&subunit_num!=0){
                result[i].state = 'open';
            }else if((children==null||children.length==0)&&subunit_num!=0){
                result[i].state = 'closed';
            }else if((children==null||children.length==0)&&subunit_num==0){
                result[i].state = 'open';
            }else{
                result[i].state = 'closed';
            }

            if(children&&children.length>0){
                for(var j=0; j<result[i].children.length; j++){
                    setClose(result[i].children[j]);
                }
            }
        }
    }else{
        var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
        $.messager.alert('查询错误',message,'error');
        return null;
    }
    return result;
}

//递归子节点
function setClose(data){
    var subunit_num = data.subunit_num;
    var children = data.children;
    if(children&&children.length>0&&subunit_num!=0){
        data.state = 'open';
    }else if((children==null||children.length==0)&&subunit_num!=0){
        data.state = 'closed';
    }else if((children==null||children.length==0)&&subunit_num==0){
        data.state = 'open';
    }else{
        data.state = 'closed';
    }
    if(data.children){
        for(var i=0; i<data.children.length; i++){
            setClose(data.children[i]);
        }
    }
}

//点击展开节点
function expandTree(node,param){
    unit_id = node.id;
    var url=sy.data.url+'/webapi/ras/getOrgNodeChildren/?parent='+node.id+'&depth=3&flag=1';
    $("#deptTree").tree("options").url=url;
}


//修改管理员密码
function changeAdminUserPassword(id) {
    var dialog = parent.sy.modalDialog({
        title : '修改密码',
        url : 'pages/logAdmin/changeAdminUserPassword.html?id='+id,
        buttons : [ {
            text : '保存',
            width :58,
            handler : function() {
                dialog.find('iframe').get(0).contentWindow.changeLogAdminUserPasswordSure(dialog);
            }},{
            text : '关闭',
            width :58,
            handler : function() {
                dialog.dialog('destroy');
            }}
        ]
    });
}


