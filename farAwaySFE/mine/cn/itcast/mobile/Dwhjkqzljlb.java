
package cn.itcast.mobile;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>dwhjkqzljlb complex type�� Java �ࡣ
 * 
 * <p>����ģʽƬ��ָ�������ڴ����е�Ԥ�����ݡ�
 * 
 * <pre>
 * &lt;complexType name="dwhjkqzljlb">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="co" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="dqy" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fs" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="fx" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="jzbh" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="no2" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="o3" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="pm10" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="pm25" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="sd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="so2" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *         &lt;element name="testNo" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="wd" type="{http://www.w3.org/2001/XMLSchema}double"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "dwhjkqzljlb", propOrder = {
    "co",
    "dqy",
    "fs",
    "fx",
    "jzbh",
    "no2",
    "o3",
    "pm10",
    "pm25",
    "sd",
    "so2",
    "testNo",
    "wd"
})
public class Dwhjkqzljlb {

    protected double co;
    protected double dqy;
    protected double fs;
    protected String fx;
    protected String jzbh;
    protected double no2;
    protected double o3;
    protected double pm10;
    protected double pm25;
    protected double sd;
    protected double so2;
    protected String testNo;
    protected double wd;

    /**
     * ��ȡco���Ե�ֵ��
     * 
     */
    public double getCo() {
        return co;
    }

    /**
     * ����co���Ե�ֵ��
     * 
     */
    public void setCo(double value) {
        this.co = value;
    }

    /**
     * ��ȡdqy���Ե�ֵ��
     * 
     */
    public double getDqy() {
        return dqy;
    }

    /**
     * ����dqy���Ե�ֵ��
     * 
     */
    public void setDqy(double value) {
        this.dqy = value;
    }

    /**
     * ��ȡfs���Ե�ֵ��
     * 
     */
    public double getFs() {
        return fs;
    }

    /**
     * ����fs���Ե�ֵ��
     * 
     */
    public void setFs(double value) {
        this.fs = value;
    }

    /**
     * ��ȡfx���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFx() {
        return fx;
    }

    /**
     * ����fx���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFx(String value) {
        this.fx = value;
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
     * ��ȡno2���Ե�ֵ��
     * 
     */
    public double getNo2() {
        return no2;
    }

    /**
     * ����no2���Ե�ֵ��
     * 
     */
    public void setNo2(double value) {
        this.no2 = value;
    }

    /**
     * ��ȡo3���Ե�ֵ��
     * 
     */
    public double getO3() {
        return o3;
    }

    /**
     * ����o3���Ե�ֵ��
     * 
     */
    public void setO3(double value) {
        this.o3 = value;
    }

    /**
     * ��ȡpm10���Ե�ֵ��
     * 
     */
    public double getPm10() {
        return pm10;
    }

    /**
     * ����pm10���Ե�ֵ��
     * 
     */
    public void setPm10(double value) {
        this.pm10 = value;
    }

    /**
     * ��ȡpm25���Ե�ֵ��
     * 
     */
    public double getPm25() {
        return pm25;
    }

    /**
     * ����pm25���Ե�ֵ��
     * 
     */
    public void setPm25(double value) {
        this.pm25 = value;
    }

    /**
     * ��ȡsd���Ե�ֵ��
     * 
     */
    public double getSd() {
        return sd;
    }

    /**
     * ����sd���Ե�ֵ��
     * 
     */
    public void setSd(double value) {
        this.sd = value;
    }

    /**
     * ��ȡso2���Ե�ֵ��
     * 
     */
    public double getSo2() {
        return so2;
    }

    /**
     * ����so2���Ե�ֵ��
     * 
     */
    public void setSo2(double value) {
        this.so2 = value;
    }

    /**
     * ��ȡtestNo���Ե�ֵ��
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTestNo() {
        return testNo;
    }

    /**
     * ����testNo���Ե�ֵ��
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTestNo(String value) {
        this.testNo = value;
    }

    /**
     * ��ȡwd���Ե�ֵ��
     * 
     */
    public double getWd() {
        return wd;
    }

    /**
     * ����wd���Ե�ֵ��
     * 
     */
    public void setWd(double value) {
        this.wd = value;
    }

}
