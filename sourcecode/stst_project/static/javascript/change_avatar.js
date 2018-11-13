floatContainer = document.getElementById("floatContainer");
avatarPicks = document.querySelectorAll(".avatarPick");
myAvatar = document.querySelectorAll(".previewAvatar")[0];
avatarInput = document.getElementById("registerAvatar");

avatarPicks.forEach(function(avatarPick){
  avatarPick.addEventListener("click", function(){
    avatarNum = avatarPick.getAttribute("avatar-num");
    myAvatar.setAttribute("src", "/static/avatars/" + avatarNum.toString() + ".png");
    avatarInput.setAttribute("value", avatarNum)

    floatContainer.classList.toggle("hidden");
  })
})

myAvatar.addEventListener("click", function(){
  floatContainer.classList.toggle("hidden");
})
