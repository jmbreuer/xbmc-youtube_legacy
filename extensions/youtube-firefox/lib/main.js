var self = require("self"); 

var pageMod = require("page-mod"); 
var self = require("self"); 
var tabs = require("tabs"); 
var Request = require('request').Request;
const xhr = require("api-utils/xhr");
var ss = require("simple-storage");
var xbmc_path = "plugin.video.youtube";
var xbmc_url = false;
var xbmc_host = false;

if (ss.storage.xbmc_host) {
    xbmc_host = ss.storage.xbmc_host;
    xbmc_url = 'http://' + xbmc_host + '/jsonrpc';
} else {
    openSettings();
}

if (ss.storage.xbmc_path) {
    xbmc_path = ss.storage.xbmc_path;
}

if (ss.storage.xbmc_autoplay) {
    xbmc_autoplay = ss.storage.xbmc_autoplay;
} else {
    xbmc_autoplay = false
}

function openSettings() {
    const data = require("self").data;
    var tabs = require("tabs");

    tabs.on('ready', function(tab) {
	console.log("Title: " + tab.title);
	if ( tab.title == "YouTube XBMC Extension" ) {
	    worker = tab.attach({
		contentScriptWhen : 'ready',
		contentScriptFile: [self.data.url("options.js")]
	    });
            worker.on('message', function(message) {
		console.log("tabs.worker.on: " + JSON.stringify(message));
		switch(message.type) {
		case "settings":
		    console.log("settings");
		    details = "Settings";
		    console.log("settings to return: " + JSON.stringify([xbmc_path, xbmc_url, xbmc_host, xbmc_autoplay]));
		    return [xbmc_path, xbmc_url, xbmc_host, xbmc_autoplay];
		    break;
		case "open_settings":
		    openSettings();
		    break;
		case "load_settings":
		    console.log("load_settings");
		    var settings = [ xbmc_path, xbmc_url, xbmc_host, xbmc_autoplay];
		    console.log("settings to return: " + JSON.stringify(settings));
		    worker.postMessage(settings);
		    break;
		case "save_settings":
		    console.log("save_settings");
		    ss.storage.xbmc_path = message.details[0];
		    xbmc_path = message.details[0];
		    ss.storage.xbmc_host = message.details[1];
		    xbmc_host = message.details[1];
		    ss.storage.xbmc_autoplay = message.details[2];
		    xbmc_autoplay = message.details[2];
		    xbmc_url = 'http://' + xbmc_host + '/jsonrpc';
		    console.log("settings saved: " + JSON.stringify([xbmc_path, xbmc_url, xbmc_host, xbmc_autoplay]));
		    break;
		}
	    });
	}
    });

    tabs.open({
        url : self.data.url("options.html")
    });
}

exports.main = function() { 
    pageMod.PageMod({ 
        include: "*", 
        contentScriptWhen: 'ready', 
        contentScriptFile: [self.data.url('script.js')],
        onAttach: function onAttach(worker) { 
            worker.on('message', function(message) {
		console.log("worker.on: " + JSON.stringify(message));
		switch(message.type) {
		case "open_settings":
		    openSettings();
		    break;
		case "load_settings":
		    console.log("load_settings");
		    var settings = [ xbmc_path, xbmc_url, xbmc_host, xbmc_autoplay];
		    console.log("settings to return: " + JSON.stringify(settings));
		    worker.postMessage(settings);
		    break;
		case "httpRequest":
		    details = message.details;
		    console.log("httpRequest: " + JSON.stringify(details));

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
			console.log("ERROR: " + JSON.stringify(e))
			if ( typeof(details) != "undefined") {
			    if( details["onerror"] ) {
				details["onerror"]({responseXML:'',responseText:'',readyState:4,responseHeaders:'',status:403,statusText:'Forbidden'});
			    }
			}
			return;
		    }
		    if (details.headers) {
			for (var prop in details.headers) {
			    xmlhttp.setRequestHeader(prop, details.headers[prop]);
			}
		    }
		    xmlhttp.send((typeof(details.data)!='undefined')?details.data:null);
		    console.log("Did send: " + ((typeof(details.data)!='undefined')?details.data:null));
		    break;
		default:
                    console.log("default: " + message.message); 
		    break;
		    
		}
	    });
        } 
    }); 
} 

