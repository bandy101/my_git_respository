
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>ycsbzjxxb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
 * 
 * <pre>
 * &lt;complexType name="ycsbzjxxb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="bz" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzjcbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="sftg" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
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
@XmlType(name = "ycsbzjxxb", propOrder = {
    "bz",
    "jzbh",
    "jzjcbh",
    "sftg",
    "zjrq"
})
public class Ycsbzjxxb {

    protected String bz;
    protected String jzbh;
    protected String jzjcbh;
    protected String sftg;
    protected Date zjrq;

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
