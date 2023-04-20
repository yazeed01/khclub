//jQuery to collapse the navbar on scroll
// $(window).scroll(function() {
//     if ($(".navbar").offset().top > 50) {
//         $(".fixed-top").addClass("top-nav-collapse");
//     } else {
//         $(".fixed-top").removeClass("top-nav-collapse");
//     }
// });


// Unpoly Settings
// ===============

// Enable unpoly config in browser console.





// Search page
$(document).click(function() {
    $('.search-result').hide(); 
});




$(window).scroll(function() {
    var nav = $('.home');
    if (nav.length) {
        var contentNav = nav.offset().top;
        if (contentNav > 900) {
            $(".fixed-top").addClass("top-nav-collapse");
            $(".fixed-top").addClass("color-top");
            $(".fixed-top").removeClass("color-top-bis");
        } else {
            $(".fixed-top").removeClass("top-nav-collapse");
            $(".fixed-top").removeClass("color-top");
            $(".fixed-top").addClass("color-top-bis");
        }

        if ($(window).width() <= 479 | $(window).width() <= 556) {
            if ($(".home").offset().top > 900) {
                    $(".fixed-top").addClass("color-top");
                    $(".fixed-top").removeClass("color-top-bis");
            } else {
                $(".fixed-top").removeClass("color-top");
                $(".fixed-top").addClass("color-top-bis");
            }
        }
    }
});


// Toast's tiem
$(document).ready( function() {
    $('#mas-time').delay(3000).fadeOut();
});


// Important for Toast 
document.addEventListener("DOMContentLoaded", function(){
    var toastElementList = [].slice.call(document.querySelectorAll(".toast"));
  var toastList = toastElementList.map(function(element){
        return new bootstrap.Toast(element, {
          autohide: false
      });
  });
});


$(document).ready(function() {
    if ($(".list-ans-acc").slice().length > 4) {
        $("#loadMore").show()
    } else {
        $("#loadMore").hide()
    }
});


$(".list-ans-acc").slice(0, 4).show()
$("#loadMore").on("click", function(){
    $(".list-ans-acc:hidden").slice(0, 4).show()
})




// up.log.enable();


// Automatically follow all links on a page without requiring an [up-follow] attribute and
// without refreshing whole page.
// up.link.config.followSelectors.push("a[href]");

// // // //  Automatically follow all links on a page without requiring an [up-instant] attribute and
// // // // followed on mousedown instead of on click. 
// up.link.config.instantSelectors.push("a[href]");


// // // //  Automatically follow all forms on a page without requiring an [up-submit] attribute and
// // // // without refreshing whole page after submitting. 
// up.form.config.submitSelectors.push(["form"]);

// // // // Let unpoly render page from [.wrapper] class instead of [main] html tag.
// up.fragment.config.mainTargets = ".wrapper";


// // // // Disable inputs and buttons when Form submit.
// up.on("up:form:submit", () => {
//     document.querySelectorAll('button[type=submit], fieldset').forEach((element) => {
//       element.disabled = true;
//     })
//   });
