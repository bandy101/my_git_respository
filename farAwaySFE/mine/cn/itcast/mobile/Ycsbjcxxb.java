
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbjcxxb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
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
     * ��ȡbz���Ե�ֵ��
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
     * ����bz���Ե�ֵ��
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
     * ��ȡhcry���Ե�ֵ��
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
     * ����hcry���Ե�ֵ��
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
     * ��ȡjcdw���Ե�ֵ��
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
     * ����jcdw���Ե�ֵ��
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
     * ��ȡjclx���Ե�ֵ��
     * 
     */
    public int getJclx() {
        return jclx;
    }

    /**
     * ����jclx���Ե�ֵ��
     * 
     */
    public void setJclx(int value) {
        this.jclx = value;
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
     * ��ȡsftg���Ե�ֵ��
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
     * ����sftg���Ե�ֵ��
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
