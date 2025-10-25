package com.legacy.enterprise.ejb;

import com.legacy.enterprise.model.*;
import java.util.List;
import java.util.Date;
import java.math.BigDecimal;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Legacy Payroll Service EJB - Complex payroll processing logic
 * This service has grown over 8+ years with various business rules
 * 
 * @author Legacy Developer (2009)
 * @version 2.5
 * @deprecated This service has become too complex and should be refactored
 */
@Stateless
@TransactionAttribute(TransactionAttributeType.REQUIRED)
public class PayrollService {
    
    @PersistenceContext(unitName = "LegacyHRPU")
    private EntityManager em;
    
    // Legacy static variables that should be moved to configuration
    private static final BigDecimal OVERTIME_RATE = new BigDecimal("1.5");
    private static final BigDecimal DOUBLE_TIME_RATE = new BigDecimal("2.0");
    private static final BigDecimal HOLIDAY_RATE = new BigDecimal("1.5");
    private static final int REGULAR_HOURS_PER_WEEK = 40;
    private static final int REGULAR_HOURS_PER_DAY = 8;
    
    // Legacy hardcoded tax rates that should be configurable
    private static final BigDecimal FEDERAL_TAX_RATE = new BigDecimal("0.22");
    private static final BigDecimal STATE_TAX_RATE = new BigDecimal("0.05");
    private static final BigDecimal SOCIAL_SECURITY_RATE = new BigDecimal("0.062");
    private static final BigDecimal MEDICARE_RATE = new BigDecimal("0.0145");
    private static final BigDecimal ADDITIONAL_MEDICARE_RATE = new BigDecimal("0.009");
    
    /**
     * Process payroll for all employees
     * This method has grown over time with various business rules
     */
    public List<PayrollCalculation> processPayroll(Date payPeriodStart, Date payPeriodEnd) {
        List<PayrollCalculation> payrollCalculations = new ArrayList<PayrollCalculation>();
        
        // Get all active employees
        Query query = em.createNamedQuery("Employee.findActive");
        List<Employee> employees = query.getResultList();
        
        for (Employee employee : employees) {
            try {
                PayrollCalculation payroll = calculateEmployeePayroll(employee, payPeriodStart, payPeriodEnd);
                if (payroll != null) {
                    em.persist(payroll);
                    payrollCalculations.add(payroll);
                    
                    // Legacy audit logging
                    logPayrollAction(employee, payroll, "PROCESS", "Payroll processed");
                }
            } catch (Exception e) {
                // Legacy error handling - should be improved
                System.err.println("Failed to process payroll for employee " + employee.getId() + ": " + e.getMessage());
                
                // Create error payroll record
                PayrollCalculation errorPayroll = createErrorPayroll(employee, payPeriodStart, payPeriodEnd, e.getMessage());
                em.persist(errorPayroll);
                payrollCalculations.add(errorPayroll);
            }
        }
        
        return payrollCalculations;
    }
    
    /**
     * Calculate payroll for a specific employee
     * This method has grown over time with various business rules
     */
    public PayrollCalculation calculateEmployeePayroll(Employee employee, Date payPeriodStart, Date payPeriodEnd) {
        if (employee == null) {
            throw new IllegalArgumentException("Employee cannot be null");
        }
        
        PayrollCalculation payroll = new PayrollCalculation(employee, new Date(), payPeriodStart, payPeriodEnd);
        
        // Complex business logic for different employee types
        if ("FULL_TIME".equals(employee.getEmployeeType())) {
            calculateFullTimePayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        } else if ("PART_TIME".equals(employee.getEmployeeType())) {
            calculatePartTimePayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        } else if ("CONTRACTOR".equals(employee.getEmployeeType())) {
            calculateContractorPayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        } else if ("INTERN".equals(employee.getEmployeeType())) {
            calculateInternPayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        } else {
            // Legacy fallback logic
            calculateLegacyPayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        }
        
        // Calculate taxes
        calculateTaxes(employee, payroll);
        
        // Calculate benefits
        calculateBenefits(employee, payroll);
        
        // Calculate totals
        payroll.calculateTotals();
        
        // Set status
        payroll.setStatus("PROCESSED");
        payroll.setProcessedDate(new Date());
        
        return payroll;
    }
    
    /**
     * Complex full-time payroll calculation
     * This method has grown over time with various business rules
     */
    private void calculateFullTimePayroll(Employee employee, PayrollCalculation payroll, 
                                        Date payPeriodStart, Date payPeriodEnd) {
        // Get time entries for the period
        List<TimeEntry> timeEntries = getTimeEntriesForPeriod(employee.getId(), payPeriodStart, payPeriodEnd);
        
        BigDecimal totalRegularHours = BigDecimal.ZERO;
        BigDecimal totalOvertimeHours = BigDecimal.ZERO;
        BigDecimal totalDoubleTimeHours = BigDecimal.ZERO;
        BigDecimal totalHolidayHours = BigDecimal.ZERO;
        BigDecimal totalVacationHours = BigDecimal.ZERO;
        BigDecimal totalSickHours = BigDecimal.ZERO;
        
        for (TimeEntry entry : timeEntries) {
            if (entry.getRegularHours() != null) {
                totalRegularHours = totalRegularHours.add(entry.getRegularHours());
            }
            if (entry.getOvertimeHours() != null) {
                totalOvertimeHours = totalOvertimeHours.add(entry.getOvertimeHours());
            }
            if (entry.getDoubleTimeHours() != null) {
                totalDoubleTimeHours = totalDoubleTimeHours.add(entry.getDoubleTimeHours());
            }
            if (entry.getHolidayHours() != null) {
                totalHolidayHours = totalHolidayHours.add(entry.getHolidayHours());
            }
            if (entry.getVacationHours() != null) {
                totalVacationHours = totalVacationHours.add(entry.getVacationHours());
            }
            if (entry.getSickHours() != null) {
                totalSickHours = totalSickHours.add(entry.getSickHours());
            }
        }
        
        // Calculate regular pay (bi-weekly salary)
        BigDecimal regularPay = employee.getBaseSalary().divide(new BigDecimal("26"), 2, BigDecimal.ROUND_HALF_UP);
        payroll.setRegularPay(regularPay);
        
        // Calculate overtime pay
        if (totalOvertimeHours.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal overtimeRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP)
                                            .multiply(OVERTIME_RATE);
            BigDecimal overtimePay = totalOvertimeHours.multiply(overtimeRate);
            payroll.setOvertimePay(overtimePay);
        }
        
        // Calculate double time pay
        if (totalDoubleTimeHours.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal doubleTimeRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP)
                                               .multiply(DOUBLE_TIME_RATE);
            BigDecimal doubleTimePay = totalDoubleTimeHours.multiply(doubleTimeRate);
            payroll.setDoubleTimePay(doubleTimePay);
        }
        
        // Calculate holiday pay
        if (totalHolidayHours.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal holidayRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP)
                                           .multiply(HOLIDAY_RATE);
            BigDecimal holidayPay = totalHolidayHours.multiply(holidayRate);
            payroll.setHolidayPay(holidayPay);
        }
        
        // Calculate vacation pay
        if (totalVacationHours.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal vacationRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP);
            BigDecimal vacationPay = totalVacationHours.multiply(vacationRate);
            payroll.setVacationPay(vacationPay);
        }
        
        // Calculate sick pay
        if (totalSickHours.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal sickRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP);
            BigDecimal sickPay = totalSickHours.multiply(sickRate);
            payroll.setSickPay(sickPay);
        }
        
        // Calculate gross pay
        BigDecimal grossPay = regularPay;
        if (payroll.getOvertimePay() != null) {
            grossPay = grossPay.add(payroll.getOvertimePay());
        }
        if (payroll.getDoubleTimePay() != null) {
            grossPay = grossPay.add(payroll.getDoubleTimePay());
        }
        if (payroll.getHolidayPay() != null) {
            grossPay = grossPay.add(payroll.getHolidayPay());
        }
        if (payroll.getVacationPay() != null) {
            grossPay = grossPay.add(payroll.getVacationPay());
        }
        if (payroll.getSickPay() != null) {
            grossPay = grossPay.add(payroll.getSickPay());
        }
        
        payroll.setGrossPay(grossPay);
        
        // Set hours
        payroll.setRegularHours(totalRegularHours);
        payroll.setOvertimeHours(totalOvertimeHours);
        payroll.setDoubleTimeHours(totalDoubleTimeHours);
        payroll.setHolidayHours(totalHolidayHours);
        payroll.setVacationHours(totalVacationHours);
        payroll.setSickHours(totalSickHours);
    }
    
    /**
     * Complex part-time payroll calculation
     */
    private void calculatePartTimePayroll(Employee employee, PayrollCalculation payroll, 
                                       Date payPeriodStart, Date payPeriodEnd) {
        // Similar logic to full-time but with different rates
        // This method has been copied and modified from full-time calculation
        // Should be refactored to use common logic
        
        List<TimeEntry> timeEntries = getTimeEntriesForPeriod(employee.getId(), payPeriodStart, payPeriodEnd);
        
        BigDecimal totalRegularHours = BigDecimal.ZERO;
        BigDecimal totalOvertimeHours = BigDecimal.ZERO;
        
        for (TimeEntry entry : timeEntries) {
            if (entry.getRegularHours() != null) {
                totalRegularHours = totalRegularHours.add(entry.getRegularHours());
            }
            if (entry.getOvertimeHours() != null) {
                totalOvertimeHours = totalOvertimeHours.add(entry.getOvertimeHours());
            }
        }
        
        // Part-time employees get overtime after 8 hours per day
        BigDecimal hourlyRate = employee.getHourlyRate();
        if (hourlyRate == null) {
            hourlyRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP);
        }
        
        BigDecimal regularPay = totalRegularHours.multiply(hourlyRate);
        payroll.setRegularPay(regularPay);
        
        if (totalOvertimeHours.compareTo(BigDecimal.ZERO) > 0) {
            BigDecimal overtimeRate = hourlyRate.multiply(OVERTIME_RATE);
            BigDecimal overtimePay = totalOvertimeHours.multiply(overtimeRate);
            payroll.setOvertimePay(overtimePay);
        }
        
        BigDecimal grossPay = regularPay;
        if (payroll.getOvertimePay() != null) {
            grossPay = grossPay.add(payroll.getOvertimePay());
        }
        
        payroll.setGrossPay(grossPay);
        payroll.setRegularHours(totalRegularHours);
        payroll.setOvertimeHours(totalOvertimeHours);
    }
    
    /**
     * Complex contractor payroll calculation
     */
    private void calculateContractorPayroll(Employee employee, PayrollCalculation payroll, 
                                         Date payPeriodStart, Date payPeriodEnd) {
        // Contractors have different rules
        // This logic has been added over time and is inconsistent
        
        List<TimeEntry> timeEntries = getTimeEntriesForPeriod(employee.getId(), payPeriodStart, payPeriodEnd);
        
        BigDecimal totalHours = BigDecimal.ZERO;
        for (TimeEntry entry : timeEntries) {
            if (entry.getRegularHours() != null) {
                totalHours = totalHours.add(entry.getRegularHours());
            }
        }
        
        BigDecimal hourlyRate = employee.getHourlyRate();
        if (hourlyRate == null) {
            hourlyRate = employee.getBaseSalary().divide(new BigDecimal("2080"), 2, BigDecimal.ROUND_HALF_UP);
        }
        
        BigDecimal grossPay = totalHours.multiply(hourlyRate);
        payroll.setGrossPay(grossPay);
        payroll.setRegularPay(grossPay);
        payroll.setRegularHours(totalHours);
    }
    
    /**
     * Complex intern payroll calculation
     */
    private void calculateInternPayroll(Employee employee, PayrollCalculation payroll, 
                                      Date payPeriodStart, Date payPeriodEnd) {
        // Interns have different rules
        // This logic has been added over time and is inconsistent
        
        List<TimeEntry> timeEntries = getTimeEntriesForPeriod(employee.getId(), payPeriodStart, payPeriodEnd);
        
        BigDecimal totalHours = BigDecimal.ZERO;
        for (TimeEntry entry : timeEntries) {
            if (entry.getRegularHours() != null) {
                totalHours = totalHours.add(entry.getRegularHours());
            }
        }
        
        BigDecimal hourlyRate = employee.getHourlyRate();
        if (hourlyRate == null) {
            hourlyRate = new BigDecimal("15.00"); // Default intern rate
        }
        
        BigDecimal grossPay = totalHours.multiply(hourlyRate);
        payroll.setGrossPay(grossPay);
        payroll.setRegularPay(grossPay);
        payroll.setRegularHours(totalHours);
    }
    
    /**
     * Legacy payroll calculation method
     * This method is kept for backward compatibility
     * @deprecated Use specific calculation methods instead
     */
    private void calculateLegacyPayroll(Employee employee, PayrollCalculation payroll, 
                                     Date payPeriodStart, Date payPeriodEnd) {
        // Legacy calculation logic
        // This method has been modified multiple times and is inconsistent
        
        BigDecimal grossPay = employee.getBaseSalary().divide(new BigDecimal("26"), 2, BigDecimal.ROUND_HALF_UP);
        payroll.setGrossPay(grossPay);
        payroll.setRegularPay(grossPay);
        payroll.setRegularHours(new BigDecimal("40"));
    }
    
    /**
     * Complex tax calculation method
     * This method has grown over time with various tax rules
     */
    private void calculateTaxes(Employee employee, PayrollCalculation payroll) {
        BigDecimal grossPay = payroll.getGrossPay();
        if (grossPay == null || grossPay.compareTo(BigDecimal.ZERO) <= 0) {
            return;
        }
        
        // Federal tax calculation
        BigDecimal federalTax = grossPay.multiply(FEDERAL_TAX_RATE);
        payroll.setFederalTax(federalTax);
        
        // State tax calculation
        BigDecimal stateTax = grossPay.multiply(STATE_TAX_RATE);
        payroll.setStateTax(stateTax);
        
        // Social Security calculation
        BigDecimal socialSecurity = grossPay.multiply(SOCIAL_SECURITY_RATE);
        payroll.setSocialSecurity(socialSecurity);
        
        // Medicare calculation
        BigDecimal medicare = grossPay.multiply(MEDICARE_RATE);
        payroll.setMedicare(medicare);
        
        // Additional Medicare for high earners
        if (grossPay.multiply(new BigDecimal("26")).compareTo(new BigDecimal("200000")) > 0) {
            BigDecimal additionalMedicare = grossPay.multiply(ADDITIONAL_MEDICARE_RATE);
            payroll.setAdditionalMedicare(additionalMedicare);
        }
        
        // Calculate total taxes
        BigDecimal totalTaxes = federalTax.add(stateTax).add(socialSecurity).add(medicare);
        if (payroll.getAdditionalMedicare() != null) {
            totalTaxes = totalTaxes.add(payroll.getAdditionalMedicare());
        }
        payroll.setTotalTaxes(totalTaxes);
    }
    
    /**
     * Complex benefits calculation method
     * This method has grown over time with various benefit rules
     */
    private void calculateBenefits(Employee employee, PayrollCalculation payroll) {
        // Get active benefit enrollments
        List<BenefitEnrollment> benefits = getActiveBenefitEnrollments(employee.getId());
        
        BigDecimal totalBenefits = BigDecimal.ZERO;
        
        for (BenefitEnrollment benefit : benefits) {
            if (benefit.getEmployeeCost() != null) {
                totalBenefits = totalBenefits.add(benefit.getEmployeeCost());
                
                // Set specific benefit deductions
                if ("HEALTH".equals(benefit.getBenefitType())) {
                    payroll.setHealthInsurance(benefit.getEmployeeCost());
                } else if ("DENTAL".equals(benefit.getBenefitType())) {
                    payroll.setDentalInsurance(benefit.getEmployeeCost());
                } else if ("VISION".equals(benefit.getBenefitType())) {
                    payroll.setVisionInsurance(benefit.getEmployeeCost());
                } else if ("LIFE".equals(benefit.getBenefitType())) {
                    payroll.setLifeInsurance(benefit.getEmployeeCost());
                } else if ("DISABILITY".equals(benefit.getBenefitType())) {
                    payroll.setDisabilityInsurance(benefit.getEmployeeCost());
                } else if ("RETIREMENT".equals(benefit.getBenefitType())) {
                    payroll.setRetirement401k(benefit.getEmployeeCost());
                }
            }
        }
        
        payroll.setTotalBenefits(totalBenefits);
    }
    
    /**
     * Get time entries for a specific period
     */
    private List<TimeEntry> getTimeEntriesForPeriod(Long employeeId, Date startDate, Date endDate) {
        Query query = em.createNamedQuery("TimeEntry.findByEmployeeAndDateRange");
        query.setParameter("employeeId", employeeId);
        query.setParameter("startDate", startDate);
        query.setParameter("endDate", endDate);
        return query.getResultList();
    }
    
    /**
     * Get active benefit enrollments for an employee
     */
    private List<BenefitEnrollment> getActiveBenefitEnrollments(Long employeeId) {
        Query query = em.createNamedQuery("BenefitEnrollment.findByEmployee");
        query.setParameter("employeeId", employeeId);
        List<BenefitEnrollment> allBenefits = query.getResultList();
        
        List<BenefitEnrollment> activeBenefits = new ArrayList<BenefitEnrollment>();
        for (BenefitEnrollment benefit : allBenefits) {
            if (benefit.getActive() != null && benefit.getActive()) {
                activeBenefits.add(benefit);
            }
        }
        
        return activeBenefits;
    }
    
    /**
     * Create error payroll record
     */
    private PayrollCalculation createErrorPayroll(Employee employee, Date payPeriodStart, Date payPeriodEnd, String errorMessage) {
        PayrollCalculation errorPayroll = new PayrollCalculation(employee, new Date(), payPeriodStart, payPeriodEnd);
        errorPayroll.setStatus("ERROR");
        errorPayroll.setErrorMessage(errorMessage);
        errorPayroll.setGrossPay(BigDecimal.ZERO);
        errorPayroll.setNetPay(BigDecimal.ZERO);
        return errorPayroll;
    }
    
    /**
     * Legacy audit logging method for payroll
     * @deprecated Use modern audit logging instead
     */
    private void logPayrollAction(Employee employee, PayrollCalculation payroll, String action, String description) {
        try {
            LegacyAuditLog auditLog = new LegacyAuditLog(employee, action, new Date());
            auditLog.setNotes(description + " - Payroll ID: " + payroll.getId());
            auditLog.setUserId("SYSTEM");
            em.persist(auditLog);
        } catch (Exception e) {
            // Legacy error handling - should be improved
            System.err.println("Failed to log payroll action: " + e.getMessage());
        }
    }
    
    /**
     * Get payroll calculations for a specific period
     */
    public List<PayrollCalculation> getPayrollCalculations(Date startDate, Date endDate) {
        Query query = em.createNamedQuery("PayrollCalculation.findByDateRange");
        query.setParameter("startDate", startDate);
        query.setParameter("endDate", endDate);
        return query.getResultList();
    }
    
    /**
     * Get payroll calculations for a specific employee
     */
    public List<PayrollCalculation> getPayrollCalculations(Long employeeId) {
        Query query = em.createNamedQuery("PayrollCalculation.findByEmployee");
        query.setParameter("employeeId", employeeId);
        return query.getResultList();
    }
    
    /**
     * Approve payroll calculation
     */
    public void approvePayrollCalculation(Long payrollId, String approvedBy) {
        PayrollCalculation payroll = em.find(PayrollCalculation.class, payrollId);
        if (payroll != null) {
            payroll.setStatus("APPROVED");
            payroll.setApprovedBy(approvedBy);
            payroll.setApprovedDate(new Date());
            em.merge(payroll);
        }
    }
    
    /**
     * Legacy method for payroll statistics
     * This method has grown over time with various statistics
     */
    public Map<String, Object> getPayrollStatistics(Date startDate, Date endDate) {
        Map<String, Object> stats = new HashMap<String, Object>();
        
        // Total payroll calculations
        Query totalQuery = em.createQuery("SELECT COUNT(p) FROM PayrollCalculation p WHERE p.calculationDate BETWEEN :startDate AND :endDate");
        totalQuery.setParameter("startDate", startDate);
        totalQuery.setParameter("endDate", endDate);
        Long totalCalculations = (Long) totalQuery.getSingleResult();
        stats.put("totalCalculations", totalCalculations);
        
        // Total gross pay
        Query grossQuery = em.createQuery("SELECT SUM(p.grossPay) FROM PayrollCalculation p WHERE p.calculationDate BETWEEN :startDate AND :endDate");
        grossQuery.setParameter("startDate", startDate);
        grossQuery.setParameter("endDate", endDate);
        BigDecimal totalGrossPay = (BigDecimal) grossQuery.getSingleResult();
        stats.put("totalGrossPay", totalGrossPay);
        
        // Total net pay
        Query netQuery = em.createQuery("SELECT SUM(p.netPay) FROM PayrollCalculation p WHERE p.calculationDate BETWEEN :startDate AND :endDate");
        netQuery.setParameter("startDate", startDate);
        netQuery.setParameter("endDate", endDate);
        BigDecimal totalNetPay = (BigDecimal) netQuery.getSingleResult();
        stats.put("totalNetPay", totalNetPay);
        
        // Total taxes
        Query taxQuery = em.createQuery("SELECT SUM(p.totalTaxes) FROM PayrollCalculation p WHERE p.calculationDate BETWEEN :startDate AND :endDate");
        taxQuery.setParameter("startDate", startDate);
        taxQuery.setParameter("endDate", endDate);
        BigDecimal totalTaxes = (BigDecimal) taxQuery.getSingleResult();
        stats.put("totalTaxes", totalTaxes);
        
        return stats;
    }
}
