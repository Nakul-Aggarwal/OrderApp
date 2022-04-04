function CallWaiter(tableNumber) {
    $.ajax({
        type: 'GET',
        url: 'http://' + window.location.host + '/order/waiter/',
        data: {
            tableNumber: tableNumber
        },
    })
}

function diablePlaceOrder() {
  if (diablePlaceOrderCount == 0) {
    document.getElementById("orderButton").disabled = true;
  }
}

function functionMinus(id) {
    var quantity = $(`span.${id}`)[0];
    let value = quantity.innerText - 1;
    quantity = +quantity.innerText;
    if (value < 1) {
        $(`span.${id}`)[0].innerText = 0;
        value = 0;
        $(`section.${id}`)[0].style.display = "none";
        diablePlaceOrderCount--;
        diablePlaceOrder();
    } else {
        $(`span.${id}`)[0].innerText = value;
    }
    changePrice(id, value, quantity);
    updateCartStorage(id);
}

function functionPlus(id) {
    var quantity = $(`span.${id}`)[0];
    let value = parseInt(quantity.innerText) + 1;
    quantity = +quantity.innerText;
    $(`span.${id}`)[0].innerText = value;
    changePrice(id, value, quantity);
    updateCartStorage(id);
}

function changePrice(id, value, quantity) {
    var price = +$(`p.price${id}`)[0].getAttribute('data-id');
    var grandtotal = +$(`p.grandtotal`)[0].getAttribute('data-id');
    var pricePerItem = price / quantity;
    pricePerItem = pricePerItem * value;
    pricePerItem = parseFloat(pricePerItem).toFixed(2);
    $(`p.price${id}`)[0].innerText = "€ " + pricePerItem;
    $(`p.price${id}`)[0].setAttribute('data-id', pricePerItem);
    grandtotal = parseFloat(grandtotal - price).toFixed(2);
    grandtotal = parseFloat(grandtotal) + parseFloat(pricePerItem);
    grandtotal = parseFloat(grandtotal).toFixed(2);
    $(`p.grandtotal`)[0].innerText = "€ " + grandtotal;
    $(`p.grandtotal`)[0].setAttribute('data-id', grandtotal);
}

async function addMoreItems(tableNumber) {
    let order = createOrder();
    console.log(order);
    let starters = $(`input.starters`)[0].checked;
    let url = '/order/updateCart';
    await $.ajax({
        type: 'GET',
        url: url,
        data: {
            order: order,
            starters: starters,
            tableNumber: tableNumber
        },
        success: function(response) {
            console.log(response);
            window.location.href = addMoreItems_url;
        }
    });
}

async function OrderList(tableNumber) {
    let order = createOrder();
    let starters = $(`input.starters`)[0].checked;
    let url = '/order/updateCart';
    await $.ajax({
        type: 'GET',
        url: url,
        data: {
            order: order,
            starters: starters,
            tableNumber: tableNumber
        },
        success: function(response) {
            console.log(response);
            window.location.href = order_url;
        }
    });
}

async function Order(tableNumber) {
    let order = createOrder();
    let starters = $(`input.starters`)[0].checked;
    let url = '/order/updateCart';
    await $.ajax({
        type: 'GET',
        url: url,
        data: {
            order: order,
            starters: starters,
            tableNumber: tableNumber
        },
        success: function(response) {
            console.log(response);
            window.location.href = cart_url;
        }
    });
}


async function placeOrder(tableNumber) {
    let order = createOrder();
    let starters = $(`input.starters`)[0].checked;
    let url = '/order/updateCart';
    await $.ajax({
        type: 'GET',
        url: url,
        data: {
            order: order,
            starters: starters,
            tableNumber: tableNumber
        },
        success: function(response) {
            sessionStorage.clear();
            window.location.href = success_url;
        }
    });
}

function createOrder() {
    let items = document.querySelectorAll("section");
    let i;
    var order = {};
    if (itemsCount) {
      for (i = 1; i < items.length - 1; i++) {
          var id = items[i].getAttribute('data-id');
          var quantity = +$(`span.${id}`)[0].innerText;
          var inst = $(`input.${id}`)[0].value;
          temp = [quantity, inst]
          order[id] = JSON.stringify(temp);
      }
    }
    return order;
}

function updateCartStorage(id) {
    var quantity = $(`span.${id}`)[0];
    var itemID = quantity.getAttribute('data-id');
    quantity = parseInt(quantity.innerText);
    var spice = $(`p.${id}`)[0];
    var option2 = $(`p.option2${id}`)[0];
    var addOn = $(`p.addOn${id}`)[0];
    var person = $(`p.person${id}`)[0];

    if (spice) {
        spice = spice.getAttribute('data-id');
    } else {
        spice = false;
    }

    if (person) {
        person = person.getAttribute('data-id');
    } else {
        person = false;
    }

    if (option2) {
        option2 = option2.getAttribute('data-id');
    } else {
        option2 = false;
    }

    if (addOn) {
        addOn = addOn.getAttribute('data-id');
    } else {
        if ($(`span.${id}`)[0].getAttribute('data-addOn') == "True") {
            addOn = 'None';
        } else {
            addOn = false;
        }

    }

    let items = JSON.parse(sessionStorage.getItem(itemID));
    if (quantity < 1) {
        count = JSON.parse(sessionStorage.getItem('count'));
        count--;
        sessionStorage.setItem('count', JSON.stringify(count));
        if (itemID.split(/(\d+)/)[0] == 'item') {
            if (spice && addOn && option2) {
                delete items[spice][option2][addOn];
                if (Object.keys(items[spice][option2]).length == 0) {
                    delete items[spice][addOn];
                    if (Object.keys(items[spice]).length == 0) {
                        delete items[spice];
                        if (Object.keys(items).length == 0) {
                            sessionStorage.removeItem(itemID);
                            return;
                        } else {
                            sessionStorage.setItem(itemID, JSON.stringify(items));
                        }
                    } else {
                        sessionStorage.setItem(itemID, JSON.stringify(items));
                        return;
                    }
                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else if (spice && addOn) {
                delete items[spice][addOn];
                if (Object.keys(items[spice]).length == 0) {
                    delete items[spice];
                    if (Object.keys(items).length == 0) {
                        sessionStorage.removeItem(itemID);
                        return;
                    } else {
                        sessionStorage.setItem(itemID, JSON.stringify(items));
                        return;
                    }

                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else if (spice && option2) {
                delete items[spice][option2];
                if (Object.keys(items[spice]).length == 0) {
                    delete items[spice];
                    if (Object.keys(items).length == 0) {
                        sessionStorage.removeItem(itemID);
                        return;
                    } else {
                        sessionStorage.setItem(itemID, JSON.stringify(items));
                        return;
                    }

                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else if (option2 && addOn) {
                delete items[option2][addOn];
                if (Object.keys(items[option2]).length == 0) {
                    delete items[option2];
                    if (Object.keys(items).length == 0) {
                        sessionStorage.removeItem(itemID);
                        return;
                    } else {
                        sessionStorage.setItem(itemID, JSON.stringify(items));
                        return;
                    }

                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else if (spice) {
                delete items[spice];
                if (Object.keys(items).length == 0) {
                    sessionStorage.removeItem(itemID);
                    return;
                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else if (addOn) {
                delete items[addOn];
                if (Object.keys(items).length == 0) {
                    sessionStorage.removeItem(itemID);
                    return;
                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else if (option2) {
                delete items[option2];
                if (Object.keys(items).length == 0) {
                    sessionStorage.removeItem(itemID);
                    return;
                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else {
                sessionStorage.removeItem(itemID);
                return;
            }
        } else {
            delete items[spice][person];
            if (Object.keys(items[spice]).length == 0) {
                delete items[spice];
                if (Object.keys(items).length == 0) {
                    sessionStorage.removeItem(itemID);
                    return;
                } else {
                    sessionStorage.setItem(itemID, JSON.stringify(items));
                    return;
                }
            } else {
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            }
        }
    } else {
        if (itemID.split(/(\d+)/)[0] == 'item') {
            if (spice && addOn && option2) {
                items[spice][option2][addOn] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else if (spice && addOn) {
                items[spice][addOn] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else if (spice && option2) {
                items[spice][option2] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else if (option2 && addOn) {
                items[option2][addOn] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else if (spice) {
                items[spice] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else if (addOn) {
                items[addOn] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else if (option2) {
                items[option2] = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            } else {
                items = quantity;
                sessionStorage.setItem(itemID, JSON.stringify(items));
                return;
            }
        } else {
            items[spice][person] = quantity;
            sessionStorage.setItem(itemID, JSON.stringify(items));
            return;
        }
    }
}


//Sticky Navbar Function
window.onscroll = function() { myFunction() };
var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function myFunction() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky");
    }
}

$(".feedback").on("click", function() {
    if ($("#contact").css("display") == "none") {
        $("#contact").css("display", "block");
        $(".feedback").css("margin-bottom", "10px");
    } else {
        $("#contact").css("display", "none");
        $(".feedback").css("margin-bottom", "0px");

    }
});

$(window).on("load", function() {
    $(".preloader-wrapper").fadeOut("slow");
})
