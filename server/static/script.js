var socket = io();

window.addEventListener("load", function() {
	var log = document.getElementById("log");
	var maxChats = 100;

	var sendMessage = function() {
		socket.emit('command', {
			"message": document.getElementById("message").value,
			"username": document.getElementById("username").value
		});
		document.getElementById("message").value="";
	}

	document.getElementById("send").addEventListener("click", sendMessage);
	document.getElementById("message").addEventListener("keyup", function(evt) {
		if (evt.keyCode == 13) {
			sendMessage();
		}
	});
	socket.on('command', function(command) {
		var m = document.createElement("div");
		m.className="message";

		var t = document.createElement("div");
		t.className = "text";
		t.innerHTML = command.message;
		

		var u = document.createElement("div");
		u.className="user";
		u.innerHTML = command.username;

		m.appendChild(u);
		m.appendChild(t);

		while (log.childNodes.length>maxChats) {
			log.removeChild(log.firstChild);
		}

		log.appendChild(m);
		log.scrollTop = log.scrollHeight;
	});

	var tick = 0;
	var context = document.getElementById("video").getContext("2d");
	var updateTimer = setInterval(function() {
		tick++;
		var img = document.createElement("img");
		img.src = "stream.jpg?tick=" + tick;
		img.addEventListener("load", function() {
			context.drawImage(img, 0, 0);
		});
	}, 1000);
});