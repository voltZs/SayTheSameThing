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
  userInfoCont.classList.add("whiteOrangeText");
});
userSideBar.addEventListener("mouseleave", function(){
  userInfoCont.classList.remove("whiteOrangeText");
});
