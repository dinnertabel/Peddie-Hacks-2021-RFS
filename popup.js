var scamscum = "";
console.log("Anti-Scam Script started!");

document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('go');
    // onClick's logic below:
    link.addEventListener('click', function() {
        getURL();
    });
});
function getURL() {         // gets website url
   chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;
    if(url.length > 9){
      if(url.substring(0,9)=="chrome://"){
        document.getElementById("status").innerHTML="Not A SCAM!";
        return;
      }
    }
    sphasend(url);
});
}

function sphasend(currentURL) {           //gets url of current page then sends url to external website
    document.getElementById("status").innerHTML="Checking site...";
    console.log("Button pressed")
    console.log("current URL: "+currentURL);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:3000/scamchecker", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ URL: currentURL}));
    xhr.onload = function() {
        console.log("Page Loaded.")
        console.log(this.responseText);
        scamscum = this.responseText;
        let output = this.responseText;
        output = output.replace('\\n','');
        document.getElementById("status").innerHTML=output;

    }
 }

  function Scam() {       // getter for value returned
      return scamscum;
  }