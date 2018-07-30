var imgnum = 0;

function cancel() {
    $("#create_dialog").hide();
}
// 设备名称和设备编号
// $(function() {
//     require(['../module/date', '../module/url', '../module/check'], function(dateModule, urlModule, checkModule) {
//         id = urlModule.getUrlParam("id");
//         if(id != null) {
//             $.ajax({
//                 url: "/api/manage/repairdisposeinfo/" + id,
//                 type: 'get',
//                 dataType: "json",
//                 contentType: "application/json",
//                 timeout: checkModule.getTimeout(),
//                 success: function(data) {
//                     $('#loadingToast').fadeOut(100);
//                     checkModule.checkOut(data);
//                     if(data.errcode === 0 && data.content) {
//                         var equipment = data.content.equipment;
//                         $("#equipment__name").text(equipment.name);
//                         $("#equipment__code").text(equipment.code);
//
//                     }
//                 },
//                 error: function(e) {
//                     checkModule.checkTimeout(e);
//                 }
//             });
//         }
//     });
// });
$(function() {
    require(['../module/date', '../module/url', '../module/check'], function(dateModule, urlModule, checkModule) {
        id = urlModule.getUrlParam("id");
        if(id != null) {
            $.ajax({
                url: "/api/manage/repairdisposeinfo/" + id,
                type: 'get',
                dataType: "json",
                contentType: "application/json",
                timeout: checkModule.getTimeout(),
                success: function(data) {
                    $('#loadingToast').fadeOut(100);
                    checkModule.checkOut(data);
                    if(data.errcode === 0 && data.content) {
                        var equipment = data.content.equipment;
                        var repair = data.content.repair;
                        $("#equipment__name").text(equipment.name);
                        $("#equipment__code").text(equipment.code);
                        if(repair != null) {
                            var title;
                            type = repair.type;
                            var back = "javascript:location.replace('repair_list.html?type=" + type + "&flag=1')";
                            $("#back").attr("href", back);
                            switch(type) {
                                case 1:
                                    title = "检修";
                                    break;
                                case 2:
                                    title = "报修";
                                    break;
                                case 3:
                                    title = "维护";
                                    break;
                                case 4:
                                    title = "返厂";
                                    break;
                                case 5:
                                    title = "升级";
                                    break;
                            }
                            $("[name='title']").html(title);
                            if(repair.exception) {
                                $("#item").text(repair.exception);
                                $("#item_div").show();
                            }
                            $("#assign").text(repair.workerName);
                            $("#createtime").text(dateModule.getTime(repair.createtime));
                            preresult = repair.result;
                            var results = preresult.split("->");
                            var resultHtml = dateModule.getTime(repair.createtime) + ">" +" <br/>"+ results[0];
                            if(repair.state == 0) {
                                $("#state").text("未处理");
                                $("#submit").text("撤单");
                                $("#submit").attr("href", "javascript:repeal(" + repair.id + ")");
                            }
                            if(repair.state == 1) {
                                $("#state").text("已出勤");
                                $("#submit").text("完成审核");
                                $("#submit").attr("href", "javascript:finish(" + repair.id + ")");
                                resultHtml += "\n" + dateModule.getTime(repair.checktime) + "> " + results[1];
                                $("#result_type").show();
                                if(repair.imgurl) {
                                    var imgs = repair.imgurl.split(";");
                                    for(var i = 0; i < imgs.length; i++) {
                                        $(".form-preview__bd").append("<img src='" + imgs[i] + "'  width=\"100%\">");
                                    }
                                    $(".form-preview__ft").attr("style", "width:100%;position:fixed;bottom:0;background-color: #fff;");
                                }
                            }
                            if(repair.state > 1 && repair.state < 4) {
                                if(repair.state == 2) {
                                    $("#state").text("已解决");
                                } else if(repair.state == 3) {
                                    $("#state").text("未解决");
                                }
                                resultHtml += "\n" + dateModule.getTime(repair.checktime) + "> " + results[1];
                                resultHtml += "\n" + dateModule.getTime(repair.finishtime) + "> " + results[2];
                                $(".form-preview__ft").hide();
                            }
                            if(repair.state == 4) {
                                $("#state").text("待后台核复");
                                $("#result").attr("placeholder", "请填写核复内容");
                                $("#result").show();
                            }
                            if(repair.state == 5) {
                                $("#state").text("待现场确认");
                                resultHtml += "\n" + dateModule.getTime(repair.checktime) + "> "+"<br/>" + results[1];
                                $(".form-preview__ft").hide();
                            }
                            $("#pre_result").val(resultHtml);
                        } else {
                            $("#assign").html("<a id='assign_a' href='javascript:assign(" + equipment.areaId + ");'>点击指派</a>");
                        }
                    }
                },
                error: function(e) {
                    checkModule.checkTimeout(e);
                }
            });
        }
    });
    $("#switchCP").on("change", function() {
        if($(this).prop("checked")) {
            $("#result").hide();
            $("#result").val("");
        } else {
            $("#result").show();
        }
    });
});
// 设备名称和设备编号结束
function addpoint() {
    require(['../module/checkInput'], function(checkInputModule) {
        var pointcontent = $("#point_content").val();
        if(checkInputModule.isNotNeedInputText(pointcontent)) {
            alert("请输入节点内容");
            return
        }
        var imgarr = new Array();
        for(var i = 1; i <= imgnum; i++) {
            var pic = "#pic-" + i;
            imgarr.push($(pic).attr("src"));
        }

        var now = new Date();
        var year = now.getFullYear();
        var month = now.getMonth()+1;
        var day = now.getDate();
        var hour = now.getHours();
        var minute = now.getMinutes();
        var second = now.getSeconds();
        if(month <= 9) month = "0"+month;
        if(day <= 9) day = "0"+day;
        if(hour<= 9) hour = "0"+hour;
        if(minute<= 9) minute = "0"+minute;
        if(second<= 9) second = "0"+second;
        var nowdate =year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second;



        var html = "<li><span>张三</span>\n" +
            "            <p>\n" +
            "                <span>"+ nowdate +"</span>\n" +
            "                <span>" + pointcontent + "</span>\n" +
            "                <span><img src='"+ imgarr +"' class='smallimg'></span>\n" +
            "            </p>\n" +
            "        </li>";
        $("#main").append(html);


        $.ajax({
            url: "/api/node/nodeinfo",
            type: 'post',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                content:pointcontent,
                imgurl:imgarr
            }),
            success: function(data) {

            }

        });
    });
    $("#create_dialog").hide();
}


$("input[type=file]").change(function() {
    if(imgnum < 2) {
        imgnum++;
    }
    if(imgnum == 2) {
        $("#uploader").hide();
    }
    var pic = "#pic-" + imgnum;
    /* 压缩图片 */
    lrz(this.files[0], {
        width: 600 //设置压缩参数
    }).then(function(rst) {
        /* 处理成功后执行 */
        $(pic).attr("src", rst.base64);
        $(pic).show();
        $("#imgnum").text(imgnum);
    }).catch(function(err) {
        /* 处理失败后执行 */
    })
});

$(".uploader__file__pop").on("click", function() {
    $(this).attr("src", "");
    $(this).hide();
    imgnum--;
    if(imgnum == 1) {
        $("#uploader").show();
    }
    $("#imgnum").text(imgnum);
});



$("#add").click(function() {
    $("#create_dialog").show();
});
$(".close-dialog").click(function() {
    $("#create_dialog").hide();
});

// 缩略图
$(function(){
    /*
     smallimg   // 小图
     bigimg  //点击放大的图片
     mask   //黑色遮罩
     */
    var obj = new zoom('mask_pop', 'bigimg','smallimg');
    obj.init();
});