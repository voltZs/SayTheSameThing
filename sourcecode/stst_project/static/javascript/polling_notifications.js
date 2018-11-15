var floatWindow = document.getElementById("floatNotification");
var userButton = document.getElementById("usernameNavigbar");

userButton.addEventListener("click", function(event){
  floatWindow.classList.toggle("hidden");
  event.stopPropagation();
  $.post("/clear_notifications");
  //code to make red blob disappear
})

document.body.addEventListener("click", function(){
  floatWindow.classList.add("hidden");
})

checkNotifications();
setInterval(checkNotifications, 20000);

function checkNotifications() {

  var numOfNotifications = document.getElementById("data-div").getAttribute("data-newnotifications");

  var passinData = {
    numOfNotifications : numOfNotifications
  }

  var displayNotifications = [];
  $.ajax({
      url:"/check_for_notifications",
      data: passinData,
      timeout: 60000,
      success: function(data) {
          // If a change occured to database, refresh, if it just timed out, poll again
          notifications = data;

          if (notifications.length>0) {
            floatWindow.innerHTML = "";

            for(var x = notifications.length-1; x>=0; x--){
              var message = "";
              message += notifications[x].opponent;
              message += " started a new game with you"

              var notificationBubble = document.createElement("DIV");
              notificationBubble.classList.add("notificationBubble");
              notificationBubble.classList.add("compOrange");
              notificationBubble.textContent = message;
              var aTag = document.createElement("A");
              aTag.setAttribute("href", "/play/"+ notifications[x].game_id.toString());
              aTag.appendChild(notificationBubble);
              floatWindow.appendChild(aTag);
            }
          } else {
            floatWindow.innerHTML = "";
            var message = "No new notifications";
            var notificationBubble = document.createElement("DIV");
            notificationBubble.classList.add("notificationBubble");
            notificationBubble.classList.add("compWhite");
            notificationBubble.textContent = message;
            floatWindow.appendChild(notificationBubble);
          }


       },
      error: function(jqXHR, textStatus, errorThrown) {
          console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);
      }
  });

}
