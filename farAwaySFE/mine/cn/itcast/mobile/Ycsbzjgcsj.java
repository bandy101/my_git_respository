
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbzjgcsj complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="ycsbzjgcsj">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="bwbzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="bwclz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="co2bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="co2clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="cobzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="coclz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="dexbzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="dexclz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="nobzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="noclz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp1bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp1clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp2bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp2clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp3bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp3clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp4bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp4clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp5bzz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ydp5clz" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="zjrq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "ycsbzjgcsj", propOrder = {
    "bwbzz",
    "bwclz",
    "co2Bzz",
    "co2Clz",
    "cobzz",
    "coclz",
    "dexbzz",
    "dexclz",
    "jzbh",
    "jzjcbh",
    "nobzz",
    "noclz",
    "ydp1Bzz",
    "ydp1Clz",
    "ydp2Bzz",
    "ydp2Clz",
    "ydp3Bzz",
    "ydp3Clz",
    "ydp4Bzz",
    "ydp4Clz",
    "ydp5Bzz",
    "ydp5Clz",
    "zjrq"
})
public class Ycsbzjgcsj {

    protected double bwbzz;
    protected double bwclz;
    @XmlElement(name = "co2bzz")
    protected double co2Bzz;
    @XmlElement(name = "co2clz")
    protected double co2Clz;
    protected double cobzz;
    protected double coclz;
    protected double dexbzz;
    protected double dexclz;
    protected String jzbh;
    protected String jzjcbh;
    protected double nobzz;
    protected double noclz;
    @XmlElement(name = "ydp1bzz")
    protected double ydp1Bzz;
    @XmlElement(name = "ydp1clz")
    protected double ydp1Clz;
    @XmlElement(name = "ydp2bzz")
    protected double ydp2Bzz;
    @XmlElement(name = "ydp2clz")
    protected double ydp2Clz;
    @XmlElement(name = "ydp3bzz")
    protected double ydp3Bzz;
    @XmlElement(name = "ydp3clz")
    protected double ydp3Clz;
    @XmlElement(name = "ydp4bzz")
    protected double ydp4Bzz;
    @XmlElement(name = "ydp4clz")
    protected double ydp4Clz;
    @XmlElement(name = "ydp5bzz")
    protected double ydp5Bzz;
    @XmlElement(name = "ydp5clz")
    protected double ydp5Clz;
    protected Date zjrq;

    /**
     * 获取bwbzz属性的值。
     * 
     */
    public double getBwbzz() {
        return bwbzz;
    }

    /**
     * 设置bwbzz属性的值。
     * 
     */
    public void setBwbzz(double value) {
        this.bwbzz = value;
    }

    /**
     * 获取bwclz属性的值。
     * 
     */
    public double getBwclz() {
        return bwclz;
    }

    /**
     * 设置bwclz属性的值。
     * 
     */
    public void setBwclz(double value) {
        this.bwclz = value;
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
     * 获取dexbzz属性的值。
     * 
     */
    public double getDexbzz() {
        return dexbzz;
    }

    /**
     * 设置dexbzz属性的值。
     * 
     */
    public void setDexbzz(double value) {
        this.dexbzz = value;
    }

    /**
     * 获取dexclz属性的值。
     * 
     */
    public double getDexclz() {
        return dexclz;
    }

    /**
     * 设置dexclz属性的值。
     * 
     */
    public void setDexclz(double value) {
        this.dexclz = value;
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

    /**
     * 获取ydp1Bzz属性的值。
     * 
     */
    public double getYdp1Bzz() {
        return ydp1Bzz;
    }

    /**
     * 设置ydp1Bzz属性的值。
     * 
     */
    public void setYdp1Bzz(double value) {
        this.ydp1Bzz = value;
    }

    /**
     * 获取ydp1Clz属性的值。
     * 
     */
    public double getYdp1Clz() {
        return ydp1Clz;
    }

    /**
     * 设置ydp1Clz属性的值。
     * 
     */
    public void setYdp1Clz(double value) {
        this.ydp1Clz = value;
    }

    /**
     * 获取ydp2Bzz属性的值。
     * 
     */
    public double getYdp2Bzz() {
        return ydp2Bzz;
    }

    /**
     * 设置ydp2Bzz属性的值。
     * 
     */
    public void setYdp2Bzz(double value) {
        this.ydp2Bzz = value;
    }

    /**
     * 获取ydp2Clz属性的值。
     * 
     */
    public double getYdp2Clz() {
        return ydp2Clz;
    }

    /**
     * 设置ydp2Clz属性的值。
     * 
     */
    public void setYdp2Clz(double value) {
        this.ydp2Clz = value;
    }

    /**
     * 获取ydp3Bzz属性的值。
     * 
     */
    public double getYdp3Bzz() {
        return ydp3Bzz;
    }

    /**
     * 设置ydp3Bzz属性的值。
     * 
     */
    public void setYdp3Bzz(double value) {
        this.ydp3Bzz = value;
    }

    /**
     * 获取ydp3Clz属性的值。
     * 
     */
    public double getYdp3Clz() {
        return ydp3Clz;
    }

    /**
     * 设置ydp3Clz属性的值。
     * 
     */
    public void setYdp3Clz(double value) {
        this.ydp3Clz = value;
    }

    /**
     * 获取ydp4Bzz属性的值。
     * 
     */
    public double getYdp4Bzz() {
        return ydp4Bzz;
    }

    /**
     * 设置ydp4Bzz属性的值。
     * 
     */
    public void setYdp4Bzz(double value) {
        this.ydp4Bzz = value;
    }

    /**
     * 获取ydp4Clz属性的值。
     * 
     */
    public double getYdp4Clz() {
        return ydp4Clz;
    }

    /**
     * 设置ydp4Clz属性的值。
     * 
     */
    public void setYdp4Clz(double value) {
        this.ydp4Clz = value;
    }

    /**
     * 获取ydp5Bzz属性的值。
     * 
     */
    public double getYdp5Bzz() {
        return ydp5Bzz;
    }

    /**
     * 设置ydp5Bzz属性的值。
     * 
     */
    public void setYdp5Bzz(double value) {
        this.ydp5Bzz = value;
    }

    /**
     * 获取ydp5Clz属性的值。
     * 
     */
    public double getYdp5Clz() {
        return ydp5Clz;
    }

    /**
     * 设置ydp5Clz属性的值。
     * 
     */
    public void setYdp5Clz(double value) {
        this.ydp5Clz = value;
    }

    /**
     * 获取zjrq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getZjrq() {
        return zjrq;
    }

    /**
     * 设置zjrq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setZjrq(Date value) {
        this.zjrq = value;
    }

}
