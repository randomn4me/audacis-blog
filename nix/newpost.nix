{ pkgs }:

pkgs.writeShellScriptBin "newpost" ''
  #!/usr/bin/env bash
  set -e
  
  if [ -z "$1" ]; then
    echo "Usage: nix run .#newpost -- <title>"
    echo "Example: nix run .#newpost -- My Awesome Post"
    exit 1
  fi
  
  # Get the filename from the first argument
  title="$@"
  filename=$(echo "$title" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
  
  # Remove .md extension if provided
  filename="''${filename%.md}"
  
  # Create the full filepath
  filepath="content/posts/''${filename}.md"
  
  # Check if file already exists
  if [ -f "$filepath" ]; then
    echo "Error: File $filepath already exists!"
    exit 1
  fi
  
  # Get current date in YYYY-MM-DD format
  current_date=$(date +%Y-%m-%d)
  
  # Create the markdown file with template
  cat > "$filepath" << EOF
  +++
  title = "$title"
  description = "A brief description of the post"
  date = $current_date
  draft = true
  
  [taxonomies]
  tags = ["tag1", "tag2"]
  +++
  
  <!-- Summary/excerpt that appears in post listings -->
  Brief description of the post goes here...
  
  <!-- more -->
  EOF

  nvim "$filepath"
  
  echo "✅ Created new post: $filepath"
  echo ""
  echo "Next steps:"
  echo "1. Edit the title in the frontmatter"
  echo "2. Update tags as needed"
  echo "3. Write your content"
  echo "4. Set 'draft = false' when ready to publish"
''
