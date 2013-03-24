javascript:(function(){
    var service_host = 'localhost:6543';
    var cur_url = location.toString();
    var e = encodeURIComponent;
    var service_url = 'http://' + service_host + '/edit?url=' + e(cur_url) + '&title=' + e(document.title);
    var wnd = open(service_url, '_blank');
    if (wnd) {
        wnd.focus();
    } else {
        alert('failed to open service new window');
    }
})()

//javascript:(function(){var service_host="localhost:6543";var cur_url=location.toString();var e=encodeURIComponent;var service_url="http://"+service_host+"/edit?url="+e(cur_url)+"&title="+e(document.title);var wnd=open(service_url,"_blank");if(wnd){wnd.focus()}else{alert("failed to open service new window")}})()