//JavaScript Document

function $$(id){
	return document.getElementById(id);
}

//调用画图
function draw(){
	onload = drawstart(100, 120, 40);
	onload = drawend(560,120+180,40);
	onload = drawrect(235, 93, 135, 54);
	onload = drawline(140, 114 ,65, 13);
	onload = drawtext(250,125);
}
//起始点
function drawstart(x,y,r){
	var can = $$('can');
	var cans = can.getContext('2d');
	cans.beginPath();
	cans.arc(x,y,r,0,Math.PI*2,false);
	cans.closePath();
	cans.lineWidth = 3;
	cans.fillStyle = "#039a98";
	cans.fill();
	//画空心圆
	//cans.strokeStyle = 'green';
	//cans.stroke();
}
//结束点
function drawend(x,y,r){	
	var can = $$('can');
	var cans = can.getContext('2d');
	cans.beginPath();
	cans.arc(x,y,r,0,Math.PI*2,false);
	cans.closePath();
	cans.lineWidth = 3;
	cans.fillStyle = 'red';
	cans.fill();
}
//流程矩形框
function drawrect(x,y,w,h){
    var can = $$('can');
    var cans = can.getContext('2d');
    //cans.strokeStyle = '#cfe2f3';
	cans.fillStyle = "#039a63"
    cans.fillRect(x,y,w,h);
	cans.fillRect(x+230,y,w,h);
	cans.fillRect(x+460,y,w,h);
	cans.fillRect(x+690,y,w,h);
	//流程转折
	cans.fillRect(x+690,y+180,w,h);
	cans.fillRect(x+460,y+180,w,h);
	//cans.strokeStyle = '#dd7c09';
	//cans.strokeRect(300,y,w,h);
}
//箭头
function drawline(x,y,w,h){
	var can = $$('can');
    var cans = can.getContext('2d');
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(x+w,107);
	cans.lineTo(x+w,133);
	cans.lineTo(x+w+27,120);
	cans.fill();
	cans.fillRect( x,y,w,h );
	cans.closePath();
	
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(x+230+w,107);
	cans.lineTo(x+230+w,133);
	cans.lineTo(x+230+w+27,120);
	cans.fill();
	cans.fillRect( x+230,y,w,h );
	cans.closePath();
	
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(x+460+w,107);
	cans.lineTo(x+460+w,133);
	cans.lineTo(x+460+w+27,120);
	cans.fill();
	cans.fillRect( x+460,y,w,h );
	cans.closePath();
	
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(x+690+w,107);
	cans.lineTo(x+690+w,133);
	cans.lineTo(x+690+w+27,120);
	cans.fill();
	cans.fillRect( x+690,y,w,h );
	cans.closePath();

	//流程转折,向下箭头 
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(986,247);
	cans.lineTo(1011,247);
	cans.lineTo(999,273);
	cans.fill();
	cans.fillRect( 992,147,15,100 );
	cans.closePath();	
	
	//反向箭头
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(x+690+w-38,107+180);
	cans.lineTo(x+690+w-38,133+180);
	cans.lineTo(x+690+w-65,120+180);
	cans.fill();
	cans.fillRect( x+690+27,y+180,w,h );
	cans.closePath();
	
	
	cans.beginPath();
	cans.fillStyle="#d7d7d7";
	cans.moveTo(x+460+w-38,107+180);
	cans.lineTo(x+460+w-38,133+180);
	cans.lineTo(x+460+w-65,120+180);
	cans.fill();
	cans.fillRect( x+460+27,y+180,w,h );
	cans.closePath();
	
		
}
//文字
function drawtext(x,y){
	var can = $$('can');
    var cans = can.getContext('2d');
	cans.fillStyle = "#ffffff";
	cans.font ="bold 20px 微软雅黑";
	cans.fillText(" 开 始",70,125);
	cans.fillText("结 束",540,125+185);
	cans.fillText(" ① 起 草",x,y);
	cans.fillText(" ② 审 核",x+230,y);
	cans.fillText(" ③ 会 签",x+460,y);
	cans.fillText(" ④ 签 发",x+690,y);
	cans.fillText(" ⑤ 成 文",x+690,y+180);
	cans.fillText(" ⑥ 发 送",x+460,y+180);
	
}