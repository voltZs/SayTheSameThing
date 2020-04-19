var floatContainer = document.getElementById("floatContainer");
var avatarPicks = document.querySelectorAll(".avatarPick");
var myAvatar = document.getElementById("previewAvatar");
var avatarInput = document.getElementById("registerAvatar");

var original_src = myAvatar.getAttribute("src");
var saveButton = document.getElementById("saveButton");
var changeAvatarForm = document.getElementById("avatarForm");

avatarPicks.forEach(function(avatarPick){
  avatarPick.addEventListener("click", function(){
    avatarNum = avatarPick.getAttribute("avatar-num");
    if(avatarInput){
      avatarInput.setAttribute("value", avatarNum);
    }
    floatContainer.classList.toggle("hidden");
    var new_src = "/static/avatars/" + avatarNum.toString() + ".png"
    if(saveButton){
      if(original_src != new_src){
        saveButton.classList.remove("hidden");
      } else {
        saveButton.classList.add("hidden");
      }
    }

    myAvatar.setAttribute("src", new_src);
  })
})

myAvatar.addEventListener("click", function(event){
  floatContainer.classList.toggle("hidden");
  event.stopPropagation();
})

document.body.addEventListener("click", function(){
  floatContainer.classList.add("hidden");
})

if(saveButton){
  saveButton.addEventListener("click", function(){
    changeAvatarForm.submit();
  })
}
