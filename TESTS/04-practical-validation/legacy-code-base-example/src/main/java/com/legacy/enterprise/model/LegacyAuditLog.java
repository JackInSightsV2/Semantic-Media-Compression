package com.legacy.enterprise.model;

import java.io.Serializable;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;

/**
 * LegacyAuditLog Entity - Legacy audit logging system
 * This is a legacy entity that should be removed but is referenced everywhere
 * 
 * @author Legacy Developer (2007)
 * @version 1.0
 * @deprecated This class should be removed and replaced with modern audit logging
 */
@Entity
@Table(name = "LEGACY_AUDIT_LOG", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "LegacyAuditLog.findByEmployee", 
                query = "SELECT l FROM LegacyAuditLog l WHERE l.employee.id = :employeeId"),
    @NamedQuery(name = "LegacyAuditLog.findByDateRange", 
                query = "SELECT l FROM LegacyAuditLog l WHERE l.auditDate BETWEEN :startDate AND :endDate"),
    @NamedQuery(name = "LegacyAuditLog.findByAction", 
                query = "SELECT l FROM LegacyAuditLog l WHERE l.action = :action")
})
@SequenceGenerator(name = "LEGACY_AUDIT_SEQ", sequenceName = "LEGACY_AUDIT_SEQUENCE", allocationSize = 1)
public class LegacyAuditLog implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "LEGACY_AUDIT_SEQ")
    @Column(name = "AUDIT_ID")
    private Long id;
    
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "EMPLOYEE_ID", nullable = false)
    private Employee employee;
    
    @NotNull
    @Column(name = "ACTION", nullable = false, length = 50)
    private String action;
    
    @NotNull
    @Column(name = "AUDIT_DATE", nullable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date auditDate;
    
    @Column(name = "OLD_VALUE", length = 1000)
    private String oldValue;
    
    @Column(name = "NEW_VALUE", length = 1000)
    private String newValue;
    
    @Column(name = "FIELD_NAME", length = 50)
    private String fieldName;
    
    @Column(name = "USER_ID", length = 50)
    private String userId;
    
    @Column(name = "IP_ADDRESS", length = 20)
    private String ipAddress;
    
    @Column(name = "SESSION_ID", length = 100)
    private String sessionId;
    
    @Column(name = "NOTES", length = 500)
    private String notes;
    
    // Constructors
    public LegacyAuditLog() {
    }
    
    public LegacyAuditLog(Employee employee, String action, Date auditDate) {
        this.employee = employee;
        this.action = action;
        this.auditDate = auditDate;
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
    
    public String getAction() {
        return action;
    }
    
    public void setAction(String action) {
        this.action = action;
    }
    
    public Date getAuditDate() {
        return auditDate;
    }
    
    public void setAuditDate(Date auditDate) {
        this.auditDate = auditDate;
    }
    
    public String getOldValue() {
        return oldValue;
    }
    
    public void setOldValue(String oldValue) {
        this.oldValue = oldValue;
    }
    
    public String getNewValue() {
        return newValue;
    }
    
    public void setNewValue(String newValue) {
        this.newValue = newValue;
    }
    
    public String getFieldName() {
        return fieldName;
    }
    
    public void setFieldName(String fieldName) {
        this.fieldName = fieldName;
    }
    
    public String getUserId() {
        return userId;
    }
    
    public void setUserId(String userId) {
        this.userId = userId;
    }
    
    public String getIpAddress() {
        return ipAddress;
    }
    
    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }
    
    public String getSessionId() {
        return sessionId;
    }
    
    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
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
        if (!(object instanceof LegacyAuditLog)) {
            return false;
        }
        LegacyAuditLog other = (LegacyAuditLog) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.LegacyAuditLog[ id=" + id + " ]";
    }
}
