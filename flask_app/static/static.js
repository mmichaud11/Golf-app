

var checks = document.querySelectorAll(".form-check-input");
var max = 6;
for (var i = 0; i < checks.length; i++)
    checks[i].onclick = selectiveCheck;
function selectiveCheck (event) {
    var checkedChecks = document.querySelectorAll(".form-check-input:checked");
    if (checkedChecks.length >= max + 1)
    return false;
}