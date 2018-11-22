
window.setTimeout(checkForChanges, 4000);

function checkForChanges() {

  otherUserTurns = document.querySelectorAll('div.stst_left div.turnBubble').length + document.querySelectorAll('div.stst_common div.turnBubble').length;
  gameId = document.getElementById('data-div').getAttribute("data-gameid");

  console.log("checking for changes")

  passinData = {
    otherTurns : otherUserTurns,
    gameId : gameId
  }

  $.ajax({
      url:"/poll_game",
      data: passinData,
      timeout: 60000,
      success: function(data) {
          // If a change occured to database, refresh, if it just timed out, poll again
          retrievedNum = parseInt(data)
          if (otherUserTurns != retrievedNum){
            window.location.replace('/game/'+ gameId.toString());
          } else {
            checkForChanges();
          }
       },
      error: function(jqXHR, textStatus, errorThrown) {

          console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);

          checkForChanges();

      }
  });

}

// function checkForChanges() {
//
//   otherUserTurns = document.querySelectorAll('div.stst_left div.turnBubble').length + document.querySelectorAll('div.stst_common div.turnBubble').length;
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
//       url:"/poll_other_user_moves",
//       data: passinData,
//       timeout: 60000,
//       success: function(data) {
//           // retrievedNum = parseInt(numOfTurns)
//           // if (otherUserTurns != retrievedNum){
//           //   console.log("new num of turns:" + retrievedNum.toString());
//           // }
//           //
//           if (otherUserTurns != JSON.parse(data)){
//             window.location.replace('/game/'+ gameId.toString());
//           };
//
//        }
//        ,
//       error: function(jqXHR, textStatus, errorThrown) {
//
//           console.log(jqXHR.status + "," + textStatus + ", " + errorThrown);
//
//
//       }
//   });
//

// }
