// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    var m = angular.module('AngularAgora', ['ngResource']); 
    m.config(function($interpolateProvider) { $interpolateProvider.startSymbol('{='); $interpolateProvider.endSymbol('=}'); });

    m.factory('Vote', function ($resource) {
        return $resource('/api/v1/vote/?decision=:decisionId&format=json', {}, {
            'save': {method:'PUT'}
        });
    });

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

function VoteListCtrl($scope, $location, Vote) {
  $scope.votes = Vote.get({decisionId:1});
}
