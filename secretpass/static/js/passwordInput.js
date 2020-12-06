const generateEl = document.getElementById('generatePassword')
const resultEl = document.getElementById('passwordResult')
const clipboardEl = document.getElementById('copyClipboard')

clipboardEl.addEventListener('click', () => {
    const textarea = document.createElement('textarea')
    const password = resultEl.value

    if (!password) { return }

    textarea.value = password
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    textarea.remove()
    alert("Password copied to clipboard")
})

generateEl.addEventListener('click', () => {
    resultEl.value = generatePassword()
})

function showPassword(id) {
    var x = document.getElementById(id);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
