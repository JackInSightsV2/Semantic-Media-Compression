package com.legacy.enterprise.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.DecimalMin;

/**
 * PayrollCalculation Entity - Complex payroll calculation logic
 * This class has grown significantly over the years with various business rules
 * 
 * @author Legacy Developer (2009)
 * @version 2.1
 */
@Entity
@Table(name = "PAYROLL_CALCULATION", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "PayrollCalculation.findByEmployee", 
                query = "SELECT p FROM PayrollCalculation p WHERE p.employee.id = :employeeId"),
    @NamedQuery(name = "PayrollCalculation.findByDateRange", 
                query = "SELECT p FROM PayrollCalculation p WHERE p.calculationDate BETWEEN :startDate AND :endDate"),
    @NamedQuery(name = "PayrollCalculation.findByPayPeriod", 
                query = "SELECT p FROM PayrollCalculation p WHERE p.payPeriodStart = :start AND p.payPeriodEnd = :end"),
    // Legacy query that's still used but inefficient
    @NamedQuery(name = "PayrollCalculation.findLegacy", 
                query = "SELECT p FROM PayrollCalculation p, Employee e WHERE p.employee.id = e.id " +
                       "AND e.department = :dept AND p.calculationDate >= :date")
})
@SequenceGenerator(name = "PAYROLL_SEQ", sequenceName = "PAYROLL_SEQUENCE", allocationSize = 1)
public class PayrollCalculation implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "PAYROLL_SEQ")
    @Column(name = "PAYROLL_ID")
    private Long id;
    
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "EMPLOYEE_ID", nullable = false)
    private Employee employee;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "CALCULATION_DATE", nullable = false)
    private Date calculationDate;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "PAY_PERIOD_START", nullable = false)
    private Date payPeriodStart;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "PAY_PERIOD_END", nullable = false)
    private Date payPeriodEnd;
    
    @NotNull
    @DecimalMin("0.00")
    @Column(name = "GROSS_PAY", nullable = false, precision = 10, scale = 2)
    private BigDecimal grossPay;
    
    @NotNull
    @DecimalMin("0.00")
    @Column(name = "NET_PAY", nullable = false, precision = 10, scale = 2)
    private BigDecimal netPay;
    
    @DecimalMin("0.00")
    @Column(name = "REGULAR_HOURS", precision = 8, scale = 2)
    private BigDecimal regularHours;
    
    @DecimalMin("0.00")
    @Column(name = "OVERTIME_HOURS", precision = 8, scale = 2)
    private BigDecimal overtimeHours;
    
    @DecimalMin("0.00")
    @Column(name = "DOUBLE_TIME_HOURS", precision = 8, scale = 2)
    private BigDecimal doubleTimeHours;
    
    @DecimalMin("0.00")
    @Column(name = "HOLIDAY_HOURS", precision = 8, scale = 2)
    private BigDecimal holidayHours;
    
    @DecimalMin("0.00")
    @Column(name = "VACATION_HOURS", precision = 8, scale = 2)
    private BigDecimal vacationHours;
    
    @DecimalMin("0.00")
    @Column(name = "SICK_HOURS", precision = 8, scale = 2)
    private BigDecimal sickHours;
    
    @DecimalMin("0.00")
    @Column(name = "REGULAR_PAY", precision = 10, scale = 2)
    private BigDecimal regularPay;
    
    @DecimalMin("0.00")
    @Column(name = "OVERTIME_PAY", precision = 10, scale = 2)
    private BigDecimal overtimePay;
    
    @DecimalMin("0.00")
    @Column(name = "DOUBLE_TIME_PAY", precision = 10, scale = 2)
    private BigDecimal doubleTimePay;
    
    @DecimalMin("0.00")
    @Column(name = "HOLIDAY_PAY", precision = 10, scale = 2)
    private BigDecimal holidayPay;
    
    @DecimalMin("0.00")
    @Column(name = "VACATION_PAY", precision = 10, scale = 2)
    private BigDecimal vacationPay;
    
    @DecimalMin("0.00")
    @Column(name = "SICK_PAY", precision = 10, scale = 2)
    private BigDecimal sickPay;
    
    // Tax deductions
    @DecimalMin("0.00")
    @Column(name = "FEDERAL_TAX", precision = 10, scale = 2)
    private BigDecimal federalTax;
    
    @DecimalMin("0.00")
    @Column(name = "STATE_TAX", precision = 10, scale = 2)
    private BigDecimal stateTax;
    
    @DecimalMin("0.00")
    @Column(name = "LOCAL_TAX", precision = 10, scale = 2)
    private BigDecimal localTax;
    
    @DecimalMin("0.00")
    @Column(name = "SOCIAL_SECURITY", precision = 10, scale = 2)
    private BigDecimal socialSecurity;
    
    @DecimalMin("0.00")
    @Column(name = "MEDICARE", precision = 10, scale = 2)
    private BigDecimal medicare;
    
    @DecimalMin("0.00")
    @Column(name = "ADDITIONAL_MEDICARE", precision = 10, scale = 2)
    private BigDecimal additionalMedicare;
    
    // Benefits deductions
    @DecimalMin("0.00")
    @Column(name = "HEALTH_INSURANCE", precision = 10, scale = 2)
    private BigDecimal healthInsurance;
    
    @DecimalMin("0.00")
    @Column(name = "DENTAL_INSURANCE", precision = 10, scale = 2)
    private BigDecimal dentalInsurance;
    
    @DecimalMin("0.00")
    @Column(name = "VISION_INSURANCE", precision = 10, scale = 2)
    private BigDecimal visionInsurance;
    
    @DecimalMin("0.00")
    @Column(name = "LIFE_INSURANCE", precision = 10, scale = 2)
    private BigDecimal lifeInsurance;
    
    @DecimalMin("0.00")
    @Column(name = "DISABILITY_INSURANCE", precision = 10, scale = 2)
    private BigDecimal disabilityInsurance;
    
    @DecimalMin("0.00")
    @Column(name = "RETIREMENT_401K", precision = 10, scale = 2)
    private BigDecimal retirement401k;
    
    @DecimalMin("0.00")
    @Column(name = "RETIREMENT_401K_MATCH", precision = 10, scale = 2)
    private BigDecimal retirement401kMatch;
    
    // Other deductions
    @DecimalMin("0.00")
    @Column(name = "UNION_DUES", precision = 10, scale = 2)
    private BigDecimal unionDues;
    
    @DecimalMin("0.00")
    @Column(name = "PARKING", precision = 10, scale = 2)
    private BigDecimal parking;
    
    @DecimalMin("0.00")
    @Column(name = "MEALS", precision = 10, scale = 2)
    private BigDecimal meals;
    
    @DecimalMin("0.00")
    @Column(name = "OTHER_DEDUCTIONS", precision = 10, scale = 2)
    private BigDecimal otherDeductions;
    
    // Totals
    @DecimalMin("0.00")
    @Column(name = "TOTAL_DEDUCTIONS", precision = 10, scale = 2)
    private BigDecimal totalDeductions;
    
    @DecimalMin("0.00")
    @Column(name = "TOTAL_TAXES", precision = 10, scale = 2)
    private BigDecimal totalTaxes;
    
    @DecimalMin("0.00")
    @Column(name = "TOTAL_BENEFITS", precision = 10, scale = 2)
    private BigDecimal totalBenefits;
    
    // Status and processing
    @Column(name = "STATUS", length = 20)
    private String status; // PENDING, PROCESSED, APPROVED, PAID, ERROR
    
    @Column(name = "PROCESSED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date processedDate;
    
    @Column(name = "APPROVED_BY", length = 50)
    private String approvedBy;
    
    @Column(name = "APPROVED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date approvedDate;
    
    @Column(name = "ERROR_MESSAGE", length = 500)
    private String errorMessage;
    
    // Legacy fields
    @Column(name = "LEGACY_CALCULATION_ID", length = 20)
    private String legacyCalculationId;
    
    @Column(name = "LEGACY_SYSTEM_FLAG")
    private Boolean legacySystemFlag = false;
    
    @Column(name = "MANUAL_OVERRIDE")
    private Boolean manualOverride = false;
    
    @Column(name = "OVERRIDE_REASON", length = 200)
    private String overrideReason;
    
    @Column(name = "OVERRIDE_BY", length = 50)
    private String overrideBy;
    
    @Column(name = "OVERRIDE_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date overrideDate;
    
    // Constructors
    public PayrollCalculation() {
    }
    
    public PayrollCalculation(Employee employee, Date calculationDate, Date payPeriodStart, Date payPeriodEnd) {
        this.employee = employee;
        this.calculationDate = calculationDate;
        this.payPeriodStart = payPeriodStart;
        this.payPeriodEnd = payPeriodEnd;
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
    
    public Date getCalculationDate() {
        return calculationDate;
    }
    
    public void setCalculationDate(Date calculationDate) {
        this.calculationDate = calculationDate;
    }
    
    public Date getPayPeriodStart() {
        return payPeriodStart;
    }
    
    public void setPayPeriodStart(Date payPeriodStart) {
        this.payPeriodStart = payPeriodStart;
    }
    
    public Date getPayPeriodEnd() {
        return payPeriodEnd;
    }
    
    public void setPayPeriodEnd(Date payPeriodEnd) {
        this.payPeriodEnd = payPeriodEnd;
    }
    
    public BigDecimal getGrossPay() {
        return grossPay;
    }
    
    public void setGrossPay(BigDecimal grossPay) {
        this.grossPay = grossPay;
    }
    
    public BigDecimal getNetPay() {
        return netPay;
    }
    
    public void setNetPay(BigDecimal netPay) {
        this.netPay = netPay;
    }
    
    public BigDecimal getRegularHours() {
        return regularHours;
    }
    
    public void setRegularHours(BigDecimal regularHours) {
        this.regularHours = regularHours;
    }
    
    public BigDecimal getOvertimeHours() {
        return overtimeHours;
    }
    
    public void setOvertimeHours(BigDecimal overtimeHours) {
        this.overtimeHours = overtimeHours;
    }
    
    public BigDecimal getDoubleTimeHours() {
        return doubleTimeHours;
    }
    
    public void setDoubleTimeHours(BigDecimal doubleTimeHours) {
        this.doubleTimeHours = doubleTimeHours;
    }
    
    public BigDecimal getHolidayHours() {
        return holidayHours;
    }
    
    public void setHolidayHours(BigDecimal holidayHours) {
        this.holidayHours = holidayHours;
    }
    
    public BigDecimal getVacationHours() {
        return vacationHours;
    }
    
    public void setVacationHours(BigDecimal vacationHours) {
        this.vacationHours = vacationHours;
    }
    
    public BigDecimal getSickHours() {
        return sickHours;
    }
    
    public void setSickHours(BigDecimal sickHours) {
        this.sickHours = sickHours;
    }
    
    public BigDecimal getRegularPay() {
        return regularPay;
    }
    
    public void setRegularPay(BigDecimal regularPay) {
        this.regularPay = regularPay;
    }
    
    public BigDecimal getOvertimePay() {
        return overtimePay;
    }
    
    public void setOvertimePay(BigDecimal overtimePay) {
        this.overtimePay = overtimePay;
    }
    
    public BigDecimal getDoubleTimePay() {
        return doubleTimePay;
    }
    
    public void setDoubleTimePay(BigDecimal doubleTimePay) {
        this.doubleTimePay = doubleTimePay;
    }
    
    public BigDecimal getHolidayPay() {
        return holidayPay;
    }
    
    public void setHolidayPay(BigDecimal holidayPay) {
        this.holidayPay = holidayPay;
    }
    
    public BigDecimal getVacationPay() {
        return vacationPay;
    }
    
    public void setVacationPay(BigDecimal vacationPay) {
        this.vacationPay = vacationPay;
    }
    
    public BigDecimal getSickPay() {
        return sickPay;
    }
    
    public void setSickPay(BigDecimal sickPay) {
        this.sickPay = sickPay;
    }
    
    public BigDecimal getFederalTax() {
        return federalTax;
    }
    
    public void setFederalTax(BigDecimal federalTax) {
        this.federalTax = federalTax;
    }
    
    public BigDecimal getStateTax() {
        return stateTax;
    }
    
    public void setStateTax(BigDecimal stateTax) {
        this.stateTax = stateTax;
    }
    
    public BigDecimal getLocalTax() {
        return localTax;
    }
    
    public void setLocalTax(BigDecimal localTax) {
        this.localTax = localTax;
    }
    
    public BigDecimal getSocialSecurity() {
        return socialSecurity;
    }
    
    public void setSocialSecurity(BigDecimal socialSecurity) {
        this.socialSecurity = socialSecurity;
    }
    
    public BigDecimal getMedicare() {
        return medicare;
    }
    
    public void setMedicare(BigDecimal medicare) {
        this.medicare = medicare;
    }
    
    public BigDecimal getAdditionalMedicare() {
        return additionalMedicare;
    }
    
    public void setAdditionalMedicare(BigDecimal additionalMedicare) {
        this.additionalMedicare = additionalMedicare;
    }
    
    public BigDecimal getHealthInsurance() {
        return healthInsurance;
    }
    
    public void setHealthInsurance(BigDecimal healthInsurance) {
        this.healthInsurance = healthInsurance;
    }
    
    public BigDecimal getDentalInsurance() {
        return dentalInsurance;
    }
    
    public void setDentalInsurance(BigDecimal dentalInsurance) {
        this.dentalInsurance = dentalInsurance;
    }
    
    public BigDecimal getVisionInsurance() {
        return visionInsurance;
    }
    
    public void setVisionInsurance(BigDecimal visionInsurance) {
        this.visionInsurance = visionInsurance;
    }
    
    public BigDecimal getLifeInsurance() {
        return lifeInsurance;
    }
    
    public void setLifeInsurance(BigDecimal lifeInsurance) {
        this.lifeInsurance = lifeInsurance;
    }
    
    public BigDecimal getDisabilityInsurance() {
        return disabilityInsurance;
    }
    
    public void setDisabilityInsurance(BigDecimal disabilityInsurance) {
        this.disabilityInsurance = disabilityInsurance;
    }
    
    public BigDecimal getRetirement401k() {
        return retirement401k;
    }
    
    public void setRetirement401k(BigDecimal retirement401k) {
        this.retirement401k = retirement401k;
    }
    
    public BigDecimal getRetirement401kMatch() {
        return retirement401kMatch;
    }
    
    public void setRetirement401kMatch(BigDecimal retirement401kMatch) {
        this.retirement401kMatch = retirement401kMatch;
    }
    
    public BigDecimal getUnionDues() {
        return unionDues;
    }
    
    public void setUnionDues(BigDecimal unionDues) {
        this.unionDues = unionDues;
    }
    
    public BigDecimal getParking() {
        return parking;
    }
    
    public void setParking(BigDecimal parking) {
        this.parking = parking;
    }
    
    public BigDecimal getMeals() {
        return meals;
    }
    
    public void setMeals(BigDecimal meals) {
        this.meals = meals;
    }
    
    public BigDecimal getOtherDeductions() {
        return otherDeductions;
    }
    
    public void setOtherDeductions(BigDecimal otherDeductions) {
        this.otherDeductions = otherDeductions;
    }
    
    public BigDecimal getTotalDeductions() {
        return totalDeductions;
    }
    
    public void setTotalDeductions(BigDecimal totalDeductions) {
        this.totalDeductions = totalDeductions;
    }
    
    public BigDecimal getTotalTaxes() {
        return totalTaxes;
    }
    
    public void setTotalTaxes(BigDecimal totalTaxes) {
        this.totalTaxes = totalTaxes;
    }
    
    public BigDecimal getTotalBenefits() {
        return totalBenefits;
    }
    
    public void setTotalBenefits(BigDecimal totalBenefits) {
        this.totalBenefits = totalBenefits;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public Date getProcessedDate() {
        return processedDate;
    }
    
    public void setProcessedDate(Date processedDate) {
        this.processedDate = processedDate;
    }
    
    public String getApprovedBy() {
        return approvedBy;
    }
    
    public void setApprovedBy(String approvedBy) {
        this.approvedBy = approvedBy;
    }
    
    public Date getApprovedDate() {
        return approvedDate;
    }
    
    public void setApprovedDate(Date approvedDate) {
        this.approvedDate = approvedDate;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
    
    public String getLegacyCalculationId() {
        return legacyCalculationId;
    }
    
    public void setLegacyCalculationId(String legacyCalculationId) {
        this.legacyCalculationId = legacyCalculationId;
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
    
    // Business logic methods that should be in service layer
    public void calculateTotals() {
        // Calculate total deductions
        BigDecimal deductions = BigDecimal.ZERO;
        if (federalTax != null) deductions = deductions.add(federalTax);
        if (stateTax != null) deductions = deductions.add(stateTax);
        if (localTax != null) deductions = deductions.add(localTax);
        if (socialSecurity != null) deductions = deductions.add(socialSecurity);
        if (medicare != null) deductions = deductions.add(medicare);
        if (additionalMedicare != null) deductions = deductions.add(additionalMedicare);
        if (healthInsurance != null) deductions = deductions.add(healthInsurance);
        if (dentalInsurance != null) deductions = deductions.add(dentalInsurance);
        if (visionInsurance != null) deductions = deductions.add(visionInsurance);
        if (lifeInsurance != null) deductions = deductions.add(lifeInsurance);
        if (disabilityInsurance != null) deductions = deductions.add(disabilityInsurance);
        if (retirement401k != null) deductions = deductions.add(retirement401k);
        if (unionDues != null) deductions = deductions.add(unionDues);
        if (parking != null) deductions = deductions.add(parking);
        if (meals != null) deductions = deductions.add(meals);
        if (otherDeductions != null) deductions = deductions.add(otherDeductions);
        
        this.totalDeductions = deductions;
        
        // Calculate net pay
        if (grossPay != null && totalDeductions != null) {
            this.netPay = grossPay.subtract(totalDeductions);
        }
    }
    
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof PayrollCalculation)) {
            return false;
        }
        PayrollCalculation other = (PayrollCalculation) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.PayrollCalculation[ id=" + id + " ]";
    }
}
