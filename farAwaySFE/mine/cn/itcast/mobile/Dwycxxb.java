
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>dwycxxb complex type的 Java 类。
 * 
 * <p>以下模式片段指定包含在此类中的预期内容。
 * 
 * <pre>
 * &lt;complexType name="dwycxxb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="cdbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="csyyxq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzxtbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzxtmc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzxtscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzxtxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="pdjscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="pdjxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="pdjyxq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="qtcsyscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="qtcsyxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="qtcsyyxq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="qxzscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="qxzxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="qxzyxq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="sxjscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="sxjxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="sxjyxq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *         &lt;element name="ydjscc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="ydjxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="ydjyxq" type="{http://webservice.shengwei.com/}date" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "dwycxxb", propOrder = {
    "cdbh",
    "csyyxq",
    "jzbh",
    "jzjcbh",
    "jzxtbh",
    "jzxtmc",
    "jzxtscc",
    "jzxtxh",
    "pdjscc",
    "pdjxh",
    "pdjyxq",
    "qtcsyscc",
    "qtcsyxh",
    "qtcsyyxq",
    "qxzscc",
    "qxzxh",
    "qxzyxq",
    "sxjscc",
    "sxjxh",
    "sxjyxq",
    "ydjscc",
    "ydjxh",
    "ydjyxq"
})
public class Dwycxxb {

    protected String cdbh;
    protected Date csyyxq;
    protected String jzbh;
    protected String jzjcbh;
    protected String jzxtbh;
    protected String jzxtmc;
    protected String jzxtscc;
    protected String jzxtxh;
    protected String pdjscc;
    protected String pdjxh;
    protected Date pdjyxq;
    protected String qtcsyscc;
    protected String qtcsyxh;
    protected Date qtcsyyxq;
    protected String qxzscc;
    protected String qxzxh;
    protected Date qxzyxq;
    protected String sxjscc;
    protected String sxjxh;
    protected Date sxjyxq;
    protected String ydjscc;
    protected String ydjxh;
    protected Date ydjyxq;

    /**
     * 获取cdbh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCdbh() {
        return cdbh;
    }

    /**
     * 设置cdbh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCdbh(String value) {
        this.cdbh = value;
    }

    /**
     * 获取csyyxq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getCsyyxq() {
        return csyyxq;
    }

    /**
     * 设置csyyxq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setCsyyxq(Date value) {
        this.csyyxq = value;
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
     * 获取jzxtbh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzxtbh() {
        return jzxtbh;
    }

    /**
     * 设置jzxtbh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzxtbh(String value) {
        this.jzxtbh = value;
    }

    /**
     * 获取jzxtmc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzxtmc() {
        return jzxtmc;
    }

    /**
     * 设置jzxtmc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzxtmc(String value) {
        this.jzxtmc = value;
    }

    /**
     * 获取jzxtscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzxtscc() {
        return jzxtscc;
    }

    /**
     * 设置jzxtscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzxtscc(String value) {
        this.jzxtscc = value;
    }

    /**
     * 获取jzxtxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzxtxh() {
        return jzxtxh;
    }

    /**
     * 设置jzxtxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzxtxh(String value) {
        this.jzxtxh = value;
    }

    /**
     * 获取pdjscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPdjscc() {
        return pdjscc;
    }

    /**
     * 设置pdjscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPdjscc(String value) {
        this.pdjscc = value;
    }

    /**
     * 获取pdjxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPdjxh() {
        return pdjxh;
    }

    /**
     * 设置pdjxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPdjxh(String value) {
        this.pdjxh = value;
    }

    /**
     * 获取pdjyxq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getPdjyxq() {
        return pdjyxq;
    }

    /**
     * 设置pdjyxq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setPdjyxq(Date value) {
        this.pdjyxq = value;
    }

    /**
     * 获取qtcsyscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQtcsyscc() {
        return qtcsyscc;
    }

    /**
     * 设置qtcsyscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQtcsyscc(String value) {
        this.qtcsyscc = value;
    }

    /**
     * 获取qtcsyxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQtcsyxh() {
        return qtcsyxh;
    }

    /**
     * 设置qtcsyxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQtcsyxh(String value) {
        this.qtcsyxh = value;
    }

    /**
     * 获取qtcsyyxq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getQtcsyyxq() {
        return qtcsyyxq;
    }

    /**
     * 设置qtcsyyxq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setQtcsyyxq(Date value) {
        this.qtcsyyxq = value;
    }

    /**
     * 获取qxzscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQxzscc() {
        return qxzscc;
    }

    /**
     * 设置qxzscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQxzscc(String value) {
        this.qxzscc = value;
    }

    /**
     * 获取qxzxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQxzxh() {
        return qxzxh;
    }

    /**
     * 设置qxzxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQxzxh(String value) {
        this.qxzxh = value;
    }

    /**
     * 获取qxzyxq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getQxzyxq() {
        return qxzyxq;
    }

    /**
     * 设置qxzyxq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setQxzyxq(Date value) {
        this.qxzyxq = value;
    }

    /**
     * 获取sxjscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSxjscc() {
        return sxjscc;
    }

    /**
     * 设置sxjscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSxjscc(String value) {
        this.sxjscc = value;
    }

    /**
     * 获取sxjxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSxjxh() {
        return sxjxh;
    }

    /**
     * 设置sxjxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSxjxh(String value) {
        this.sxjxh = value;
    }

    /**
     * 获取sxjyxq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getSxjyxq() {
        return sxjyxq;
    }

    /**
     * 设置sxjyxq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setSxjyxq(Date value) {
        this.sxjyxq = value;
    }

    /**
     * 获取ydjscc属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getYdjscc() {
        return ydjscc;
    }

    /**
     * 设置ydjscc属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setYdjscc(String value) {
        this.ydjscc = value;
    }

    /**
     * 获取ydjxh属性的值。
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getYdjxh() {
        return ydjxh;
    }

    /**
     * 设置ydjxh属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setYdjxh(String value) {
        this.ydjxh = value;
    }

    /**
     * 获取ydjyxq属性的值。
     * 
     * @return
     *     possible object is
     *     {@link Date }
     *     
     */
    public Date getYdjyxq() {
        return ydjyxq;
    }

    /**
     * 设置ydjyxq属性的值。
     * 
     * @param value
     *     allowed object is
     *     {@link Date }
     *     
     */
    public void setYdjyxq(Date value) {
        this.ydjyxq = value;
    }

}
