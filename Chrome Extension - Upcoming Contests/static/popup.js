var cnt = 1, loading = true, i;
var par = document.getElementById("contest_details");

const generate_html = function(contest){
  ret = "<div class = \"card text-bg-primary mb-3\">";
  ret += "<div class = \"card-header\">" + contest.head + "</div>";
  ret += "<div class = \"card-body text-bg-info\">";
  console.log(contest);
  if (contest.high_priority){
    ret += "<div class = \"time red_text\">" + contest.time + "</div>";
  }
  else{
    ret += "<div class = \"time\">" + contest.time + "</div>";
  };
  ret += "<div>" + contest.name + "</div>";
  ret += "</div>";
  ret += "</div>";
  return ret;
};

//Fetch contest details
const fetch_content = function(){
  fetch('http://127.0.0.1:5000/get_contests').then(
    response => response.text()).then(result => {
      obj = JSON.parse(result);
      var generatedHTML = "";
      obj.forEach((item, index) => {
        generatedHTML += generate_html(item);
      });

      par.innerHTML = generatedHTML;
      loading = false;
    }
  );
};

//Loading animation
setInterval(() => {
  if (loading){
    cnt = (cnt + 1);
    if (cnt == 4){
      cnt = 1;
    }

    par.innerHTML = "Loading ";
    for (i = 0; i < cnt; i++){
      par.innerHTML += ".";
    };
  };
}, 300);

fetch_content();