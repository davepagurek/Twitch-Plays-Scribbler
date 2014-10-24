var socket = io.connect();

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
    console.log(command);
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

  socket.on('selected', function(command) {
    console.log(command);
		var m = document.createElement("div");
		m.className="message";

		var t = document.createElement("div");
		t.className = "selected";
		t.innerHTML = "Moved " + command.message + " , thanks to " + command.username;

		m.appendChild(t);

		while (log.childNodes.length>maxChats) {
			log.removeChild(log.firstChild);
		}

		log.appendChild(m);
		log.scrollTop = log.scrollHeight;
	});

	//256x192, scaled x3
	var context = document.getElementById("video").getContext("2d");
	socket.on("photo", function(photo) {
    console.log(photo);
		var image = new Image();
		image.src = "data:image/png;base64," + photo;
		image.onload = function() {
      console.log(image);
			context.drawImage(image, 0, 0, 512, 384);
		};
	});
});
