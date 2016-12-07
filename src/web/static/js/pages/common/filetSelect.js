/**
 * Created by 丞寅 on 2014/11/13.
 */
var parentFilePath = "";
var dirNode=null;

$(function() {
    $('#fileTree').tree({
        method:'post',
        animate:true,
        cascadeCheck:false,
        checkbox:false,
        onSelect:onSelectTree
    });
    var filepath = "";
    parentFilePath = filepath;
    //获取目录
    window.parent.parent.msg_dir(window.parent.parent.sy.data.socket_id,filepath, msg_dir_bak);
})

//获取目录返回值
function msg_dir_bak(result,jsonDate){
    if(result == 0)//
    {
        if(jsonDate!=null){
            for(var i=0;i<jsonDate.length;i++){
                jsonDate[i].filePath = "/" + jsonDate[i].text;
            }
            $('#fileTree').tree('loadData', jsonDate);
        }

    }
    else  //errcode 不等于0 获取目录jsoncode
    {
        console.log("dir empty");
    }
}

//获取目录返回值
function msg_dir_expand(result,jsonDate){
    if(result == 0)//
    {
        if(jsonDate!=null){
            var childrenNodes = $('#fileTree').tree('getChildren',dirNode.target);
            for(var i=0;i<childrenNodes.length;i++) {
                $('#fileTree').tree('remove',childrenNodes[i].target);
            }

            for(var i=0;i<jsonDate.length;i++) {
                jsonDate[i].filePath = parentFilePath + "/" + jsonDate[i].text;
            }
            $('#fileTree').tree('append', {
                parent: dirNode.target,
                data: jsonDate
            });
            $('#fileTree').tree('expand',dirNode.target);
        }

    }
    else  //errcode 不等于0 获取目录jsoncode
    {
        console.log("dir empty");
    }
}


function onSelectTree(node){
    if(node.isDir==1){//是文件夹的话
        dirNode = node;
        var filePath = node.filePath;
        parentFilePath = filePath;
        window.parent.parent.msg_dir(window.parent.parent.sy.data.socket_id,filePath, msg_dir_expand);
    }

}

function selectFile(){
    var row = $('#fileTree').tree('getSelected');
    if(row==null||row.length==0){
        $.messager.alert('提示','请选择需要上传的文件!','info');
        return;
    }else if(row.isDir==1){
        $.messager.alert('提示','请选择需要上传的文件!','info');
        return;
    }
    window.parent.selectFile(row);

}

function closeWindow(){
    //window.parent.$('#deptSelectWindow').window('close');
    window.parent.cloaseFileSelect();
}