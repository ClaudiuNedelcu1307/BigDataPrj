
function lightTheModalUp(status) {
    if(status == true) {
        document.getElementById("id01").style.display = "block";
    } else {
        document.getElementById("id01").style.display = "none";
    }
}

function passedFunc(x, y) {
    document.getElementById('resultFinal').style.color = "black";
    if(x === y) {
        document.getElementById('resultFinal').style.color = "green";
    } else {
        document.getElementById('resultFinal').style.color = "red";
    }

}

function lightTheUploadModalUp(status, fileName) {
    if(status == true) {
        document.getElementById("miculX").style.display = "block";
        document.getElementById("finishLine").style.display = "block";
        document.getElementById("confirmReg").style.display = "inline-block";
        document.getElementById("cancelReg").style.display = "inline-block";
        document.getElementById("finishLine").innerHTML = "Your file " + fileName + " is ready to be converted!";
    } else {
        document.getElementById("miculX").style.display = "none";
        document.getElementById("finishLine").style.display = "none";
        document.getElementById("confirmReg").style.display = "none";
        document.getElementById("cancelReg").style.display = "none";
        document.getElementById("finishLine").innerHTML = "...";
        document.getElementById('id02').style.display='none'
        document.getElementById('id01').style.display='none'
    }
}

String.prototype.replaceAll = function(str1, str2, ignore) 
{
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
} 

$(function() {
    $('#btnSend').click(function() {
        lightTheModalUp(true);
        text = document.getElementById("SQLField").value;
        inputName = 'DA'
        pasteTextArea = document.getElementById("NoSQLField");
        text = text.replaceAll("&", "and");
        if(inputName) {
            $.ajax({
                url: '/uploadCmd',
                // data: $('form').serialize(),
                data: 'inputName=' + inputName + "&text=" + text,
                type: 'POST',
                success: function(response) {
                    //console.log(response);
                    aux = response['NoSQL'].replaceAll('\\n','\r\n');
                    pasteTextArea.value = aux;
                    console.log(aux)
                    document.getElementById('durrInput').value = response['duration']
                    document.getElementById('numInput').value = response['nums']
                    passedFunc(response['nums'], response['succ']);
                    document.getElementById('resultFinal').innerHTML = "Result: "+ response['succ'] + "/" + response['nums'] +" passed";
                    lightTheModalUp(false);
                },
                error: function(error) {
                    pasteTextArea.value = "Invalid Request";
                    console.log(error);
                    lightTheModalUp(false);
                }
            });
        }
        else {
            alert("Nup");
        }
    });
});


function uploadNormal()
{
    document.getElementById('id02').style.display='block';
    var fd = new FormData();
    var fileName = $('#sqlFileToUpload')[0].files[0] ? $('#sqlFileToUpload')[0].files[0].name : "null";
    fd.append('file', $('#sqlFileToUpload')[0].files[0]);
    fd.append('id', "75");
    $.ajax({
        url: '/uploadFile',
        type: 'POST',
        data: fd,
        contentType: false,
        processData: false,
        success: function(data){
            console.log(data);
            if (data === 'Bad file') {
                document.getElementById("finishLine").style.display = "block";
                document.getElementById("miculX").style.display = "block";
                document.getElementById("finishLine").innerHTML = "Your file " + fileName + " is not supported";
            } else {
                setTimeout(function() {
                    lightTheUploadModalUp(true, fileName);
                }, 2000);
            }
        },
        error: function(error){
            alert('eroare');
            document.getElementById("finishLine").style.display = "block";
            document.getElementById("miculX").style.display = "block";
            document.getElementById("finishLine").innerHTML = "Your file " + fileName + " is: " + error;
        }
    });
}

function sendTransformSignal() {
    var fileName = $('#sqlFileToUpload')[0].files[0] ? $('#sqlFileToUpload')[0].files[0].name : "null";
    lightTheModalUp(true);
    $.ajax({
        url: '/resolveFile',
        data: 'fileName=' + fileName + "&convert=" + true,
        type: 'GET',
        success: function(response) {
            console.log(response);

            setTimeout(function() {
                // document.getElementById("NoSQLField").value = $('#sqlFileToUpload')[0].files[0];
                var preview = document.getElementById("SQLField");
                var file = $('#sqlFileToUpload')[0].files[0];
                var reader = new FileReader()
                reader.onload = function (event) {
                    preview.value = event.target.result;
                }
                reader.readAsText(file);
                document.getElementById("NoSQLField").value = response['NoSQL'];
                document.getElementById('durrInput').value = response['duration'];
                document.getElementById('numInput').value = response['nums'];
                passedFunc(response['nums'], response['succ']);
                document.getElementById('resultFinal').innerHTML = "Result: "+ response['succ'] + "/" + response['nums'] +" passed";
                document.getElementById('id02').style.display='none';
                
                lightTheUploadModalUp(false, fileName);
            }, 150);
        },
        error: function(error) {
            document.getElementById("NoSQLField").value = "Invalid Request!";
            document.getElementById("SQLField").value = "Invalid Request!";
            console.log(error);
            document.getElementById('id02').style.display='none'
            lightTheModalUp(false);
        }
    });
}

function ShouldTransform() {
    if(document.getElementById("SQLField").value == '' && document.getElementById("sqlFileToUpload").value == '')
    {
        document.getElementById("btnSend").disabled = true;
    } else {
        document.getElementById("btnSend").disabled = false;
    }
}

