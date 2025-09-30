package com.legacy.enterprise.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.DecimalMin;

/**
 * TaxDeduction Entity - Complex tax calculation logic
 * Handles various types of tax deductions and exemptions
 * 
 * @author Legacy Developer (2012)
 * @version 1.2
 */
@Entity
@Table(name = "TAX_DEDUCTION", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "TaxDeduction.findByEmployee", 
                query = "SELECT t FROM TaxDeduction t WHERE t.employee.id = :employeeId"),
    @NamedQuery(name = "TaxDeduction.findByTaxYear", 
                query = "SELECT t FROM TaxDeduction t WHERE t.taxYear = :year"),
    @NamedQuery(name = "TaxDeduction.findByType", 
                query = "SELECT t FROM TaxDeduction t WHERE t.deductionType = :type")
})
@SequenceGenerator(name = "TAX_DEDUCTION_SEQ", sequenceName = "TAX_DEDUCTION_SEQUENCE", allocationSize = 1)
public class TaxDeduction implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "TAX_DEDUCTION_SEQ")
    @Column(name = "TAX_DEDUCTION_ID")
    private Long id;
    
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "EMPLOYEE_ID", nullable = false)
    private Employee employee;
    
    @NotNull
    @Column(name = "DEDUCTION_TYPE", nullable = false, length = 50)
    private String deductionType; // FEDERAL, STATE, LOCAL, SOCIAL_SECURITY, MEDICARE
    
    @NotNull
    @Column(name = "DEDUCTION_NAME", nullable = false, length = 100)
    private String deductionName;
    
    @NotNull
    @DecimalMin("0.00")
    @Column(name = "AMOUNT", nullable = false, precision = 10, scale = 2)
    private BigDecimal amount;
    
    @NotNull
    @Column(name = "TAX_YEAR", nullable = false)
    private Integer taxYear;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "EFFECTIVE_DATE", nullable = false)
    private Date effectiveDate;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "END_DATE")
    private Date endDate;
    
    @Column(name = "EXEMPTIONS")
    private Integer exemptions;
    
    @Column(name = "DEPENDENTS")
    private Integer dependents;
    
    @Column(name = "FILING_STATUS", length = 20)
    private String filingStatus; // SINGLE, MARRIED_JOINT, MARRIED_SEPARATE, HEAD_OF_HOUSEHOLD
    
    @Column(name = "ADDITIONAL_WITHHOLDING", precision = 10, scale = 2)
    private BigDecimal additionalWithholding;
    
    @Column(name = "ACTIVE", nullable = false)
    private Boolean active = true;
    
    @Column(name = "AUTO_CALCULATE", nullable = false)
    private Boolean autoCalculate = true;
    
    @Column(name = "MANUAL_OVERRIDE")
    private Boolean manualOverride = false;
    
    @Column(name = "OVERRIDE_REASON", length = 200)
    private String overrideReason;
    
    @Column(name = "OVERRIDE_BY", length = 50)
    private String overrideBy;
    
    @Column(name = "OVERRIDE_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date overrideDate;
    
    @Column(name = "NOTES", length = 500)
    private String notes;
    
    // Legacy fields
    @Column(name = "LEGACY_TAX_ID", length = 20)
    private String legacyTaxId;
    
    @Column(name = "LEGACY_SYSTEM_FLAG")
    private Boolean legacySystemFlag = false;
    
    // Constructors
    public TaxDeduction() {
    }
    
    public TaxDeduction(Employee employee, String deductionType, String deductionName, 
                       BigDecimal amount, Integer taxYear, Date effectiveDate) {
        this.employee = employee;
        this.deductionType = deductionType;
        this.deductionName = deductionName;
        this.amount = amount;
        this.taxYear = taxYear;
        this.effectiveDate = effectiveDate;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Employee getEmployee() {
        return employee;
    }
    
    public void setEmployee(Employee employee) {
        this.employee = employee;
    }
    
    public String getDeductionType() {
        return deductionType;
    }
    
    public void setDeductionType(String deductionType) {
        this.deductionType = deductionType;
    }
    
    public String getDeductionName() {
        return deductionName;
    }
    
    public void setDeductionName(String deductionName) {
        this.deductionName = deductionName;
    }
    
    public BigDecimal getAmount() {
        return amount;
    }
    
    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }
    
    public Integer getTaxYear() {
        return taxYear;
    }
    
    public void setTaxYear(Integer taxYear) {
        this.taxYear = taxYear;
    }
    
    public Date getEffectiveDate() {
        return effectiveDate;
    }
    
    public void setEffectiveDate(Date effectiveDate) {
        this.effectiveDate = effectiveDate;
    }
    
    public Date getEndDate() {
        return endDate;
    }
    
    public void setEndDate(Date endDate) {
        this.endDate = endDate;
    }
    
    public Integer getExemptions() {
        return exemptions;
    }
    
    public void setExemptions(Integer exemptions) {
        this.exemptions = exemptions;
    }
    
    public Integer getDependents() {
        return dependents;
    }
    
    public void setDependents(Integer dependents) {
        this.dependents = dependents;
    }
    
    public String getFilingStatus() {
        return filingStatus;
    }
    
    public void setFilingStatus(String filingStatus) {
        this.filingStatus = filingStatus;
    }
    
    public BigDecimal getAdditionalWithholding() {
        return additionalWithholding;
    }
    
    public void setAdditionalWithholding(BigDecimal additionalWithholding) {
        this.additionalWithholding = additionalWithholding;
    }
    
    public Boolean getActive() {
        return active;
    }
    
    public void setActive(Boolean active) {
        this.active = active;
    }
    
    public Boolean getAutoCalculate() {
        return autoCalculate;
    }
    
    public void setAutoCalculate(Boolean autoCalculate) {
        this.autoCalculate = autoCalculate;
    }
    
    public Boolean getManualOverride() {
        return manualOverride;
    }
    
    public void setManualOverride(Boolean manualOverride) {
        this.manualOverride = manualOverride;
    }
    
    public String getOverrideReason() {
        return overrideReason;
    }
    
    public void setOverrideReason(String overrideReason) {
        this.overrideReason = overrideReason;
    }
    
    public String getOverrideBy() {
        return overrideBy;
    }
    
    public void setOverrideBy(String overrideBy) {
        this.overrideBy = overrideBy;
    }
    
    public Date getOverrideDate() {
        return overrideDate;
    }
    
    public void setOverrideDate(Date overrideDate) {
        this.overrideDate = overrideDate;
    }
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    public String getLegacyTaxId() {
        return legacyTaxId;
    }
    
    public void setLegacyTaxId(String legacyTaxId) {
        this.legacyTaxId = legacyTaxId;
    }
    
    public Boolean getLegacySystemFlag() {
        return legacySystemFlag;
    }
    
    public void setLegacySystemFlag(Boolean legacySystemFlag) {
        this.legacySystemFlag = legacySystemFlag;
    }
    
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof TaxDeduction)) {
            return false;
        }
        TaxDeduction other = (TaxDeduction) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.TaxDeduction[ id=" + id + " ]";
    }
}
