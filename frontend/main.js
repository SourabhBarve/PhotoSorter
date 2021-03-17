var Constants;
fetch("constants.json").then(resp => {
    console.log(resp);
    return resp.json();
}).then(data => {
    Constants = data;
    console.log(Constants);
});

eel.expose(showInfo);
function showInfo(text){
    document.getElementById("infoText").innerHTML = text;
}

function showLabeller() {
    sectEls = document.getElementsByTagName("section")
    for (element of sectEls) {
        element.style.display = "none";
    };
    document.getElementById("labeller").style.display = "flex";

    eel.setContext(Constants.Contexts.Labeller);
}

function showSorter() {}

function setPreprocessor() {
    var preprocessor = document.getElementById("preprocessor").value;
    eel.setPreprocessor(Constants.Preprocessors[preprocessor]);
}

function openSourceDirectorySelector() {
    eel.openSourceDirectorySelector();
}

function startLabelling() {
    document.getElementById("labelDropdown").style.display = "block";
    document.getElementById("confirmLabel").style.display = "block";
    eel.startLabelling();
}

eel.expose(setOriginalImage);
function setOriginalImage(pixels) {
    // console.log(pixels.substring(0, 20));
    // console.log(pixels.substring(pixels.length - 20, pixels.length));
    var imgEl = document.getElementById('original');
    if (imgEl) {
        imgEl.onerror = function(e) {
            console.error(e);
        }
        imgEl.src = "data:image/jpeg;base64," + pixels;
    }

}

eel.expose(setPreviewImage);
function setPreviewImage(face) {
    var imgEl = document.getElementById('preview');
    if (imgEl) {
        imgEl.onerror = function(e) {
            console.error(e);
        }
        imgEl.src = "data:image/jpeg;base64," + face;
    }

    // return "I dont know";
}

function setLabel() {
    var label = document.getElementById("labelDropdown").value;
    showInfo("Label selected: " + label);

    // TODO: Add handling of create new label
    if(label == "createLabel") {
        var newLabel = prompt("Label:");
        var options = document.getElementById("labelDropdown").options;
        for(var i=0; i<options.length; i++) {
            if(newLabel == options[i].value) {
                alert("The '" + newLabel + "' already exists!");
                return;
            }
        }
        var newOption = document.createElement('option');
        newOption.innerHTML = newLabel;
        newOption.value = newLabel;
        var x = document.getElementById("labelDropdown");
        x.add(newOption);
    }
}

function confirmLabel() {
    // TODO: Add handling of create new label and default selection

    var label = document.getElementById("labelDropdown").value;
    eel.setLabel(label);
}