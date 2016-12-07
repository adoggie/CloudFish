var OFD = function() {
	/*
	 * 常量
	 */
	var Constant = {
		// CLSID
		CLSID : "C7F277DC-6C47-AB2C-FB6A-070DC8BE7533",
		// 控件的注册名
		ACTIVE_NAME : "suwellreaderax.SuwellOfdActiveX",
		// 嵌入类型
		EMBED_TYPE : "application/ofd",
		// 随机字符种子
		RANDOM_SEED : "0123456789qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
	};

	/*
	 * 方法和控件方法的映射. 一般来说,名称相同.key为js的方法名称;
	 * value中,real为控件的方法名,如果省略,则认为和js的方法相同.args为控件中该方法接受的参数名称
	 */
	var Method = {
		// 控件组件的显示或隐藏
		"setCompsiteVisible" : {
			args : [ "name", "visible" ]
		},
		// 兼容旧版
		"setCompositeVisible" : {
			real : "setCompsiteVisible",
			args : [ "name", "visible" ]
		},
		// 打文件(包括本地和远程)
		"openFile" : {
			args : [ "path" ]
		},
		// 打开内容推送服务器上的文件
		"openSvcFile" : {
			args : [ "url", "name" ]
		},
		// 打开远程文件
		"openURL" : {
			real : "openFile",
			args : [ "path" ]
		},
		// 将文件保存到本地磁盘或远程服务器上
		"saveFile" : {
			args : [ "path" ]
		},
		// 关闭当前文件
		"closeFile" : {
			args : []
		},
		// 设置印章名称
		"setSealName" : {
			args : [ "name" ]
		},
		// 设置印章标识
		"setSealId" : {
			args : [ "id" ]
		},
		// 设置签名算法
		"setSealSignMethod" : {
			args : [ "method" ]
		},
		// 设置阅读器的当前模式
		"setReaderMode" : {
			args : [ "mode" ]
		},
		// 在原有位置盖章
		"signOnLastPostion" : {
			args : []
		},
		// 获取语义内容
		"getTagedText" : {
			args : [ "name" ]
		},
		// 设置打印份数
		"setPrintCopies" : {
			args : [ "number" ]
		},
		// 打印文件
		"printFile" : {
			args : [ "number" ]
		},
		// 组件灰显不灰显
		"setCompsiteEnable" : {
			args : [ "name", "enable" ]
		},
		// 设置回调函数
		"setCallback" : {
			args : [ "name", "func", "after" ]
		},
		// 转换并打开转换后缓存于服务器上的文件
		"convertFile" : {
			args : [ "srcpath", "operate", "metacont" ]
		},
		// 执行指定的操作如打开、保存等，效果相当于点击对应按钮
		"performClick" : {
			args : [ "cmd" ]
		},
		// 配置服务地址，打印控制服务（print）,转换服务（convert）
		"setServiceAddr" : {
			args : [ "tag", "url" ]
		},
		// 配置选择文字后的菜单项
		"setSendtoInfo" : {
			args : [ "path" ]
		},
		//设置追踪水印
		"setBarcodeInfo" : {
			args : [ "barInfo" ]
		}
	};

	/*
	 * 一些简单的css
	 */
	var CSS = {
		info : "margin: 10px 0px; padding: 12px; border-radius:10px; color: #00529B; background-color: #BDE5F8;",
		success : "margin: 10px 0px; padding: 12px; border-radius:10px; color: #4F8A10; background-color: #DFF2BF;",
		warning : "margin: 10px 0px; padding: 12px; border-radius:10px; color: #9F6000; background-color: #FEEFB3;",
		error : "margin: 10px 0px; padding: 12px; border-radius:10px; color: #D8000C; background-color: #FFBABA;"
	};
	/*
	 * 工具
	 */
	var Tool = {
		// 合并对象
		extend : function(defs, target) {
			var r = target;
			if (this.isNull(r)) {
				if (this.isArray(defs)) {
					r = [];
				} else {
					r = {};
				}
			}
			this.each(defs, function(n, v) {
				if (!(n in r)) {
					r[n] = v;
				}
			});
			return r;
		},
		// 判断参数是否是数组
		isArray : function(v) {
			return Object.prototype.toString.call(v) === "[object Array]";
		},
		// 判断是否为纯粹对象,like jquery.isPlainObject
		isPlainObject : function(v) {
			if (!v || v.toString() !== "[object Object]" || v.nodeType
					|| "setInterval" in v) {
				return false;
			}
			try {
				if (v.constructor
						&& !v.hasOwnProperty("constructor")
						&& !v.constructor.prototype
								.hasOwnProperty("isPrototypeOf")) {
					return false;
				}
			} catch (e) {
				return false;
			}
			var key;
			for (key in v) {
			}
			return key === undefined || v.hasOwnProperty(key);
		},
		// 判断参数是否是undefined或null
		isNull : function(v) {
			return typeof v == "undefined" || (v != 0 && !v);
		},
		// 判断参数是有有效值
		isValid : function(v) {
			return this.isNull(v) !== true;
		},
		// getElementById
		_$ : function(id) {
			return document.getElementById(id);
		},
		// createElement
		_new : function(tag) {
			return document.createElement(tag);
		},
		// for-each like jquery
		each : function(o, fn) {
			if (this.isNull(o)) {
				return o;
			}
			if (this.isArray(o)) {
				for (var i = 0, ol = o.length, val = o[0]; i < ol
						&& fn.call(val, i, val) !== false; val = o[++i]) {
				}
			} else {
				for ( var i in o) {
					if (fn.call(o[i], i, o[i]) === false) {
						break;
					}
				}
			}
			return o;
		},
		// 对字符串进行转义
		escape : function(s) {
			return ('' + s).replace(/["'\\\n\r\u2028\u2029]/g, function(
					character) {
				// http://www.ecma-international.org/ecma-262/5.1/#sec-7.8.4
				switch (character) {
				case '"':
				case "'":
				case '\\':
					return '\\' + character
				case '\n':
					return '\\n'
				case '\r':
					return '\\r'
				case '\u2028':
					return '\\u2028'
				case '\u2029':
					return '\\u2029'
				}
			});
		},
		/*
		 * 浏览器类型判断 http://
		 * stackoverflow.com/questions/9847580/how-to-detect-safari-chrome-ie-firefox-and-opera-browser
		 */
		Browser : {
			// Opera 8.0+ (UA detection to detect Blink/v8-powered Opera)
			isOpera : function() {
				return !!window.opera
						|| navigator.userAgent.indexOf(' OPR/') >= 0;
			},
			// Firefox 1.0+
			isFirefox : function() {
				return typeof InstallTrigger !== 'undefined';
			},
			// At least Safari 3+: "[object HTMLElementConstructor]"
			isSafari : function() {
				return Object.prototype.toString.call(window.HTMLElement)
						.indexOf('Constructor') > 0;
			},
			// Chrome 1+
			isChrome : function() {
				return !!window.chrome && !this.isOpera();
			},
			// IE6-11
			isIE : function() {// At least IE6
				// 此处防止编辑器把正则误认为注释而出现问题
				return eval('/*@cc_on!@*/false || !!document.documentMode');
			}
		},
		/*
		 * 系统和浏览器位数
		 */
		Bit : {
			// 操作系统位数
			os : function() {
				var agent = navigator.userAgent;
				var isX64OS = agent.indexOf("WOW64") != -1
						|| agent.indexOf("Win64") != -1;
				return isX64OS ? 64 : 32;
			},
			// ie的位数
			ie : function() {
				var agent = navigator.userAgent;
				var o = OFD.Bit.os;
				var isX64IE = (o == 64) && agent.indexOf("MSIE") != -1
						&& agent.indexOf("x64") != -1;
				return isX64IE ? 64 : 32;
			}
		},
		/*
		 * 页面方法
		 */
		Page : {
			// 获取窗口宽度
			width : function() {
				var w = 0;
				if (window.innerWidth) {
					w = window.innerWidth;
				} else if ((document.body) && (document.body.clientWidth)) {
					w = document.body.clientWidth;
				}
				// 通过深入Document内部对body进行检测，获取窗口大小
				if (document.documentElement
						&& document.documentElement.clientHeight
						&& document.documentElement.clientWidth) {
					w = document.documentElement.clientWidth;
				}
				return w;
			},
			// 获取窗口高度
			height : function() {
				var h = 0;
				if (window.innerHeight) {
					h = window.innerHeight;
				} else if ((document.body) && (document.body.clientHeight)) {
					h = document.body.clientHeight;
				}
				// 通过深入Document内部对body进行检测，获取窗口大小
				if (document.documentElement
						&& document.documentElement.clientHeight
						&& document.documentElement.clientWidth) {
					h = document.documentElement.clientHeight;
				}
				return h;
			}
		}
	};

	/*
	 * 控件封装
	 */
	function Reader(config) {
		// 配置
		this.cfg = Tool.extend(
				{
					// 容纳控件的div的id
					div : undefined,
					// 控件宽度
					width : "auto",
					// 控件高度
					height : "auto",
					// 组件初始化时的状态
					compsite : {
						// 显示的控件
						show : [],
						// 隐藏的控件
						hide : [ "menu", "navigator" ]
					},
					// 控件安装程序的下载路径
					downURL : undefined,
					// 是否检查控件已经安装
					checkInstalled : true,
					// 是否在未给定容纳控件的div时自动新建
					autoNewDiv : false,
					// codebase
					codebase : undefined
				}, config);

		// 控件object封装
		this.ref = {
			// object的id
			id : undefined,
			// 控件对象
			obj : undefined
		};
		// 缓存未完成的操作
		this.operates = {};
	}

	/*
	 * 生成随机串
	 */
	var randomText = function(length) {
		var x = Constant.RANDOM_SEED;
		var s = "";
		for (var i = 0; i < length; i++) {
			s += x.charAt(Math.ceil(Math.random() * 100000000) % x.length);
		}
		return s;
	};

	/*
	 * 写出HTML信息
	 */
	Reader.prototype.message = function(html, level) {
		var div = Tool._$(this.cfg.div);
		if (Tool.isValid(div)) {
			if (Tool.isNull(level)) {
				level = "error";
			}
			if (level == "none") {
				div.innerHTML = html;
			} else {
				div.innerHTML = "<span style='" + CSS[level] + "'>" + html
						+ "</span>";
			}
		} else {
			alert(html);
		}
	}

	/*
	 * 判断组件是否已经安装
	 */
	Reader.prototype.checkComponent = function() {
		if (Tool.Browser.isIE()) {
			return this.hasActiveX();
		} else if (Tool.Browser.isFirefox()) {
			return this.hasEmbed();
		}
		return "不支持的浏览器类型";
	}

	/*
	 * 判断Firefox是否已经安装了OFD控件
	 */
	Reader.prototype.hasEmbed = function() {
		return true;
	}

	/*
	 * 判断IE是否安装了OFD控件
	 */
	Reader.prototype.hasActiveX = function() {
		if ("ActiveXObject" in window) {// 判断是否IE
			if (this.cfg.checkInstalled !== true) {
				return true;
			}
			try {// 判断是否安装OFD阅读器
				var axo = new ActiveXObject(Constant.ACTIVE_NAME);
				return true;
			} catch (e) {
				var html = "OFD阅读控件没有正确安装，请下载安装！";
				if (Tool.isValid(this.cfg.downURL)) {
					html += "<br><a href='"// 
							+ this.cfg.downURL //
							+ "' target='_blank'>&gt;&gt;&gt;&gt;&nbsp;&nbsp;下载&nbsp;&nbsp;&lt;&lt;&lt;&lt;</a>";
				}
				// html +=
				// "<br>由于安装程序会更改IE的安全设置并注册dll文件，安全软件可能会弹出安全警告，允许本软件继续即可。<br>建议使用管理员权限运行本软件。";
				this.message(html, "warn");
			}
		} else {
			this.message("无法显示ActiveX控件,请使用IE访问", "warn");
		}
		return false;
	};

	/*
	 * 输出控件的HTML
	 */
	Reader.prototype.write = function() {
		var w = this.cfg.width;
		if (Tool.isNull(w) || w == "auto") {
			w = "100%";
		}
		var h = this.cfg.height;
		if (Tool.isNull(h) || h == "auto") {
			h = (Tool.Page.height() - 10) + "px";
		}

		if (Tool.Browser.isIE()) {
			this.message("<object id='" + this.ref.id // id
					+ "' width='" + w// width
					+ "' height='" + h// heigth
					+ "' classid='CLSID:" + Constant.CLSID // clsid
					// + "' codebase='" + this.cfg.codebase //
					// codebase,不使用cab时注释掉此行
					+ "'><param name='object_id' value = '" + this.ref.id
					+ "'><param name='inited_call' value = '__OFD_OCX_Ready'> "
					+ "</object>", "none");
		} else if (Tool.Browser.isFirefox()) {
			this.message("<embed id='" + this.ref.id // id
					+ "' width='" + w// width
					+ "' height='" + h// heigth
					+ "' type='" + Constant.EMBED_TYPE// type
					+ "' object_id='" + this.ref.id
					+ "' inited_call='__OFD_OCX_Ready"// callback
					+ "' >", "none");
		} else {
			this.message("不支持的浏览器类型", "error");
		}

	};

	/*
	 * 加载控件
	 */
	Reader.prototype.load = function() {
		var rand = randomText(10);
		if (Tool.isNull(this.cfg.div)) {
			if (this.cfg.autoNewDiv === true) {
				// 新建一个div放置控件,并追加到body的最后
				var div = Tool._new("div");
				div.id = "ofd_div_" + rand;
				var body = document.body;
				if (Tool.isNull(body)) {
					this.message("请在onload中调用本方法", "warn");
					return;
				} else {
					body.appendChild(div);
				}
				this.cfg.div = div.id;
			} else {
				this.message("请指定一个div,以便写入控件!");
				return;
			}
		}
		var check = this.checkComponent();
		if (check === true) {
			this.message("正在加载控件，请稍候...", "info");
			this.ref.id = "ofd_ocx_" + rand;
			this.write();
		} else if (check === false) {
			this.message("控件加载失败", "error");
		} else {
			this.message(check);
		}
	};

	/*
	 * 缓存操作
	 */
	Reader.prototype.cache = function(fnName, fnArgs) {
		var o = this.operates[fnName];
		if (Tool.isNull(o)) {
			o = new Array();
			this.operates[fnName] = o;
		}
		o.push(fnArgs);
	};

	/*
	 * 检查组件是否准备完毕
	 */
	Reader.prototype.valid = function() {
		return Tool.isValid(this.ref.obj);
	};

	// 遍历注册所有的方法
	Tool.each(Method, function(name, val) {
		Reader.prototype[name] = function() {
			// 方法名
			var n = val.real;
			if (Tool.isNull(n)) {
				n = name;
			}

			// 参数
			var l = val.args.length, al = arguments.length;
			if (l > al) {
				l = al;
			}
			var arg = [];
			for (var i = 0; i < l; i++) {
				arg[i] = arguments[i];
			}

			// 返回值
			var ret;
			if (this.valid()) {
				var o = this.ref.obj;
				if (Tool.isArray(arg[0])) {// 第一个参数是数组,拆开执行
					var A = arg.slice();
					Tool.each(arg[0], function(i, v) {
						A[0] = v;
						_eval(o, n, A);
					});
				} else {// 执行并返回值
					ret = _eval(o, n, arg);
				}
			} else {// 缓存操作
				this.cache(n, arg);
			}
			return ret;
		}
	});

	// 执行控件的方法
	var _eval = function(o, m, args) {
		var arg = "";
		Tool.each(args, function(i, v) {
			if (i > 0) {
				arg += ", ";
			}
			if (typeof (v) === "string") {
				arg += "\"" + Tool.escape(v) + "\"";
			} else {
				arg += v;
			}
		});
		try {
			return eval("o." + m + "(" + arg + ")");
		} catch (e) {
			window.console && console.log("Eval " + m + " : " + e);
		}
	}

	/*
	 * 控件版本号
	 */
	Reader.prototype.version = function() {
		var o = Tool._$(this.ref.id);
		try {
			return o.version();
		} catch (e) {
		}
		return false;
	}

	/*
	 * 加载配置,完成准备工作,只执行一次
	 */
	Reader.prototype.ready = function() {
		if (this.valid()) {// 已经初始化
			return;
		}

		var o = Tool._$(this.ref.id);
		if (Tool.isNull(o)) {// 判断是否有对象
			this.message("控件未正确初始化!");
			return;
		}
		// 赋值,很重要
		this.ref.obj = o;

		var T = this;

		// 控制初始化时的组件显示
		Tool.each([ "show", "hide" ], function(i, n) {
			var v = T.cfg.compsite[n];
			if (Tool.isValid(v) && v.length > 0) {
				T.setCompsiteVisible(v, n == "show");
			}
		});

		// 加载完毕前的动作都执行一遍
		Tool.each(this.operates, function(n, v) {
			if (Tool.isArray(v) && v.length > 0) {
				var fn = T[n];// 得到本对象的函数
				if (fn) {// 如果正确,执行函数
					Tool.each(v, function(i, args) {
						try {
							fn.apply(T, args);
						} catch (e) {
						}
					});
				}

				v.length = 0;// 清除缓存
			}
		});
	};

	return {// 防止外界的非法访问
		OCX : {
			// 缓存所有的控件对象
			_cache : {},
			// 初始化一个控件
			init : function(a) {
				var config = {};
				if (Tool.isPlainObject(a)) {
					config = Tool.extend(config, a);
				} else {
					var name = [ "div", "width", "height", "downURL" ];
					for (var i = 0; i < arguments.length; i++) {
						if (i > name.length - 1) {
							break;
						}
						var n = name[i], v = arguments[i];
						if (Tool.isValid(v)) {
							config[n] = arguments[i];
						}
					}
				}

				// 新对象
				var reader = new Reader(config);
				reader.load();// 加载
				var id = reader.ref.id;
				// 尝试用版本号来确定是否已经加载
				var _t = this;
				var i = setInterval(function() {
					if (reader.version() !== false) {
						_t.ready(id);
					}
				}, 500);
				this._cache[id] = {// 缓存起来
					o : reader,
					t : i
				};
				return reader;
			},
			// 控件已准备好
			ready : function(id) {
				var r = this._cache[id];
				if (Tool.isValid(r) && Tool.isValid(r.o)) {
					r.o.ready();
					clearInterval(r.t);

					window.console
							&& console.log("Reader is ready, version is "
									+ r.o.version());
				}
				return r;
			}
		}
	}
}();// 立即执行函数,使其成为单例

/*
 * 供控件在加载完毕后回调
 */
function __OFD_OCX_Ready(id) {
	OFD.OCX.ready(id);
}

var suwell = {};
// 加载并初始化阅读器OCX控件
suwell.ofdReaderInit = function(divID, width, height) {
	return OFD.OCX.init(divID, width, height);
};
// 加载并初始化转换器OCX控件
suwell.ofdCreatorInit = function(divID, width, height) {
	return OFD.OCX.init(divID, width, height);
};

// 菜单栏对应的ID
// "menu" 针对整个菜单栏
// "menu_file" 文件菜单项
// "menu_document" 文档菜单项
// "menu_view" 视图菜单项
// "menu_tool" 工具菜单项
// "menu_windows" 窗口菜单项
// "menu_help" 帮助菜单项
//
// 工具栏对应的ID
// "toolbar_file" 文件工具栏
// "toolbar_view" 视图工具栏
// "toolbar_operat" 文档操作工具栏
// "toolbar_documentview" 文档视图工具栏
// "toolbar_signature" 签章工具栏
// "navigator" "导航栏"
//
// 各个工具项对应的ID
// "open" "打开"
// "save" "保存"
// "print" "打印"
// "zoom_in" "放大"
// zoom_out" "缩小"
// "full_screen" "全屏显示"
// "zoom_original" "原始大小"
// "zoom_fitwidth" "适合宽度"
// "rotate_clock" "顺时针旋转90°"
// "rotate_anti" "逆时针旋转90°"
// "pagelayout_singlepage" "单页"
// "pagelayout_singleflow" "单页连续"
// "find_text" "查找文本"
// "toolstate_textselect" "文本选择"
// toolstate_handtool" "手型工具"
// "frist_page" "第一页"
// "previous_page" "前一页"
// "next_page" "下一页"
// "last_page" "最后一页"
// "annot_sealsign" "印章签名"
// "tool_stamp" "橡皮图章"
