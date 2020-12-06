function decryptPassword(url, id, csrf) {
    var password = ""
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let result = JSON.parse(this.response)
            let field = "decryptionResult-" + id
            let input = document.getElementById(field)
            input.value = result.plain_password
            input.select()
            document.execCommand('copy')
            swapButtons(id)
        }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrf);
    xhttp.send();
}

function swapButtons(id) {

    var decryptButton = document.getElementById("decryptButton-"+id)
    var copyButton = document.getElementById("copyButton-"+id)
    decryptButton.style.display = "none";
    copyButton.style.display = "block";
}

function copyPassword(id) {
    const textarea = document.createElement('textarea')
    const field = document.getElementById("decryptionResult-"+id)
    const password = field.value

    if (!password) { return }

    textarea.value = password
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    textarea.remove()
    alert("Password copied to clipboard")
}
