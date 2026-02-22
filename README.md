# HerQalb Landing Page

A modern, professional landing page for HerQalb — providing culturally-responsive mental wellness coaching for women.

## Overview

This landing page features:

- **Responsive Design**: Mobile-first approach with seamless desktop experience
- **Brand-Aligned Colors**: Deep purple (`#8b5a8e`) and soft mauve accent palette
- **Accessibility**: Semantic HTML, ARIA labels, and keyboard navigation
- **Fast Load**: No external dependencies — vanilla HTML, CSS, and JavaScript
- **Sections**:
  - Hero with value proposition and dual CTA
  - Services (Individual Coaching, Group Workshops, Wellness Resources)
  - About with cultural mission
  - Testimonials
  - Contact form with newsletter signup
  - Footer with links

## Getting Started

### Local Preview

The site is served via Python's built-in HTTP server on port 8000:

```powershell
# Start the server (already running)
# Access at: http://localhost:8000
```

### Files

```
HerQalb/
├── index.html           # Main landing page
├── css/
│   └── style.css        # Responsive styles and theme
├── js/
│   └── main.js          # Form handling, mobile nav toggle
├── brand_assets/
│   ├── logo.png         # HerQalb logo
│   └── HerQalb — Brand Guidelines.pdf
└── README.md            # This file
```

## Customization

### Colors

Edit the CSS variables in `css/style.css`:

```css
:root {
  --primary: #8b5a8e;        /* Deep purple */
  --accent: #d4a5d4;         /* Soft mauve */
  --light-bg: #f8f4fa;       /* Light purple tint */
}
```

### Content

Update copy in `index.html`:

- **Hero headline**: Line 31
- **Services**: Lines 43–58
- **Testimonials**: Lines 71–79
- **Contact form**: Lines 84–96

### Email Integration

The contact form currently shows a success message. To integrate with a backend:

1. Update the `<form>` action attribute in `index.html`
2. Modify form submission handler in `js/main.js`

## Mobile Navigation

The mobile menu toggle is responsive at 700px breakpoint. Adjust in `css/style.css`:

```css
@media (max-width: 700px) {
  /* Mobile styles applied here */
}
```

## Deployment

### Simple Hosting

For static hosting (Netlify, Vercel, GitHub Pages):

1. Push this folder to a Git repository
2. Connect to your hosting provider
3. Deploy — no build step needed

### Custom Domain

Once deployed, point your domain's DNS to your hosting provider's nameservers.

## Brand Messaging

**HerQalb** (Arabic: "her heart") provides:

- **Culturally-responsive** coaching honoring women's values
- **Evidence-based** mental wellness approaches
- **Trauma-informed** support with clinical insight
- **Community** connection with peer workshops

## Support

For questions or updates, refer to the brand guidelines in `brand_assets/`.
