<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, maximum-scale=1.0, initial-scale=1.0, user-scalable=0" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>${projectName}</title>
    <meta name="keyword" content=" ${projectName} ">
    <meta name="description" content=" ${projectName} ">
    <link type="text/css" rel="stylesheet" href="/css/style.css">
    <link rel="shortcut icon" href="favicon.ico" />
    <link rel="bookmark" type="image/x-icon" href="favicon.ico" />
</head>
<body>
<div class="box">
    <span class="left"></span>
    <div class="right">
        <span class="logo"></span>
        <span class="txt">项目名称：${projectName}</span>
        <span class="txt">软件版本：${versions} </span>
        <span class="txt">备注：${remark} </span>
        <span class="txt"><br>技术支持：${technicalSupport} </span>
        <span class="txt">官方网站：<a href="${link}">${link}</a></span>
        <span class="txt">E-mail：<a href="mailto:${email}">${email}</a></span>
    </div>
</div>
</body>
</html>
