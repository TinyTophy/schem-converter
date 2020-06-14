const { ipcRenderer } = require("electron");

ipcRenderer.on("upload", (event, message) => {
  // console.log(message)
  const imContainer = document.getElementById("imgContainer");
  var img = document.createElement("IMG");
  img.setAttribute("src", message);
  img.setAttribute("id", "imgPreview");
  imContainer.appendChild(img);
});

function convert() {
  const img_path = document.getElementById("imgPreview").src;
  console.log(ipcRenderer.send("async-message", img_path));
}

ipcRenderer.on("async-reply", (event, arg) => {
  if (arg) {
    var schem = document.getElementById("schem");
    schem.setAttribute("class", "alert alert-success");
    var strong = document.createElement("STRONG");
    strong.innerHTML = "Success!";
    schem.appendChild(strong);
  } else {
    var schem = document.getElementById("schem");
    schem.setAttribute("class", "alert alert-danger");
    var strong = document.createElement("STRONG");
    strong.innerHTML = "Failed!";
    schem.appendChild(strong);
  }
});
