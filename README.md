# Audacis - A Clean Zola Theme

A minimal, elegant Zola theme for personal websites, portfolios, CVs, and blogs. Features support for curated lists and BibTeX publications.

## Features

- 📱 Fully responsive design with mobile menu
- 📝 Blog with tags and summaries
- 📄 CV/Resume page with sections for experience, education, skills, and publications
- 📚 Curated lists with ratings, years, and expandable notes
- 📖 BibTeX support for academic publications
- 🎨 Customizable color scheme
- 💻 Syntax highlighting with copy buttons
- 🔍 Clean, readable typography
- ⚡ Fast and lightweight

## Installation

### As a Theme (Recommended for reuse)

1. Create a `themes` directory in your Zola project:
   ```bash
   mkdir themes
   ```

2. Clone or copy this theme into the themes directory:
   ```bash
   cd themes
   git clone https://github.com/yourusername/audacis.git
   # or copy the audacis-template directory to themes/audacis
   ```

3. Update your `config.toml`:
   ```toml
   theme = "audacis"
   ```

### As a Template (For direct customization)

1. Clone this repository as your site:
   ```bash
   git clone https://github.com/yourusername/audacis.git my-website
   cd my-website
   ```

2. Start customizing the content and styles directly

## Configuration

### Basic Configuration

Edit your `config.toml`:

```toml
base_url = "https://yoursite.com"
title = "Your Name"
compile_sass = true
build_search_index = true

taxonomies = [
    {name = "tags", feed = true},
]

[extra]
# Primary color (used throughout the site)
primary_color = "#384b63"

# Meta separator (used between date and tags)
meta_separator = "•"

# Profile image path (optional)
profile_image = "/images/profile.png"

# Number of recent posts to show on homepage
recent_posts_count = 3

# Show CV intro on homepage
show_cv_intro = true

# Navigation menu items
menu = [
    { name = "Home", url = "@/_index.md" },
    { name = "Blog", url = "@/blog/_index.md" },
    { name = "Lists", url = "@/lists/_index.md" },
    { name = "CV", url = "@/cv/_index.md" },
]
```

### CV Configuration

To use BibTeX for publications, add to your `content/cv/_index.md`:

```toml
+++
title = "Curriculum Vitae"
template = "cv.html"

[extra]
publications_show_count = 5
bibtex_file = "static/data/publications.bib"
+++
```

Place your BibTeX file at `static/data/publications.bib`.

### Curated Lists

Create list pages with custom items. See `content/lists/books.md` for an example:

```toml
+++
title = "Reading List"
template = "list.html"

[[extra.items]]
title = "Clean Code"
year = 2008
rating = 5
link = "https://example.com"
description = "A great book on software craftsmanship"
+++
```

## Content Structure

```
content/
├── _index.md           # Homepage
├── blog/
│   ├── _index.md       # Blog index
│   └── post.md         # Blog posts
├── lists/
│   ├── _index.md       # Lists index
│   └── books.md        # Example list
└── cv/
    └── _index.md       # CV page
```

## Customization

### Colors

Change the primary color in `config.toml`:

```toml
[extra]
primary_color = "#your-color"
```

### Styles

Modify `sass/style.scss` to customize the appearance.

### Templates

Key templates:
- `base.html` - Base layout
- `index.html` - Homepage
- `section.html` - Section pages
- `page.html` - Individual pages
- `cv.html` - CV page
- `list.html` - Curated lists

## License

MIT License - feel free to use and modify for your projects.

## Credits

Created with [Zola](https://www.getzola.org/) static site generator.
