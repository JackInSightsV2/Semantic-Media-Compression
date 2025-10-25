package com.legacy.enterprise.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.DecimalMin;

/**
 * BenefitEnrollment Entity - Complex benefit enrollment logic
 * This class has grown over time with various benefit types and rules
 * 
 * @author Legacy Developer (2010)
 * @version 1.5
 */
@Entity
@Table(name = "BENEFIT_ENROLLMENT", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "BenefitEnrollment.findByEmployee", 
                query = "SELECT b FROM BenefitEnrollment b WHERE b.employee.id = :employeeId"),
    @NamedQuery(name = "BenefitEnrollment.findActive", 
                query = "SELECT b FROM BenefitEnrollment b WHERE b.active = true"),
    @NamedQuery(name = "BenefitEnrollment.findByBenefitType", 
                query = "SELECT b FROM BenefitEnrollment b WHERE b.benefitType = :type")
})
@SequenceGenerator(name = "BENEFIT_SEQ", sequenceName = "BENEFIT_SEQUENCE", allocationSize = 1)
public class BenefitEnrollment implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "BENEFIT_SEQ")
    @Column(name = "BENEFIT_ID")
    private Long id;
    
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "EMPLOYEE_ID", nullable = false)
    private Employee employee;
    
    @NotNull
    @Column(name = "BENEFIT_TYPE", nullable = false, length = 50)
    private String benefitType; // HEALTH, DENTAL, VISION, LIFE, DISABILITY, RETIREMENT
    
    @NotNull
    @Column(name = "BENEFIT_NAME", nullable = false, length = 100)
    private String benefitName;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "ENROLLMENT_DATE", nullable = false)
    private Date enrollmentDate;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "TERMINATION_DATE")
    private Date terminationDate;
    
    @NotNull
    @DecimalMin("0.00")
    @Column(name = "EMPLOYEE_COST", nullable = false, precision = 10, scale = 2)
    private BigDecimal employeeCost;
    
    @DecimalMin("0.00")
    @Column(name = "EMPLOYER_COST", precision = 10, scale = 2)
    private BigDecimal employerCost;
    
    @Column(name = "COVERAGE_LEVEL", length = 20)
    private String coverageLevel; // INDIVIDUAL, FAMILY, EMPLOYEE_PLUS_ONE
    
    @Column(name = "ACTIVE", nullable = false)
    private Boolean active = true;
    
    @Column(name = "AUTO_RENEW", nullable = false)
    private Boolean autoRenew = true;
    
    @Column(name = "WAITING_PERIOD_DAYS")
    private Integer waitingPeriodDays;
    
    @Column(name = "ELIGIBILITY_DATE")
    @Temporal(TemporalType.DATE)
    private Date eligibilityDate;
    
    @Column(name = "COVERAGE_START_DATE")
    @Temporal(TemporalType.DATE)
    private Date coverageStartDate;
    
    @Column(name = "COVERAGE_END_DATE")
    @Temporal(TemporalType.DATE)
    private Date coverageEndDate;
    
    // Legacy fields
    @Column(name = "LEGACY_BENEFIT_ID", length = 20)
    private String legacyBenefitId;
    
    @Column(name = "LEGACY_SYSTEM_FLAG")
    private Boolean legacySystemFlag = false;
    
    @Column(name = "MANUAL_OVERRIDE")
    private Boolean manualOverride = false;
    
    @Column(name = "OVERRIDE_REASON", length = 200)
    private String overrideReason;
    
    @Column(name = "NOTES", length = 500)
    private String notes;
    
    // Constructors
    public BenefitEnrollment() {
    }
    
    public BenefitEnrollment(Employee employee, String benefitType, String benefitName, 
                           Date enrollmentDate, BigDecimal employeeCost) {
        this.employee = employee;
        this.benefitType = benefitType;
        this.benefitName = benefitName;
        this.enrollmentDate = enrollmentDate;
        this.employeeCost = employeeCost;
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
    
    public String getBenefitType() {
        return benefitType;
    }
    
    public void setBenefitType(String benefitType) {
        this.benefitType = benefitType;
    }
    
    public String getBenefitName() {
        return benefitName;
    }
    
    public void setBenefitName(String benefitName) {
        this.benefitName = benefitName;
    }
    
    public Date getEnrollmentDate() {
        return enrollmentDate;
    }
    
    public void setEnrollmentDate(Date enrollmentDate) {
        this.enrollmentDate = enrollmentDate;
    }
    
    public Date getTerminationDate() {
        return terminationDate;
    }
    
    public void setTerminationDate(Date terminationDate) {
        this.terminationDate = terminationDate;
    }
    
    public BigDecimal getEmployeeCost() {
        return employeeCost;
    }
    
    public void setEmployeeCost(BigDecimal employeeCost) {
        this.employeeCost = employeeCost;
    }
    
    public BigDecimal getEmployerCost() {
        return employerCost;
    }
    
    public void setEmployerCost(BigDecimal employerCost) {
        this.employerCost = employerCost;
    }
    
    public String getCoverageLevel() {
        return coverageLevel;
    }
    
    public void setCoverageLevel(String coverageLevel) {
        this.coverageLevel = coverageLevel;
    }
    
    public Boolean getActive() {
        return active;
    }
    
    public void setActive(Boolean active) {
        this.active = active;
    }
    
    public Boolean getAutoRenew() {
        return autoRenew;
    }
    
    public void setAutoRenew(Boolean autoRenew) {
        this.autoRenew = autoRenew;
    }
    
    public Integer getWaitingPeriodDays() {
        return waitingPeriodDays;
    }
    
    public void setWaitingPeriodDays(Integer waitingPeriodDays) {
        this.waitingPeriodDays = waitingPeriodDays;
    }
    
    public Date getEligibilityDate() {
        return eligibilityDate;
    }
    
    public void setEligibilityDate(Date eligibilityDate) {
        this.eligibilityDate = eligibilityDate;
    }
    
    public Date getCoverageStartDate() {
        return coverageStartDate;
    }
    
    public void setCoverageStartDate(Date coverageStartDate) {
        this.coverageStartDate = coverageStartDate;
    }
    
    public Date getCoverageEndDate() {
        return coverageEndDate;
    }
    
    public void setCoverageEndDate(Date coverageEndDate) {
        this.coverageEndDate = coverageEndDate;
    }
    
    public String getLegacyBenefitId() {
        return legacyBenefitId;
    }
    
    public void setLegacyBenefitId(String legacyBenefitId) {
        this.legacyBenefitId = legacyBenefitId;
    }
    
    public Boolean getLegacySystemFlag() {
        return legacySystemFlag;
    }
    
    public void setLegacySystemFlag(Boolean legacySystemFlag) {
        this.legacySystemFlag = legacySystemFlag;
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
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof BenefitEnrollment)) {
            return false;
        }
        BenefitEnrollment other = (BenefitEnrollment) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.BenefitEnrollment[ id=" + id + " ]";
    }
}
