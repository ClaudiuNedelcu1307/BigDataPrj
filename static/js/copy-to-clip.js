function bannerCopy() {
    var copyText = document.getElementById("bannerCopyText");
    copyText.select();
    document.execCommand("copy");
    alert("Copied the text: " + copyText.value);
  }