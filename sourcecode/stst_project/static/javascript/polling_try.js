
window.setInterval(checkForChanges, 8000);

// function checkForChanges() {
//
//   otherUserTurns = document.querySelectorAll('div.stst_left div.turnBubble').length;
//   gameId = document.getElementById('data-div').getAttribute("data-gameid");
//
//   console.log("checking for changes")
//
//   passinData = {
//     otherTurns : otherUserTurns,
//     gameId : gameId
//   }
//
//   $.ajax({
//       url:"/poll",
//       data: passinData,
//       timeout: 60000,
//       success: function(data) {
//           // retrievedNum = parseInt(numOfTurns)
//           // if (otherUserTurns != retrievedNum){
//           //   console.log("new num of turns:" + retrievedNum.toString());
//           // }
//
//           window.location.replace('/play/'+ gameId.toString())
//
//        }
//        ,
//       error: function(jqXHR, textStatus, errorThrown) {
//
//           console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);
//
//           checkForChanges();
//
//       }
//   });
//
// }

function checkForChanges() {

  otherUserTurns = document.querySelectorAll('div.stst_left div.turnBubble').length;
  gameId = document.getElementById('data-div').getAttribute("data-gameid");

  console.log("checking for changes")

  passinData = {
    otherTurns : otherUserTurns,
    gameId : gameId
  }

  $.ajax({
      url:"/poll_other_user_moves",
      data: passinData,
      timeout: 60000,
      success: function(data) {
          // retrievedNum = parseInt(numOfTurns)
          // if (otherUserTurns != retrievedNum){
          //   console.log("new num of turns:" + retrievedNum.toString());
          // }
          //
          if (otherUserTurns != JSON.parse(data)){
            window.location.replace('/play/'+ gameId.toString());
          };

       }
       ,
      error: function(jqXHR, textStatus, errorThrown) {

          console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);

          checkForChanges();

      }
  });


}
