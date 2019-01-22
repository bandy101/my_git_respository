
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>clsjxxb complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="clsjxxb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="ccdjrq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="clscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="clxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="hphm" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="hpys" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="hpzl" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="PF" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="rlzl" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="scjyjg" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="scjyrq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="syxz" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="vin" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="xzcode" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "clsjxxb", propOrder = {
    "ccdjrq",
    "clscc",
    "clxh",
    "hphm",
    "hpys",
    "hpzl",
    "pf",
    "rlzl",
    "scjyjg",
    "scjyrq",
    "syxz",
    "vin",
    "xzcode"
})
public class Clsjxxb {

    protected Date ccdjrq;
    protected String clscc;
    protected String clxh;
    protected String hphm;
    protected String hpys;
    protected String hpzl;
    @XmlElement(name = "PF")
    protected String pf;
    protected String rlzl;
    protected String scjyjg;
    protected Date scjyrq;
    protected String syxz;
    protected String vin;
    protected String xzcode;

    /**
     * 获取ccdjrq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getCcdjrq() {
        return ccdjrq;
    }

    /**
     * 设置ccdjrq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setCcdjrq(Date value) {
        this.ccdjrq = value;
    }

    /**
     * 获取clscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClscc() {
        return clscc;
    }

    /**
     * 设置clscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClscc(String value) {
        this.clscc = value;
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
     * 获取hpys属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHpys() {
        return hpys;
    }

    /**
     * 设置hpys属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHpys(String value) {
        this.hpys = value;
    }

    /**
     * 获取hpzl属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHpzl() {
        return hpzl;
    }

    /**
     * 设置hpzl属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHpzl(String value) {
        this.hpzl = value;
    }

    /**
     * 获取pf属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPF() {
        return pf;
    }

    /**
     * 设置pf属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPF(String value) {
        this.pf = value;
    }

    /**
     * 获取rlzl属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRlzl() {
        return rlzl;
    }

    /**
     * 设置rlzl属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRlzl(String value) {
        this.rlzl = value;
    }

    /**
     * 获取scjyjg属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getScjyjg() {
        return scjyjg;
    }

    /**
     * 设置scjyjg属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setScjyjg(String value) {
        this.scjyjg = value;
    }

    /**
     * 获取scjyrq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getScjyrq() {
        return scjyrq;
    }

    /**
     * 设置scjyrq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setScjyrq(Date value) {
        this.scjyrq = value;
    }

    /**
     * 获取syxz属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSyxz() {
        return syxz;
    }

    /**
     * 设置syxz属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSyxz(String value) {
        this.syxz = value;
    }

    /**
     * 获取vin属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getVin() {
        return vin;
    }

    /**
     * 设置vin属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setVin(String value) {
        this.vin = value;
    }

    /**
     * 获取xzcode属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getXzcode() {
        return xzcode;
    }

    /**
     * 设置xzcode属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setXzcode(String value) {
        this.xzcode = value;
    }

}
