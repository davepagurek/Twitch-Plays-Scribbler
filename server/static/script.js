var socket = io();

window.addEventListener("load", function() {
	var log = document.getElementById("log");
	var maxChats = 100;

	var sendMessage = function() {
		socket.emit('command', document.getElementById("message").value);
		document.getElementById("message").value="";
	}

	document.getElementById("send").addEventListener("click", sendMessage);
	document.getElementById("message").addEventListener("keyup", function(evt) {
		if (evt.keyCode == 13) {
			sendMessage();
		}
	});
	socket.on('command', function(msg) {
		var m = document.createElement("div");
		m.className="message";

		var t = document.createElement("div");
		t.className = "text";
		t.innerHTML = msg;
		

		var u = document.createElement("div");
		u.className="user";
		u.innerHTML = "Steven";

		m.appendChild(u);
		m.appendChild(t);

		while (log.childNodes.length>maxChats) {
			log.removeChild(log.firstChild);
		}

		log.appendChild(m);
		log.scrollTop = log.scrollHeight;
	});
});