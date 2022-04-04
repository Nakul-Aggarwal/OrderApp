function buttonDisable(row) {
  button = row.querySelector(".addToCart");
  if (button) {
  button.disabled = false;
  selects = row.querySelectorAll(".select");
  for (var i=0; i<selects.length; i++) {
    if (selects[i].value == "None") {
      row.querySelector(".addToCart").disabled = true;
    }
  }
}
}


var rows = document.getElementsByClassName("item");
for (var i=0; i<rows.length; i++) {
  buttonDisable(rows[i]);
}

function buttonDisableOnClick(id) {
  txt = "div."+id;
  row = document.querySelector(txt);
  buttonDisable(row);
}

function functionMinus(id) {
        var quantity = $(`span.${id}`)[0];
        let value = quantity.innerText - 1;
        if (value<1){
          quantity.innerText = 1;

        } else{
          quantity.innerText = value;
        }
      }

function functionPlus(id) {
        var quantity = $(`span.${id}`)[0];
        let value = parseInt(quantity.innerText) + 1;
        quantity.innerText = value;
}

function CallWaiter(tableNumber) {
  $.ajax({
    type: 'GET',
    url: 'http://' + window.location.host + '/order/waiter/',
    data:{
      tableNumber: tableNumber
    },
  })

}


var count = JSON.parse(sessionStorage.getItem('count'));
if (!count) {
  count = 0;
} else {
  animateAddToCart()
}

function animateAddToCart() {
  //event.preventDefault();
  $('#counter').removeClass('animation-counter');
  $('#counter').width();
  document.getElementById("counter").innerText = String(count);
  setTimeout(function() {
  $('#counter').addClass('animation-counter');
  }, false);
}

function addSingleToCart(id) {
  let quantity = 1;
  let spice = $(`select.${id}`)[0];
  let addOn = $(`select.addon${id}`)[0];
  let option2 = $(`select.option2${id}`)[0];
  let items = JSON.parse(sessionStorage.getItem(id));


  if (typeof (spice) != 'undefined' && spice != 'null') {
    spice = spice.value;
    $(`select.${id}`)[0].value = "None";
  } else {
    spice = "None";
  }

  if (typeof (addOn) != 'undefined' && addOn != 'null') {
    addOn = addOn.value;
    $(`select.addon${id}`)[0].value = "None";
  }

  if (typeof (option2) != 'undefined' && option2 != 'null') {
    option2 = option2.value;
    $(`select.option2${id}`)[0].value = "None";
  } else {
    option2 = "None";
  }

  if (items) {
    if (spice != "None" && option2 != "None" && addOn) {
      if (Object.keys(items).includes(spice)) {
        if (Object.keys(items[spice]).includes(option2)) {
          if (Object.keys(items[spice][option2]).includes(addOn)) {
            items[spice][option2][addOn] += quantity;
          } else {
            items[spice][option2][addOn] = quantity;
            count++;
          }
        } else {
          items[spice][option2] = { [addOn] : quantity };
          count++;
        }
      } else {
        items[spice] = { [option2] : { [addOn] : quantity } };
        count++;
      }
    } else if (spice != "None" && option2 != "None") {
      if (Object.keys(items).includes(spice)) {
        if (Object.keys(items[spice]).includes(option2)) {
          items[spice][option2] += quantity;
        } else {
          items[spice][option2] = quantity;
          count++;
        }
      } else {
        items[spice] = { [option2] : quantity };
        count++;
      }
    } else if (spice != "None" && addOn) {
      if (Object.keys(items).includes(spice)) {
        if (Object.keys(items[spice]).includes(addOn)) {
          items[spice][addOn] += quantity;
        } else {
          items[spice][addOn] = quantity;
          count++;
        }
      } else {
        items[spice] = { [addOn] : quantity };
        count++;
      }
    } else if (option2 != "None" && addOn) {
      if (Object.keys(items).includes(option2)) {
        if (Object.keys(items[option2]).includes(addOn)) {
          items[option2][addOn] += quantity;
        } else {
          items[option2][addOn] = quantity;
          count++;
        }
      } else {
        items[spice] = { [addOn] : quantity };
        count++;
      }
    } else if (spice != "None") {
      if (Object.keys(items).includes(spice)) {
        items[spice] += quantity;
      } else {
        items[spice] = quantity;
        count++;
      }
    } else if (option2 != "None") {
      if (Object.keys(items).includes(option2)) {
        items[option2] += quantity;
      } else {
        items[option2] = quantity;
        count++;
      }
    } else if (addOn) {
      if (Object.keys(items).includes(addOn)) {
        items[addOn] += quantity;
      } else {
        items[addOn] = quantity;
        count++;
      }
    } else {
      items += quantity;
    }
    animateAddToCart()
  } else {
    if (spice != "None" && option2 != "None" && addOn) {
      items = { [spice] : { [option2] : { [addOn] : quantity } } };
    } else if (spice != "None" && option2 != "None") {
      items = { [spice] : { [option2] : quantity } };
    } else if (spice != "None" && addOn) {
      items = { [spice] : { [addOn] : quantity } };
    } else if (option2 != "None" && addOn) {
      items = { [option2] : { [addOn] : quantity } };
    } else if (spice != "None") {
      items = { [spice] : quantity };
    } else if (option2 != "None") {
      items = { [option2] : quantity };
    } else if (addOn) {
      items = { [addOn] : quantity };
    } else {
      items = quantity;
    }
    count++;
    animateAddToCart();
  }
  sessionStorage.setItem(id, JSON.stringify(items));

}
function addToCart(id) {

    // check if request is from menu or item
    if (id.split(/(\d+)/)[0] == 'item') { //if item is added
        let quantity = +$(`span.${id}`)[0].innerText;
        $(`span.${id}`)[0].innerText = 1;
        let spice = $(`select.${id}`)[0];
        let addOn = $(`select.addon${id}`)[0];
        let option2 = $(`select.option2${id}`)[0];
        let items = JSON.parse(sessionStorage.getItem(id));


        if (typeof (spice) != 'undefined' && spice != 'null') {
          spice = spice.value;
          $(`select.${id}`)[0].value = "None";
        } else {
          spice = "None";
        }

        if (typeof (addOn) != 'undefined' && addOn != 'null') {
          addOn = addOn.value;
          $(`select.addon${id}`)[0].value = "None";
        }

        if (typeof (option2) != 'undefined' && option2 != 'null') {
          option2 = option2.value;
          $(`select.option2${id}`)[0].value = "None";
        } else {
          option2 = "None";
        }

        if (items) {
          if (spice != "None" && option2 != "None" && addOn) {
            if (Object.keys(items).includes(spice)) {
              if (Object.keys(items[spice]).includes(option2)) {
                if (Object.keys(items[spice][option2]).includes(addOn)) {
                  items[spice][option2][addOn] += quantity;
                } else {
                  items[spice][option2][addOn] = quantity;
                  count++;
                }
              } else {
                items[spice][option2] = { [addOn] : quantity };
                count++;
              }
            } else {
              items[spice] = { [option2] : { [addOn] : quantity } };
              count++;
            }
          } else if (spice != "None" && option2 != "None") {
            if (Object.keys(items).includes(spice)) {
              if (Object.keys(items[spice]).includes(option2)) {
                items[spice][option2] += quantity;
              } else {
                items[spice][option2] = quantity;
                count++;
              }
            } else {
              items[spice] = { [option2] : quantity };
              count++;
            }
          } else if (spice != "None" && addOn) {
            if (Object.keys(items).includes(spice)) {
              if (Object.keys(items[spice]).includes(addOn)) {
                items[spice][addOn] += quantity;
              } else {
                items[spice][addOn] = quantity;
                count++;
              }
            } else {
              items[spice] = { [addOn] : quantity };
              count++;
            }
          } else if (option2 != "None" && addOn) {
            if (Object.keys(items).includes(option2)) {
              if (Object.keys(items[option2]).includes(addOn)) {
                items[option2][addOn] += quantity;
              } else {
                items[option2][addOn] = quantity;
                count++;
              }
            } else {
              items[spice] = { [addOn] : quantity };
              count++;
            }
          } else if (spice != "None") {
            if (Object.keys(items).includes(spice)) {
              items[spice] += quantity;
            } else {
              items[spice] = quantity;
              count++;
            }
          } else if (option2 != "None") {
            if (Object.keys(items).includes(option2)) {
              items[option2] += quantity;
            } else {
              items[option2] = quantity;
              count++;
            }
          } else if (addOn) {
            if (Object.keys(items).includes(addOn)) {
              items[addOn] += quantity;
            } else {
              items[addOn] = quantity;
              count++;
            }
          } else {
            items += quantity;
          }
          animateAddToCart()
        } else {
          if (spice != "None" && option2 != "None" && addOn) {
            items = { [spice] : { [option2] : { [addOn] : quantity } } };
          } else if (spice != "None" && option2 != "None") {
            items = { [spice] : { [option2] : quantity } };
          } else if (spice != "None" && addOn) {
            items = { [spice] : { [addOn] : quantity } };
          } else if (option2 != "None" && addOn) {
            items = { [option2] : { [addOn] : quantity } };
          } else if (spice != "None") {
            items = { [spice] : quantity };
          } else if (option2 != "None") {
            items = { [option2] : quantity };
          } else if (addOn) {
            items = { [addOn] : quantity };
          } else {
            items = quantity;
          }
          count++;
          animateAddToCart();
        }
        sessionStorage.setItem(id, JSON.stringify(items));

    } else { //if menu is added

        let quantity = +$(`select.quantity${id}`)[0].value;
        $(`select.quantity${id}`)[0].value = 'None';
        let spice = $(`select.${id}`)[0].value;
        $(`select.${id}`)[0].value = "None";
        let items = JSON.parse(sessionStorage.getItem(id));

        if (items) { //menu already exist
            if (Object.keys(items).includes(spice)) { //same spice exist, update quantity
                if (quantity > 0) {
                    if (items[spice][quantity]){
                      items[spice][quantity] += 1;
                    } else {
                      items[spice][quantity] = 1;
                      count++;
                    }
                    animateAddToCart();
                    sessionStorage.setItem(id, JSON.stringify(items));

                }
            } else { // same spice does not exist
                if (quantity > 0) {
                    items[spice] = { [quantity] : 1 };
                    count++;
                    sessionStorage.setItem(id, JSON.stringify(items));
                    animateAddToCart();
                }
            }
        } else { // create new menu in storage
            if (quantity > 0) {
                items = {
                    [spice]: { [quantity] : 1 }
                };
                sessionStorage.setItem(id, JSON.stringify(items));
                count++;
                animateAddToCart();
            }
        }

    }
    sessionStorage.setItem('count',JSON.stringify(count));
    buttonDisableOnClick(id);
}

// Place order button function
async function placeOrder(tableNumber){
  var order = {};
  let url = '/order/placeOrder'
  sessionStorage.removeItem('count');
  Object.keys(sessionStorage).forEach(function(key){
    order[key] = sessionStorage.getItem(key);
  });
  console.log(order)
  var token = '{{ csrf_token }}'
  await $.ajax({
    headers: { "X-CSRFToken": token },
    type: 'GET',
    url: url,
    data:{
      order: order,
      tableNumber: tableNumber
    },
    success: function(response){
      console.log(response)
      console.log("success function is working")
      sessionStorage.setItem('count',JSON.stringify(count));
      // sessionStorage.clear();
      window.location.href = success_url;
    }
  });
  sessionStorage.setItem('count',JSON.stringify(count));
  // sessionStorage.clear();
  window.location.href = success_url;
}


// Place order button function
async function Order(tableNumber){
  var order = {};
  let url = '/order/placeOrder'
  sessionStorage.removeItem('count');
  Object.keys(sessionStorage).forEach(function(key){
    order[key] = sessionStorage.getItem(key);
  });
  console.log(order)
  var token = '{{ csrf_token }}'
  await $.ajax({
    headers: { "X-CSRFToken": token },
    type: 'GET',
    url: url,
    data:{
      order: order,
      tableNumber: tableNumber
    },
    success: function(response){
      console.log(response)
      console.log("success function is working")
      sessionStorage.setItem('count',JSON.stringify(count));
      // sessionStorage.clear();
      window.location.href = order_url;
    }
  });
  sessionStorage.setItem('count',JSON.stringify(count));
  // sessionStorage.clear();
  window.location.href = order_url;
}

var slideIndex = 0;
showSlides();

function showSlides() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 2000); // Change image every 2 seconds
}

var _img = document.getElementById('id1');
var newImg = new Image;
newImg.onload = function() {
    _img.src = this.src;
}
newImg.src = slideImage1;

var _img1 = document.getElementById('id2');
var newImg1 = new Image;
newImg1.onload = function() {
    _img1.src = this.src;
}
newImg1.src = slideImage2;


var _img2 = document.getElementById('id3');
var newImg2 = new Image;
newImg2.onload = function() {
    _img2.src = this.src;
}
newImg2.src = slideImage3;

//Sticky Navbar Function
        window.onscroll = function() {myFunction()};
        var navbar = document.getElementById("navbar");
        var searchbr = document.getElementById("search51")
        var sticky = navbar.offsetTop;
        function myFunction() {
            if (window.pageYOffset >= sticky) {
                navbar.classList.add("sticky")
            } else {
                navbar.classList.remove("sticky");
            }
        }

//Collapsible Button For Menu Details
    var coll = document.getElementsByClassName("collapsible");
    var i;
    for (i = 0; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.maxHeight){
        content.style.maxHeight = null;
      } else {
        content.style.display = "block";
        content.style.maxHeight = content.scrollHeight + "px";
      }
      });
    }

////Filter Button Categories Function
$("#filterBtn").on("click", function() {
    if ($("#category-panel").css("display") == "none"){
        $("#category-panel").css("display","block");
        }
    else{
          $("#category-panel").css("display","none");
                   }


});

 $('#filterBtn').click(function(e) { //button click class name is myDiv
  e.stopPropagation();
 })

 $('.switchb').click(function(e) { //button click class name is myDiv
  e.stopPropagation();
 })

 $(function(){
  $(document).click(function(){
  $('#category-panel').hide(); //hide the button

  });
});



//Pre Loader Function
$(window).on("load",function(){
    $(".preloader-wrapper").fadeOut("slow");
})

// JavaScript code
function myfood() {
	let input = document.getElementById('search51').value
	input=input.toLowerCase();
	let x = document.getElementsByClassName('menu-title');
  let y = document.getElementsByClassName('menu-subtitle');
  let flag = 0;

	for (i = 0; i < x.length; i++) {
		if (!x[i].innerText.toLowerCase().includes(input)) {
            x[i].parentElement.parentElement.style.display="none";
		}
		else {
			x[i].parentElement.parentElement.style.display="inline-block";
      flag = 1;
		}
	}
  for (i = 0; i < y.length; i++) {
		if (y[i].innerText.toLowerCase().includes(input)) {
            y[i].parentElement.parentElement.style.display="inline-block";
            flag=1;
		}

	}

  if (flag == 0){
        document.getElementById('not-found').style.display="block";
  }
  else{
      document.getElementById('not-found').style.display="none";
  }
}

$("#search51").keyup(function(){
    console.log($('#search51').val().length)
    if ($('#search51').val().length){
        $(".parallax").addClass('hiddens');
        $(".imageSlider").addClass('hiddens');
        $("footer").addClass('hiddens');
        $("#parralaxaside").addClass('hiddens');
        $(".main-header").addClass('hiddens');
        $(".double-border-seprator").addClass('hiddens');
        $(".double-border-seprator").addClass('hiddens');
        $(".dot").addClass('hiddens');
        $("#extra").css('display','block');
        $(".content").css('display','none');
        $("#filterBtn").css('display','none');
        $("#cross").css('display','block');
    }
    else{
        $(".parallax").removeClass('hiddens');
        $(".imageSlider").removeClass('hiddens');
        $("footer").removeClass('hiddens');
        $("#parralaxaside").removeClass('hiddens');
        $(".main-header").removeClass('hiddens');
        $(".double-border-seprator").removeClass('hiddens');
        $(".dot").removeClass('hiddens');
        $("#extra").css('display','none');
        $("#filterBtn").css('display','block');
        $("#cross").css('display','none')
    }

});



$('#cross').on('click', function(){
    $('#search51').val('');
    console.log($('#search51').val().length);
    document.getElementById("search51").focus();
});
