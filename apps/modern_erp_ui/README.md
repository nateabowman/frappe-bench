# Modern ERP UI

A contemporary, modern UI theme for ERPNext and Frappe Framework that provides a fresh, professional interface with enhanced user experience.

## ✨ Features

- **Modern Design System**: Clean, professional interface with a cohesive color palette
- **Smooth Animations**: Elegant transitions and hover effects throughout
- **Enhanced Forms**: Better input validation and user feedback
- **Responsive Design**: Works beautifully on all screen sizes
- **Dark Mode Ready**: Built-in support for dark mode preferences
- **Accessibility**: Improved keyboard navigation and screen reader support
- **Performance**: Lightweight CSS and optimized JavaScript

## 🎨 Design Highlights

- **Color Palette**: Modern indigo and purple gradients
- **Typography**: Clean, readable font stack with proper hierarchy
- **Spacing**: Consistent spacing system using CSS custom properties
- **Shadows**: Subtle depth with modern shadow system
- **Border Radius**: Rounded corners for a friendly, modern feel

## 📦 Installation

### Using Bench CLI

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app modern_erp_ui
bench install-app modern_erp_ui
bench build --app modern_erp_ui
bench restart
```

### Manual Installation

1. Clone or copy this app to your `apps` directory
2. Run `bench install-app modern_erp_ui`
3. Build assets: `bench build --app modern_erp_ui`
4. Restart your Frappe server

## 🚀 Usage

Once installed, the Modern ERP UI theme will automatically apply to your ERPNext/Frappe installation. The theme enhances:

- **Navigation Bar**: Modern, clean navigation with smooth hover effects
- **Buttons**: Gradient buttons with ripple effects
- **Forms**: Enhanced input fields with validation feedback
- **Tables**: Modern data tables with hover effects
- **Cards**: Elevated card designs with shadows
- **Login Page**: Beautiful gradient login page
- **Modals**: Modern dialog boxes
- **Alerts**: Color-coded notification system

## 🎯 Customization

The theme uses CSS custom properties (variables) that can be easily customized. Edit `modern_erp_ui/public/css/modern_erp_ui.css` and modify the `:root` variables:

```css
:root {
    --primary-color: #6366f1;  /* Your primary color */
    --secondary-color: #8b5cf6; /* Your secondary color */
    /* ... more variables */
}
```

## ⌨️ Keyboard Shortcuts

- `Ctrl/Cmd + K`: Focus search
- `Escape`: Close modals

## 🔧 Development

### Building Assets

```bash
# Development build
bench build --app modern_erp_ui

# Production build (minified)
bench build --app modern_erp_ui --production
```

### File Structure

```
modern_erp_ui/
├── modern_erp_ui/
│   ├── __init__.py
│   ├── hooks.py
│   └── public/
│       ├── css/
│       │   └── modern_erp_ui.css
│       └── js/
│           └── modern_erp_ui.js
├── pyproject.toml
└── README.md
```

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🐛 Troubleshooting

**Theme not applying?**
- Clear browser cache
- Rebuild assets: `bench build --app modern_erp_ui --force`
- Check that the app is installed: `bench list-apps`

**Styles conflicting?**
- The theme uses specific selectors to avoid conflicts
- Check browser console for CSS errors
- Ensure no other theme apps are conflicting

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on the repository.

---

**Enjoy your modern ERP experience!** 🎉

