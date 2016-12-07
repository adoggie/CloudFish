/**
 * Created by 丞寅 on 2014/11/13.
 */
var feedback_type = "";

$(function(){
    $('#readList').datagrid({
        title:'阅文详情',
        singleSelect : true,
        fitColumns:true,
        columns:[[
            {field:'reader_name',title:'姓名',width:$(this).width() * 0.3,align:'center'},
            {field:'authorize_time',title:'授权时间',width:$(this).width() * 0.35,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            },
            {field:'read_time',title:'阅文时间',width:$(this).width() * 0.35,align:'center',
                formatter:function(value,row){
                    if(value){
                        return sy.setStringByDateTime(value,"YYYY-MM-DD hh:mm:ss");
                    }else{
                        return "";
                    }
                }
            }
        ]],
        footer:'#ft'
    });

    $('#joinTable').datagrid({
        rownumbers : true,
        singleSelect : true,
        idField : 'id',
        nowrap:false,//不折行
        fitColumns:true,
        columns:[[
            {field:'name',title:'姓名',width:$(this).width() * 0.1,align:'center'},
            {field:'dept_name',title:'单位',width:$(this).width() * 0.1,align:'center'},
            {field:'duty',title:'职务',width:$(this).width() * 0.1,align:'center'},
            {field:'sex',title:'性别',width:$(this).width() * 0.1,align:'center',
             formatter: function (value, row) {
                var str = '';
                if(value=="1"){
                    str = "男";
                }else{
                    str = "女";
                }
                return str;
            }},
            {field:'car_no',title:'车号',width:$(this).width() * 0.15,align:'center'},
            {field:'photo',title:'照片',width:$(this).width() * 0.5,align:'center',
                formatter:function(value,row){
                    var str = '';
                    if(!sy.isEmpty(value)){
                        str = '<img src="'+value+'" width="60" height="40" />'
                    }
                    return str;
                }
            }
        ]]
    });

    var id = sy.getUrlParam('arc_ras_id');//发送时如果有 就说明已经保存过
    if(id&&id!=''){
        $.ajax({
            type: "post",
            url: sy.data.url+"/webapi/ras/getSentArchiveUnitAttrDetail/",
            data: {arc_ras_id: id},
            dataType: "json",
            success: function(data){
                if(data.status == 0){
                    var result = data.result;
                    $("#receive_unit").html(result.receive_unit);
                    $("#receiver").html(result.receiver);
                    $("#receiver_phone").html(result.receiver_phone);
                    $("#relay_count").html(result.relay_count);
                    $("#relayed_count").html(result.relayed_count);
                    $("#printed_count").html(result.printed_count);
                    var receive_status = result.receive_status;
                    $("#receive_status").html(result.receive_status);
                    $("#is_hasten").html(getHasten(result.is_hasten));
                    $("#can_downlaod").html(getYesOrNo(result.can_download));
                    $("#reprint_need_approve").html(getYesOrNo(result.reprint_need_approve));
                    $("#relay_need_approve").html(getYesOrNo(result.relay_need_approve));
                    $('#print_count').html(result.print_count);
                    var receive_time = result.receive_time;
                    if(receive_time&&receive_time!=''){
                        receive_time = sy.setStringByDateTime(receive_time,'YYYY-MM-DD');
                        $("#receive_time").html(receive_time);
                    }else{
                        receive_time = "";
                        $("#receive_time").html(receive_time);
                    }
                    $("#feedback_status").html(getFeedback(result.fb_status));
                    feedback_type = result.feedback_type;
                    $('#readList').datagrid('loadData', {total:result.reader_detail.length,rows:result.reader_detail});

                    if(feedback_type==3||feedback_type==4||feedback_type==2){
                        $('#receiptView').show();
                        //$('#fb_status').html(result.fb_status);
                        $('#fb_attend_count').html(result.fb_attend_count);
                        $('#fb_description').html(result.fb_description);
                        $('#joinTable').datagrid('loadData', {total:result.fb_attenders.length,rows:result.fb_attenders});
                        if(feedback_type==2){//普通回执
                            $('#fb_attend_count_th').hide();
                            $('#fb_attend_count').hide();
                            $('#joinTable_tr').hide();
                        }
                    }else{
                        $('#receiptView').hide();
                    }
                }else{
                    var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                    $.messager.alert('查询错误',message,'error');
                }
            }
        });
    }
})

function getReceiveStatus(receive_status){
    var str = '';
    if(receive_status%2 !=0){
        str = "撤回";
    }else if(receive_status == 2){
        str = "未阅";
    }else{
        str = "已阅";
    }

    return str;
}

function getHasten(is_hasten){
    var str = '';
    if(is_hasten==1){
        str = "已催";
    }else{
        str = "未催";
    }
    return str;
}

function getYesOrNo(value){
    var str = '';
    if(value==1){
        str = "是";
    }else{
        str = "否";
    }
    return str;
}

function getFeedback(feedback_status){
    var str = '';
    if(feedback_status==1){
        str = "已回复";
    }else{
        str = "未回复";
    }
    return str;
}

$(window).resize(function(){
    $('#readList').datagrid('resize');
});

function closeWindow(){
    window.parent.$('#deptReceivedDetailWindow').window('close');
}