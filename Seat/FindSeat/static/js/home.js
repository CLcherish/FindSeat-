/**
 * Created by tedu on 2018/10/15.
 */

if (typeof FileReader == 'undefined') {
    document.getElementById("xmTanDiv").InnerHTML = "<h1>��ǰ�������֧��FileReader�ӿ�</h1>";
    document.getElementById("xdaTanFileImg").setAttribute("disabled", "disabled");
}
//ѡ��ͼƬ������Ԥ��
function xmTanUploadImg(obj) {
    var file = obj.files[0];
    console.log(obj);console.log(file);
    console.log("file.size = " + file.size);
    var reader = new FileReader();
    reader.onloadstart = function (e) {
        console.log("��ʼ��ȡ....");
    }
    reader.onprogress = function (e) {
        console.log("���ڶ�ȡ��....");
    }
    reader.onabort = function (e) {
        console.log("�ж϶�ȡ....");
    }
    reader.onerror = function (e) {
        console.log("��ȡ�쳣....");
    }
    reader.onload = function (e) {
        console.log("�ɹ���ȡ....");
        var img = document.getElementById("avarimgs");
        img.src = e.target.result;
        //���� img.src = this.result;  //e.target == this
    }
    reader.readAsDataURL(file)
}
