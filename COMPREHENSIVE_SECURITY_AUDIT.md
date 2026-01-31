# Comprehensive Security Audit Report
**Date:** Generated on comprehensive audit  
**Scope:** Full codebase security review

## Executive Summary

This comprehensive security audit identified **multiple critical and high-severity vulnerabilities** across the codebase. While some fixes have been implemented (as documented in `SECURITY_FIXES_SUMMARY.md`), **significant security issues remain** that require immediate attention.

### Critical Findings Summary
- **15+ SQL Injection vulnerabilities** in `dashboard.py` (CRITICAL)
- **766 instances** of `ignore_permissions=True` requiring review (HIGH)
- **Multiple f-string SQL queries** in other modules (MEDIUM-HIGH)
- **Potential command injection** in shell execution functions (MEDIUM)
- **Unsafe eval() usage** in salary slip calculations (MEDIUM)

---

## CRITICAL VULNERABILITIES

### 1. SQL Injection in `dashboard.py` - Multiple Functions (CRITICAL) ⚠️

**Status:** Partially Fixed - 15+ functions still vulnerable

**Location:** `/apps/crm/crm/api/dashboard.py`

**Issue:** Despite having a `validate_user_parameter()` helper function, **15+ functions still directly interpolate user input into SQL queries using f-strings**, creating SQL injection vulnerabilities.

#### Vulnerable Functions:

1. **`get_won_deals()`** - Lines 290-346
   ```python
   if user:
       conds += f" AND d.deal_owner = '{user}'"
   result = frappe.db.sql(f"""SELECT ... {conds} ...""", ...)
   ```

2. **`get_average_won_deal_value()`** - Lines 349-403
   ```python
   if user:
       conds += f" AND d.deal_owner = '{user}'"
   ```

3. **`get_average_deal_value()`** - Lines 406-461
   ```python
   if user:
       conds += f" AND d.deal_owner = '{user}'"
   ```

4. **`get_average_time_to_close_a_lead()`** - Lines 464-515
   ```python
   if user:
       conds += f" AND d.deal_owner = '{user}'"
   ```

5. **`get_average_time_to_close_a_deal()`** - Lines 518-569
   ```python
   if user:
       conds += f" AND d.deal_owner = '{user}'"
   ```

6. **`get_sales_trend()`** - Lines 572-659
   ```python
   if user:
       lead_conds += f" AND lead_owner = '{user}'"
       deal_conds += f" AND deal_owner = '{user}'"
   ```

7. **`get_forecasted_revenue()`** - Lines 662-726
   ```python
   if user:
       deal_conds += f" AND d.deal_owner = '{user}'"
   ```

8. **`get_funnel_conversion()`** - Lines 729-793
   ```python
   if user:
       lead_conds += f" AND lead_owner = '{user}'"
       deal_conds += f" AND deal_owner = '{user}'"
   ```

9. **`get_deals_by_stage_axis()`** - Lines 796-843
   ```python
   if user:
       deal_conds += f" AND d.deal_owner = '{user}'"
   ```

10. **`get_deals_by_stage_donut()`** - Lines 846-887
    ```python
    if user:
        deal_conds += f" AND d.deal_owner = '{user}'"
    ```

11. **`get_lost_deal_reasons()`** - Lines 890-941
    ```python
    if user:
        deal_conds += f" AND d.deal_owner = '{user}'"
    ```

12. **`get_leads_by_source()`** - Lines 944-983
    ```python
    if user:
        lead_conds += f" AND lead_owner = '{user}'"
    ```

13. **`get_deals_by_source()`** - Lines 986-1025
    ```python
    if user:
        deal_conds += f" AND deal_owner = '{user}'"
    ```

14. **`get_deals_by_territory()`** - Lines 1028-1081
    ```python
    if user:
        deal_conds += f" AND d.deal_owner = '{user}'"
    ```

15. **`get_deals_by_salesperson()`** - Lines 1084-1138
    ```python
    if user:
        deal_conds += f" AND d.deal_owner = '{user}'"
    ```

**Vulnerability:**
- User-controlled `user` parameter is directly inserted into SQL using f-strings
- Even if `validate_user_parameter()` is called at the function entry point, the validation can be bypassed if the function is called directly
- The f-string interpolation happens AFTER validation, but the SQL is still constructed unsafely

**Impact:** 
- Full database compromise
- Unauthorized data access
- Data exfiltration
- Privilege escalation

**Recommendation:**
Apply the same pattern used in `get_total_leads()`, `get_ongoing_deals()`, and `get_average_ongoing_deal_value()`:

```python
def get_won_deals(from_date, to_date, user=""):
    # Validate user parameter
    user = validate_user_parameter(user)
    
    diff = frappe.utils.date_diff(to_date, from_date)
    if diff == 0:
        diff = 1

    # Use parameterized query
    user_condition = " AND d.deal_owner = %(user)s" if user else ""
    
    result = frappe.db.sql(
        """
        SELECT
            COUNT(CASE
                WHEN d.closed_date >= %(from_date)s AND d.closed_date < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)
                    AND s.type = 'Won'
                    """ + user_condition + """
                THEN d.name
                ELSE NULL
            END) as current_month_deals,
            ...
        FROM `tabCRM Deal` d
        JOIN `tabCRM Deal Status` s ON d.status = s.name
        """,
        {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
            "user": user,
        } if user else {
            "from_date": from_date,
            "to_date": to_date,
            "prev_from_date": frappe.utils.add_days(from_date, -diff),
        },
        as_dict=1,
    )
    ...
```

---

### 2. SQL Injection in Other Modules (HIGH)

**Location:** Multiple files across the codebase

**Issue:** Found 72+ instances of f-string SQL queries that may be vulnerable to SQL injection.

#### Examples:

1. **`apps/erpnext/erpnext/bulk_transaction/doctype/bulk_transaction_log/bulk_transaction_log.py:34`**
   ```python
   f"select exists (select * from `tabBulk Transaction Log Detail` where date = '{self.name}');"
   ```
   - **Risk:** If `self.name` is user-controlled, this is vulnerable
   - **Status:** Needs review

2. **`apps/erpnext/erpnext/setup/doctype/transaction_deletion_record/transaction_deletion_record.py:401`**
   ```python
   f"""select max(name) from `tab{doctype_name}`
   ```
   - **Risk:** `doctype_name` should be validated against a whitelist
   - **Status:** Needs review

3. **`apps/frappe/frappe/database/postgres/setup_db.py:15`**
   ```python
   if root_conn.sql(f"SELECT 1 FROM pg_roles WHERE rolname='{frappe.conf.db_name}'"):
   ```
   - **Risk:** `db_name` from config should be safe, but worth verifying
   - **Status:** Low risk, but should use parameterization

**Recommendation:**
- Audit all f-string SQL queries
- Replace with parameterized queries
- Validate all user inputs
- Use whitelist validation for table/doctype names

---

## HIGH SEVERITY VULNERABILITIES

### 3. Authorization Bypass via `ignore_permissions=True` (HIGH)

**Location:** 766 instances found across the codebase

**Issue:** Extensive use of `ignore_permissions=True` bypasses Frappe's permission system.

**Analysis:**
- Many instances are in **test files** (legitimate use)
- Many instances are in **setup/installation scripts** (legitimate use)
- **Some instances are in production code** (requires review)

#### Critical Areas Requiring Review:

1. **Production API endpoints** - Any `ignore_permissions=True` in whitelisted functions
2. **Document hooks** - `on_update`, `validate`, etc. that bypass permissions
3. **Background jobs** - Should verify permissions even in background tasks
4. **System operations** - Should be limited to specific system-level operations

**Recommendation:**
1. Create a whitelist of legitimate uses (tests, setup, system operations)
2. Review all production code instances
3. Add explicit permission checks where `ignore_permissions` is used
4. Document why `ignore_permissions` is necessary for each instance

**Example of problematic usage:**
```python
@frappe.whitelist()
def some_api_function(docname):
    doc = frappe.get_doc("Some DocType", docname)
    doc.save(ignore_permissions=True)  # BAD - No permission check
```

**Should be:**
```python
@frappe.whitelist()
def some_api_function(docname):
    doc = frappe.get_doc("Some DocType", docname)
    # Check permissions
    if not frappe.has_permission("Some DocType", "write", doc):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    doc.save()  # Remove ignore_permissions
```

---

### 4. Command Injection Risk (MEDIUM-HIGH)

**Location:** `apps/frappe/frappe/utils/__init__.py:445`

**Issue:** The `execute_in_shell()` function uses `shell=True` with user-controlled input.

```python
def execute_in_shell(cmd, verbose=False, low_priority=False, check_exit_code=False):
    import shlex
    from subprocess import Popen
    
    if isinstance(cmd, list):
        cmd = shlex.join(cmd)  # Good - uses shlex
    
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        kwargs = {
            "shell": True,  # RISK: shell=True
            "stdout": stdout,
            "stderr": stderr,
            "executable": shutil.which("bash") or "/bin/bash",
        }
        p = Popen(cmd, **kwargs)  # cmd could be user-controlled
```

**Vulnerability:**
- If `cmd` is a string and contains user input, command injection is possible
- Even with `shlex.join()`, if the original `cmd` string contains shell metacharacters, it's risky

**Recommendation:**
1. **Prefer list format** - Always pass commands as lists, not strings
2. **Avoid shell=True** when possible - Use `subprocess.run(cmd, shell=False)` with list arguments
3. **Validate inputs** - Sanitize any user input before passing to shell functions
4. **Use frappe.commands.popen()** - Which has better security practices

**Safer approach:**
```python
def execute_in_shell(cmd, verbose=False, low_priority=False, check_exit_code=False):
    from subprocess import Popen
    
    # Ensure cmd is a list
    if isinstance(cmd, str):
        import shlex
        cmd = shlex.split(cmd)
    
    # Use shell=False for better security
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        kwargs = {
            "shell": False,  # Safer
            "stdout": stdout,
            "stderr": stderr,
        }
        p = Popen(cmd, **kwargs)
```

---

### 5. Unsafe eval() Usage (MEDIUM)

**Location:** `apps/hrms/hrms/payroll/doctype/salary_slip/salary_slip.py:2340`

**Issue:** The `_safe_eval()` function uses `eval()` which can be dangerous.

```python
def _safe_eval(code: str, eval_globals: dict | None = None, eval_locals: dict | None = None):
    ...
    return eval(code, eval_globals, eval_locals)  # nosemgrep
```

**Analysis:**
- The function name suggests it's "safe" but uses `eval()` directly
- There's a `_check_attributes()` function that may provide some protection
- The `nosemgrep` comment suggests this was reviewed, but needs verification

**Recommendation:**
1. Review the `_check_attributes()` function to ensure it properly restricts eval
2. Consider using `ast.literal_eval()` for simple expressions
3. Use a restricted execution environment
4. Document what expressions are allowed

---

## MEDIUM SEVERITY ISSUES

### 6. Path Traversal Risk

**Location:** `apps/frappe/frappe/core/doctype/file/file.py:585`

**Issue:** File path construction from user input.

**Analysis:**
- The code does use `is_safe_path()` validation (line 612)
- File names are validated (line 615)
- However, the path construction logic is complex and should be reviewed

**Recommendation:**
- Continue using `is_safe_path()` validation
- Add additional path normalization
- Test with various path traversal attempts (`../`, `..\\`, etc.)

---

### 7. XSS Prevention

**Location:** Multiple frontend components

**Analysis:**
- Frappe has `frappe.utils.xss_sanitise()` function (found in `frappe/public/js/frappe/utils/common.js`)
- Some Vue components use `v-html` which could be risky
- ContentEditable components need careful review

**Examples:**
- `apps/insights/frontend/src/components/ContentEditable.vue` - Uses `innerHTML` when `noHtml=false`
- `apps/insights/frontend/src2/query/components/AlertSetupDialog.vue:249` - Uses `v-html`

**Recommendation:**
1. Always sanitize user input before rendering with `v-html` or `innerHTML`
2. Use `frappe.utils.xss_sanitise()` for all user-generated content
3. Prefer text content over HTML when possible
4. Use Content Security Policy (CSP) headers

---

### 8. Insecure Deserialization

**Location:** Multiple locations using pickle

**Analysis:**
- Found pickle usage in various places
- Most appear to be in third-party libraries (pandas, etc.)
- The `BaseDocument.__getstate__()` method properly handles unpicklable values

**Recommendation:**
- Avoid unpickling data from untrusted sources
- Use JSON for data serialization when possible
- If pickle is necessary, validate the source

---

## CODE QUALITY & BEST PRACTICES

### 9. Missing Input Validation

**Location:** Multiple API endpoints

**Issue:** Some endpoints don't validate input types, ranges, or formats.

**Recommendation:**
- Implement comprehensive input validation framework
- Validate all user inputs at API boundaries
- Use type hints and validation libraries
- Implement whitelist validation where possible

### 10. Error Information Disclosure

**Location:** Error handling throughout codebase

**Issue:** Some error messages may expose internal details.

**Recommendation:**
- Sanitize error messages in production
- Log detailed errors server-side
- Return generic messages to clients
- Avoid exposing stack traces to end users

### 11. Missing Rate Limiting

**Location:** All API endpoints

**Issue:** No rate limiting on API endpoints.

**Recommendation:**
- Implement rate limiting for API endpoints
- Especially for:
  - Authentication endpoints
  - File upload endpoints
  - Search endpoints
  - Expensive operations

---

## PRIORITY FIXES

### Immediate (Critical - Fix Now)

1. ✅ **Fix SQL injection in `dashboard.py`** - 15+ functions need parameterized queries
2. ⚠️ **Review and fix SQL injection in other modules** - Audit all f-string SQL queries
3. ⚠️ **Review `ignore_permissions=True` usage** - Identify and fix authorization bypasses in production code

### Short-term (High Priority - Fix This Week)

1. **Fix command injection risks** - Review and secure shell execution functions
2. **Review eval() usage** - Ensure safe execution environment
3. **Implement input validation** - Add validation to all API endpoints
4. **Add rate limiting** - Protect against DoS attacks

### Medium-term (Fix This Month)

1. **XSS prevention review** - Audit all HTML rendering
2. **Path traversal testing** - Comprehensive testing of file operations
3. **Error handling improvement** - Prevent information disclosure
4. **Security logging** - Log security events for monitoring

---

## TESTING RECOMMENDATIONS

### 1. SQL Injection Testing
- Test all dashboard functions with SQL injection payloads
- Test with various user parameter values
- Verify parameterized queries prevent injection

### 2. Authorization Testing
- Test that users can only access their own data
- Test that permission checks work correctly
- Test with different user roles

### 3. Input Validation Testing
- Test with invalid inputs (wrong types, out of range, etc.)
- Test with malicious inputs (XSS, SQL injection, etc.)
- Test edge cases

### 4. Penetration Testing
- Conduct professional penetration testing
- Use tools like OWASP ZAP, Burp Suite
- Test all identified vulnerabilities

---

## FILES REQUIRING IMMEDIATE ATTENTION

1. **`/apps/crm/crm/api/dashboard.py`** - 15+ SQL injection vulnerabilities
2. **`/apps/erpnext/erpnext/bulk_transaction/doctype/bulk_transaction_log/bulk_transaction_log.py`** - SQL injection risk
3. **`/apps/erpnext/erpnext/setup/doctype/transaction_deletion_record/transaction_deletion_record.py`** - SQL injection risk
4. **`/apps/frappe/frappe/utils/__init__.py`** - Command injection risk
5. **`/apps/hrms/hrms/payroll/doctype/salary_slip/salary_slip.py`** - eval() usage review

---

## CONCLUSION

The codebase has **critical SQL injection vulnerabilities** that require **immediate attention**. While some security fixes have been implemented, **15+ functions in `dashboard.py` remain vulnerable** to SQL injection attacks.

**Priority Actions:**
1. **Fix all SQL injection vulnerabilities in `dashboard.py`** (CRITICAL)
2. **Audit and fix SQL injection in other modules** (CRITICAL)
3. **Review `ignore_permissions=True` usage in production code** (HIGH)
4. **Secure shell execution functions** (HIGH)
5. **Implement comprehensive input validation** (HIGH)

**Estimated Time to Fix Critical Issues:** 2-3 days for SQL injection fixes in dashboard.py

---

**Report Generated By:** Comprehensive Security Audit  
**Next Review Date:** After critical fixes are implemented  
**Contact:** Security Team

