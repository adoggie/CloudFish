
//获取关联应用

$(function() {

    $.ajax({
     type:"post",
     url:sy.data.url+"/webapi/admin/getAllApp/",
     dataType: "json",
     success: function (data) {
     if(data.status == 0){
     $("#app_id").combobox('loadData',data.result);
     }else{
     var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
     $.messager.alert('查询错误',message,'error');
     }
     }
     });


   /* $.ajax({
        type:"post",
       // url:sy.data.url+"/webapi/admin/getAllApp/",
        url:'http://localhost:63342/cloudfish/src/web/static/js/test/secAdmin/getAllApp.json',
        dataType: "json",
        success: function(data){
            if(data.status == 0){
              //  var app_id = $("#app_id");
               // app_id.empty();
               // alert(data.result.length);
                var selObj = $("#app_id");
                for(var i=0;i<data.result.length;i++) {
                    alert(data.result[i].name);


                    var value="value";
                    var text="text";
                    selObj.append("<option value='"+value+"'>"+text+"</option>");
                   // app_id.append("<option value='"+(data.result[i].id +"'>"+data.result[i].name + " < /option>");
                   // $("#app_id").append("<option value='1'>ss</option>");
                }
                alert(selObj.length)
            }else{
                var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                $.messager.alert('查询错误',message,'error');
            }
        }
    });*/
   /* var selObj = $("#app_id");
    selObj.empty();
    var value="1";
    var text="yesterday";
    selObj.attr("value","yesterday");
    selObj.value("mm");*/
   // selObj.append("<option value='"+value+"'>"+text+"</option>");
    //selObj.refresh();

});
function saveApp(){
    if(!($("#addLogAdmin").form('validate'))){
        return;
    }

    var name = $("#name").val();
    var ip_addr = $("#ip_addr").val();
    //var app_id = $("#ip_addr").val();
   // var app_name = $("#app_id").val();
    var is_addr_restricted = $('input[name="is_addr_restricted"]:checked').val()==null?0:parseInt($('input[name="is_addr_restricted"]:checked').val());
    var status = $('input[name="status"]:checked').val()==null?0:parseInt($('input[name="status"]:checked').val());
    var app_id = $("#app_id").combobox("getValue");


     $.ajax({
            type:"post",
         //   url:'/webapi/admin/createAppServer/',
            url: sy.data.url+"/webapi/admin/createAppServer/",
            data: {
                name:name,
                ip_addr:ip_addr,
                app_id:app_id,
                is_addr_restricted:is_addr_restricted,
                status:status
            },

            dataType: "json",
            success: function(data){
                if(data.status == 0){
                   /* $.messager.alert('提示','保存成功!','info',function(){
                        closeWindow();
                        if (typeof window.parent.refush === 'function') {
                            window.parent.refush();
                        }
                    });*/
                    $.messager.alert('提示','保存成功!','info',function(){
                        closeWindow();
                       /* if (typeof window.parent.refush === 'function') {
                            window.parent.refush();
                        }*/
                    })
                }else{
                    var message = '错误代码:'+data.errcode+',错误信息'+data.errmsg+'!';
                    $.messager.alert('查询错误',message,'error');
                }
            }
     });

}


function closeWindow(){
    var frames = window.parent.frames;
    if(frames){
        for(var i=0;i<frames.length;i++){
            var dialogWindow =frames[i].dialogWindow;
            if(dialogWindow!=null){
                frames[i].searchAppServerList();
                dialogWindow.dialog('destroy');
                break;
            }
        }
    }


}