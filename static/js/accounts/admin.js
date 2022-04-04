const ws = new WebSocket(
			'ws://'
			+ window.location.host
			+ '/ws/chat/'
		)

ws.onopen = function(event) {
	console.log("Connection is opened");
}
ws.onclose = function(event) {
	console.log("Connection is closed");
}
ws.onmessage = function(event) {
	console.log(event);
	console.log("Message is received");
	received_message = JSON.parse(event['data']);
	console.log(received_message);
	addNotification(received_message);
}
ws.onerror = function(event) {
	console.log("error occured");
}

count = 0;

function moveToInactive(id) {
  table = document.getElementById(id);
  inactive = document.getElementsByClassName("inactivetables")[0];
  row = inactive.querySelectorAll(".rowInactive")[0];
  row.appendChild(table);
  checkEmpty();
}

function moveToActive(id) {
  table = document.getElementById(id);
  active = document.getElementsByClassName("activetables")[0];
  row = active.querySelectorAll(".rowActive")[0];
  row.appendChild(table);
  checkEmpty();
}

function checkEmpty() {
  inactive = document.getElementsByClassName("inactivetables")[0];
  active = document.getElementsByClassName("activetables")[0];
  rowInactive = inactive.querySelectorAll(".rowInactive")[0];
  rowActive = active.querySelectorAll(".rowActive")[0];
  if (rowActive.childElementCount < 1) {
    rowActive.parentElement.querySelectorAll(".no-active-text")[0].style.display = "block";
  } else {
    rowActive.parentElement.querySelectorAll(".no-active-text")[0].style.display = "none";
  }

  if (rowInactive.childElementCount < 1) {
    rowInactive.parentElement.querySelectorAll(".no-active-text")[0].style.display = "block";
  } else {
    rowInactive.parentElement.querySelectorAll(".no-active-text")[0].style.display = "none";
  }
}

var removeNotification = function(){
  notification = this.parentElement.parentElement.parentElement;
  count--;
  document.getElementById("counter").innerText = String(count);
  var number = parseInt(this.getAttribute('data-number'));
  console.log(number);
  var id = this.getAttribute('data-id');
  var dataType = this.getAttribute('data-type');
  if (dataType == 'Inactive') {
    tableCount[number] = tableCount[number]-1;
    if (tableCount[number] == 0) {
      ws.send(JSON.stringify({ 'type':dataType, 'tableNumber': number }))
      moveToInactive(id);
    }
  }
  notification.style.opacity = '0';
  setTimeout(function(){notification.parentNode.removeChild(notification);}, 900);
};

var buttons = document.getElementsByClassName("green");
for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('click', removeNotification);
}

checkEmpty()

function addNotification(received_message) {

	if (received_message['type'] == 'move_to_inactive') {
		var tableNumber = received_message["tableNumber"];
		moveToInactive("Table"+tableNumber);
		return;
	}

	if (received_message['type'] == 'move_to_active') {
		var tableNumber = received_message["tableNumber"]
		moveToActive("Table"+tableNumber)
		return;
	}
      var tableNumber = received_message["tableNumber"];
      var dataType = received_message["type"];
      var section = document.createElement("section");
      section.classList.add("notification");
      var row = document.createElement("div");
      row.classList.add("row");
      var col = document.createElement("col");
      col.classList.add("col-xs-12");
      row.appendChild(col);
      section.appendChild(row);
			console.log(received_message)

    	if (received_message.hasOwnProperty("message")) {
        var p = document.createElement("p");
        p.classList.add("message");
        var textNode = document.createTextNode(received_message["message"]);
        p.appendChild(textNode);
        col.appendChild(p);
    	}

			else {
				let message = document.createElement("p");
        message.classList.add("message");
				var textNode = document.createTextNode("Table Number " + received_message["tableNumber"] + " has placed an Order");
				message.appendChild(textNode);
				col.appendChild(message);

				for (const property in received_message["order_placed"]) {
					item = received_message["order_placed"][property];
					var txt = '';
					if (item['article_number']) {
            txt = item['article_number'] + ". " + item['name'];
					} else {
            txt = item['name']
					}
					var name = document.createElement("p");
          name.classList.add('item');
          name.appendChild(document.createTextNode(txt));
          quantity = document.createElement("span");
          quantity.classList.add('foodquan');
          quantity.appendChild(document.createTextNode(item['quantity']));
          name.appendChild(quantity);
          col.appendChild(name);

					if (item['person']) {
						txt = "(for " + item['person'] + " person)";
						let person = document.createElement("span");
            person.classList.add("float-left");
						person.appendChild(document.createTextNode(txt));
						name.appendChild(document.createElement("br"));
						name.appendChild(person);
					}
					if (item['option1']) {
						txt = "(" + item['option1'] + ")";
						let spice = document.createElement("span");
						spice.classList.add("float-left");
						spice.appendChild(document.createTextNode(txt));
						name.appendChild(document.createElement("br"));
						name.appendChild(spice);
          }
          if (item['option2']) {
            txt = "(" + item['option2'] + ")";
            let spice = document.createElement("span");
            spice.classList.add("float-left");
            spice.appendChild(document.createTextNode(txt));
            name.appendChild(document.createElement("br"));
            name.appendChild(spice);
          }
					if (item['addOn']) {
						txt = "(" + item['addOn'] + ")";
						let addOn = document.createElement("span");
						addOn.classList.add("float-left");
						addOn.appendChild(document.createTextNode(txt));
						name.appendChild(document.createElement("br"));
						name.appendChild(addOn);
					}
					if (item['description']) {
						txt = "(" + item['description'] + ")";
						let description = document.createElement("span");
						description.classList.add("float-left");
						description.appendChild(document.createTextNode(txt));
						name.appendChild(document.createElement("br"));
						name.appendChild(description);
					}
				}
			}
      let a = document.createElement("a");
      a.classList.add("green");
      a.appendChild(document.createTextNode("Mark as Done"));
      a.setAttribute('data-number',tableNumber);
      a.setAttribute('data-type', dataType);
      a.setAttribute('data-id',"Table"+tableNumber);
      a.addEventListener('click', removeNotification);
      col.appendChild(a);
      time = document.createElement("p");
      time.classList.add("time");
      time.appendChild(document.createTextNode(received_message['time']));
      col.appendChild(time);
      document.getElementById("notification").prepend(section);
      if (dataType == 'Active') {
        if (tableCount[tableNumber] == 0) {
          moveToActive("Table"+tableNumber);
        }
        tableCount[tableNumber] = tableCount[tableNumber] + 1;
      }
      count++;
      document.getElementById("counter").innerText = String(count);
		}
