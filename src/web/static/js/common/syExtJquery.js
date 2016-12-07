/**
 * Created by 丞寅 on 2014/11/11.
 */
var sy = sy || {};
sy.data = sy.data || {
    user_name:"",
    login_name:"",
    unit_name:"",
    unit_id:"",
    role_id:"",
    url:"",//ip地址
    reg_id:"" //标签标识平台应用注册时返回的ID
};// 用于存放临时的数据或者对象

sy.jsProgressBar;//滚动条对象

/**
 * 屏蔽右键
 * @requires jQuery
 */
$(document).bind('contextmenu', function() {
    // return false;
});


//日期格式化
//---------------------------------------------------
// 日期格式化
// 格式 YYYY/yyyy/YY/yy 表示年份
// MM/M 月份
// W/w 星期
// dd/DD/d/D 日期
// hh/HH/h/H 时间
// mm/m 分钟
// ss/SS/s/S 秒
//---------------------------------------------------
Date.prototype.Format = function(formatStr)
{
    var str = formatStr;
    var Week = ['日','一','二','三','四','五','六'];

    str=str.replace(/yyyy|YYYY/,this.getFullYear());
    str=str.replace(/yy|YY/,(this.getYear() % 100)>9?(this.getYear() % 100).toString():'0' + (this.getYear() % 100));

    str=str.replace(/MM/,(this.getMonth()+1)>9?(this.getMonth()+1).toString():'0' + (this.getMonth()+1));
    str=str.replace(/M/g,this.getMonth()+1);

    str=str.replace(/w|W/g,Week[this.getDay()]);

    str=str.replace(/dd|DD/,this.getDate()>9?this.getDate().toString():'0' + this.getDate());
    str=str.replace(/d|D/g,this.getDate());

    str=str.replace(/hh|HH/,this.getHours()>9?this.getHours().toString():'0' + this.getHours());
    str=str.replace(/h|H/g,this.getHours());
    str=str.replace(/mm/,this.getMinutes()>9?this.getMinutes().toString():'0' + this.getMinutes());
    str=str.replace(/m/g,this.getMinutes());

    str=str.replace(/ss|SS/,this.getSeconds()>9?this.getSeconds().toString():'0' + this.getSeconds());
    str=str.replace(/s|S/g,this.getSeconds());

    return str;
}

//+---------------------------------------------------
//| 字符串转成日期类型
//| 格式 MM/dd/YYYY MM-dd-YYYY YYYY/MM/dd YYYY-MM-dd
//+---------------------------------------------------
sy.stringToDate = function(DateStr)
{
    if(DateStr==null||DateStr==""){
        return null;
    }
    var converted = Date.parse(DateStr);
    var myDate = new Date(converted);
    if (isNaN(myDate))
    {
        var arys= DateStr.split('-');
        myDate = new Date(arys[0],--arys[1],arys[2]);
    }
    return myDate;
}

//获取秒数
//
sy.getDateTime = function(DateStr){
    var date = sy.stringToDate(DateStr);
    if(date&&date!=''){
        date.setHours(0);
        date.setMinutes(0);
        date.setSeconds(0);
        date.setMilliseconds(0);
        return date.getTime()/1000;
    }else{
        return null;
    }
}

//获取秒数
//+ 23:59:59
sy.getDateTimeEnd = function(DateStr){
    var date = sy.stringToDate(DateStr);
    if(date&&date!=''){
        date.setHours(0);
        date.setMinutes(0);
        date.setSeconds(0);
        date.setMilliseconds(0);
        return date.getTime()/1000+86399;
    }else{
        return null;
    }
}

//获取秒数
//+ 23:59:59
sy.getDateTimeEndFromDate = function(date){
    if(date&&date!=''){
        date.setHours(0);
        date.setMinutes(0);
        date.setSeconds(0);
        date.setMilliseconds(0);
        return date.getTime()/1000+86399;
    }else{
        return null;
    }
}

sy.setStringByDateTime = function(DateTime,formatStr){
    if(DateTime==null||DateTime==''){
        return null
    }else{
        if(formatStr==null||formatStr==""){
            formatStr = "YYYY-MM-DD";
        }
        var date=new Date(Number(DateTime*1000));//后台给的是秒
        return date.Format(formatStr);
    }
}

/**
 * 禁止复制
 * @requires jQuery
 */
$(document).bind('selectstart', function() {
    // return false;
});

/**
 * 增加命名空间功能
 *
 * 使用方法：sy.ns('jQuery.bbb.ccc','jQuery.eee.fff');
 */
sy.ns = function() {
    var o = {}, d;
    for (var i = 0; i < arguments.length; i++) {
        d = arguments[i].split(".");
        o = window[d[0]] = window[d[0]] || {};
        for (var k = 0; k < d.slice(1).length; k++) {
            o = o[d[k + 1]] = o[d[k + 1]] || {};
        }
    }
    return o;
};

/**
 * 将form表单元素的值序列化成对象
 *
 * @example sy.serializeObject($('#formId'))
 * @requires jQuery
 *
 * @returns object
 */
sy.serializeObject = function(form) {
    var o = {};
    $.each(form.serializeArray(), function(index) {
        if (this['value'] != undefined && this['value'].length > 0) {// 如果表单项的值非空，才进行序列化操作
            if (o[this['name']]) {
                o[this['name']] = o[this['name']] + "," + this['value'];
            } else {
                o[this['name']] = this['value'];
            }
        }
    });
    return o;
};

/**
 * 增加formatString功能
 * @example sy.formatString('字符串{0}字符串{1}字符串','第一个变量','第二个变量');
 *
 * @returns 格式化后的字符串
 */
sy.formatString = function(str) {
    for (var i = 0; i < arguments.length - 1; i++) {
        str = str.replace("{" + i + "}", arguments[i + 1]);
    }
    return str;
};

/**
 * 接收一个以逗号分割的字符串，返回List，list里每一项都是一个字符串
 * @returns list
 */
sy.stringToList = function(value) {
    if (value != undefined && value != '') {
        var values = [];
        var t = value.split(',');
        for (var i = 0; i < t.length; i++) {
            values.push('' + t[i]);/* 避免他将ID当成数字 */
        }
        return values;
    } else {
        return [];
    }
};

/**
 * JSON对象转换成String
 *
 * @param o
 * @returns
 */
sy.jsonToString = function(o) {
    var r = [];
    if (typeof o == "string")
        return "\"" + o.replace(/([\'\"\\])/g, "\\$1").replace(/(\n)/g, "\\n").replace(/(\r)/g, "\\r").replace(/(\t)/g, "\\t") + "\"";
    if (typeof o == "object") {
        if (!o.sort) {
            for ( var i in o)
                r.push(i + ":" + sy.jsonToString(o[i]));
            if (!!document.all && !/^\n?function\s*toString\(\)\s*\{\n?\s*\[native code\]\n?\s*\}\n?\s*$/.test(o.toString)) {
                r.push("toString:" + o.toString.toString());
            }
            r = "{" + r.join() + "}";
        } else {
            for (var i = 0; i < o.length; i++)
                r.push(sy.jsonToString(o[i]));
            r = "[" + r.join() + "]";
        }
        return r;
    }
    return o.toString();
};

/**
 * Create a cookie with the given key and value and other optional parameters.
 *
 * @example sy.cookie('the_cookie', 'the_value');
 * @desc Set the value of a cookie.
 * @example sy.cookie('the_cookie', 'the_value', { expires: 7, path: '/', domain: 'jquery.com', secure: true });
 * @desc Create a cookie with all available options.
 * @example sy.cookie('the_cookie', 'the_value');
 * @desc Create a session cookie.
 * @example sy.cookie('the_cookie', null);
 * @desc Delete a cookie by passing null as value. Keep in mind that you have to use the same path and domain used when the cookie was set.
 *
 * @param String
 *            key The key of the cookie.
 * @param String
 *            value The value of the cookie.
 * @param Object
 *            options An object literal containing key/value pairs to provide optional cookie attributes.
 * @option Number|Date expires Either an integer specifying the expiration date from now on in days or a Date object. If a negative value is specified (e.g. a date in the past), the cookie will be deleted. If set to null or omitted, the cookie will be a session cookie and will not be retained when the the browser exits.
 * @option String path The value of the path atribute of the cookie (default: path of page that created the cookie).
 * @option String domain The value of the domain attribute of the cookie (default: domain of page that created the cookie).
 * @option Boolean secure If true, the secure attribute of the cookie will be set and the cookie transmission will require a secure protocol (like HTTPS).
 * @type undefined
 *
 * @name sy.cookie
 * @cat Plugins/Cookie
 * @author Klaus Hartl/klaus.hartl@stilbuero.de
 *
 * Get the value of a cookie with the given key.
 *
 * @example sy.cookie('the_cookie');
 * @desc Get the value of a cookie.
 *
 * @param String
 *            key The key of the cookie.
 * @return The value of the cookie.
 * @type String
 *
 * @name sy.cookie
 * @cat Plugins/Cookie
 * @author Klaus Hartl/klaus.hartl@stilbuero.de
 */
sy.cookie = function(key, value, options) {
    if (arguments.length > 1 && (value === null || typeof value !== "object")) {
        options = $.extend({}, options);
        if (value === null) {
            options.expires = -1;
        }
        if (typeof options.expires === 'number') {
            var days = options.expires, t = options.expires = new Date();
            t.setDate(t.getDate() + days);
        }
        return (document.cookie = [ encodeURIComponent(key), '=', options.raw ? String(value) : encodeURIComponent(String(value)), options.expires ? '; expires=' + options.expires.toUTCString() : '', options.path ? '; path=' + options.path : '', options.domain ? '; domain=' + options.domain : '', options.secure ? '; secure' : '' ].join(''));
    }
    options = value || {};
    var result, decode = options.raw ? function(s) {
        return s;
    } : decodeURIComponent;
    return (result = new RegExp('(?:^|; )' + encodeURIComponent(key) + '=([^;]*)').exec(document.cookie)) ? decode(result[1]) : null;
};

/**
 * 改变jQuery的AJAX默认属性和方法
 * @requires jQuery
 *
 */
$.ajaxSetup({
    type : 'POST',
    error : function(XMLHttpRequest, textStatus, errorThrown) {
        try {
            parent.$.messager.progress('close');
            parent.$.messager.alert('错误', XMLHttpRequest.responseText);
        } catch (e) {
            alert(XMLHttpRequest.responseText);
        }
    }
});

/**
 * 解决class="iconImg"的img标记，没有src的时候，会出现边框问题
 * @requires jQuery
 */
$(function() {
    $('.iconImg').attr('src', sy.pixel_0);
});

/**
 * 滚动条
 *
 * @requires jQuery,EasyUI
 */
sy.progressBar = function(options) {
    if (typeof options == 'string') {
        if (options == 'close') {
            $('#syProgressBarDiv').dialog('destroy');
        }
    } else {
        if ($('#syProgressBarDiv').length < 1) {
            var opts = $.extend({
                title : '&nbsp;',
                closable : false,
                width : 300,
                height : 60,
                modal : true,
                content : '<div id="syProgressBar" class="easyui-progressbar" data-options="value:0"></div>'
            }, options);
            $('<div id="syProgressBarDiv"/>').dialog(opts);
            $.parser.parse('#syProgressBarDiv');
        } else {
            $('#syProgressBarDiv').dialog('open');
        }
        if (options.value) {
            $('#syProgressBar').progressbar('setValue', options.value);
        }
    }
};

/**
 * 滚动条
 *
 * @requires jQuery,EasyUI
 */
sy.progressBarJs = function(options) {
    if (typeof options == 'string') {
        if (options == 'close') {
            $('#progressDiv').progressbar('setValue',0);
            $('#syProgressBarDiv').dialog('close');
        }
    } else {
        $('#syProgressBarDiv').dialog('open');
    }
    if (options&&options.value) {
        $('#progressDiv').progressbar('setValue',options.value);
    }
    if (options&&options.text) {
        $('#progressMsg').html(options.text);
    }

};

/**
 * 获取url中的参数
 */
sy.getUrlParam=function(name){
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if(r != null){
        return unescape(r[2]);
    }else{
        return null; //返回参数值
    }
};

/**
 * 创建一个模式化的dialog
 *
 * @requires jQuery,EasyUI
 *
 */
sy.modalDialog = function(options) {
    var opts = $.extend({
        iconCls:'document_new',
        title : '&nbsp;',
        width : 640,
        height : 500,
        modal : true,
        onClose : function() {
            $(this).dialog('destroy');
        }
    }, options);
    opts.modal = true;// 强制此dialog为模式化，无视传递过来的modal参数
    if (options.url) {
        opts.content = '<iframe id="" src="' + options.url + '" allowTransparency="true" scrolling="auto" width="100%" height="98%" frameBorder="0" name=""></iframe>';
    }
    return $('<div/>').dialog(opts);
};

/**
 * 去字符串空格
 */
sy.trim = function(str) {
    return str.replace(/(^\s*)|(\s*$)/g, '');
};
sy.ltrim = function(str) {
    return str.replace(/(^\s*)/g, '');
};
sy.rtrim = function(str) {
    return str.replace(/(\s*$)/g, '');
};

/**
 * 判断开始字符是否是XX
 */
sy.startWith = function(source, str) {
    var reg = new RegExp("^" + str);
    return reg.test(source);
};
/**
 * 判断结束字符是否是XX
 */
sy.endWith = function(source, str) {
    var reg = new RegExp(str + "$");
    return reg.test(source);
};

/**
 * iframe自适应高度
 * @param iframe
 */
sy.autoIframeHeight = function(iframe) {
    iframe.style.height = iframe.contentWindow.document.body.offsetHeight + "px";
};

/**
 * 设置iframe高度
 * @param iframe
 */
sy.setIframeHeight = function(iframe, height) {
    iframe.height = height;
};

sy.isEmpty = function(value){
    if(value==null||value==""||typeof(value) == "undefined"||value.toString().trim()==""){
        return true;
    }else{
        return false;
    }
}

/**
 * 防止panel/window/dialog组件超出浏览器边界
 * @requires jQuery,EasyUI
 */
sy.onMove = {
    onMove : function(left, top) {
        var l = left;
        var t = top;
        if (l < 1) {
            l = 1;
        }
        if (t < 1) {
            t = 1;
        }
        var width = parseInt($(this).parent().css('width')) + 14;
        var height = parseInt($(this).parent().css('height')) + 14;
        var right = l + width;
        var buttom = t + height;
        var browserWidth = $(window).width();
        var browserHeight = $(window).height();
        if (right > browserWidth) {
            l = browserWidth - width;
        }
        if (buttom > browserHeight) {
            t = browserHeight - height;
        }
        $(this).parent().css({/* 修正面板位置 */
            left : l,
            top : t
        });
    }
};
$.extend($.fn.dialog.defaults, sy.onMove);
$.extend($.fn.window.defaults, sy.onMove);
$.extend($.fn.panel.defaults, sy.onMove);

/**
 *
 * 通用错误提示
 *
 * 用于datagrid/treegrid/tree/combogrid/combobox/form加载数据出错时的操作
 * @requires jQuery,EasyUI
 */
sy.onLoadError = {
    onLoadError : function(XMLHttpRequest) {
        if (parent.$ && parent.$.messager) {
            parent.$.messager.progress('close');
            parent.$.messager.alert('错误', XMLHttpRequest.responseText);
        } else {
            $.messager.progress('close');
            $.messager.alert('错误', XMLHttpRequest.responseText);
        }
    }
};
$.extend($.fn.datagrid.defaults, sy.onLoadError);
$.extend($.fn.treegrid.defaults, sy.onLoadError);
$.extend($.fn.tree.defaults, sy.onLoadError);
$.extend($.fn.combogrid.defaults, sy.onLoadError);
$.extend($.fn.combobox.defaults, sy.onLoadError);
$.extend($.fn.form.defaults, sy.onLoadError);

/**
 * panel关闭时回收内存，主要用于layout使用iframe嵌入网页时的内存泄漏问题
 * @requires jQuery,EasyUI
 *
 */
$.extend($.fn.panel.defaults, {
    onBeforeDestroy : function() {
        var frame = $('iframe', this);
        try {
            if (frame.length > 0) {
                for (var i = 0; i < frame.length; i++) {
                    frame[i].src = '';
                    frame[i].contentWindow.document.write('');
                    frame[i].contentWindow.close();
                }
                frame.remove();
                if (navigator.userAgent.indexOf("MSIE") > 0) {// IE特有回收内存方法
                    try {
                        CollectGarbage();
                    } catch (e) {
                    }
                }
            }
        } catch (e) {
        }
    }
});

function isPicture(sourceStr){
    var FileListType="jpg,JPG,gif,GIF,jpeg,JPEG,png,PNG";
    var destStr = sourceStr.substring(sourceStr.lastIndexOf(".")+1,sourceStr.length)
    if(FileListType.indexOf(destStr) == -1){
        alert("只允许上传jpg,JPG,gif,GIF,jpeg,JPEG,png,PNG文件");
        return false;
    }
    return true;
}


/**
 * 上传附件编辑框
 *
 */
$.extend($.fn.datagrid.defaults.editors, {
    fileBox: {
        init: function(container, options){
            var div = $('<div />');
            var fileInput = $('<input type="file"  />');//accept="image/*"
            var hiddenInput = $('<input type="hidden" style="width:0px"  />');
            var updateInput = $('<input type="button" value="修改" style="display:none" >');
            var clearInput = $('<input type="button" value="清空"  style="display:none" >');
            $(fileInput).on('change',function(event){
                var files = event.target.files,file;
                if (files && files.length > 0) {
                    file = files[0];
                    if(isPicture(file.name)){
                        var fileReader = new FileReader();
                        fileReader.onload = function (event) {
                            div[0].childNodes[1].value = event.target.result;
                            //var hidden = $('<input type="hidden" value="'+event.target.result+'" />').appendTo(container);
                        };
                        fileReader.readAsDataURL(file);
                        return true;
                    }else{
                        return false;
                    }
                }

            });
            $(updateInput).on('click',function(event){
                div[0].childNodes[0].style.display = "";
                div[0].childNodes[2].style.display = "none";
                div[0].childNodes[3].style.display = "none";
            });
            $(clearInput).on('click',function(event){
                div[0].childNodes[1].value = "";
                div[0].childNodes[2].style.display = "none";
                div[0].childNodes[3].style.display = "none";
                div[0].childNodes[0].style.display = "";
            });
            div.append(fileInput);
            div.append(hiddenInput);
            div.append(updateInput);
            div.append(clearInput);
            div.appendTo(container);
            return div;
        },
        getValue: function(target){
            var inputs = target[0].childNodes[1];
            return sy.isEmpty(inputs)?null:inputs.value;
        },
        setValue: function(target, value){
            if(!sy.isEmpty(value)){
                target[0].childNodes[1].value = value;
                target[0].childNodes[0].style.display = "none";
                target[0].childNodes[2].style.display = "";
                target[0].childNodes[3].style.display = "";
            }else{
                target[0].childNodes[0].style.display = "";
                target[0].childNodes[2].style.display = "none";
                target[0].childNodes[3].style.display = "none";
            }

        },
        resize: function(target, width){
            var input = $(target);
            if ($.boxModel == true){
                input.width(width - (input.outerWidth() - input.width()));
            } else {
                input.width(width);
            }
        }
    }
});

/**
 * 扩展validatebox，添加新的验证功能
 *
 * @requires jQuery,EasyUI
 */
$.extend($.fn.validatebox.defaults.rules, {
    eqPwd : {/* 验证两次密码是否一致功能 */
        validator : function(value, param) {
            return value == $(param[0]).val();
        },
        message : '密码不一致！'
    },
    idCard : {// 验证身份证
        validator : function(value) {
            return /^\d{15}(\d{2}[A-Za-z0-9])?$/i.test(value);
        },
        message : '身份证号码格式不正确'
    },
    mobile : {// 验证手机号码
        validator : function(value) {
            return /^(13|15|18)\d{9}$/i.test(value);
        },
        message : '手机号码格式不正确'
    },
    zip : {// 验证邮政编码
        validator : function(value) {
            return /^[1-9]\d{5}$/i.test(value);
        },
        message : '邮政编码格式不正确'
    },
    phone : {// 验证电话号码
        validator : function(value) {
            return /^((\(\d{2,3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}(\-\d{1,4})?$/i.test(value);
        },
        message : '格式不正确,请使用下面格式:020-88888888'
    },
    fax : {// 验证电话号码
        validator : function(value) {
            return /^((\(\d{2,3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}(\-\d{1,4})?$/i.test(value);
        },
        message : '格式不正确,请使用下面格式:888-88888888'
    },
    isBlank: {
        validator: function (value, param) { return $.trim(value) != '' },
        message: '不能为空，全空格也不行'
    },
    checkIp : {// 验证IP地址
        validator : function(value) {
            var reg = /^((1?\d?\d|(2([0-4]\d|5[0-5])))\.){3}(1?\d?\d|(2([0-4]\d|5[0-5])))$/ ;
            return reg.test(value);
        },
        message : 'IP地址格式不正确'
    },
    phoneAndMobile:{
        validator : function(value) {
            var isPhone = /^([0-9]{3,4}-)?[0-9]{7,8}$/;
            var isMob=/^((\+?86)|(\(\+86\)))?(13[012356789][0-9]{8}|15[012356789][0-9]{8}|18[02356789][0-9]{8}|147[0-9]{8}|1349[0-9]{7})$/;
            return isMob.test(value)||isPhone.test(value);
        },
        message : '格式不正确,请输入手机或者电话'
    }
});

/**
 * 判断是否为非负整形
 * @param value
 * @returns {boolean}
 */
sy.checkInt = function(value) {
    var pattern = /^[1-9]\d*|0$/; //匹配非负整数
    value = value.replace(/[^\d]/g, "");

    if (!pattern.test(value)) {
        value = "";
        return false;
    }else{
        return true;
    }
};

/**
 * 字符串截取，并补充...
 * @param str
 * @param length
 * @param char
 * @returns {*}
 */
sy.fixedWidth =function(str,length,char){
        str=str.toString();
        if(!char) char="...";
        var num=length-lengthB(str);
        if(num<0)
        {
            str=substringB(str,length-lengthB(char))+char;
        }
        return str;
        function substringB(str,length)
        {
            var num= 0,len=str.length,tenp="";
            if(len)
            {
                for(var i=0;i<len;i++)
                {
                    if(num>length) break;
                    if(str.charCodeAt(i)>255)
                    {
                        num+=2;
                        tenp+=str.charAt(i);
                    }
                    else
                    {
                        num++;
                        tenp+=str.charAt(i);
                    }
                }
                return tenp;
            }
            else
            {
                return null;
            }
        }
        function lengthB(str)
        {
            var num= 0,len=str.length;
            if(len)
            {
                for(var i=0;i<len;i++)
                {
                    if(str.charCodeAt(i)>255)
                    {
                        num+=2;
                    }
                    else
                    {
                        num++;
                    }
                }
                return num;
            }
            else
            {
                return 0;
            }
        }
};

sy.addOrRemoveClass = function(object,addClassArr,removeClassArr){
    if(removeClassArr&&removeClassArr.length>0){
        for(var i=0;i<removeClassArr.length;i++){
            $(object).removeClass(removeClassArr[i]);
        }
    }
    if(addClassArr&&addClassArr.length>0){
        for(var i=0;i<addClassArr.length;i++){
            $(object).addClass(addClassArr[i]);
        }

    };
};

/**
 * databox添加清空按钮操作
 * @type {*|void}
 */
sy.databoxbtn= $.extend([], $.fn.datebox.defaults.buttons);
sy.databoxbtn.splice(1, 0, {
    text: '清空',
    handler: function(target){
        $(target).datebox('setValue', '');
    }
});

$.ajaxSetup({
    complete:function(event,xhr, settings){
        //对返回的数据data做判断，
        //session过期的话，就location到一个页面
        if (event.responseJSON&&event.responseJSON.status&&event.responseJSON.status != 0) {
            var errcode = event.responseJSON.errcode;
            if(errcode == 1001) {//未登录或会话过期
                window.location.href=  "/admin/";
                if (window != top)
                    top.location.href = window.location.href;
                return;
            }
        }
    }
});

//jQuery(function($){
//    // 备份jquery的ajax方法
//    var _ajax=$.ajax;
//    // 重写ajax方法，先判断登录在执行success函数
//    $.ajax=function(opt){
//        var _success = opt && opt.success || function(a, b){};
//        var _opt = $.extend(opt, {
//            success:function(data, textStatus){
//                // 如果后台将请求重定向到了登录页，则data里面存放的就是登录页的源码，这里需要找到data是登录页的证据(标记)
//                if (data.status != 0) {
//                    var errcode = data.errcode;
//                    if(errcode == 1001) {//未登录或会话过期
//                        window.location.href=  + "/login.html";
//                        return;
//                    }
//                    _success(data, textStatus);
//                }
//
//            }
//        });
//        _ajax(_opt);
//    };
//});