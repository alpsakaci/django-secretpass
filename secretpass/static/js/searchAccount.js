function searchAccount() {
    var input, filter, accountList, account, a, i, txtValue;
    input = document.getElementById('searchInput');
    filter = input.value.toUpperCase();
    accountList = document.getElementById("accountList");
    accounts = accountList.getElementsByClassName("account");

    for (i = 0; i < accounts.length; i++) {
        var service = accounts[i].getElementsByTagName("input")[0].value;
        var username = accounts[i].getElementsByTagName("input")[1].value;
        if (service.toUpperCase().indexOf(filter) > -1 || username.toUpperCase().indexOf(filter) > -1) {
            accounts[i].style.display = "";
        } else {
            accounts[i].style.display = "none";
        }
    }
}
