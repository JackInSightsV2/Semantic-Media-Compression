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
import javax.persistence.TypedQuery;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Legacy Employee Service EJB - Complex business logic with technical debt
 * This service has grown over 8+ years with various business rules
 * 
 * @author Legacy Developer (2008)
 * @version 3.2
 * @deprecated This service has become too complex and should be refactored
 */
@Stateless
@TransactionAttribute(TransactionAttributeType.REQUIRED)
public class EmployeeService {
    
    @PersistenceContext(unitName = "LegacyHRPU")
    private EntityManager em;
    
    // Legacy static variables that should be moved to configuration
    private static final BigDecimal OVERTIME_RATE = new BigDecimal("1.5");
    private static final BigDecimal DOUBLE_TIME_RATE = new BigDecimal("2.0");
    private static final BigDecimal HOLIDAY_RATE = new BigDecimal("1.5");
    private static final int REGULAR_HOURS_PER_WEEK = 40;
    private static final int REGULAR_HOURS_PER_DAY = 8;
    
    // Legacy hardcoded values that should be configurable
    private static final BigDecimal FEDERAL_TAX_RATE = new BigDecimal("0.22");
    private static final BigDecimal STATE_TAX_RATE = new BigDecimal("0.05");
    private static final BigDecimal SOCIAL_SECURITY_RATE = new BigDecimal("0.062");
    private static final BigDecimal MEDICARE_RATE = new BigDecimal("0.0145");
    
    /**
     * Legacy method - should be removed but referenced in 20+ places
     * @deprecated Use findEmployeeById instead
     */
    public Employee getEmployee(Long id) {
        return em.find(Employee.class, id);
    }
    
    public Employee findEmployeeById(Long id) {
        return em.find(Employee.class, id);
    }
    
    public List<Employee> findAllEmployees() {
        Query query = em.createNamedQuery("Employee.findAll");
        return query.getResultList();
    }
    
    public List<Employee> findEmployeesByDepartment(String department) {
        Query query = em.createNamedQuery("Employee.findByDepartment");
        query.setParameter("dept", department);
        return query.getResultList();
    }
    
    public List<Employee> findActiveEmployees() {
        Query query = em.createNamedQuery("Employee.findActive");
        return query.getResultList();
    }
    
    /**
     * Complex business logic for employee creation
     * This method has grown over time with various validation rules
     */
    public Employee createEmployee(Employee employee) {
        // Legacy validation logic that should be moved to validators
        if (employee.getFirstName() == null || employee.getFirstName().trim().isEmpty()) {
            throw new IllegalArgumentException("First name is required");
        }
        if (employee.getLastName() == null || employee.getLastName().trim().isEmpty()) {
            throw new IllegalArgumentException("Last name is required");
        }
        if (employee.getEmail() == null || employee.getEmail().trim().isEmpty()) {
            throw new IllegalArgumentException("Email is required");
        }
        if (employee.getBaseSalary() == null || employee.getBaseSalary().compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Base salary must be greater than zero");
        }
        
        // Legacy business rules that should be configurable
        if (employee.getDepartment() == null) {
            employee.setDepartment("UNASSIGNED");
        }
        if (employee.getEmployeeType() == null) {
            employee.setEmployeeType("FULL_TIME");
        }
        if (employee.getPayFrequency() == null) {
            employee.setPayFrequency("BIWEEKLY");
        }
        
        // Legacy audit logging
        logEmployeeAction(employee, "CREATE", "Employee created");
        
        em.persist(employee);
        return employee;
    }
    
    public Employee updateEmployee(Employee employee) {
        // Legacy validation
        if (employee.getId() == null) {
            throw new IllegalArgumentException("Employee ID is required for update");
        }
        
        // Legacy audit logging
        logEmployeeAction(employee, "UPDATE", "Employee updated");
        
        return em.merge(employee);
    }
    
    public void deleteEmployee(Long id) {
        Employee employee = em.find(Employee.class, id);
        if (employee != null) {
            // Legacy audit logging
            logEmployeeAction(employee, "DELETE", "Employee deleted");
            
            em.remove(employee);
        }
    }
    
    /**
     * Complex payroll calculation method
     * This method has grown significantly over time with various business rules
     */
    public PayrollCalculation calculatePayroll(Long employeeId, Date payPeriodStart, Date payPeriodEnd) {
        Employee employee = em.find(Employee.class, employeeId);
        if (employee == null) {
            throw new IllegalArgumentException("Employee not found");
        }
        
        PayrollCalculation payroll = new PayrollCalculation(employee, new Date(), payPeriodStart, payPeriodEnd);
        
        // Complex business logic for different employee types
        if ("FULL_TIME".equals(employee.getEmployeeType())) {
            calculateFullTimePayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        } else if ("PART_TIME".equals(employee.getEmployeeType())) {
            calculatePartTimePayroll(employee, payroll, payPeriodStart, payPeriodEnd);
        } else if ("CONTRACTOR".equals(employee.getEmployeeType())) {
            calculateContractorPayroll(employee, payroll, payPeriodStart, payPeriodEnd);
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
        
        // Legacy audit logging
        logPayrollAction(employee, payroll, "CALCULATE", "Payroll calculated");
        
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
        }
        
        // Calculate regular pay
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
        
        payroll.setGrossPay(grossPay);
        
        // Set hours
        payroll.setRegularHours(totalRegularHours);
        payroll.setOvertimeHours(totalOvertimeHours);
        payroll.setDoubleTimeHours(totalDoubleTimeHours);
        payroll.setHolidayHours(totalHolidayHours);
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
            BigDecimal additionalMedicare = grossPay.multiply(new BigDecimal("0.009"));
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
     * Legacy audit logging method
     * This method should be replaced with modern audit logging
     * @deprecated Use modern audit logging instead
     */
    private void logEmployeeAction(Employee employee, String action, String description) {
        try {
            LegacyAuditLog auditLog = new LegacyAuditLog(employee, action, new Date());
            auditLog.setNotes(description);
            auditLog.setUserId("SYSTEM");
            em.persist(auditLog);
        } catch (Exception e) {
            // Legacy error handling - should be improved
            System.err.println("Failed to log employee action: " + e.getMessage());
        }
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
     * Legacy method for complex employee search
     * This method has grown over time with various search criteria
     * @deprecated Use specific search methods instead
     */
    public List<Employee> searchEmployees(Map<String, Object> criteria) {
        StringBuilder jpql = new StringBuilder("SELECT e FROM Employee e WHERE 1=1");
        
        if (criteria.containsKey("firstName")) {
            jpql.append(" AND e.firstName LIKE :firstName");
        }
        if (criteria.containsKey("lastName")) {
            jpql.append(" AND e.lastName LIKE :lastName");
        }
        if (criteria.containsKey("department")) {
            jpql.append(" AND e.department = :department");
        }
        if (criteria.containsKey("active")) {
            jpql.append(" AND e.active = :active");
        }
        
        Query query = em.createQuery(jpql.toString());
        
        if (criteria.containsKey("firstName")) {
            query.setParameter("firstName", "%" + criteria.get("firstName") + "%");
        }
        if (criteria.containsKey("lastName")) {
            query.setParameter("lastName", "%" + criteria.get("lastName") + "%");
        }
        if (criteria.containsKey("department")) {
            query.setParameter("department", criteria.get("department"));
        }
        if (criteria.containsKey("active")) {
            query.setParameter("active", criteria.get("active"));
        }
        
        return query.getResultList();
    }
    
    /**
     * Legacy method for employee statistics
     * This method has grown over time with various statistics
     */
    public Map<String, Object> getEmployeeStatistics() {
        Map<String, Object> stats = new HashMap<String, Object>();
        
        // Total employees
        Query totalQuery = em.createQuery("SELECT COUNT(e) FROM Employee e");
        Long totalEmployees = (Long) totalQuery.getSingleResult();
        stats.put("totalEmployees", totalEmployees);
        
        // Active employees
        Query activeQuery = em.createQuery("SELECT COUNT(e) FROM Employee e WHERE e.active = true");
        Long activeEmployees = (Long) activeQuery.getSingleResult();
        stats.put("activeEmployees", activeEmployees);
        
        // Employees by department
        Query deptQuery = em.createQuery("SELECT e.department, COUNT(e) FROM Employee e GROUP BY e.department");
        List<Object[]> deptResults = deptQuery.getResultList();
        Map<String, Long> deptStats = new HashMap<String, Long>();
        for (Object[] result : deptResults) {
            deptStats.put((String) result[0], (Long) result[1]);
        }
        stats.put("departmentStats", deptStats);
        
        return stats;
    }
}
