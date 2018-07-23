package com.sfe.ssm.util;

import com.sfe.ssm.common.tool.CreateFileUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import sun.misc.BASE64Decoder;

import javax.servlet.http.HttpServletRequest;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service("ImageUtil")
public class ImageUtil {

    @Autowired
    private BaseToolUtil baseTool;

    public String SaveIMGbyBASE64(List<String> imgarr,HttpServletRequest request){

        List<String> imgurls = new ArrayList();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMdd");
        String path = "/upload/img/" + formatter.format( new Date());
        String pathDir = request.getSession().getServletContext().getRealPath(path);
        if(!CreateFileUtil.isExistDir(pathDir)) {
            CreateFileUtil.createDir(pathDir);
        }
        for (String img : imgarr) {
            if(img.indexOf("/upload/img/")!=-1){
                imgurls.add(img);
            }else {
                String filename = System.currentTimeMillis() + ".jpg";
                String imgFilePath = pathDir + "/" + filename;//新生成的图片
                BASE64Decoder decoder = new BASE64Decoder();
                try {
                    //Base64解码
                    byte[] b = decoder.decodeBuffer(img.split("base64,")[1]);
                    for (int i = 0; i < b.length; ++i) {
                        if (b[i] < 0) {//调整异常数据
                            b[i] += 256;
                        }
                    }
                    //生成jpeg图片
                    OutputStream out = new FileOutputStream(imgFilePath);
                    out.write(b);
                    out.flush();
                    out.close();
                } catch (Exception e) {
                } finally {
                    imgurls.add(path + "/" + filename);
                }
            }
        }
        return baseTool.joinByList(";",imgurls);
    }


}
