
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbjtjcgcsj complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
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
     * ��ȡbolq���Ե�ֵ��
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
     * ����bolq���Ե�ֵ��
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
     * ��ȡjcrq���Ե�ֵ��
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
     * ����jcrq���Ե�ֵ��
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
     * ��ȡjzhb���Ե�ֵ��
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
     * ����jzhb���Ե�ֵ��
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

}
