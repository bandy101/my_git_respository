
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.datatype.XMLGregorianCalendar;


/**
 * <p>jcsbxx complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="jcsbxx">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="d_InfraredIntensity" type="{http://www.w3.org/2001/XMLSchema}double" minOccurs="0"/>
 *         &lt;element name="d_InfraredTime" type="{http://www.w3.org/2001/XMLSchema}double" minOccurs="0"/>
 *         &lt;element name="d_Name" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="d_UltraviolenIntensity" type="{http://www.w3.org/2001/XMLSchema}double" minOccurs="0"/>
 *         &lt;element name="d_UltravionletTime" type="{http://www.w3.org/2001/XMLSchema}double" minOccurs="0"/>
 *         &lt;element name="d_time" type="{http://www.w3.org/2001/XMLSchema}dateTime" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "jcsbxx", propOrder = {
    "dInfraredIntensity",
    "dInfraredTime",
    "dName",
    "dUltraviolenIntensity",
    "dUltravionletTime",
    "dTime",
    "jzbh"
})
public class Jcsbxx {

    @XmlElement(name = "d_InfraredIntensity")
    protected Double dInfraredIntensity;
    @XmlElement(name = "d_InfraredTime")
    protected Double dInfraredTime;
    @XmlElement(name = "d_Name")
    protected String dName;
    @XmlElement(name = "d_UltraviolenIntensity")
    protected Double dUltraviolenIntensity;
    @XmlElement(name = "d_UltravionletTime")
    protected Double dUltravionletTime;
    @XmlElement(name = "d_time")
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar dTime;
    protected String jzbh;

    /**
     * 获取dInfraredIntensity属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Double }
     *     
     */
    public Double getDInfraredIntensity() {
        return dInfraredIntensity;
    }

    /**
     * 设置dInfraredIntensity属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Double }
     *     
     */
    public void setDInfraredIntensity(Double value) {
        this.dInfraredIntensity = value;
    }

    /**
     * 获取dInfraredTime属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Double }
     *     
     */
    public Double getDInfraredTime() {
        return dInfraredTime;
    }

    /**
     * 设置dInfraredTime属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Double }
     *     
     */
    public void setDInfraredTime(Double value) {
        this.dInfraredTime = value;
    }

    /**
     * 获取dName属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDName() {
        return dName;
    }

    /**
     * 设置dName属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDName(String value) {
        this.dName = value;
    }

    /**
     * 获取dUltraviolenIntensity属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Double }
     *     
     */
    public Double getDUltraviolenIntensity() {
        return dUltraviolenIntensity;
    }

    /**
     * 设置dUltraviolenIntensity属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Double }
     *     
     */
    public void setDUltraviolenIntensity(Double value) {
        this.dUltraviolenIntensity = value;
    }

    /**
     * 获取dUltravionletTime属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Double }
     *     
     */
    public Double getDUltravionletTime() {
        return dUltravionletTime;
    }

    /**
     * 设置dUltravionletTime属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Double }
     *     
     */
    public void setDUltravionletTime(Double value) {
        this.dUltravionletTime = value;
    }

    /**
     * 获取dTime属性的值。
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getDTime() {
        return dTime;
    }

    /**
     * 设置dTime属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setDTime(XMLGregorianCalendar value) {
        this.dTime = value;
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

}
