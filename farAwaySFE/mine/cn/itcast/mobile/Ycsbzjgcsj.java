
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbzjgcsj complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
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
     * ��ȡbwbzz���Ե�ֵ��
     * 
     */
    public double getBwbzz() {
        return bwbzz;
    }

    /**
     * ����bwbzz���Ե�ֵ��
     * 
     */
    public void setBwbzz(double value) {
        this.bwbzz = value;
    }

    /**
     * ��ȡbwclz���Ե�ֵ��
     * 
     */
    public double getBwclz() {
        return bwclz;
    }

    /**
     * ����bwclz���Ե�ֵ��
     * 
     */
    public void setBwclz(double value) {
        this.bwclz = value;
    }

    /**
     * ��ȡco2Bzz���Ե�ֵ��
     * 
     */
    public double getCo2Bzz() {
        return co2Bzz;
    }

    /**
     * ����co2Bzz���Ե�ֵ��
     * 
     */
    public void setCo2Bzz(double value) {
        this.co2Bzz = value;
    }

    /**
     * ��ȡco2Clz���Ե�ֵ��
     * 
     */
    public double getCo2Clz() {
        return co2Clz;
    }

    /**
     * ����co2Clz���Ե�ֵ��
     * 
     */
    public void setCo2Clz(double value) {
        this.co2Clz = value;
    }

    /**
     * ��ȡcobzz���Ե�ֵ��
     * 
     */
    public double getCobzz() {
        return cobzz;
    }

    /**
     * ����cobzz���Ե�ֵ��
     * 
     */
    public void setCobzz(double value) {
        this.cobzz = value;
    }

    /**
     * ��ȡcoclz���Ե�ֵ��
     * 
     */
    public double getCoclz() {
        return coclz;
    }

    /**
     * ����coclz���Ե�ֵ��
     * 
     */
    public void setCoclz(double value) {
        this.coclz = value;
    }

    /**
     * ��ȡdexbzz���Ե�ֵ��
     * 
     */
    public double getDexbzz() {
        return dexbzz;
    }

    /**
     * ����dexbzz���Ե�ֵ��
     * 
     */
    public void setDexbzz(double value) {
        this.dexbzz = value;
    }

    /**
     * ��ȡdexclz���Ե�ֵ��
     * 
     */
    public double getDexclz() {
        return dexclz;
    }

    /**
     * ����dexclz���Ե�ֵ��
     * 
     */
    public void setDexclz(double value) {
        this.dexclz = value;
    }

    /**
     * ��ȡjzbh���Ե�ֵ��
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
     * ����jzbh���Ե�ֵ��
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
     * ��ȡjzjcbh���Ե�ֵ��
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
     * ����jzjcbh���Ե�ֵ��
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
     * ��ȡnobzz���Ե�ֵ��
     * 
     */
    public double getNobzz() {
        return nobzz;
    }

    /**
     * ����nobzz���Ե�ֵ��
     * 
     */
    public void setNobzz(double value) {
        this.nobzz = value;
    }

    /**
     * ��ȡnoclz���Ե�ֵ��
     * 
     */
    public double getNoclz() {
        return noclz;
    }

    /**
     * ����noclz���Ե�ֵ��
     * 
     */
    public void setNoclz(double value) {
        this.noclz = value;
    }

    /**
     * ��ȡydp1Bzz���Ե�ֵ��
     * 
     */
    public double getYdp1Bzz() {
        return ydp1Bzz;
    }

    /**
     * ����ydp1Bzz���Ե�ֵ��
     * 
     */
    public void setYdp1Bzz(double value) {
        this.ydp1Bzz = value;
    }

    /**
     * ��ȡydp1Clz���Ե�ֵ��
     * 
     */
    public double getYdp1Clz() {
        return ydp1Clz;
    }

    /**
     * ����ydp1Clz���Ե�ֵ��
     * 
     */
    public void setYdp1Clz(double value) {
        this.ydp1Clz = value;
    }

    /**
     * ��ȡydp2Bzz���Ե�ֵ��
     * 
     */
    public double getYdp2Bzz() {
        return ydp2Bzz;
    }

    /**
     * ����ydp2Bzz���Ե�ֵ��
     * 
     */
    public void setYdp2Bzz(double value) {
        this.ydp2Bzz = value;
    }

    /**
     * ��ȡydp2Clz���Ե�ֵ��
     * 
     */
    public double getYdp2Clz() {
        return ydp2Clz;
    }

    /**
     * ����ydp2Clz���Ե�ֵ��
     * 
     */
    public void setYdp2Clz(double value) {
        this.ydp2Clz = value;
    }

    /**
     * ��ȡydp3Bzz���Ե�ֵ��
     * 
     */
    public double getYdp3Bzz() {
        return ydp3Bzz;
    }

    /**
     * ����ydp3Bzz���Ե�ֵ��
     * 
     */
    public void setYdp3Bzz(double value) {
        this.ydp3Bzz = value;
    }

    /**
     * ��ȡydp3Clz���Ե�ֵ��
     * 
     */
    public double getYdp3Clz() {
        return ydp3Clz;
    }

    /**
     * ����ydp3Clz���Ե�ֵ��
     * 
     */
    public void setYdp3Clz(double value) {
        this.ydp3Clz = value;
    }

    /**
     * ��ȡydp4Bzz���Ե�ֵ��
     * 
     */
    public double getYdp4Bzz() {
        return ydp4Bzz;
    }

    /**
     * ����ydp4Bzz���Ե�ֵ��
     * 
     */
    public void setYdp4Bzz(double value) {
        this.ydp4Bzz = value;
    }

    /**
     * ��ȡydp4Clz���Ե�ֵ��
     * 
     */
    public double getYdp4Clz() {
        return ydp4Clz;
    }

    /**
     * ����ydp4Clz���Ե�ֵ��
     * 
     */
    public void setYdp4Clz(double value) {
        this.ydp4Clz = value;
    }

    /**
     * ��ȡydp5Bzz���Ե�ֵ��
     * 
     */
    public double getYdp5Bzz() {
        return ydp5Bzz;
    }

    /**
     * ����ydp5Bzz���Ե�ֵ��
     * 
     */
    public void setYdp5Bzz(double value) {
        this.ydp5Bzz = value;
    }

    /**
     * ��ȡydp5Clz���Ե�ֵ��
     * 
     */
    public double getYdp5Clz() {
        return ydp5Clz;
    }

    /**
     * ����ydp5Clz���Ե�ֵ��
     * 
     */
    public void setYdp5Clz(double value) {
        this.ydp5Clz = value;
    }

    /**
     * ��ȡzjrq���Ե�ֵ��
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
     * ����zjrq���Ե�ֵ��
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
