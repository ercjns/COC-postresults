// OutilsJs.js

function toggleTeamDetails(id){
  var cclass = document.getElementById(id);
  var rows = cclass.getElementsByClassName("tmember");
  for (i=0; i<rows.length; i++) {
	rows[i].style.display = (rows[i].style.display == "none" ? "" : "none");
	}
}
