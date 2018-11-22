loadingDots = document.getElementById("loadingDots");

window.setInterval(changeDots, 800);
pollWaitingUsers();


function changeDots(){
  if(loadingDots.textContent.length == 3){
    loadingDots.textContent = "";
  } else {
    loadingDots.textContent += "."
  }
  loadingDots.textContent
}



function pollWaitingUsers() {

  $.ajax({
      url:"/find_waiting_user",
      timeout: 60000,
      success: function(data) {
          if(data){
            gameId = parseInt(data);
            window.location.replace('/game/'+ gameId.toString());
          }else{
            pollWaitingUsers();
          }
       },
      error: function(jqXHR, textStatus, errorThrown) {

          console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);

          pollWaitingUsers();

      }
  });

}
