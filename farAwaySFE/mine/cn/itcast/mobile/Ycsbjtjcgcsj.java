
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbjtjcgcsj complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="ycsbjtjcgcsj">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="bolq" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="co2bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="co2clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="cobzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="coclz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="jcrq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="jzhb" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="nobzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="noclz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "ycsbjtjcgcsj", propOrder = {
    "bolq",
    "co2Bzz",
    "co2Clz",
    "cobzz",
    "coclz",
    "jcrq",
    "jzhb",
    "jzjcbh",
    "nobzz",
    "noclz"
})
public class Ycsbjtjcgcsj {

    protected String bolq;
    @XmlElement(name = "co2bzz")
    protected double co2Bzz;
    @XmlElement(name = "co2clz")
    protected double co2Clz;
    protected double cobzz;
    protected double coclz;
    protected Date jcrq;
    protected String jzhb;
    protected String jzjcbh;
    protected double nobzz;
    protected double noclz;

    /**
     * 获取bolq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getBolq() {
        return bolq;
    }

    /**
     * 设置bolq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setBolq(String value) {
        this.bolq = value;
    }

    /**
     * 获取co2Bzz属性的值。
     * 
     */
    public double getCo2Bzz() {
        return co2Bzz;
    }

    /**
     * 设置co2Bzz属性的值。
     * 
     */
    public void setCo2Bzz(double value) {
        this.co2Bzz = value;
    }

    /**
     * 获取co2Clz属性的值。
     * 
     */
    public double getCo2Clz() {
        return co2Clz;
    }

    /**
     * 设置co2Clz属性的值。
     * 
     */
    public void setCo2Clz(double value) {
        this.co2Clz = value;
    }

    /**
     * 获取cobzz属性的值。
     * 
     */
    public double getCobzz() {
        return cobzz;
    }

    /**
     * 设置cobzz属性的值。
     * 
     */
    public void setCobzz(double value) {
        this.cobzz = value;
    }

    /**
     * 获取coclz属性的值。
     * 
     */
    public double getCoclz() {
        return coclz;
    }

    /**
     * 设置coclz属性的值。
     * 
     */
    public void setCoclz(double value) {
        this.coclz = value;
    }

    /**
     * 获取jcrq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getJcrq() {
        return jcrq;
    }

    /**
     * 设置jcrq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setJcrq(Date value) {
        this.jcrq = value;
    }

    /**
     * 获取jzhb属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzhb() {
        return jzhb;
    }

    /**
     * 设置jzhb属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzhb(String value) {
        this.jzhb = value;
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
     * 获取nobzz属性的值。
     * 
     */
    public double getNobzz() {
        return nobzz;
    }

    /**
     * 设置nobzz属性的值。
     * 
     */
    public void setNobzz(double value) {
        this.nobzz = value;
    }

    /**
     * 获取noclz属性的值。
     * 
     */
    public double getNoclz() {
        return noclz;
    }

    /**
     * 设置noclz属性的值。
     * 
     */
    public void setNoclz(double value) {
        this.noclz = value;
    }

}
