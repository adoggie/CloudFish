/**
 * Created by 丞寅 on 2014/11/13.
 */
$(function() {
    firstLoad = true;
    $('#deptTable').datagrid({
        rownumbers : true,
        singleSelect : false,
        idField : 'unit_id',
        fitColumns:true,
        fit:true,
        singleSelect:false,
        border:false,
        columns:[[
            {field:'ck',checkbox:true},
            {field:'dept_name',title:'收文单位'}
        ]],
        footer:'#ft'
    })

    $('#deptTree').tree({
        method:'post',
        animate:true,
        loadFilter:myLoadFilter,
        onBeforeExpand:expandTree,
        cascadeCheck:false,
        checkbox:true,
        url:sy.data.url+'/webapi/ras/getOrgNodeChildren/?parent=&depth=2&flag=1',
        onBeforeLoad:function(node, param){
            param.parent='';
            param.depth='2';
            param.flag='1';
            param.name=$('#name').textbox('getValue');;
        },
        onLoadSuccess:function(node, data){
            firstLoad = false;
        }
    });

})

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

//TODO
function expandTree(node,param){
    var url='/webapi/ras/getOrgNodeChildren/?parent='+node.id+'&depth=2&flag=1';
    $("#deptTree").tree("options").url=url;
}

function searchTree(){
    var name = $('#name').textbox('getValue');
    if(name.length>200){
        $.messager.alert('提示','查询条件不能超过200个字符!','info');
    }
    var url='/webapi/ras/getOrgNodeChildren/?parent=&depth=2&flag=1&name='+name;
    $("#deptTree").tree("options").url=url;
    $("#deptTree").tree("reload");
}

//根据所选树节点添加到表格
function getCheckedNode(){
    var nodes = $('#deptTree').tree('getChecked');
    if(nodes==null||nodes.length==0){
        $.messager.alert('提示','请从部门树勾选需要添加的部门!','info');
    }
    var rows = $('#deptTable').datagrid('getRows');
    for(var i=0; i<nodes.length; i++){
        var hasSame = false;
        for(var j=0; j<rows.length; j++){
            if(rows[j].unit_id == nodes[i].id){
                hasSame = true;
                break;
            }
        }
        if(!hasSame){
            var row = {};
            row.unit_id = nodes[i].id;
            row.dept_name = nodes[i].unit_name;
            $('#deptTable').datagrid('appendRow',row);
        }
    }
}

function deleteGridCheckedRows(){
    var rows = $('#deptTable').datagrid('getChecked');
    if(rows==null||rows.length==0){
        $.messager.alert('提示','请从部门表格中选择需要删除的部门!','info');
        return;
    }
    var copyRows = [];
    for ( var j= 0; j < rows.length; j++) {
        copyRows.push(rows[j]);
    }
    for(var i=0; i<copyRows.length; i++){
        var index = $('#deptTable').datagrid('getRowIndex',copyRows[i]);
        $('#deptTable').datagrid('deleteRow',index);
    }
    $('#deptTable').datagrid('clearChecked');
}

function clearGrid(){

    var rows = $('#deptTable').datagrid('getRows');

    var copyRows = [];
    for ( var j= 0; j < rows.length; j++) {
        copyRows.push(rows[j]);
    }
    for(var i=0; i<copyRows.length; i++){
        var index = $('#deptTable').datagrid('getRowIndex',copyRows[i]);
        $('#deptTable').datagrid('deleteRow',index);
    }
    $('#deptTable').datagrid('clearChecked');


    //$('#deptTable').datagrid('clearChecked');
   // $('#deptTable').datagrid('loadData', { total: 1, rows: [] });
}

function sendDept(){
    var rows = $('#deptTable').datagrid('getRows');
    if(rows==null||rows.length==0){
        $.messager.alert('提示','请从部门树中添加需要的部门!','info');
        return;
    }
    window.parent.doSendDept(rows);

}

function closeWindow(){
    //window.parent.$('#deptSelectWindow').window('close');
    window.parent.cloaseDeptSelect();
}