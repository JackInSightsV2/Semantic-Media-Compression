/**
 * Legacy JavaScript Functions - Accumulated over 8+ years
 * This file has grown significantly and contains many legacy functions
 * 
 * @author Legacy Developer (2008)
 * @version 3.1
 * @deprecated This file has become too complex and should be refactored
 */

// Legacy global variables that should be removed
var legacyGlobalVar = null;
var legacyCounter = 0;
var legacyFlags = {
    debug: true,
    legacy: true,
    deprecated: true
};

// Legacy utility functions that should be removed
function legacyUtilityFunction() {
    // Legacy function that has been modified multiple times
    console.log("Legacy utility function called");
    return true;
}

// Legacy validation functions
function validateEmployeeForm() {
    // Legacy validation logic that should be moved to proper validation framework
    var firstName = document.getElementById("firstName");
    var lastName = document.getElementById("lastName");
    var email = document.getElementById("email");
    var salary = document.getElementById("baseSalary");
    
    var errors = [];
    
    if (!firstName || firstName.value.trim() === "") {
        errors.push("First name is required");
    }
    
    if (!lastName || lastName.value.trim() === "") {
        errors.push("Last name is required");
    }
    
    if (!email || email.value.trim() === "") {
        errors.push("Email is required");
    } else if (!isValidEmail(email.value)) {
        errors.push("Invalid email format");
    }
    
    if (!salary || salary.value.trim() === "") {
        errors.push("Base salary is required");
    } else if (isNaN(salary.value) || parseFloat(salary.value) <= 0) {
        errors.push("Base salary must be a positive number");
    }
    
    if (errors.length > 0) {
        showLegacyErrors(errors);
        return false;
    }
    
    return true;
}

function validatePayrollForm() {
    // Legacy validation logic that should be moved to proper validation framework
    var startDate = document.getElementById("payPeriodStart");
    var endDate = document.getElementById("payPeriodEnd");
    
    var errors = [];
    
    if (!startDate || startDate.value.trim() === "") {
        errors.push("Pay period start date is required");
    }
    
    if (!endDate || endDate.value.trim() === "") {
        errors.push("Pay period end date is required");
    }
    
    if (startDate && endDate && startDate.value && endDate.value) {
        var start = new Date(startDate.value);
        var end = new Date(endDate.value);
        
        if (start >= end) {
            errors.push("Pay period start date must be before end date");
        }
    }
    
    if (errors.length > 0) {
        showLegacyErrors(errors);
        return false;
    }
    
    return true;
}

// Legacy email validation
function isValidEmail(email) {
    // Legacy email validation that should be improved
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Legacy error handling
function showLegacyErrors(errors) {
    // Legacy error display logic that should be improved
    var errorDiv = document.getElementById("errorMessages");
    if (!errorDiv) {
        errorDiv = document.createElement("div");
        errorDiv.id = "errorMessages";
        errorDiv.className = "error-messages";
        document.body.appendChild(errorDiv);
    }
    
    errorDiv.innerHTML = "<ul>" + errors.map(function(error) {
        return "<li>" + error + "</li>";
    }).join("") + "</ul>";
    errorDiv.style.display = "block";
}

function hideLegacyErrors() {
    // Legacy error hiding logic
    var errorDiv = document.getElementById("errorMessages");
    if (errorDiv) {
        errorDiv.style.display = "none";
    }
}

// Legacy success handling
function showLegacySuccess(message) {
    // Legacy success display logic that should be improved
    var successDiv = document.getElementById("successMessages");
    if (!successDiv) {
        successDiv = document.createElement("div");
        successDiv.id = "successMessages";
        successDiv.className = "success-messages";
        document.body.appendChild(successDiv);
    }
    
    successDiv.innerHTML = message;
    successDiv.style.display = "block";
    
    // Legacy auto-hide after 5 seconds
    setTimeout(function() {
        successDiv.style.display = "none";
    }, 5000);
}

// Legacy form handling
function handleLegacyFormSubmit(formId) {
    // Legacy form submission logic that should be improved
    var form = document.getElementById(formId);
    if (!form) {
        console.error("Form not found: " + formId);
        return false;
    }
    
    // Legacy validation
    if (formId === "employeeForm") {
        if (!validateEmployeeForm()) {
            return false;
        }
    } else if (formId === "payrollForm") {
        if (!validatePayrollForm()) {
            return false;
        }
    }
    
    // Legacy form processing
    hideLegacyErrors();
    showLegacyLoading();
    
    return true;
}

// Legacy loading handling
function showLegacyLoading() {
    // Legacy loading display logic
    var loadingDiv = document.getElementById("loadingDiv");
    if (!loadingDiv) {
        loadingDiv = document.createElement("div");
        loadingDiv.id = "loadingDiv";
        loadingDiv.className = "loading";
        loadingDiv.innerHTML = "Loading...";
        document.body.appendChild(loadingDiv);
    }
    
    loadingDiv.style.display = "block";
}

function hideLegacyLoading() {
    // Legacy loading hiding logic
    var loadingDiv = document.getElementById("loadingDiv");
    if (loadingDiv) {
        loadingDiv.style.display = "none";
    }
}

// Legacy table handling
function handleLegacyTableSort(columnIndex) {
    // Legacy table sorting logic that should be improved
    console.log("Sorting table by column: " + columnIndex);
    // Legacy sorting implementation
}

function handleLegacyTableFilter(filterValue) {
    // Legacy table filtering logic that should be improved
    console.log("Filtering table with: " + filterValue);
    // Legacy filtering implementation
}

// Legacy pagination handling
function handleLegacyPagination(action) {
    // Legacy pagination logic that should be improved
    console.log("Pagination action: " + action);
    // Legacy pagination implementation
}

// Legacy AJAX handling
function legacyAjaxRequest(url, data, callback) {
    // Legacy AJAX implementation that should be replaced with modern fetch/axios
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                if (callback) {
                    callback(xhr.responseText);
                }
            } else {
                console.error("AJAX request failed: " + xhr.status);
            }
        }
    };
    
    xhr.send(data);
}

// Legacy date handling
function formatLegacyDate(date) {
    // Legacy date formatting that should be improved
    if (!date) return "";
    
    var d = new Date(date);
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var year = d.getFullYear();
    
    return month + "/" + day + "/" + year;
}

function parseLegacyDate(dateString) {
    // Legacy date parsing that should be improved
    if (!dateString) return null;
    
    var parts = dateString.split("/");
    if (parts.length === 3) {
        return new Date(parts[2], parts[0] - 1, parts[1]);
    }
    
    return new Date(dateString);
}

// Legacy number handling
function formatLegacyCurrency(amount) {
    // Legacy currency formatting that should be improved
    if (!amount) return "$0.00";
    
    return "$" + parseFloat(amount).toFixed(2);
}

function parseLegacyCurrency(currencyString) {
    // Legacy currency parsing that should be improved
    if (!currencyString) return 0;
    
    return parseFloat(currencyString.replace("$", "").replace(",", ""));
}

// Legacy utility functions
function legacyUtilityFunction1() {
    // Legacy utility function that has been modified multiple times
    console.log("Legacy utility function 1 called");
    return true;
}

function legacyUtilityFunction2() {
    // Legacy utility function that has been modified multiple times
    console.log("Legacy utility function 2 called");
    return true;
}

function legacyUtilityFunction3() {
    // Legacy utility function that has been modified multiple times
    console.log("Legacy utility function 3 called");
    return true;
}

// Legacy event handling
function addLegacyEventListeners() {
    // Legacy event listener setup that should be improved
    document.addEventListener("DOMContentLoaded", function() {
        // Legacy initialization
        console.log("Legacy event listeners added");
    });
}

// Legacy debugging
function legacyDebug(message) {
    // Legacy debugging function that should be improved
    if (legacyFlags.debug) {
        console.log("[LEGACY DEBUG] " + message);
    }
}

function legacyWarning(message) {
    // Legacy warning function that should be improved
    console.warn("[LEGACY WARNING] " + message);
}

function legacyError(message) {
    // Legacy error function that should be improved
    console.error("[LEGACY ERROR] " + message);
}

// Legacy initialization
function legacyInitialize() {
    // Legacy initialization function that should be improved
    console.log("Legacy system initializing...");
    
    // Legacy setup
    addLegacyEventListeners();
    
    // Legacy configuration
    legacyDebug("Legacy system initialized");
}

// Legacy cleanup
function legacyCleanup() {
    // Legacy cleanup function that should be improved
    console.log("Legacy system cleaning up...");
    
    // Legacy cleanup logic
    hideLegacyErrors();
    hideLegacyLoading();
    
    legacyDebug("Legacy system cleaned up");
}

// Legacy global error handling
window.onerror = function(message, source, lineno, colno, error) {
    // Legacy global error handling that should be improved
    legacyError("Global error: " + message + " at " + source + ":" + lineno + ":" + colno);
    return false;
};

// Legacy initialization on page load
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", legacyInitialize);
} else {
    legacyInitialize();
}

// Legacy cleanup on page unload
window.addEventListener("beforeunload", legacyCleanup);
