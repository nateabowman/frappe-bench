/**
 * Chart helper utilities
 */

/**
 * Format currency value for charts
 */
export function formatCurrency(value, currency = "USD") {
	return new Intl.NumberFormat("en-US", {
		style: "currency",
		currency: currency,
		minimumFractionDigits: 0,
	}).format(value)
}

/**
 * Format percentage value
 */
export function formatPercentage(value, decimals = 1) {
	return `${value.toFixed(decimals)}%`
}

/**
 * Get chart color by index
 */
export function getChartColor(index) {
	const colors = [
		"#3b82f6", // blue
		"#10b981", // green
		"#f59e0b", // yellow
		"#ef4444", // red
		"#8b5cf6", // purple
		"#ec4899", // pink
		"#06b6d4", // cyan
		"#84cc16", // lime
	]
	return colors[index % colors.length]
}

/**
 * Generate gradient colors for charts
 */
export function getGradientColors(baseColor, opacity = 0.3) {
	return {
		type: "linear",
		gradientToColors: [baseColor],
		stops: [0, 100],
		opacityFrom: opacity,
		opacityTo: 0.1,
	}
}

/**
 * Format date for chart labels
 */
export function formatChartDate(dateString, format = "short") {
	const date = new Date(dateString)
	
	if (format === "short") {
		return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
	} else if (format === "month") {
		return date.toLocaleDateString("en-US", { month: "short", year: "numeric" })
	} else if (format === "year") {
		return date.toLocaleDateString("en-US", { year: "numeric" })
	}
	
	return date.toLocaleDateString("en-US")
}

/**
 * Calculate trend (increase/decrease percentage)
 */
export function calculateTrend(current, previous) {
	if (!previous || previous === 0) return null
	const change = ((current - previous) / previous) * 100
	return {
		value: change,
		isPositive: change >= 0,
		formatted: `${change >= 0 ? "+" : ""}${change.toFixed(1)}%`,
	}
}

/**
 * Get heatmap color intensity based on value
 */
export function getHeatmapColor(value, maxValue) {
	if (!maxValue || maxValue === 0) return "bg-gray-200"
	
	const intensity = value / maxValue
	
	if (intensity < 0.2) return "bg-blue-200"
	if (intensity < 0.4) return "bg-blue-400"
	if (intensity < 0.6) return "bg-blue-600"
	if (intensity < 0.8) return "bg-blue-700"
	return "bg-blue-800"
}
