console.log("YOOOO");

req_json = $.getJSON("/current_user_details").done(function(user_data){
  $("#currentUserBarFill").css("width", String(user_data.xp_to_level*100)+"%")
});
// user_data = JSON.parse(req_json).responseJSON
// console.log(req_json);

$("#currentUserBarFill").css("width", "")
