
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbjcxxb complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="ycsbjcxxb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="bz" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="hcry" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jcdw" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jclx" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="jcrq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="sftg" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "ycsbjcxxb", propOrder = {
    "bz",
    "hcry",
    "jcdw",
    "jclx",
    "jcrq",
    "jzbh",
    "jzjcbh",
    "sftg"
})
public class Ycsbjcxxb {

    protected String bz;
    protected String hcry;
    protected String jcdw;
    protected int jclx;
    protected Date jcrq;
    protected String jzbh;
    protected String jzjcbh;
    protected String sftg;

    /**
     * 获取bz属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getBz() {
        return bz;
    }

    /**
     * 设置bz属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setBz(String value) {
        this.bz = value;
    }

    /**
     * 获取hcry属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHcry() {
        return hcry;
    }

    /**
     * 设置hcry属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHcry(String value) {
        this.hcry = value;
    }

    /**
     * 获取jcdw属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJcdw() {
        return jcdw;
    }

    /**
     * 设置jcdw属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJcdw(String value) {
        this.jcdw = value;
    }

    /**
     * 获取jclx属性的值。
     * 
     */
    public int getJclx() {
        return jclx;
    }

    /**
     * 设置jclx属性的值。
     * 
     */
    public void setJclx(int value) {
        this.jclx = value;
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
     * 获取sftg属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSftg() {
        return sftg;
    }

    /**
     * 设置sftg属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSftg(String value) {
        this.sftg = value;
    }

}
