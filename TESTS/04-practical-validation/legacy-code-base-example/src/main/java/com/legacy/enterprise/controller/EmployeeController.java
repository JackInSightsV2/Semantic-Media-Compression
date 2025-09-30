package com.legacy.enterprise.controller;

import com.legacy.enterprise.model.*;
import com.legacy.enterprise.ejb.*;
import java.util.List;
import java.util.Date;
import java.math.BigDecimal;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.bean.ManagedProperty;
import javax.faces.context.FacesContext;
import javax.faces.application.FacesMessage;
import javax.faces.validator.ValidatorException;
import javax.ejb.EJB;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.io.Serializable;

/**
 * Legacy Employee Controller - JSF Managed Bean
 * This controller has grown over 8+ years with various business logic
 * 
 * @author Legacy Developer (2008)
 * @version 4.1
 * @deprecated This controller has become too complex and should be refactored
 */
@ManagedBean(name = "employeeController")
@SessionScoped
public class EmployeeController implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @EJB
    private EmployeeService employeeService;
    
    @EJB
    private PayrollService payrollService;
    
    // Legacy managed properties that should be removed
    @ManagedProperty(value = "#{userController}")
    private UserController userController;
    
    // Current employee being edited
    private Employee currentEmployee;
    
    // Employee list for display
    private List<Employee> employeeList;
    
    // Search criteria
    private String searchFirstName;
    private String searchLastName;
    private String searchDepartment;
    private Boolean searchActive;
    
    // Pagination
    private int currentPage = 1;
    private int pageSize = 10;
    private int totalPages;
    
    // Legacy fields that should be removed
    private String legacyFilter;
    private Boolean showLegacyEmployees = false;
    
    // Error handling
    private String errorMessage;
    private String successMessage;
    
    // Legacy static variables that should be moved to configuration
    private static final BigDecimal MIN_SALARY = new BigDecimal("15000");
    private static final BigDecimal MAX_SALARY = new BigDecimal("500000");
    private static final int MIN_AGE = 16;
    private static final int MAX_AGE = 80;
    
    /**
     * Constructor
     */
    public EmployeeController() {
        // Legacy initialization
        initializeLegacyData();
    }
    
    /**
     * Legacy initialization method
     * This method should be removed
     * @deprecated Use proper initialization instead
     */
    private void initializeLegacyData() {
        try {
            // Legacy hardcoded initialization
            currentEmployee = new Employee();
            employeeList = new ArrayList<Employee>();
            
            // Legacy error handling
        } catch (Exception e) {
            System.err.println("Legacy initialization error: " + e.getMessage());
        }
    }
    
    /**
     * Load all employees
     * This method has grown over time with various business logic
     */
    public String loadEmployees() {
        try {
            // Legacy business logic that should be moved to service layer
            if (showLegacyEmployees) {
                employeeList = employeeService.findAllEmployees();
            } else {
                employeeList = employeeService.findActiveEmployees();
            }
            
            // Legacy pagination logic that should be improved
            calculatePagination();
            
            return "employeeList";
        } catch (Exception e) {
            // Legacy error handling - should be improved
            errorMessage = "Failed to load employees: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Search employees
     * This method has grown over time with various search criteria
     */
    public String searchEmployees() {
        try {
            Map<String, Object> criteria = new HashMap<String, Object>();
            
            if (searchFirstName != null && !searchFirstName.trim().isEmpty()) {
                criteria.put("firstName", searchFirstName);
            }
            if (searchLastName != null && !searchLastName.trim().isEmpty()) {
                criteria.put("lastName", searchLastName);
            }
            if (searchDepartment != null && !searchDepartment.trim().isEmpty()) {
                criteria.put("department", searchDepartment);
            }
            if (searchActive != null) {
                criteria.put("active", searchActive);
            }
            
            // Legacy search logic that should be improved
            employeeList = employeeService.searchEmployees(criteria);
            
            // Legacy pagination logic
            calculatePagination();
            
            return "employeeList";
        } catch (Exception e) {
            // Legacy error handling
            errorMessage = "Failed to search employees: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Load employee for editing
     */
    public String loadEmployee(Long id) {
        try {
            currentEmployee = employeeService.findEmployeeById(id);
            if (currentEmployee == null) {
                errorMessage = "Employee not found";
                return "error";
            }
            return "editEmployee";
        } catch (Exception e) {
            errorMessage = "Failed to load employee: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Create new employee
     */
    public String createEmployee() {
        try {
            // Legacy validation that should be moved to validators
            if (!validateEmployee(currentEmployee)) {
                return null;
            }
            
            // Legacy business logic that should be moved to service layer
            if (currentEmployee.getBaseSalary().compareTo(MIN_SALARY) < 0) {
                errorMessage = "Salary must be at least $" + MIN_SALARY;
                return null;
            }
            
            if (currentEmployee.getBaseSalary().compareTo(MAX_SALARY) > 0) {
                errorMessage = "Salary cannot exceed $" + MAX_SALARY;
                return null;
            }
            
            // Legacy age validation
            int age = currentEmployee.getAge();
            if (age < MIN_AGE || age > MAX_AGE) {
                errorMessage = "Age must be between " + MIN_AGE + " and " + MAX_AGE;
                return null;
            }
            
            // Legacy business rules
            if (currentEmployee.getDepartment() == null || currentEmployee.getDepartment().trim().isEmpty()) {
                currentEmployee.setDepartment("UNASSIGNED");
            }
            
            if (currentEmployee.getEmployeeType() == null || currentEmployee.getEmployeeType().trim().isEmpty()) {
                currentEmployee.setEmployeeType("FULL_TIME");
            }
            
            if (currentEmployee.getPayFrequency() == null || currentEmployee.getPayFrequency().trim().isEmpty()) {
                currentEmployee.setPayFrequency("BIWEEKLY");
            }
            
            // Legacy audit logging
            logEmployeeAction("CREATE", "Employee created");
            
            employeeService.createEmployee(currentEmployee);
            successMessage = "Employee created successfully";
            
            return "employeeList";
        } catch (Exception e) {
            errorMessage = "Failed to create employee: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Update employee
     */
    public String updateEmployee() {
        try {
            // Legacy validation
            if (!validateEmployee(currentEmployee)) {
                return null;
            }
            
            // Legacy business logic
            if (currentEmployee.getBaseSalary().compareTo(MIN_SALARY) < 0) {
                errorMessage = "Salary must be at least $" + MIN_SALARY;
                return null;
            }
            
            if (currentEmployee.getBaseSalary().compareTo(MAX_SALARY) > 0) {
                errorMessage = "Salary cannot exceed $" + MAX_SALARY;
                return null;
            }
            
            // Legacy age validation
            int age = currentEmployee.getAge();
            if (age < MIN_AGE || age > MAX_AGE) {
                errorMessage = "Age must be between " + MIN_AGE + " and " + MAX_AGE;
                return null;
            }
            
            // Legacy audit logging
            logEmployeeAction("UPDATE", "Employee updated");
            
            employeeService.updateEmployee(currentEmployee);
            successMessage = "Employee updated successfully";
            
            return "employeeList";
        } catch (Exception e) {
            errorMessage = "Failed to update employee: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Delete employee
     */
    public String deleteEmployee(Long id) {
        try {
            // Legacy business logic
            Employee employee = employeeService.findEmployeeById(id);
            if (employee == null) {
                errorMessage = "Employee not found";
                return "error";
            }
            
            // Legacy validation
            if (employee.getActive() != null && employee.getActive()) {
                errorMessage = "Cannot delete active employee";
                return "error";
            }
            
            // Legacy audit logging
            logEmployeeAction("DELETE", "Employee deleted");
            
            employeeService.deleteEmployee(id);
            successMessage = "Employee deleted successfully";
            
            return "employeeList";
        } catch (Exception e) {
            errorMessage = "Failed to delete employee: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Legacy validation method
     * This method has grown over time with various validation rules
     * @deprecated Use proper validation framework instead
     */
    private boolean validateEmployee(Employee employee) {
        if (employee == null) {
            errorMessage = "Employee cannot be null";
            return false;
        }
        
        if (employee.getFirstName() == null || employee.getFirstName().trim().isEmpty()) {
            errorMessage = "First name is required";
            return false;
        }
        
        if (employee.getLastName() == null || employee.getLastName().trim().isEmpty()) {
            errorMessage = "Last name is required";
            return false;
        }
        
        if (employee.getEmail() == null || employee.getEmail().trim().isEmpty()) {
            errorMessage = "Email is required";
            return false;
        }
        
        // Legacy email validation
        if (!employee.getEmail().contains("@")) {
            errorMessage = "Invalid email format";
            return false;
        }
        
        if (employee.getBaseSalary() == null || employee.getBaseSalary().compareTo(BigDecimal.ZERO) <= 0) {
            errorMessage = "Base salary must be greater than zero";
            return false;
        }
        
        if (employee.getDateOfBirth() == null) {
            errorMessage = "Date of birth is required";
            return false;
        }
        
        if (employee.getHireDate() == null) {
            errorMessage = "Hire date is required";
            return false;
        }
        
        // Legacy business rules
        if (employee.getHireDate().before(employee.getDateOfBirth())) {
            errorMessage = "Hire date cannot be before date of birth";
            return false;
        }
        
        return true;
    }
    
    /**
     * Legacy pagination calculation
     * This method should be improved
     * @deprecated Use proper pagination framework instead
     */
    private void calculatePagination() {
        if (employeeList != null && !employeeList.isEmpty()) {
            totalPages = (int) Math.ceil((double) employeeList.size() / pageSize);
        } else {
            totalPages = 0;
        }
    }
    
    /**
     * Legacy audit logging method
     * This method should be replaced with modern audit logging
     * @deprecated Use modern audit logging instead
     */
    private void logEmployeeAction(String action, String description) {
        try {
            // Legacy audit logging logic
            System.out.println("Employee action: " + action + " - " + description);
        } catch (Exception e) {
            // Legacy error handling
            System.err.println("Failed to log employee action: " + e.getMessage());
        }
    }
    
    /**
     * Get employee statistics
     */
    public Map<String, Object> getEmployeeStatistics() {
        try {
            return employeeService.getEmployeeStatistics();
        } catch (Exception e) {
            errorMessage = "Failed to get employee statistics: " + e.getMessage();
            return new HashMap<String, Object>();
        }
    }
    
    /**
     * Legacy method for employee export
     * This method should be improved
     * @deprecated Use proper export framework instead
     */
    public String exportEmployees() {
        try {
            // Legacy export logic
            // This method has been modified multiple times and is inconsistent
            
            return "exportSuccess";
        } catch (Exception e) {
            errorMessage = "Failed to export employees: " + e.getMessage();
            return "error";
        }
    }
    
    /**
     * Legacy method for employee import
     * This method should be improved
     * @deprecated Use proper import framework instead
     */
    public String importEmployees() {
        try {
            // Legacy import logic
            // This method has been modified multiple times and is inconsistent
            
            return "importSuccess";
        } catch (Exception e) {
            errorMessage = "Failed to import employees: " + e.getMessage();
            return "error";
        }
    }
    
    // Getters and Setters
    public Employee getCurrentEmployee() {
        return currentEmployee;
    }
    
    public void setCurrentEmployee(Employee currentEmployee) {
        this.currentEmployee = currentEmployee;
    }
    
    public List<Employee> getEmployeeList() {
        return employeeList;
    }
    
    public void setEmployeeList(List<Employee> employeeList) {
        this.employeeList = employeeList;
    }
    
    public String getSearchFirstName() {
        return searchFirstName;
    }
    
    public void setSearchFirstName(String searchFirstName) {
        this.searchFirstName = searchFirstName;
    }
    
    public String getSearchLastName() {
        return searchLastName;
    }
    
    public void setSearchLastName(String searchLastName) {
        this.searchLastName = searchLastName;
    }
    
    public String getSearchDepartment() {
        return searchDepartment;
    }
    
    public void setSearchDepartment(String searchDepartment) {
        this.searchDepartment = searchDepartment;
    }
    
    public Boolean getSearchActive() {
        return searchActive;
    }
    
    public void setSearchActive(Boolean searchActive) {
        this.searchActive = searchActive;
    }
    
    public int getCurrentPage() {
        return currentPage;
    }
    
    public void setCurrentPage(int currentPage) {
        this.currentPage = currentPage;
    }
    
    public int getPageSize() {
        return pageSize;
    }
    
    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }
    
    public int getTotalPages() {
        return totalPages;
    }
    
    public void setTotalPages(int totalPages) {
        this.totalPages = totalPages;
    }
    
    public String getLegacyFilter() {
        return legacyFilter;
    }
    
    public void setLegacyFilter(String legacyFilter) {
        this.legacyFilter = legacyFilter;
    }
    
    public Boolean getShowLegacyEmployees() {
        return showLegacyEmployees;
    }
    
    public void setShowLegacyEmployees(Boolean showLegacyEmployees) {
        this.showLegacyEmployees = showLegacyEmployees;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
    
    public String getSuccessMessage() {
        return successMessage;
    }
    
    public void setSuccessMessage(String successMessage) {
        this.successMessage = successMessage;
    }
    
    public UserController getUserController() {
        return userController;
    }
    
    public void setUserController(UserController userController) {
        this.userController = userController;
    }
}
