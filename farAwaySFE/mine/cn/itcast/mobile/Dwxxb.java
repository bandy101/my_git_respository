
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>dwxxb complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="dwxxb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="cdpd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="cdsl" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="clxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="ddjd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ddwd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fxix" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="hphm" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzdz" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcs" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="jzlx" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzmc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzrp" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzzt" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "dwxxb", propOrder = {
    "cdpd",
    "cdsl",
    "clxh",
    "ddjd",
    "ddwd",
    "fxix",
    "hphm",
    "jzbh",
    "jzdz",
    "jzjcs",
    "jzlx",
    "jzmc",
    "jzrp",
    "jzzt"
})
public class Dwxxb {

    protected double cdpd;
    protected int cdsl;
    protected String clxh;
    protected double ddjd;
    protected double ddwd;
    protected String fxix;
    protected String hphm;
    protected String jzbh;
    protected String jzdz;
    protected int jzjcs;
    protected String jzlx;
    protected String jzmc;
    protected String jzrp;
    protected String jzzt;

    /**
     * 获取cdpd属性的值。
     * 
     */
    public double getCdpd() {
        return cdpd;
    }

    /**
     * 设置cdpd属性的值。
     * 
     */
    public void setCdpd(double value) {
        this.cdpd = value;
    }

    /**
     * 获取cdsl属性的值。
     * 
     */
    public int getCdsl() {
        return cdsl;
    }

    /**
     * 设置cdsl属性的值。
     * 
     */
    public void setCdsl(int value) {
        this.cdsl = value;
    }

    /**
     * 获取clxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClxh() {
        return clxh;
    }

    /**
     * 设置clxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClxh(String value) {
        this.clxh = value;
    }

    /**
     * 获取ddjd属性的值。
     * 
     */
    public double getDdjd() {
        return ddjd;
    }

    /**
     * 设置ddjd属性的值。
     * 
     */
    public void setDdjd(double value) {
        this.ddjd = value;
    }

    /**
     * 获取ddwd属性的值。
     * 
     */
    public double getDdwd() {
        return ddwd;
    }

    /**
     * 设置ddwd属性的值。
     * 
     */
    public void setDdwd(double value) {
        this.ddwd = value;
    }

    /**
     * 获取fxix属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFxix() {
        return fxix;
    }

    /**
     * 设置fxix属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFxix(String value) {
        this.fxix = value;
    }

    /**
     * 获取hphm属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHphm() {
        return hphm;
    }

    /**
     * 设置hphm属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHphm(String value) {
        this.hphm = value;
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
     * 获取jzdz属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzdz() {
        return jzdz;
    }

    /**
     * 设置jzdz属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzdz(String value) {
        this.jzdz = value;
    }

    /**
     * 获取jzjcs属性的值。
     * 
     */
    public int getJzjcs() {
        return jzjcs;
    }

    /**
     * 设置jzjcs属性的值。
     * 
     */
    public void setJzjcs(int value) {
        this.jzjcs = value;
    }

    /**
     * 获取jzlx属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzlx() {
        return jzlx;
    }

    /**
     * 设置jzlx属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzlx(String value) {
        this.jzlx = value;
    }

    /**
     * 获取jzmc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzmc() {
        return jzmc;
    }

    /**
     * 设置jzmc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzmc(String value) {
        this.jzmc = value;
    }

    /**
     * 获取jzrp属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzrp() {
        return jzrp;
    }

    /**
     * 设置jzrp属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzrp(String value) {
        this.jzrp = value;
    }

    /**
     * 获取jzzt属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzzt() {
        return jzzt;
    }

    /**
     * 设置jzzt属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzzt(String value) {
        this.jzzt = value;
    }

}
