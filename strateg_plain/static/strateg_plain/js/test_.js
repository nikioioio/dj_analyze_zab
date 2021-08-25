//Модуль для скачивания нескольких файлов
var file_to_upl

function test_gen(){


    var token = '{{ csrf_token }}';

    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open('POST', 'upl_test/');

    xhr.onload = function (e) {

        if (this.status == 200) {
            file_to_upl = this.response['file1']

            file1 = _base64ToArrayBuffer(this.response['file1'])
            file2 = _base64ToArrayBuffer(this.response['file2'])
            arr = this.response['arr']
            console.log(arr)



            var blob = new Blob([file1], { type: 'application/vnd.ms-excel' });

            var downloadUrl = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = downloadUrl;
            a.download = 'test.xlsx';
            document.body.appendChild(a);
            a.click()


            var blob = new Blob([file2], { type: 'application/vnd.ms-excel' });

            var downloadUrl = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = downloadUrl;
            a.download = 'test1.xlsx';
            document.body.appendChild(a);
            a.click();

        }

    }

    xhr.send()

}


function test_gen2(){

    var data1 = new FormData()
    data1.append('amp_and_amd', file_to_upl)

    var token = '{{ csrf_token }}';

    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open('POST', 'upl_test1/');

    xhr.onload = function (e) {

        if (this.status == 200) {

            console.log('200')

        }

    }

    xhr.send(data1)

}



function decode_base64(s) {
  var b=l=0, r='',
  m='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  s.split('').forEach(function (v) {
    b=(b<<6)+m.indexOf(v); l+=6;
    if (l>=8) r+=String.fromCharCode((b>>>(l-=8))&0xff);
  });
  return r;
}

function _base64ToArrayBuffer(base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}


//Запрос к конейнеру flask gunicorn nginx
function test_gen1(){

    var control = document.getElementById("ctrl");
    var data1 = new FormData()

    var arr = control.files
    for (index = 0; index < arr.length; index++) {
        console.log(arr[index].name)
        if (arr[index].name == "3Первый передел МПФ.xlsx") {
            data1.append('test', arr[index])
        }
    }

    data1.append('year', 222);

    var token = '{{ csrf_token }}';

    let xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open('POST', 'http://127.0.0.1:5000/get_val');

    xhr.onload = function (e) {

        if (this.status == 200) {

            console.log(this.response)

        }

    }
    console.log(data1)
    xhr.send(data1)

}