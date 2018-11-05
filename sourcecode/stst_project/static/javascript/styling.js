bubbles = document.querySelectorAll(".rightContBubble")


bubbles.forEach(function(elem){
  elem.addEventListener("mouseenter", function(){
    elem.getElementsByClassName('bubblecomp1')[0].classList.add("lightOrange");
  });

  elem.addEventListener("mouseleave", function(){
    elem.getElementsByClassName('bubblecomp1')[0].classList.remove("lightOrange");
  });
})
