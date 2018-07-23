package com.sfe.ssm.controller.extension;

import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.common.tool.CreateFileUtil;
import com.sfe.ssm.common.version.ApiVersion;
import org.apache.commons.io.FileUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.commons.CommonsMultipartFile;

import javax.imageio.ImageIO;
import javax.servlet.http.HttpServletRequest;
import java.awt.image.BufferedImage;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;

/**
 * @author 廖志群
 * @version 1.00
 * @date 九月  18 2017,17:16
 * 视频上传控制器
 */
@RestController
@RequestMapping("/api/{version}/video")
public class UploadVideoController {


    //region 视频相关
    //单视频上传

    /**
     * 单文件上传
     * @param file 上传文件
     * @param request 返回文件名
     * @return
     */
    @RequestMapping(value = "/upload.do", method = RequestMethod.POST)
    @ApiVersion(1)
    public ResultMsg queryFileVideoData(
            @RequestParam("file") CommonsMultipartFile file,
            HttpServletRequest request) {
        // MultipartFile是对当前上传的文件的封装，当要同时上传多个文件时，可以给定多个MultipartFile参数(数组)
        SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMdd");
        String curTime = formatter.format( new Date());

        ResultMsg resultMsg;
        if (!file.isEmpty()) {
            String type = file.getOriginalFilename().substring(
                    file.getOriginalFilename().indexOf("."));// 取文件格式后缀名
            String filename = System.currentTimeMillis() + type;// 取当前时间戳作为文件名
            String pathDir = request.getSession().getServletContext()
                    .getRealPath("/upload/video/" + curTime);// 存放文件夹

            if(!CreateFileUtil.isExistDir(pathDir)) {
                CreateFileUtil.createDir(pathDir);
            }

            String path = pathDir+"/"+ filename;// 存放位置

            File destFile = new File(path);
            try {
                // FileUtils.copyInputStreamToFile()这个方法里对IO进行了自动操作，不需要额外的再去关闭IO流
                FileUtils.copyInputStreamToFile(file.getInputStream(), destFile);// 复制临时文件到指定目录下
            } catch (IOException e) {
                e.printStackTrace();
            }
            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), filename);

            return resultMsg;
        } else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "图片上传失败");
            return resultMsg;
        }
    }
    /**
     * 多文件上传
     * @param files
     * @param request
     * @return
     */
    @RequestMapping(value = "/uploads.do", method = RequestMethod.POST)
    @ApiVersion(1)
    public ResultMsg queryFileVideoDatas(
            @RequestParam("file") CommonsMultipartFile[] files,
            HttpServletRequest request) {
        ResultMsg resultMsg;
        SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMdd");
        String curTime = formatter.format( new Date());

        if (files != null) {
            List<String> lstFile = new ArrayList<String>();
            String pathDir = request.getSession().getServletContext()
                    .getRealPath("/upload/video/" + curTime);// 存放文件夹

            if(!CreateFileUtil.isExistDir(pathDir)) {
                CreateFileUtil.createDir(pathDir);
            }

            for (int i = 0; i < files.length; i++) {
                String type = files[i].getOriginalFilename().substring(
                        files[i].getOriginalFilename().indexOf("."));// 取文件格式后缀名
                String filename = System.currentTimeMillis() + type;// 取当前时间戳作为文件名
                String path = pathDir+"/"+ filename;// 存放位置
                File destFile = new File(path);
                try {
                    FileUtils.copyInputStreamToFile(files[i].getInputStream(), destFile);// 复制临时文件到指定目录下
                } catch (IOException e) {
                    e.printStackTrace();
                }
                lstFile.add(filename);
            }

            resultMsg = new ResultMsg(ResultStatusCode.OK.getErrcode(),
                    ResultStatusCode.OK.getErrmsg(), lstFile);

            return resultMsg;
        } else {
            resultMsg = new ResultMsg(ResultStatusCode.SYSTEM_ERR.getErrcode(),
                    ResultStatusCode.SYSTEM_ERR.getErrmsg(), "图片上传失败");
            return resultMsg;
        }

    }

    /**
     * 获取图片
     * @param fileName
     * @param prefix
     * @return
     */
    @RequestMapping(value = "/file/{fileName}/{prefix}", method = RequestMethod.GET)
    @ApiVersion(1)
    public @ResponseBody
    byte[] getFileVideo(@PathVariable("fileName") String fileName, @PathVariable("prefix") String prefix,
                        HttpServletRequest request) {

        long msec1=Long.parseLong(CreateFileUtil.getFileNameNoEx(fileName));
        SimpleDateFormat dateformat = new SimpleDateFormat("yyyyMMdd");//将毫秒级long值转换成日期格式
        GregorianCalendar gc = new GregorianCalendar();
        gc.setTimeInMillis(msec1);
        String dateStr = dateformat.format(gc.getTime());

        ByteArrayOutputStream bao = new ByteArrayOutputStream();
        try {

            String path = request.getSession().getServletContext()
                    .getRealPath("/upload/video/"+dateStr+"/" + fileName +"."+ prefix);// 存放位置

            File destFile = new File(path);

            InputStream inputStream =new FileInputStream(destFile);

            BufferedImage img = ImageIO.read(inputStream);


            ImageIO.write(img, prefix, bao);


        } catch (Exception e) {
            e.printStackTrace();
        }

        return bao.toByteArray();


    }






    //endregion




}
