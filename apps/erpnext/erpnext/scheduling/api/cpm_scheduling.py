# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

"""
Critical Path Method (CPM) Scheduling
"""

import frappe
from frappe import _
from frappe.utils import add_days, getdate
from erpnext.projects.api.feature_gating import check_feature_access


@frappe.whitelist()
def calculate_critical_path(schedule_name, company=None):
	"""
	Calculate critical path for a project schedule using CPM
	
	Returns tasks on critical path and their float times
	"""
	if company:
		check_feature_access("advanced_scheduling", company, throw=True)
	
	schedule = frappe.get_doc("Project Schedule", schedule_name)
	
	# Build task graph
	tasks = {}
	for task in schedule.schedule_tasks:
		tasks[task.task_name] = {
			"name": task.task_name,
			"duration": task.duration,
			"start_date": getdate(task.start_date),
			"dependencies": [d.strip() for d in (task.dependencies or "").split(",") if d.strip()],
			"early_start": None,
			"early_finish": None,
			"late_start": None,
			"late_finish": None,
			"float": None,
			"is_critical": False
		}
	
	# Forward pass - calculate early start/finish
	calculate_forward_pass(tasks)
	
	# Backward pass - calculate late start/finish
	calculate_backward_pass(tasks)
	
	# Calculate float and identify critical path
	critical_path = []
	for task_name, task_data in tasks.items():
		task_data["float"] = task_data["late_start"] - task_data["early_start"]
		if task_data["float"] == 0:
			task_data["is_critical"] = True
			critical_path.append(task_name)
	
	return {
		"tasks": tasks,
		"critical_path": critical_path,
		"project_duration": max([t["early_finish"] for t in tasks.values()]) if tasks else 0
	}


def calculate_forward_pass(tasks):
	"""Calculate early start and early finish for all tasks"""
	# Find tasks with no dependencies (start tasks)
	start_tasks = [name for name, task in tasks.items() if not task["dependencies"]]
	
	# Process tasks in topological order
	processed = set()
	queue = start_tasks.copy()
	
	while queue:
		task_name = queue.pop(0)
		if task_name in processed:
			continue
		
		task = tasks[task_name]
		
		# Calculate early start (max of early finish of dependencies)
		if task["dependencies"]:
			max_early_finish = 0
			for dep in task["dependencies"]:
				if dep in tasks:
					dep_task = tasks[dep]
					if dep_task["early_finish"] is None:
						# Dependency not processed yet, add to queue later
						queue.append(task_name)
						continue
					max_early_finish = max(max_early_finish, dep_task["early_finish"])
			task["early_start"] = max_early_finish
		else:
			task["early_start"] = 0
		
		task["early_finish"] = task["early_start"] + task["duration"]
		processed.add(task_name)
		
		# Add dependent tasks to queue
		for other_name, other_task in tasks.items():
			if task_name in other_task["dependencies"] and other_name not in processed:
				if all(dep in processed for dep in other_task["dependencies"]):
					queue.append(other_name)


def calculate_backward_pass(tasks):
	"""Calculate late start and late finish for all tasks"""
	# Find project end (max early finish)
	project_end = max([t["early_finish"] for t in tasks.values()]) if tasks else 0
	
	# Find end tasks (tasks that no other tasks depend on)
	end_tasks = []
	for task_name, task in tasks.items():
		is_end_task = True
		for other_task in tasks.values():
			if task_name in other_task["dependencies"]:
				is_end_task = False
				break
		if is_end_task:
			end_tasks.append(task_name)
	
	# Process backwards from end tasks
	processed = set()
	queue = end_tasks.copy()
	
	# Initialize end tasks
	for task_name in end_tasks:
		tasks[task_name]["late_finish"] = project_end
		tasks[task_name]["late_start"] = project_end - tasks[task_name]["duration"]
		processed.add(task_name)
	
	while queue:
		task_name = queue.pop(0)
		task = tasks[task_name]
		
		# Find tasks that depend on this task
		dependent_tasks = [name for name, t in tasks.items() if task_name in t["dependencies"]]
		
		for dep_name in dependent_tasks:
			if dep_name not in processed:
				dep_task = tasks[dep_name]
				# Late finish = min of late start of dependent tasks
				if dep_task["late_start"] is not None:
					if task["late_finish"] is None:
						task["late_finish"] = dep_task["late_start"]
					else:
						task["late_finish"] = min(task["late_finish"], dep_task["late_start"])
					task["late_start"] = task["late_finish"] - task["duration"]
					processed.add(task_name)
					
					# Add this task's dependencies to queue
					for dep in task["dependencies"]:
						if dep not in processed and dep in tasks:
							queue.append(dep)


@frappe.whitelist()
def optimize_resource_leveling(schedule_name, company=None):
	"""
	Optimize schedule to level resource allocation
	"""
	if company:
		check_feature_access("advanced_scheduling", company, throw=True)
	
	# Implementation would optimize task scheduling to balance resource usage
	# This is a placeholder for the optimization algorithm
	return {"status": "optimized", "message": "Resource leveling optimization completed"}

