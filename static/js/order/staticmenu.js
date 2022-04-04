function CallWaiter(tableNumber) {
  $.ajax({
    type: 'GET',
    url: 'http://' + window.location.host + '/order/waiter/',
    data:{
      tableNumber: tableNumber
    },
  })

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
        $("#filterbtn").css('display','none');
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
        $("#filterbtn").css('display','block');
    }

});
