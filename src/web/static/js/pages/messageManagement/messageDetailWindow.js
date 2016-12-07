/**
 * Created by 丞寅 on 2014/11/19.
 */
var id = "";

$(function() {
    var table = $('#messageTab').tabs({
        tabPosition:'left',
        width:600,
        height:400,
        headerWidth:220
    });
    id = sy.getUrlParam('id');
    addTabs();
});

function addTabs() {
    $.ajax({
        type: "post",
        url: sy.data.url + "/webapi/ras/getThreadMessageList/",
        data: {msg_id: id},
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                var results = data.result;
                var tabs = $('#messageTab');
                var rootId = '';
                if(results.length>0){
                    var rootResult = results[results.length-1];
                    rootId = rootResult.id;
                }
                for (var i = 0; i < results.length; i++) {
                    var result = results[i];
                    var src = 'messageTabDetailView.html?id=' + result.id+"&rootId="+rootId;
                    var opts = {
                        id: result.id,
                        title: result.issue_unit + '-' + sy.setStringByDateTime(result.issue_time, 'YYYY-MM-DD hh:mm:ss'),
                        closable: false,
                        content: sy.formatString('<iframe src="{0}" allowTransparency="true" style="border:0;width:100%;height:99%;" frameBorder="0"></iframe>', src),
                        border: false,
                        fit: true
                    };
                    tabs.tabs('add', opts);

                }

            } else {
                var message = '错误代码:' + data.errcode + ',错误信息:' + data.errmsg + '!';
                $.messager.alert('查询错误', message, 'error');
            }
        }
    });
};

function refushTabs(){
    closeAllTabs('messageTab');
    addTabs();
}

//清空所有的Tab
function closeAllTabs(id){
    var arrTitle = new Array();
    var id = "#"+id;//Tab所在的层的ID
    var tabs = $(id).tabs("tabs");//获得所有小Tab
    var tCount = tabs.length;
    if(tCount>0){
        //收集所有Tab的title
        for(var i=0;i<tCount;i++){
            arrTitle.push(tabs[i].panel('options').title)
        }
        //根据收集的title一个一个删除=====清空Tab
        for(var i=0;i<arrTitle.length;i++){
            $(id).tabs("close",arrTitle[i]);
        }
    }
}