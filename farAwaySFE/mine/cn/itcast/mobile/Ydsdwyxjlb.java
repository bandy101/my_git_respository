
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ydsdwyxjlb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
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
     * ��ȡcbbh���Ե�ֵ��
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
     * ����cbbh���Ե�ֵ��
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
     * ��ȡcdpd���Ե�ֵ��
     * 
     */
    public double getCdpd() {
        return cdpd;
    }

    /**
     * ����cdpd���Ե�ֵ��
     * 
     */
    public void setCdpd(double value) {
        this.cdpd = value;
    }

    /**
     * ��ȡddjd���Ե�ֵ��
     * 
     */
    public double getDdjd() {
        return ddjd;
    }

    /**
     * ����ddjd���Ե�ֵ��
     * 
     */
    public void setDdjd(double value) {
        this.ddjd = value;
    }

    /**
     * ��ȡddwd���Ե�ֵ��
     * 
     */
    public double getDdwd() {
        return ddwd;
    }

    /**
     * ����ddwd���Ե�ֵ��
     * 
     */
    public void setDdwd(double value) {
        this.ddwd = value;
    }

    /**
     * ��ȡfxlx���Ե�ֵ��
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
     * ����fxlx���Ե�ֵ��
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
     * ��ȡjzrzbh���Ե�ֵ��
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
     * ����jzrzbh���Ե�ֵ��
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
     * ��ȡzzdz���Ե�ֵ��
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
     * ����zzdz���Ե�ֵ��
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
