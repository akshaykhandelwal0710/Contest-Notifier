const fetch_content = function(){
  fetch('http://127.0.0.1:5000/get_contests').then(
    response => response.text()).then(result => {
      console.log(result);
      var par = document.getElementById("contest_details");
      par.innerHTML = result;
    }
  )
};

fetch_content();