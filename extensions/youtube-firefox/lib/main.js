// Based on:
// http://greasefire.userscripts.org/scripts/review/101305 (by Frz)
// http://userscripts.org/scripts/show/92945 (by deepseth)
// http://userscripts.org/scripts/show/62064 (by Wolph)

/*
  XBMC.RunPlugin(%s?path=%s&action=play_all&playlist=%s&) <- afspil playlist
  XBMC.RunPlugin(%s?path=%s&action=play_all&shuffle=true&playlist=%s&) <- shuffle playlist
  XBMC.RunPlugin(%s?path=%s&action=play_all&playlist=%s&videoid=%s&) <- start playlist at videoid
  du skal kalde det der svare til run plugin dog
*/
var pageMod = require("page-mod"); 
var self = require("self"); 
//var request = require("request");
var Request = require('request').Request;
const xhr = require("api-utils/xhr");

exports.main = function() { 
    pageMod.PageMod({ 
        include: "*", 
        contentScriptWhen: 'ready', 
        contentScriptFile: [self.data.url('script.js')],
        onAttach: function onAttach(worker) { 
            worker.on('message', function(message) { 
		switch(message.kind) {
		case "GM_xmlhttpRequest":
		    details = message.details;
		    console.log("A: " + JSON.stringify(details));
		    /*
		    Request({
			url: details.url,
			headers: {'Content-type': 'application/json'},
			content: details.Data,
			onComplete: function (response) {
			    console.log("B: " + JSON.stringify(response.text));
			}
		    }).post();
		    */
		    
		    //var xmlhttp = new XMLHttpRequest();
		    var xmlhttp = new xhr.XMLHttpRequest();
		    xmlhttp.onreadystatechange = function() {
			var responseState = {
			    responseXML:(xmlhttp.readyState==4 ? xmlhttp.responseXML : ''),
			    responseText:(xmlhttp.readyState==4 ? xmlhttp.responseText : ''),
			    readyState:xmlhttp.readyState,
			    responseHeaders:(xmlhttp.readyState==4 ? xmlhttp.getAllResponseHeaders() : ''),
			    status:(xmlhttp.readyState==4 ? xmlhttp.status : 0),
			    statusText:(xmlhttp.readyState==4 ? xmlhttp.statusText : '')
			}
			if (details["onreadystatechange"]) {
			    details["onreadystatechange"](responseState);
			}
			if (xmlhttp.readyState==4) {
			    console.log("onload: " + JSON.stringify(responseState));
			    if (details["onload"] && xmlhttp.status>=200 && xmlhttp.status<300) {
				details["onload"](responseState);
			    }
			    if (details["onerror"] && (xmlhttp.status<200 || xmlhttp.status>=300)) {
			    details["onerror"](responseState);
			    }
			}
		    }
		    try {
			xmlhttp.open(details.method, details.url);
		    } catch(e) {
			if( details["onerror"] ) {
			    details["onerror"]({responseXML:'',responseText:'',readyState:4,responseHeaders:'',status:403,statusText:'Forbidden'});
			}
			return;
		    }
		    if (details.headers) {
			for (var prop in details.headers) {
			    xmlhttp.setRequestHeader(prop, details.headers[prop]);
			}
		    }
		    xmlhttp.send((typeof(details.data)!='undefined')?details.data:null);
		    console.log((typeof(details.data)!='undefined')?details.data:null);
		    break;
		default:
                    console.log(message.message); 
		    break;
		    
		}
	    });
        } 
    }); 
} 

