var dome=document.getElementById("dome");
var dome1=document.getElementById("dome1");
var dome2=document.getElementById("dome2");
var speed=50;//设置向上轮动的速度
dome2.innerHTML=dome1.innerHTML;//复制节点
function moveTop(){
    if(dome1.offsetHeight-dome.scrollTop<=0){
        dome.scrollTop=0;
    }else{
        dome.scrollTop++;
    }
}
var myFunction=setInterval("moveTop()",speed);
dome.onmouseover=function(){
    clearInterval(myFunction);
}
dome.onmouseout=function(){
    myFunction=setInterval(moveTop,speed);
}