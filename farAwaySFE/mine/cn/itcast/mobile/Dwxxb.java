
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>dwxxb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
 * 
 * <pre>
 * &lt;complexType name="dwxxb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="cdpd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="cdsl" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="clxh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="ddjd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="ddwd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fxix" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="hphm" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzdz" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcs" type="{http://www.w3.org/2001/XMLSchema}int"/>
 *         &lt;element name="jzlx" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzmc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzrp" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzzt" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "dwxxb", propOrder = {
    "cdpd",
    "cdsl",
    "clxh",
    "ddjd",
    "ddwd",
    "fxix",
    "hphm",
    "jzbh",
    "jzdz",
    "jzjcs",
    "jzlx",
    "jzmc",
    "jzrp",
    "jzzt"
})
public class Dwxxb {

    protected double cdpd;
    protected int cdsl;
    protected String clxh;
    protected double ddjd;
    protected double ddwd;
    protected String fxix;
    protected String hphm;
    protected String jzbh;
    protected String jzdz;
    protected int jzjcs;
    protected String jzlx;
    protected String jzmc;
    protected String jzrp;
    protected String jzzt;

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
     * ��ȡcdsl���Ե�ֵ��
     * 
     */
    public int getCdsl() {
        return cdsl;
    }

    /**
     * ����cdsl���Ե�ֵ��
     * 
     */
    public void setCdsl(int value) {
        this.cdsl = value;
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
     * ��ȡfxix���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFxix() {
        return fxix;
    }

    /**
     * ����fxix���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFxix(String value) {
        this.fxix = value;
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
     * ��ȡjzdz���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzdz() {
        return jzdz;
    }

    /**
     * ����jzdz���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzdz(String value) {
        this.jzdz = value;
    }

    /**
     * ��ȡjzjcs���Ե�ֵ��
     * 
     */
    public int getJzjcs() {
        return jzjcs;
    }

    /**
     * ����jzjcs���Ե�ֵ��
     * 
     */
    public void setJzjcs(int value) {
        this.jzjcs = value;
    }

    /**
     * ��ȡjzlx���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzlx() {
        return jzlx;
    }

    /**
     * ����jzlx���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzlx(String value) {
        this.jzlx = value;
    }

    /**
     * ��ȡjzmc���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzmc() {
        return jzmc;
    }

    /**
     * ����jzmc���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzmc(String value) {
        this.jzmc = value;
    }

    /**
     * ��ȡjzrp���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzrp() {
        return jzrp;
    }

    /**
     * ����jzrp���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzrp(String value) {
        this.jzrp = value;
    }

    /**
     * ��ȡjzzt���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getJzzt() {
        return jzzt;
    }

    /**
     * ����jzzt���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setJzzt(String value) {
        this.jzzt = value;
    }

}
