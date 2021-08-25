//В данном модуле  происходит возаимодействие с backend отчета
function get_val() {

    //удаляем стэк если он есть
    $(".trace").remove()
    $(".ffff").remove()
    //проверка на незаполненные параметры



    var control = document.getElementById("ctrl");
    var data1 = new FormData()

    var arr = control.files
    for (index = 0; index < arr.length; index++) {
        if (arr[index].name == "УКПФ_заб.xlsx") {
            data1.append('amp_and_amd', arr[index])
        }
    }
    // data1.append('year', $('#year_').val());
    // data1.append('month', $('#month_').val());


    // data1.append('test', control.files[0])

    var token = '{{ csrf_token }}';
    // alert('csrf generated');

    // $.ajax({
    //     type: 'POST',
    //     url: 'upl/',
    //     data: data1,
    //     processData: false,
    //     contentType: false,
    //     responseType: 'arraybuffer',
    //     headers: {'X-CSRFToken': token},
    //     success: function (data, status, xhr) {
    //
    //         var blob = new Blob([data], {type: 'application/vnd.ms-excel'});
    //         console.log(blob)
    //         var downloadUrl = URL.createObjectURL(blob);
    //         var a = document.createElement("a");
    //         a.href = downloadUrl;
    //         a.download = 'download.xlsx';
    //         document.body.appendChild(a);
    //         a.click();
    //         document.body.removeChild(a);
    //
    //     }
    // })

    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'upl/');
    // xhr.setRequestHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    // xhr.responseType = 'arraybuffer';
    xhr.onload = function (e) {
        if (this.status == 200) {

            $('.intro__inner').append('<h1 class="ffff">'+this.response+'</h1>')

        } else {

            function arrayBufferToString( buffer, encoding ) {
                return new Promise((resolve,reject) => {

                    var blob = new Blob([buffer],{type:'text/plain'});
                    var reader = new FileReader();
                    reader.readAsText(blob, encoding);
                    reader.onload = (ev) => {
                        if (ev.target){
                            resolve(ev.target.result)
                        }else{
                            reject(new Error('Could not convert string to string!'));
                        }
                    }
                })

            }

            arrayBufferToString(this.response, 'UTF-8').then((r)=>{
                var decoder = new TextDecoder('utf-8')
                message = JSON.parse(r)['error']
                message1 = JSON.parse(r)['error1']
                // console.log(message)
                $('body').append('<article class="trace">'+message+'</article>').css({'fontsize':'24px'})
                // $('body').append('<article class="trace">'+message1+'</article>').css({'fontsize':'24px'})
                // alert(message)
            })

            // Materialize.toast('Invalid data!', 2000)
        }
    }
    // xhr.onerror = function (ev){
    //     alert('Формирование заверщилось ошибкой')
    // }

    xhr.send(data1);
}