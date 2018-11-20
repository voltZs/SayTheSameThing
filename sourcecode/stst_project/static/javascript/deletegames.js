var editButton = document.getElementById("editButton");
var deleteButtons = document.querySelectorAll("i.tdRemove");

editButton.addEventListener("click", function(event){
  deleteButtons.forEach(function(dButton){
    dButton.classList.toggle("hidden");
  })
})
