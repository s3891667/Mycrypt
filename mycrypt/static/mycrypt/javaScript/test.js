function myfunc(val) {
    window.localStorage.setItem('coin',val.innerHTML);
};
function test(val) {
    var data = val.innerHTML;
    console.log(data);
    document.getElementById("test").innerHTML = parseFloat(data).toFixed(2);}