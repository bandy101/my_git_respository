
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>clsjxxb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
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
     * ��ȡccdjrq���Ե�ֵ��
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
     * ����ccdjrq���Ե�ֵ��
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
     * ��ȡclscc���Ե�ֵ��
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
     * ����clscc���Ե�ֵ��
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
     * ��ȡclxh���Ե�ֵ��
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
     * ����clxh���Ե�ֵ��
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
     * ��ȡhphm���Ե�ֵ��
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
     * ����hphm���Ե�ֵ��
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
     * ��ȡhpys���Ե�ֵ��
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
     * ����hpys���Ե�ֵ��
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
     * ��ȡhpzl���Ե�ֵ��
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
     * ����hpzl���Ե�ֵ��
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
     * ��ȡpf���Ե�ֵ��
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
     * ����pf���Ե�ֵ��
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
     * ��ȡrlzl���Ե�ֵ��
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
     * ����rlzl���Ե�ֵ��
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
     * ��ȡscjyjg���Ե�ֵ��
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
     * ����scjyjg���Ե�ֵ��
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
     * ��ȡscjyrq���Ե�ֵ��
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
     * ����scjyrq���Ե�ֵ��
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
     * ��ȡsyxz���Ե�ֵ��
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
     * ����syxz���Ե�ֵ��
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
     * ��ȡvin���Ե�ֵ��
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
     * ����vin���Ե�ֵ��
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
     * ��ȡxzcode���Ե�ֵ��
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
     * ����xzcode���Ե�ֵ��
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
