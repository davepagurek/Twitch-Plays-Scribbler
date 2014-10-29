var socket = io.connect();

window.addEventListener("load", function() {
	var log = document.getElementById("log");
	var maxChats = 100;

  var previous = [];
  var current = 0;

	var getRandUsername = function(){
		var list_A = ["Anonymous","Quirky","Kinky","Funny","Ignorant","Fail","Frustrated","Smart","Active"]
		var list_B = ["Steven","Yu Chen","Andrew","Dave","Alyshan","Ruo Tai","Jacklope",
		"Eleplant","Giraffe","Bravo","Lollipop","KitKat","Jellybean","Dolphin","Whales","Hasselhoff","Voyeur","Beetle","Lion"]

		return list_A[Math.floor((Math.random() * list_A.length) + 1)] + " " + list_B[Math.floor((Math.random() * list_B.length) + 1)];
	};
	//get a spiffy username
	document.getElementById("username").value = getRandUsername();

	var sendMessage = function() {
		socket.emit('command', {
			"message": document.getElementById("message").value.replace(/\n$/, ""),
			"username": document.getElementById("username").value
		});
    previous.push(document.getElementById("message").value.replace(/\n$/, ""));
    while (previous.length>maxChats) {
      previous.shift();
    }
    current = previous.length;
		document.getElementById("message").value="";
	}

	document.getElementById("send").addEventListener("click", sendMessage);
	document.getElementById("message").addEventListener("keyup", function(evt) {
		if (evt.keyCode == 13) {
			sendMessage();
      return false;
		} else if (evt.keyCode == 38 && current-1>=0 && (current<previous.length || document.getElementById("message").value=="")) {
      current--;
      document.getElementById("message").value = previous[current];
    } else if (evt.keyCode == 40 && current+1<=previous.length) {
      current++;
      if (current==previous.length) {
        document.getElementById("message").value = "";
      } else {
        document.getElementById("message").value = previous[current];
      }
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
			context.drawImage(image, 0, 0, 256, 192);
		};
	});
  socket.on("webcam", function(photo) {
    console.log(photo);
		var image = new Image();
		image.src = "data:image/png;base64," + photo;
		image.onload = function() {
			context.drawImage(image, 256, 0, 256, 192);
		};
	});
});
