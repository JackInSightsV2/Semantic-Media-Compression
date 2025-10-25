package com.legacy.enterprise.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.Past;
import javax.validation.constraints.Future;

/**
 * Legacy Employee Entity - Accumulated technical debt over 8+ years
 * Originally designed for simple employee tracking, now handles complex payroll
 * 
 * @author Legacy Developer (2008)
 * @version 1.0
 * @deprecated This class has grown too complex and should be refactored
 */
@Entity
@Table(name = "EMPLOYEE", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "Employee.findAll", query = "SELECT e FROM Employee e"),
    @NamedQuery(name = "Employee.findByDepartment", query = "SELECT e FROM Employee e WHERE e.department = :dept"),
    @NamedQuery(name = "Employee.findActive", query = "SELECT e FROM Employee e WHERE e.active = true"),
    @NamedQuery(name = "Employee.findBySalaryRange", 
                query = "SELECT e FROM Employee e WHERE e.baseSalary BETWEEN :min AND :max"),
    // Legacy query that should be removed but is used in 15+ places
    @NamedQuery(name = "Employee.findLegacy", 
                query = "SELECT e FROM Employee e WHERE e.legacyId IS NOT NULL AND e.legacyId != ''"),
    // Complex query that grew over time
    @NamedQuery(name = "Employee.findComplexPayroll", 
                query = "SELECT e FROM Employee e, PayrollCalculation p WHERE e.id = p.employeeId " +
                       "AND p.calculationDate >= :startDate AND p.calculationDate <= :endDate " +
                       "AND e.department IN (:dept1, :dept2, :dept3) " +
                       "AND e.active = true AND e.terminated = false")
})
@SequenceGenerator(name = "EMPLOYEE_SEQ", sequenceName = "EMPLOYEE_SEQUENCE", allocationSize = 1)
public class Employee implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "EMPLOYEE_SEQ")
    @Column(name = "EMP_ID")
    private Long id;
    
    // Legacy field from old system - should be removed but referenced everywhere
    @Column(name = "LEGACY_ID", length = 20)
    private String legacyId;
    
    @NotNull
    @Size(min = 1, max = 50)
    @Column(name = "FIRST_NAME", nullable = false, length = 50)
    private String firstName;
    
    @NotNull
    @Size(min = 1, max = 50)
    @Column(name = "LAST_NAME", nullable = false, length = 50)
    private String lastName;
    
    @Column(name = "MIDDLE_NAME", length = 50)
    private String middleName;
    
    @NotNull
    @Size(min = 1, max = 100)
    @Column(name = "EMAIL", nullable = false, length = 100)
    private String email;
    
    @Column(name = "PHONE", length = 20)
    private String phone;
    
    @Column(name = "ADDRESS", length = 200)
    private String address;
    
    @Column(name = "CITY", length = 50)
    private String city;
    
    @Column(name = "STATE", length = 2)
    private String state;
    
    @Column(name = "ZIP_CODE", length = 10)
    private String zipCode;
    
    @NotNull
    @Past
    @Temporal(TemporalType.DATE)
    @Column(name = "DATE_OF_BIRTH", nullable = false)
    private Date dateOfBirth;
    
    @NotNull
    @Past
    @Temporal(TemporalType.DATE)
    @Column(name = "HIRE_DATE", nullable = false)
    private Date hireDate;
    
    @Temporal(TemporalType.DATE)
    @Column(name = "TERMINATION_DATE")
    private Date terminationDate;
    
    @NotNull
    @DecimalMin("0.00")
    @Column(name = "BASE_SALARY", nullable = false, precision = 10, scale = 2)
    private BigDecimal baseSalary;
    
    @Column(name = "HOURLY_RATE", precision = 8, scale = 2)
    private BigDecimal hourlyRate;
    
    @Column(name = "OVERTIME_RATE", precision = 8, scale = 2)
    private BigDecimal overtimeRate;
    
    @NotNull
    @Column(name = "DEPARTMENT", nullable = false, length = 50)
    private String department;
    
    @Column(name = "JOB_TITLE", length = 100)
    private String jobTitle;
    
    @Column(name = "MANAGER_ID")
    private Long managerId;
    
    @Column(name = "EMPLOYEE_TYPE", length = 20)
    private String employeeType; // FULL_TIME, PART_TIME, CONTRACTOR, INTERN
    
    @Column(name = "PAY_FREQUENCY", length = 20)
    private String payFrequency; // WEEKLY, BIWEEKLY, MONTHLY
    
    @Column(name = "ACTIVE", nullable = false)
    private Boolean active = true;
    
    @Column(name = "TERMINATED", nullable = false)
    private Boolean terminated = false;
    
    // Legacy fields that should be removed
    @Column(name = "OLD_SYSTEM_FLAG")
    private Boolean oldSystemFlag = false;
    
    @Column(name = "MIGRATION_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date migrationDate;
    
    @Column(name = "LEGACY_NOTES", length = 500)
    private String legacyNotes;
    
    // Complex relationships that grew over time
    @OneToMany(mappedBy = "employee", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<PayrollCalculation> payrollCalculations = new ArrayList<PayrollCalculation>();
    
    @OneToMany(mappedBy = "employee", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<BenefitEnrollment> benefitEnrollments = new ArrayList<BenefitEnrollment>();
    
    @OneToMany(mappedBy = "employee", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<TimeEntry> timeEntries = new ArrayList<TimeEntry>();
    
    @OneToMany(mappedBy = "employee", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<TaxDeduction> taxDeductions = new ArrayList<TaxDeduction>();
    
    @OneToMany(mappedBy = "employee", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<PerformanceReview> performanceReviews = new ArrayList<PerformanceReview>();
    
    // Legacy relationship that should be removed
    @OneToMany(mappedBy = "employee", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<LegacyAuditLog> legacyAuditLogs = new ArrayList<LegacyAuditLog>();
    
    // Constructors
    public Employee() {
        // Default constructor
    }
    
    public Employee(String firstName, String lastName, String email, Date dateOfBirth, 
                   Date hireDate, BigDecimal baseSalary, String department) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.dateOfBirth = dateOfBirth;
        this.hireDate = hireDate;
        this.baseSalary = baseSalary;
        this.department = department;
    }
    
    // Getters and Setters - Generated by IDE, never refactored
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getLegacyId() {
        return legacyId;
    }
    
    public void setLegacyId(String legacyId) {
        this.legacyId = legacyId;
    }
    
    public String getFirstName() {
        return firstName;
    }
    
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }
    
    public String getLastName() {
        return lastName;
    }
    
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
    
    public String getMiddleName() {
        return middleName;
    }
    
    public void setMiddleName(String middleName) {
        this.middleName = middleName;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public String getPhone() {
        return phone;
    }
    
    public void setPhone(String phone) {
        this.phone = phone;
    }
    
    public String getAddress() {
        return address;
    }
    
    public void setAddress(String address) {
        this.address = address;
    }
    
    public String getCity() {
        return city;
    }
    
    public void setCity(String city) {
        this.city = city;
    }
    
    public String getState() {
        return state;
    }
    
    public void setState(String state) {
        this.state = state;
    }
    
    public String getZipCode() {
        return zipCode;
    }
    
    public void setZipCode(String zipCode) {
        this.zipCode = zipCode;
    }
    
    public Date getDateOfBirth() {
        return dateOfBirth;
    }
    
    public void setDateOfBirth(Date dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }
    
    public Date getHireDate() {
        return hireDate;
    }
    
    public void setHireDate(Date hireDate) {
        this.hireDate = hireDate;
    }
    
    public Date getTerminationDate() {
        return terminationDate;
    }
    
    public void setTerminationDate(Date terminationDate) {
        this.terminationDate = terminationDate;
    }
    
    public BigDecimal getBaseSalary() {
        return baseSalary;
    }
    
    public void setBaseSalary(BigDecimal baseSalary) {
        this.baseSalary = baseSalary;
    }
    
    public BigDecimal getHourlyRate() {
        return hourlyRate;
    }
    
    public void setHourlyRate(BigDecimal hourlyRate) {
        this.hourlyRate = hourlyRate;
    }
    
    public BigDecimal getOvertimeRate() {
        return overtimeRate;
    }
    
    public void setOvertimeRate(BigDecimal overtimeRate) {
        this.overtimeRate = overtimeRate;
    }
    
    public String getDepartment() {
        return department;
    }
    
    public void setDepartment(String department) {
        this.department = department;
    }
    
    public String getJobTitle() {
        return jobTitle;
    }
    
    public void setJobTitle(String jobTitle) {
        this.jobTitle = jobTitle;
    }
    
    public Long getManagerId() {
        return managerId;
    }
    
    public void setManagerId(Long managerId) {
        this.managerId = managerId;
    }
    
    public String getEmployeeType() {
        return employeeType;
    }
    
    public void setEmployeeType(String employeeType) {
        this.employeeType = employeeType;
    }
    
    public String getPayFrequency() {
        return payFrequency;
    }
    
    public void setPayFrequency(String payFrequency) {
        this.payFrequency = payFrequency;
    }
    
    public Boolean getActive() {
        return active;
    }
    
    public void setActive(Boolean active) {
        this.active = active;
    }
    
    public Boolean getTerminated() {
        return terminated;
    }
    
    public void setTerminated(Boolean terminated) {
        this.terminated = terminated;
    }
    
    public Boolean getOldSystemFlag() {
        return oldSystemFlag;
    }
    
    public void setOldSystemFlag(Boolean oldSystemFlag) {
        this.oldSystemFlag = oldSystemFlag;
    }
    
    public Date getMigrationDate() {
        return migrationDate;
    }
    
    public void setMigrationDate(Date migrationDate) {
        this.migrationDate = migrationDate;
    }
    
    public String getLegacyNotes() {
        return legacyNotes;
    }
    
    public void setLegacyNotes(String legacyNotes) {
        this.legacyNotes = legacyNotes;
    }
    
    public List<PayrollCalculation> getPayrollCalculations() {
        return payrollCalculations;
    }
    
    public void setPayrollCalculations(List<PayrollCalculation> payrollCalculations) {
        this.payrollCalculations = payrollCalculations;
    }
    
    public List<BenefitEnrollment> getBenefitEnrollments() {
        return benefitEnrollments;
    }
    
    public void setBenefitEnrollments(List<BenefitEnrollment> benefitEnrollments) {
        this.benefitEnrollments = benefitEnrollments;
    }
    
    public List<TimeEntry> getTimeEntries() {
        return timeEntries;
    }
    
    public void setTimeEntries(List<TimeEntry> timeEntries) {
        this.timeEntries = timeEntries;
    }
    
    public List<TaxDeduction> getTaxDeductions() {
        return taxDeductions;
    }
    
    public void setTaxDeductions(List<TaxDeduction> taxDeductions) {
        this.taxDeductions = taxDeductions;
    }
    
    public List<PerformanceReview> getPerformanceReviews() {
        return performanceReviews;
    }
    
    public void setPerformanceReviews(List<PerformanceReview> performanceReviews) {
        this.performanceReviews = performanceReviews;
    }
    
    public List<LegacyAuditLog> getLegacyAuditLogs() {
        return legacyAuditLogs;
    }
    
    public void setLegacyAuditLogs(List<LegacyAuditLog> legacyAuditLogs) {
        this.legacyAuditLogs = legacyAuditLogs;
    }
    
    // Business logic methods that grew over time - should be moved to service layer
    public String getFullName() {
        StringBuilder fullName = new StringBuilder();
        if (firstName != null) {
            fullName.append(firstName);
        }
        if (middleName != null && !middleName.trim().isEmpty()) {
            fullName.append(" ").append(middleName);
        }
        if (lastName != null) {
            fullName.append(" ").append(lastName);
        }
        return fullName.toString().trim();
    }
    
    public int getAge() {
        if (dateOfBirth == null) {
            return 0;
        }
        Calendar birth = new GregorianCalendar();
        birth.setTime(dateOfBirth);
        Calendar now = new GregorianCalendar();
        int age = now.get(Calendar.YEAR) - birth.get(Calendar.YEAR);
        if (now.get(Calendar.DAY_OF_YEAR) < birth.get(Calendar.DAY_OF_YEAR)) {
            age--;
        }
        return age;
    }
    
    public int getYearsOfService() {
        if (hireDate == null) {
            return 0;
        }
        Calendar hire = new GregorianCalendar();
        hire.setTime(hireDate);
        Calendar now = new GregorianCalendar();
        int years = now.get(Calendar.YEAR) - hire.get(Calendar.YEAR);
        if (now.get(Calendar.DAY_OF_YEAR) < hire.get(Calendar.DAY_OF_YEAR)) {
            years--;
        }
        return years;
    }
    
    // Legacy method that should be removed
    public boolean isLegacyEmployee() {
        return legacyId != null && !legacyId.trim().isEmpty();
    }
    
    // Complex business logic that should be in service layer
    public BigDecimal calculateGrossPay() {
        // This is a simplified calculation - real logic is much more complex
        if (baseSalary != null) {
            return baseSalary;
        }
        return BigDecimal.ZERO;
    }
    
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Employee)) {
            return false;
        }
        Employee other = (Employee) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.Employee[ id=" + id + " ]";
    }
}
