package com.legacy.enterprise.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;

/**
 * PerformanceReview Entity - Performance management and review system
 * Complex review process with multiple evaluation criteria
 * 
 * @author Legacy Developer (2013)
 * @version 1.1
 */
@Entity
@Table(name = "PERFORMANCE_REVIEW", schema = "LEGACY_HR")
@NamedQueries({
    @NamedQuery(name = "PerformanceReview.findByEmployee", 
                query = "SELECT p FROM PerformanceReview p WHERE p.employee.id = :employeeId"),
    @NamedQuery(name = "PerformanceReview.findByReviewPeriod", 
                query = "SELECT p FROM PerformanceReview p WHERE p.reviewPeriod = :period"),
    @NamedQuery(name = "PerformanceReview.findByStatus", 
                query = "SELECT p FROM PerformanceReview p WHERE p.status = :status")
})
@SequenceGenerator(name = "PERFORMANCE_REVIEW_SEQ", sequenceName = "PERFORMANCE_REVIEW_SEQUENCE", allocationSize = 1)
public class PerformanceReview implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "PERFORMANCE_REVIEW_SEQ")
    @Column(name = "REVIEW_ID")
    private Long id;
    
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "EMPLOYEE_ID", nullable = false)
    private Employee employee;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "REVIEW_DATE", nullable = false)
    private Date reviewDate;
    
    @NotNull
    @Column(name = "REVIEW_PERIOD", nullable = false, length = 20)
    private String reviewPeriod; // Q1_2023, Q2_2023, ANNUAL_2023
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "PERIOD_START", nullable = false)
    private Date periodStart;
    
    @NotNull
    @Temporal(TemporalType.DATE)
    @Column(name = "PERIOD_END", nullable = false)
    private Date periodEnd;
    
    @NotNull
    @Min(1)
    @Max(5)
    @Column(name = "OVERALL_RATING", nullable = false)
    private Integer overallRating; // 1-5 scale
    
    @Min(1)
    @Max(5)
    @Column(name = "JOB_KNOWLEDGE_RATING")
    private Integer jobKnowledgeRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "QUALITY_RATING")
    private Integer qualityRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "QUANTITY_RATING")
    private Integer quantityRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "DEPENDABILITY_RATING")
    private Integer dependabilityRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "INITIATIVE_RATING")
    private Integer initiativeRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "TEAMWORK_RATING")
    private Integer teamworkRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "COMMUNICATION_RATING")
    private Integer communicationRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "LEADERSHIP_RATING")
    private Integer leadershipRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "PROBLEM_SOLVING_RATING")
    private Integer problemSolvingRating;
    
    @Min(1)
    @Max(5)
    @Column(name = "ADAPTABILITY_RATING")
    private Integer adaptabilityRating;
    
    @Column(name = "STRENGTHS", length = 1000)
    private String strengths;
    
    @Column(name = "AREAS_FOR_IMPROVEMENT", length = 1000)
    private String areasForImprovement;
    
    @Column(name = "GOALS_ACHIEVED", length = 1000)
    private String goalsAchieved;
    
    @Column(name = "GOALS_NOT_ACHIEVED", length = 1000)
    private String goalsNotAchieved;
    
    @Column(name = "NEXT_PERIOD_GOALS", length = 1000)
    private String nextPeriodGoals;
    
    @Column(name = "DEVELOPMENT_PLAN", length = 1000)
    private String developmentPlan;
    
    @Column(name = "TRAINING_NEEDS", length = 1000)
    private String trainingNeeds;
    
    @Column(name = "CAREER_ASPIRATIONS", length = 1000)
    private String careerAspirations;
    
    @Column(name = "MANAGER_COMMENTS", length = 1000)
    private String managerComments;
    
    @Column(name = "EMPLOYEE_COMMENTS", length = 1000)
    private String employeeComments;
    
    @Column(name = "STATUS", length = 20)
    private String status; // DRAFT, SUBMITTED, REVIEWED, APPROVED, COMPLETED
    
    @Column(name = "REVIEWED_BY", length = 50)
    private String reviewedBy;
    
    @Column(name = "REVIEWED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date reviewedDate;
    
    @Column(name = "APPROVED_BY", length = 50)
    private String approvedBy;
    
    @Column(name = "APPROVED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date approvedDate;
    
    @Column(name = "EMPLOYEE_ACKNOWLEDGED")
    private Boolean employeeAcknowledged = false;
    
    @Column(name = "EMPLOYEE_ACKNOWLEDGED_DATE")
    @Temporal(TemporalType.TIMESTAMP)
    private Date employeeAcknowledgedDate;
    
    @Column(name = "SIGNATURE_REQUIRED")
    private Boolean signatureRequired = false;
    
    @Column(name = "EMPLOYEE_SIGNATURE", length = 200)
    private String employeeSignature;
    
    @Column(name = "MANAGER_SIGNATURE", length = 200)
    private String managerSignature;
    
    @Column(name = "HR_SIGNATURE", length = 200)
    private String hrSignature;
    
    // Legacy fields
    @Column(name = "LEGACY_REVIEW_ID", length = 20)
    private String legacyReviewId;
    
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
    
    @Column(name = "NOTES", length = 500)
    private String notes;
    
    // Constructors
    public PerformanceReview() {
    }
    
    public PerformanceReview(Employee employee, Date reviewDate, String reviewPeriod, 
                           Date periodStart, Date periodEnd, Integer overallRating) {
        this.employee = employee;
        this.reviewDate = reviewDate;
        this.reviewPeriod = reviewPeriod;
        this.periodStart = periodStart;
        this.periodEnd = periodEnd;
        this.overallRating = overallRating;
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
    
    public Date getReviewDate() {
        return reviewDate;
    }
    
    public void setReviewDate(Date reviewDate) {
        this.reviewDate = reviewDate;
    }
    
    public String getReviewPeriod() {
        return reviewPeriod;
    }
    
    public void setReviewPeriod(String reviewPeriod) {
        this.reviewPeriod = reviewPeriod;
    }
    
    public Date getPeriodStart() {
        return periodStart;
    }
    
    public void setPeriodStart(Date periodStart) {
        this.periodStart = periodStart;
    }
    
    public Date getPeriodEnd() {
        return periodEnd;
    }
    
    public void setPeriodEnd(Date periodEnd) {
        this.periodEnd = periodEnd;
    }
    
    public Integer getOverallRating() {
        return overallRating;
    }
    
    public void setOverallRating(Integer overallRating) {
        this.overallRating = overallRating;
    }
    
    public Integer getJobKnowledgeRating() {
        return jobKnowledgeRating;
    }
    
    public void setJobKnowledgeRating(Integer jobKnowledgeRating) {
        this.jobKnowledgeRating = jobKnowledgeRating;
    }
    
    public Integer getQualityRating() {
        return qualityRating;
    }
    
    public void setQualityRating(Integer qualityRating) {
        this.qualityRating = qualityRating;
    }
    
    public Integer getQuantityRating() {
        return quantityRating;
    }
    
    public void setQuantityRating(Integer quantityRating) {
        this.quantityRating = quantityRating;
    }
    
    public Integer getDependabilityRating() {
        return dependabilityRating;
    }
    
    public void setDependabilityRating(Integer dependabilityRating) {
        this.dependabilityRating = dependabilityRating;
    }
    
    public Integer getInitiativeRating() {
        return initiativeRating;
    }
    
    public void setInitiativeRating(Integer initiativeRating) {
        this.initiativeRating = initiativeRating;
    }
    
    public Integer getTeamworkRating() {
        return teamworkRating;
    }
    
    public void setTeamworkRating(Integer teamworkRating) {
        this.teamworkRating = teamworkRating;
    }
    
    public Integer getCommunicationRating() {
        return communicationRating;
    }
    
    public void setCommunicationRating(Integer communicationRating) {
        this.communicationRating = communicationRating;
    }
    
    public Integer getLeadershipRating() {
        return leadershipRating;
    }
    
    public void setLeadershipRating(Integer leadershipRating) {
        this.leadershipRating = leadershipRating;
    }
    
    public Integer getProblemSolvingRating() {
        return problemSolvingRating;
    }
    
    public void setProblemSolvingRating(Integer problemSolvingRating) {
        this.problemSolvingRating = problemSolvingRating;
    }
    
    public Integer getAdaptabilityRating() {
        return adaptabilityRating;
    }
    
    public void setAdaptabilityRating(Integer adaptabilityRating) {
        this.adaptabilityRating = adaptabilityRating;
    }
    
    public String getStrengths() {
        return strengths;
    }
    
    public void setStrengths(String strengths) {
        this.strengths = strengths;
    }
    
    public String getAreasForImprovement() {
        return areasForImprovement;
    }
    
    public void setAreasForImprovement(String areasForImprovement) {
        this.areasForImprovement = areasForImprovement;
    }
    
    public String getGoalsAchieved() {
        return goalsAchieved;
    }
    
    public void setGoalsAchieved(String goalsAchieved) {
        this.goalsAchieved = goalsAchieved;
    }
    
    public String getGoalsNotAchieved() {
        return goalsNotAchieved;
    }
    
    public void setGoalsNotAchieved(String goalsNotAchieved) {
        this.goalsNotAchieved = goalsNotAchieved;
    }
    
    public String getNextPeriodGoals() {
        return nextPeriodGoals;
    }
    
    public void setNextPeriodGoals(String nextPeriodGoals) {
        this.nextPeriodGoals = nextPeriodGoals;
    }
    
    public String getDevelopmentPlan() {
        return developmentPlan;
    }
    
    public void setDevelopmentPlan(String developmentPlan) {
        this.developmentPlan = developmentPlan;
    }
    
    public String getTrainingNeeds() {
        return trainingNeeds;
    }
    
    public void setTrainingNeeds(String trainingNeeds) {
        this.trainingNeeds = trainingNeeds;
    }
    
    public String getCareerAspirations() {
        return careerAspirations;
    }
    
    public void setCareerAspirations(String careerAspirations) {
        this.careerAspirations = careerAspirations;
    }
    
    public String getManagerComments() {
        return managerComments;
    }
    
    public void setManagerComments(String managerComments) {
        this.managerComments = managerComments;
    }
    
    public String getEmployeeComments() {
        return employeeComments;
    }
    
    public void setEmployeeComments(String employeeComments) {
        this.employeeComments = employeeComments;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public String getReviewedBy() {
        return reviewedBy;
    }
    
    public void setReviewedBy(String reviewedBy) {
        this.reviewedBy = reviewedBy;
    }
    
    public Date getReviewedDate() {
        return reviewedDate;
    }
    
    public void setReviewedDate(Date reviewedDate) {
        this.reviewedDate = reviewedDate;
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
    
    public Boolean getEmployeeAcknowledged() {
        return employeeAcknowledged;
    }
    
    public void setEmployeeAcknowledged(Boolean employeeAcknowledged) {
        this.employeeAcknowledged = employeeAcknowledged;
    }
    
    public Date getEmployeeAcknowledgedDate() {
        return employeeAcknowledgedDate;
    }
    
    public void setEmployeeAcknowledgedDate(Date employeeAcknowledgedDate) {
        this.employeeAcknowledgedDate = employeeAcknowledgedDate;
    }
    
    public Boolean getSignatureRequired() {
        return signatureRequired;
    }
    
    public void setSignatureRequired(Boolean signatureRequired) {
        this.signatureRequired = signatureRequired;
    }
    
    public String getEmployeeSignature() {
        return employeeSignature;
    }
    
    public void setEmployeeSignature(String employeeSignature) {
        this.employeeSignature = employeeSignature;
    }
    
    public String getManagerSignature() {
        return managerSignature;
    }
    
    public void setManagerSignature(String managerSignature) {
        this.managerSignature = managerSignature;
    }
    
    public String getHrSignature() {
        return hrSignature;
    }
    
    public void setHrSignature(String hrSignature) {
        this.hrSignature = hrSignature;
    }
    
    public String getLegacyReviewId() {
        return legacyReviewId;
    }
    
    public void setLegacyReviewId(String legacyReviewId) {
        this.legacyReviewId = legacyReviewId;
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
    
    public String getNotes() {
        return notes;
    }
    
    public void setNotes(String notes) {
        this.notes = notes;
    }
    
    // Business logic methods that should be in service layer
    public BigDecimal calculateAverageRating() {
        int count = 0;
        int total = 0;
        
        if (jobKnowledgeRating != null) {
            total += jobKnowledgeRating;
            count++;
        }
        if (qualityRating != null) {
            total += qualityRating;
            count++;
        }
        if (quantityRating != null) {
            total += quantityRating;
            count++;
        }
        if (dependabilityRating != null) {
            total += dependabilityRating;
            count++;
        }
        if (initiativeRating != null) {
            total += initiativeRating;
            count++;
        }
        if (teamworkRating != null) {
            total += teamworkRating;
            count++;
        }
        if (communicationRating != null) {
            total += communicationRating;
            count++;
        }
        if (leadershipRating != null) {
            total += leadershipRating;
            count++;
        }
        if (problemSolvingRating != null) {
            total += problemSolvingRating;
            count++;
        }
        if (adaptabilityRating != null) {
            total += adaptabilityRating;
            count++;
        }
        
        if (count > 0) {
            return new BigDecimal(total).divide(new BigDecimal(count), 2, BigDecimal.ROUND_HALF_UP);
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
        if (!(object instanceof PerformanceReview)) {
            return false;
        }
        PerformanceReview other = (PerformanceReview) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }
    
    @Override
    public String toString() {
        return "com.legacy.enterprise.model.PerformanceReview[ id=" + id + " ]";
    }
}
