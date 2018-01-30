function theme(BG,main){
	document.getElementById("demo").style.background-color=BG;
	for(i=0;i<document.getElementsByClassName("header").length-1;i++){
		document.getElementsByClassName("header")[i].style.background-color=BG;}
	for(i=0;i<document.getElementsByTagName("body").length-1;i++){
		document.getElementsByTagName("body")[i].style.color=main;}
	for(i=0;i<document.getElementsByClassName("task_link").length-1;i++){
		document.getElementsByClassName("task_link")[i].style.color=main;}
	document.getElementById("expired_con").style.border-color=main;
}

function check_deadline(year,month,day){
	var today = new Date();
	if (month!=1){
		var deadline = new Date(year,month-1,day,0,0,0,0)
	}
	else{
		var deadline = new Date(year,12,day,0,0,0,0)
	}
	today.getTime();
	if (deadline<today){
		return 1;
	}
}

function change_color(list){
	for(i=0; i<list.length; i++){
		list[i].style.color="red";
	}
}