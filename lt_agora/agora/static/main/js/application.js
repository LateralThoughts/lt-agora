$(document).ready(function() {
	$(".vote_action").click(function(event) {
		var jdata = {};
		var e = event.srcElement;
		jdata['decision'] = "/api/v1/decision/" + e.getAttribute("data-ref") + "/";
		jdata['user'] = "/api/v1/user/" + e.getAttribute("data-user") + "/";
		jdata['value'] = e.getAttribute("data-value");
		$.ajax({
		  type: 'POST',
		  url: '/api/v1/vote/',
		  data: JSON.stringify(jdata),
		  success: function(e) { alert("Votre vote a bien été pris en compte."); },
		  error: function(e) { alert("Votre vote n'a pas été pris en compte, une erreur a eu lieu."); },
		  dataType: "json",
		  contentType : "application/json"
		});
	});
});
