function searchAccount() {
    var input, filter, accountList, account, a, i, txtValue;
    input = document.getElementById('searchInput');
    filter = input.value.toUpperCase();
    accountList = document.getElementById("accountList");
    accounts = accountList.getElementsByClassName("account");

    for (i = 0; i < accounts.length; i++) {
        a = accounts[i].getElementsByTagName("h5")[0];
        txtValue = accounts[i].textContent || accounts[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            accounts[i].style.display = "";
        } else {
            accounts[i].style.display = "none";
        }
    }
}
