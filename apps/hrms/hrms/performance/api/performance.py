# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_360_feedback(employee):
	"""Get 360-degree feedback summary"""
	
	# This would query Feedback 360 doctype when created
	# For now, return structure based on existing appraisals
	
	appraisals = frappe.get_all(
		"Appraisal",
		filters={"employee": employee, "docstatus": 1},
		fields=["name", "final_score", "appraisal_cycle", "creation"],
		order_by="creation desc",
		limit=5
	)
	
	return {
		"employee": employee,
		"recent_appraisals": appraisals,
		"average_score": sum(a.final_score for a in appraisals if a.final_score) / len(appraisals) if appraisals else 0,
		"feedback_sources": {
			"self": [],
			"manager": [],
			"peers": []
		}
	}


@frappe.whitelist()
def get_goal_progress(employee):
	"""Get goal/KPI tracking progress"""
	
	# This would query Goal Tracking doctype when created
	# For now, use existing Appraisal Goals
	
	goals = frappe.get_all(
		"Appraisal Goal",
		filters={"employee": employee},
		fields=["name", "kra", "per_weightage", "score"],
		order_by="creation desc"
	)
	
	total_weight = sum(g.per_weightage or 0 for g in goals)
	weighted_score = sum((g.per_weightage or 0) * (g.score or 0) for g in goals) / total_weight if total_weight > 0 else 0
	
	return {
		"goals": goals,
		"total_goals": len(goals),
		"weighted_score": round(weighted_score, 2),
		"completion_rate": len([g for g in goals if g.score and g.score >= 80]) / len(goals) * 100 if goals else 0
	}


@frappe.whitelist()
def get_skills_matrix(employee=None, department=None):
	"""Get skills matrix analysis"""
	
	filters = {}
	if employee:
		filters["employee"] = employee
	
	# Get employee skills
	employee_skills = frappe.get_all(
		"Employee Skill Map",
		filters=filters,
		fields=["employee", "skill", "proficiency", "evaluation_date"]
	)
	
	# Get required skills for designation
	required_skills = {}
	if employee:
		emp_doc = frappe.get_cached_doc("Employee", employee)
		if emp_doc.designation:
			designation_skills = frappe.get_all(
				"Designation Skill",
				filters={"parent": emp_doc.designation},
				fields=["skill", "mandatory"]
			)
			required_skills = {ds.skill: ds.mandatory for ds in designation_skills}
	
	# Analyze skill gaps
	skill_gaps = []
	for skill, mandatory in required_skills.items():
		emp_skill = next((es for es in employee_skills if es.skill == skill), None)
		if not emp_skill or (emp_skill.proficiency or 0) < 70:
			skill_gaps.append({
				"skill": skill,
				"mandatory": mandatory,
				"current_proficiency": emp_skill.proficiency if emp_skill else 0,
				"status": "gap"
			})
	
	return {
		"employee_skills": employee_skills,
		"required_skills": required_skills,
		"skill_gaps": skill_gaps,
		"training_recommendations": [
			{"skill": gap["skill"], "priority": "high" if gap["mandatory"] else "medium"}
			for gap in skill_gaps
		]
	}
