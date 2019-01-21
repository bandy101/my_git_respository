
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>dwycxxb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
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
     * ��ȡcdbh���Ե�ֵ��
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
     * ����cdbh���Ե�ֵ��
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
     * ��ȡcsyyxq���Ե�ֵ��
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
     * ����csyyxq���Ե�ֵ��
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
     * ��ȡjzxtbh���Ե�ֵ��
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
     * ����jzxtbh���Ե�ֵ��
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
     * ��ȡjzxtmc���Ե�ֵ��
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
     * ����jzxtmc���Ե�ֵ��
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
     * ��ȡjzxtscc���Ե�ֵ��
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
     * ����jzxtscc���Ե�ֵ��
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
     * ��ȡjzxtxh���Ե�ֵ��
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
     * ����jzxtxh���Ե�ֵ��
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
     * ��ȡpdjscc���Ե�ֵ��
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
     * ����pdjscc���Ե�ֵ��
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
     * ��ȡpdjxh���Ե�ֵ��
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
     * ����pdjxh���Ե�ֵ��
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
     * ��ȡpdjyxq���Ե�ֵ��
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
     * ����pdjyxq���Ե�ֵ��
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
     * ��ȡqtcsyscc���Ե�ֵ��
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
     * ����qtcsyscc���Ե�ֵ��
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
     * ��ȡqtcsyxh���Ե�ֵ��
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
     * ����qtcsyxh���Ե�ֵ��
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
     * ��ȡqtcsyyxq���Ե�ֵ��
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
     * ����qtcsyyxq���Ե�ֵ��
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
     * ��ȡqxzscc���Ե�ֵ��
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
     * ����qxzscc���Ե�ֵ��
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
     * ��ȡqxzxh���Ե�ֵ��
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
     * ����qxzxh���Ե�ֵ��
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
     * ��ȡqxzyxq���Ե�ֵ��
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
     * ����qxzyxq���Ե�ֵ��
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
     * ��ȡsxjscc���Ե�ֵ��
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
     * ����sxjscc���Ե�ֵ��
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
     * ��ȡsxjxh���Ե�ֵ��
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
     * ����sxjxh���Ե�ֵ��
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
     * ��ȡsxjyxq���Ե�ֵ��
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
     * ����sxjyxq���Ե�ֵ��
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
     * ��ȡydjscc���Ե�ֵ��
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
     * ����ydjscc���Ե�ֵ��
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
     * ��ȡydjxh���Ե�ֵ��
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
     * ����ydjxh���Ե�ֵ��
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
     * ��ȡydjyxq���Ե�ֵ��
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
     * ����ydjyxq���Ե�ֵ��
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
