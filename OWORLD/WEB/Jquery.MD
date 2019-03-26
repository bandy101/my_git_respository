# 选择器（HTML-DOC）
# select().action()
    元素选择器
        $+[("element"),("element +.Classname|#Idname"),]
    属性选择器
        $+[("[property[=|!=|$=]]"]
                    （$= : 以某个值结尾）
    css选择器
        $("p").css("background-color","red")  //把所有 p 元素的背景颜色更改为红色

#   选择器实例
    $(this) 	当前 HTML 元素
    $("p") 	所有 <p> 元素
    $("p.intro") 	所有 class="intro" 的 <p> 元素
    $(".intro") 	所有 class="intro" 的元素
    $("#intro") 	id="intro" 的元素
    $("ul li:first") 	每个 <ul> 的第一个 <li> 元素
    $("[href$='.jpg']") 	所有带有以 ".jpg" 结尾的属性值的 href 属性
    $("div#intro .head") 	id="intro" 的 <div> 元素中的所有 class="head" 的元素  

# (效果)基本的JQ函数方法action()
    hide([speed,callback]) and show([speed,callback]) 隐藏和显示获取到的html元素  speed: 隐藏或显示的速度 , callback: 隐藏或显示完成后执行的函数  
    ``toggle() 方法来切换 [hide() 和 show()] 方法。 
        example: $(selector).toggle(speed,callback);
    淡入淡出：[speed,callback]
        fadeIn(),fadeOut(),fadeToggle()
    隐藏和淡出的区别：隐藏是从下至上从大自小逐步隐藏，淡出整体慢慢透明隐藏。
    滑动：[speed,callback]  # div property:display :None //不显示该元素 滑动会改变这个值 
        slideDown()
        slideUp()
        slideToggle()
    动画：$(selector).animate({params},speed,callback)
    {   必需的 params 参数定义形成动画的 CSS 属性。eg.{left:'250px'}
        可选的 speed 参数规定效果的时长。它可以取以下值："slow"、"fast" 或毫秒。
        可选的 callback 参数是动画完成后所执行的函数名称。
    }
    stop() 方法用于停止动画或效果，在它们完成之前。
        stop() 方法适用于所有 jQuery 效果函数，包括滑动、淡入淡出和自定义动画。
    $(selector).stop(stopAll,goToEnd);
        可选的 stopAll 参数规定是否应该清除动画队列。默认是 false，即仅停止活动的动画，允许任何排入队列的动画向后执行。
        可选的 goToEnd 参数规定是否立即完成当前动画。默认是 false。
        因此，默认地，stop() 会清除在被选元素上指定的当前动画。
    ▲``Callback 函数在当前动画 100% 完成之后执行。
    动画的链接：
        $("select").css("color","red").slideUp(2000).slideDown(2000);




# JQ关于HTML操作
    【<p id="test">这是段落中的<b>粗体</b>文本。</p>】
    text() - 设置或返回所选元素的文本内容   //Text: 这是段落中的粗体文本
    html() - 设置或返回所选元素的内容（包括 HTML 标记）//这是段落中的<b>粗体</b>文本
    val() - 设置或返回表单字段的值  <input >
    attr() 方法用于获取属性值。 // $("#w3s").attr("href") 设置 .attr('href','new values'),可以用传入字典同时设置多个property
    【text(),html(),val() 加入的参数即为将要修改成的值】
    $("#test1").text(function(i,origText){ }) origText = $(selector).text()值
    $("#w3s").attr("href", function(i,origValue){
      return origValue + "/jquery"; 
    });   origValue ：原属性值

    <添加>  $(selector).
    
    append() - 在被选元素的结尾插入内容
    prepend() - 在被选元素的开头插入内容
    after() - 在被选元素之后插入内容
    before() - 在被选元素之前插入内容

    var txt1="<p>Text.</p>";              // 以 HTML 创建新元素
    var txt2=$("<p></p>").text("Text.");  // 以 jQuery 创建新元素
    var txt3=document.createElement("p");
    txt3.innerHTML="Text.";               // 通过 DOM 来创建文本
    $("body").append(txt1,txt2,txt3);        // 追加新元素
    $("body").after(txt1,txt2,txt3);   // 追加新元素

    <删除>
    
    remove() - 删除被选元素（及其子元素）
    empty() - 从被选元素中删除子元素
    $("p").remove(".italic") 删除 class="italic" 的所有 <p> 元素

    <css>
    addClass() - 向被选元素添加一个或多个类     //多个类在之间用空格分开
    removeClass() - 从被选元素删除一个或多个类
    toggleClass() - 对被选元素进行添加/删除类的切换操作
    css() - 设置或返回样式属性
    $(selector).css({'propertyname':'value',}) or .css('propertyname','value')
    .css('property') 返回样式属性

    <处理元素和浏览器窗口的尺寸>
    
    width()     返回元素的宽度，不包括内边距、边框或外边距
    height()            高度
    innerWidth()    返回元素的宽度（包括内边距）
    innerHeight()
    outerWidth()      返回元素的宽度（包括内边距和边框）。
    outerHeight()
    outerWidth(true) 方法返回元素的宽度（包括内边距、边框和外边距）。
    outerHeight(true) 方法返回元素的高度（包括内边距、边框和外边距）。
    $("#div1").width(500).height(500);   设置指定大小（链接chaining 设置）







# JQ遍历