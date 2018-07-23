package com.sfe.ssm.controller;


import com.sfe.ssm.common.ResultMsg;
import com.sfe.ssm.common.ResultStatusCode;
import com.sfe.ssm.common.log.SystemLog;
import com.sfe.ssm.model.About;
import com.sfe.ssm.service.AboutService;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;


/**
 * @author 廖志群
 * @version 1.00
 * @date 九月  12 2017,11:13
 * 首页控制器
 */
@Controller
public class IndexController {

    @Autowired
    AboutService aboutService;
    /**
     * 添加一个日志器
     */
    private Logger log = Logger.getLogger(IndexController.class);

    @RequestMapping("/index")
    @SystemLog(module = "首页控制器",methods = "首页")
    public String showUserPage(ModelMap model){
        log.info("Index访问");

        About about = aboutService.getAboutById((long)1);
        if (about == null) {
            model.addAttribute("projectName", "");
            model.addAttribute("versions", "");
            model.addAttribute("remark", "" );
            model.addAttribute("technicalSupport", "广东胜霏尔环境科技有限公司");
            model.addAttribute("link", "http://www.etc-cn.com");
            model.addAttribute("email", "etc@etc-cn.com");
            return "Index";
        }
        else
        {
            model.addAttribute("projectName", about.getProjectName() );
            model.addAttribute("versions", about.getVersions());
            model.addAttribute("remark", about.getRemark());
            model.addAttribute("technicalSupport", about.getTechnicalSupport());
            model.addAttribute("link", about.getLink());
            model.addAttribute("email", about.getEmail());

            return "Index";
        }


    }


}
