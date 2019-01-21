
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ydsdwyxjlb complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="ydsdwyxjlb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="cbbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="cdpd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ddjd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ddwd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fxlx" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzrzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="zzdz" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "ydsdwyxjlb", propOrder = {
    "cbbh",
    "cdpd",
    "ddjd",
    "ddwd",
    "fxlx",
    "jzbh",
    "jzjcbh",
    "jzrzbh",
    "zzdz"
})
public class Ydsdwyxjlb {

    protected String cbbh;
    protected double cdpd;
    protected double ddjd;
    protected double ddwd;
    protected String fxlx;
    protected String jzbh;
    protected String jzjcbh;
    protected String jzrzbh;
    protected String zzdz;

    /**
     * 获取cbbh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCbbh() {
        return cbbh;
    }

    /**
     * 设置cbbh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCbbh(String value) {
        this.cbbh = value;
    }

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
     * 获取fxlx属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFxlx() {
        return fxlx;
    }

    /**
     * 设置fxlx属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFxlx(String value) {
        this.fxlx = value;
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
     * 获取jzjcbh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzjcbh() {
        return jzjcbh;
    }

    /**
     * 设置jzjcbh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzjcbh(String value) {
        this.jzjcbh = value;
    }

    /**
     * 获取jzrzbh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzrzbh() {
        return jzrzbh;
    }

    /**
     * 设置jzrzbh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzrzbh(String value) {
        this.jzrzbh = value;
    }

    /**
     * 获取zzdz属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getZzdz() {
        return zzdz;
    }

    /**
     * 设置zzdz属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setZzdz(String value) {
        this.zzdz = value;
    }

}
