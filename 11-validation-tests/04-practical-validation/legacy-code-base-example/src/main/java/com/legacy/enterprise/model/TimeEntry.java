package com.legacy.enterprise.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.DecimalMin;

/**
 * TimeEntry Entity - Time tracking and overtime calculation
 * Complex business rules for different types of time entries
 * 
 * @author Legacy Developer (2011)
 * @version 1.3
 */
@Entity
@Table(name = "TIME_ENTRY", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "TimeEntry.findByEmployee", 
                query = "SELECT t FROM TimeEntry t WHERE t.employee.id = :employeeId"),
    @NamedQuery(name = "TimeEntry.findByDateRange", 
                query = "SELECT t FROM TimeEntry t WHERE t.entryDate BETWEEN :startDate AND :endDate"),
    @NamedQuery(name = "TimeEntry.findByEmployeeAndDateRange", 
                query = "SELECT t FROM TimeEntry t WHERE t.employee.id = :employeeId " +
                       "AND t.entryDate BETWEEN :startDate AND :endDate"),
    @NamedQuery(name = "TimeEntry.findOvertime", 
                query = "SELECT t FROM TimeEntry t WHERE t.overtimeHours > 0")
})
@SequenceGenerator(name = "TIME_ENTRY_SEQ", sequenceName = "TIME_ENTRY_SEQUENCE", allocationSize = 1)
public class TimeEntry implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "TIME_ENTRY_SEQ")
    @Column(name = "TIME_ENTRY_ID")
    private Long id;
    
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "EMPLOYEE_ID", nullable = false)
    private Employee employee;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "ENTRY_DATE", nullable = false)
    private Date entryDate;
    
    @NotNull
    @DecimalMin("0.00")
    @Column(name = "REGULAR_HOURS", nullable = false, precision = 8, scale = 2)
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
    @Column(name = "PERSONAL_HOURS", precision = 8, scale = 2)
    private BigDecimal personalHours;
    
    @DecimalMin("0.00")
    @Column(name = "BEREAVEMENT_HOURS", precision = 8, scale = 2)
    private BigDecimal bereavementHours;
    
    @DecimalMin("0.00")
    @Column(name = "JURY_DUTY_HOURS", precision = 8, scale = 2)
    private BigDecimal juryDutyHours;
    
    @DecimalMin("0.00")
    @Column(name = "MILITARY_HOURS", precision = 8, scale = 2)
    private BigDecimal militaryHours;
    
    @Column(name = "TIME_IN")
    @Temporal(TemporalType.TIMESTAMP)
    private Date timeIn;
    
    @Column(name = "TIME_OUT")
    @Temporal(TemporalType.TIMESTAMP)
    private Date timeOut;
    
    @Column(name = "LUNCH_START")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lunchStart;
    
    @Column(name = "LUNCH_END")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lunchEnd;
    
    @Column(name = "BREAK_START")
    @Temporal(TemporalType.TIMESTAMP)
    private Date breakStart;
    
    @Column(name = "BREAK_END")
    @Temporal(TemporalType.TIMESTAMP)
    private Date breakEnd;
    
    @Column(name = "PROJECT_CODE", length = 20)
    private String projectCode;
    
    @Column(name = "DEPARTMENT_CODE", length = 10)
    private String departmentCode;
    
    @Column(name = "COST_CENTER", length = 10)
    private String costCenter;
    
    @Column(name = "APPROVED", nullable = false)
    private Boolean approved = false;
    
    @Column(name = "APPROVED_BY", length = 50)
    private String approvedBy;
    
    @Column(name = "APPROVED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date approvedDate;
    
    @Column(name = "SUBMITTED", nullable = false)
    private Boolean submitted = false;
    
    @Column(name = "SUBMITTED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date submittedDate;
    
    @Column(name = "NOTES", length = 500)
    private String notes;
    
    @Column(name = "STATUS", length = 20)
    private String status; // DRAFT, SUBMITTED, APPROVED, REJECTED, PAID
    
    // Legacy fields
    @Column(name = "LEGACY_TIME_ID", length = 20)
    private String legacyTimeId;
    
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
    public TimeEntry() {
    }
    
    public TimeEntry(Employee employee, Date entryDate, BigDecimal regularHours) {
        this.employee = employee;
        this.entryDate = entryDate;
        this.regularHours = regularHours;
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
    
    public Date getEntryDate() {
        return entryDate;
    }
    
    public void setEntryDate(Date entryDate) {
        this.entryDate = entryDate;
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
    
    public BigDecimal getPersonalHours() {
        return personalHours;
    }
    
    public void setPersonalHours(BigDecimal personalHours) {
        this.personalHours = personalHours;
    }
    
    public BigDecimal getBereavementHours() {
        return bereavementHours;
    }
    
    public void setBereavementHours(BigDecimal bereavementHours) {
        this.bereavementHours = bereavementHours;
    }
    
    public BigDecimal getJuryDutyHours() {
        return juryDutyHours;
    }
    
    public void setJuryDutyHours(BigDecimal juryDutyHours) {
        this.juryDutyHours = juryDutyHours;
    }
    
    public BigDecimal getMilitaryHours() {
        return militaryHours;
    }
    
    public void setMilitaryHours(BigDecimal militaryHours) {
        this.militaryHours = militaryHours;
    }
    
    public Date getTimeIn() {
        return timeIn;
    }
    
    public void setTimeIn(Date timeIn) {
        this.timeIn = timeIn;
    }
    
    public Date getTimeOut() {
        return timeOut;
    }
    
    public void setTimeOut(Date timeOut) {
        this.timeOut = timeOut;
    }
    
    public Date getLunchStart() {
        return lunchStart;
    }
    
    public void setLunchStart(Date lunchStart) {
        this.lunchStart = lunchStart;
    }
    
    public Date getLunchEnd() {
        return lunchEnd;
    }
    
    public void setLunchEnd(Date lunchEnd) {
        this.lunchEnd = lunchEnd;
    }
    
    public Date getBreakStart() {
        return breakStart;
    }
    
    public void setBreakStart(Date breakStart) {
        this.breakStart = breakStart;
    }
    
    public Date getBreakEnd() {
        return breakEnd;
    }
    
    public void setBreakEnd(Date breakEnd) {
        this.breakEnd = breakEnd;
    }
    
    public String getProjectCode() {
        return projectCode;
    }
    
    public void setProjectCode(String projectCode) {
        this.projectCode = projectCode;
    }
    
    public String getDepartmentCode() {
        return departmentCode;
    }
    
    public void setDepartmentCode(String departmentCode) {
        this.departmentCode = departmentCode;
    }
    
    public String getCostCenter() {
        return costCenter;
    }
    
    public void setCostCenter(String costCenter) {
        this.costCenter = costCenter;
    }
    
    public Boolean getApproved() {
        return approved;
    }
    
    public void setApproved(Boolean approved) {
        this.approved = approved;
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
    
    public Boolean getSubmitted() {
        return submitted;
    }
    
    public void setSubmitted(Boolean submitted) {
        this.submitted = submitted;
    }
    
    public Date getSubmittedDate() {
        return submittedDate;
    }
    
    public void setSubmittedDate(Date submittedDate) {
        this.submittedDate = submittedDate;
    }
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getLegacyTimeId() {
        return legacyTimeId;
    }
    
    public void setLegacyTimeId(String legacyTimeId) {
        this.legacyTimeId = legacyTimeId;
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
    public BigDecimal getTotalHours() {
        BigDecimal total = BigDecimal.ZERO;
        if (regularHours != null) total = total.add(regularHours);
        if (overtimeHours != null) total = total.add(overtimeHours);
        if (doubleTimeHours != null) total = total.add(doubleTimeHours);
        if (holidayHours != null) total = total.add(holidayHours);
        if (vacationHours != null) total = total.add(vacationHours);
        if (sickHours != null) total = total.add(sickHours);
        if (personalHours != null) total = total.add(personalHours);
        if (bereavementHours != null) total = total.add(bereavementHours);
        if (juryDutyHours != null) total = total.add(juryDutyHours);
        if (militaryHours != null) total = total.add(militaryHours);
        return total;
    }
    
    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }
    
    @Override
    public boolean equals(Object object) {
        if (!(object instanceof TimeEntry)) {
            return false;
        }
        TimeEntry other = (TimeEntry) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.TimeEntry[ id=" + id + " ]";
    }
}
