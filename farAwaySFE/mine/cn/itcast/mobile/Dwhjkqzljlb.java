
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>dwhjkqzljlb complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="dwhjkqzljlb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="co" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="dqy" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fs" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fx" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="no2" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="o3" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="pm10" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="pm25" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="sd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="so2" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="testNo" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="wd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "dwhjkqzljlb", propOrder = {
    "co",
    "dqy",
    "fs",
    "fx",
    "jzbh",
    "no2",
    "o3",
    "pm10",
    "pm25",
    "sd",
    "so2",
    "testNo",
    "wd"
})
public class Dwhjkqzljlb {

    protected double co;
    protected double dqy;
    protected double fs;
    protected String fx;
    protected String jzbh;
    protected double no2;
    protected double o3;
    protected double pm10;
    protected double pm25;
    protected double sd;
    protected double so2;
    protected String testNo;
    protected double wd;

    /**
     * 获取co属性的值。
     * 
     */
    public double getCo() {
        return co;
    }

    /**
     * 设置co属性的值。
     * 
     */
    public void setCo(double value) {
        this.co = value;
    }

    /**
     * 获取dqy属性的值。
     * 
     */
    public double getDqy() {
        return dqy;
    }

    /**
     * 设置dqy属性的值。
     * 
     */
    public void setDqy(double value) {
        this.dqy = value;
    }

    /**
     * 获取fs属性的值。
     * 
     */
    public double getFs() {
        return fs;
    }

    /**
     * 设置fs属性的值。
     * 
     */
    public void setFs(double value) {
        this.fs = value;
    }

    /**
     * 获取fx属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFx() {
        return fx;
    }

    /**
     * 设置fx属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFx(String value) {
        this.fx = value;
    }

    /**
     * 获取jzbh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzbh() {
        return jzbh;
    }

    /**
     * 设置jzbh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzbh(String value) {
        this.jzbh = value;
    }

    /**
     * 获取no2属性的值。
     * 
     */
    public double getNo2() {
        return no2;
    }

    /**
     * 设置no2属性的值。
     * 
     */
    public void setNo2(double value) {
        this.no2 = value;
    }

    /**
     * 获取o3属性的值。
     * 
     */
    public double getO3() {
        return o3;
    }

    /**
     * 设置o3属性的值。
     * 
     */
    public void setO3(double value) {
        this.o3 = value;
    }

    /**
     * 获取pm10属性的值。
     * 
     */
    public double getPm10() {
        return pm10;
    }

    /**
     * 设置pm10属性的值。
     * 
     */
    public void setPm10(double value) {
        this.pm10 = value;
    }

    /**
     * 获取pm25属性的值。
     * 
     */
    public double getPm25() {
        return pm25;
    }

    /**
     * 设置pm25属性的值。
     * 
     */
    public void setPm25(double value) {
        this.pm25 = value;
    }

    /**
     * 获取sd属性的值。
     * 
     */
    public double getSd() {
        return sd;
    }

    /**
     * 设置sd属性的值。
     * 
     */
    public void setSd(double value) {
        this.sd = value;
    }

    /**
     * 获取so2属性的值。
     * 
     */
    public double getSo2() {
        return so2;
    }

    /**
     * 设置so2属性的值。
     * 
     */
    public void setSo2(double value) {
        this.so2 = value;
    }

    /**
     * 获取testNo属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTestNo() {
        return testNo;
    }

    /**
     * 设置testNo属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTestNo(String value) {
        this.testNo = value;
    }

    /**
     * 获取wd属性的值。
     * 
     */
    public double getWd() {
        return wd;
    }

    /**
     * 设置wd属性的值。
     * 
     */
    public void setWd(double value) {
        this.wd = value;
    }

}
