var canvas,ctx;
var vertexes = [];
var diffPt = [];
var autoDiff = 500;
var verNum = 200;
var canvasW = window.innerWidth+100;
var color1="#f4f4f4";
var color2 = "#eee";
var xx = 80;
var dd = 25;
var timer;
 

function resize(){
	canvasW = window.innerWidth + 100;	
	initCanvas(canvasW,window.innerHeight);
	var cW = canvas.width;
	var cH = canvas.height;
	for(var i = 0;i < verNum;i++)
		vertexes[i] = new Vertex(cW / (verNum -1) * i , cH / 2,cH/2);
	initDiffPt();
	var win_3 = window.innerWidth/3;

}
function init(){
	resize();
	
	var FPS =10;
	var interval = 1000 / FPS >> 0;
	timer = setInterval( update, interval );
}

setInterval(function(){
	//clearInterval(timer);
	/*
	dd = Math.random() * 40;
	xx = Math.random() * 350;
	var FPS =10;
	var interval = 1000 / FPS >> 0;
	timer = setInterval( update, interval );
	*/
	mouseX = Math.random() * window.innerWidth;
	autoDiff = 1000;
	xx = 1 + Math.floor((verNum - 2) * mouseX / canvas.width);
	diffPt[xx] = autoDiff;
	
	
}, 4000)
 

function initDiffPt(){
	for(var i=0;i<verNum;i++)
	   diffPt[i]= 0;
}

function update(){
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	autoDiff -= autoDiff*0.9;
	diffPt[xx] = autoDiff;
	 
	//左侧
	//差分，使得每个点都是上一个点的下一次的解，由于差分函数出来的解是一个曲线，且每次迭代后，曲线相加的结果形成了不断地波浪
	for(var i=xx-1;i>0;i--)
		{
		    var d = xx-i;
			if(d > dd)d=dd;
			diffPt[i] -= (diffPt[i]-diffPt[i+1])*(1-0.01*d);
		}
//右侧
	for(var i=xx+1;i<verNum;i++)
		{
		    var d = i-xx;
			if(d > dd)d=dd;
			diffPt[i] -= (diffPt[i]-diffPt[i-1])*(1-0.01*d);
		}
	
	//更新点Y坐标
	for(var i = 0;i < vertexes.length;i++){
		vertexes[i].updateY(diffPt[i]);
	}
	 
	draw();
	
}

function draw(){
	ctx.beginPath();
	ctx.moveTo(0,window.innerHeight);
	ctx.fillStyle=color1;
	ctx.lineTo(vertexes[0].x,vertexes[0].y);
	for(var i = 1;i < vertexes.length;i++){
		ctx.lineTo(vertexes[i].x,vertexes[i].y);
	}
	ctx.lineTo(canvas.width,window.innerHeight);
	ctx.lineTo(0,window.innerHeight);
	ctx.fill();

	ctx.beginPath();
	ctx.moveTo(0,window.innerHeight);
	ctx.fillStyle=color2;
	ctx.lineTo(vertexes[0].x+15,vertexes[0].y+5);
	for(var i = 1;i < vertexes.length;i++){
		ctx.lineTo(vertexes[i].x+15,vertexes[i].y+5);
	}
	ctx.lineTo(canvas.width,window.innerHeight);
	ctx.lineTo(0,window.innerHeight);
	ctx.fill();
	 
}
function initCanvas(width,height){
	canvas = document.getElementById("canvas");
	canvas.width = width;
	canvas.height = 100;
	ctx = canvas.getContext("2d");
}
	
function Vertex(x,y,baseY){
	this.baseY = baseY;
	this.x = x;
	this.y = y;
	this.vy = 0;
	this.targetY = 0;
	this.friction = 0.15;
	this.deceleration = 0.95;
}
	
Vertex.prototype.updateY = function(diffVal){
	this.targetY = diffVal + this.baseY;
	this.vy += this.targetY - this.y
	this.y += this.vy * this.friction;
	this.vy *= this.deceleration;
}
 

init();
