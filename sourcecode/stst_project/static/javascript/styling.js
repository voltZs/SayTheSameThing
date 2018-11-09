var bubbles = document.querySelectorAll(".rightContBubble");
var avatarBubble = document.getElementById("avatarBub");
var userInfoCont = document.getElementById("currentUserInfo");
var userSideBar = document.getElementById("userSideBar");

bubbles.forEach(function(elem){
  if(elem.id != "avatarBub"){
    elem.addEventListener("mouseenter", function(){
      elem.getElementsByClassName('bubblecomp1right')[0].classList.add("whiteOrange");
    });

    elem.addEventListener("mouseleave", function(){
      elem.getElementsByClassName('bubblecomp1right')[0].classList.remove("whiteOrange");
    });
  }
});

userSideBar.addEventListener("mouseenter", function(){
  avatarBubble.classList.add("whiteOrange");
  bubbles[0].getElementsByClassName('bubblecomp1right')[0].classList.add("whiteOrange");
  userInfoCont.classList.add("whiteOrangeText");
});
userSideBar.addEventListener("mouseleave", function(){
  avatarBubble.classList.remove("whiteOrange");
  bubbles[0].getElementsByClassName('bubblecomp1right')[0].classList.remove("whiteOrange");
  userInfoCont.classList.remove("whiteOrangeText");
});
