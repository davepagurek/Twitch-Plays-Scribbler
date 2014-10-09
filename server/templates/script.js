window.addEventListener("load", function() {
	var log = document.getElementById("log");
	var maxChats = 100;

	var addMessage = function() {
		var m = document.createElement("div");
		m.className="message";

		var t = document.createElement("div");
		t.className = "text";
		t.innerHTML = document.getElementById("message").value;
		document.getElementById("message").value="";

		var u = document.createElement("div");
		u.className="user";
		u.innerHTML = document.getElementById("username").value;

		m.appendChild(u);
		m.appendChild(t);

		while (log.childNodes.length>maxChats) {
			log.removeChild(log.firstChild);
		}

		log.appendChild(m);
		log.scrollTop = log.scrollHeight;
	};

	document.getElementById("send").addEventListener("click", addMessage);
	document.getElementById("message").addEventListener("keyup", function(evt) {
		if (evt.keyCode == 13) {
			addMessage();
		}
	});
})