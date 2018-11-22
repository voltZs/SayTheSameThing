var floatWindow = document.getElementById("floatNotification");
var userButton = document.getElementById("usernameNavigbar");
var notificationBlob = document.getElementById("notificationBlob");
// ///////////////////

var numOfNotifications = document.getElementById("data-div").getAttribute("data-newnotifications");

if (numOfNotifications > 0) {
  notificationBlob.classList.remove("hidden");
}

updateNotificationsPanel();
checkNotifications();
setInterval(checkNotifications, 15000);

function checkNotifications() {
  var passinData = {
    numOfNotifications : numOfNotifications
  };
  var displayNotifications = [];
  $.ajax({
      url:"/check_notifications",
      data: passinData,
      timeout: 60000,
      success: function(data) {
        var retrievedNum = parseInt(JSON.parse(data));
        if (numOfNotifications != retrievedNum) {
          notificationBlob.classList.remove("hidden");
          updateNotificationsPanel();
          numOfNotifications = retrievedNum;
        }
       },
      error: function(jqXHR, textStatus, errorThrown) {
          console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);
      }
  });
}

function updateNotificationsPanel() {
  var displayNotifications = [];
  $.ajax({
      url:"/get_notifications",
      timeout: 60000,
      success: function(data) {
          notifications = data;
          floatWindow.innerHTML = "";

          if (notifications.length>0) {
            for(var x = notifications.length-1; x>=0; x--){
              var notificationBubble = document.createElement("DIV");
              notificationBubble.classList.add("notificationBubble");
              if(notifications[x].viewed){
                  notificationBubble.classList.add("compHighligh");
              } else {
                notificationBubble.classList.add("compHighlighStrong");
              }

              notificationBubble.textContent = notifications[x].content.toString();
              var aTag = document.createElement("A");
              aTag.setAttribute("href", notifications[x].link.toString());
              aTag.appendChild(notificationBubble);
              floatWindow.appendChild(aTag);
            }
          } else {
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

userButton.addEventListener("click", function(event){
  floatWindow.classList.toggle("hidden");
  event.stopPropagation();
  notificationBlob.classList.add("hidden");
  $.post("/clear_notifications");
  numOfNotifications = 0;
});

document.body.addEventListener("click", function(){
  floatWindow.classList.add("hidden");
})
