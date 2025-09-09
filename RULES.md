# TidyDesk - Custom Rules Guide

This guide explains how to create and manage custom file organization rules in TidyDesk.

## 🎯 Overview

TidyDesk allows you to create custom rules to organize files based on your specific needs. You can define which file types should go to which folders, making your file organization completely personalized.

## 🚀 Quick Start

### Quick Rule Creation

1. Click **"Quick Rule"** in the main window
2. Enter file extension (e.g., `.pdf`)
3. Enter target folder (e.g., `Documents`)
4. Enter rule name (e.g., `PDF Files`)
5. Click **"Create Rule"**

### Advanced Rule Management

1. Click **"Custom Rules"** in the main window
2. Use the **"Rule Helper"** for guided creation
3. Or manually create rules using the editor

## 📋 Rule Components

### Rule Name

- **Purpose**: Identifies the rule in the rules list
- **Format**: Any descriptive text
- **Example**: "My Photos", "Code Files", "Archives"

### File Extensions

- **Purpose**: Defines which files the rule applies to
- **Format**: Comma-separated list of extensions
- **Example**: `.jpg, .png, .gif` or `jpg, png, gif`
- **Note**: Extensions are automatically prefixed with `.` if missing

### Target Folder

- **Purpose**: Specifies where matching files should be moved
- **Format**: Folder name (will be created if it doesn't exist)
- **Example**: `Images`, `Documents`, `Videos`

### Enabled Status

- **Purpose**: Controls whether the rule is active
- **Options**: Enabled (Yes) or Disabled (No)
- **Use**: Temporarily disable rules without deleting them

## 🛠️ Rule Helper Templates

The Rule Helper provides pre-built templates for common file types:

### 📸 Images

- **Extensions**: `.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg`
- **Target**: `Images`
- **Description**: Common image formats including photos, graphics, and vector images

### 📄 Documents

- **Extensions**: `.pdf, .doc, .docx, .txt, .rtf, .odt, .pages`
- **Target**: `Documents`
- **Description**: Text documents, PDFs, and office files

### 🎬 Videos

- **Extensions**: `.mp4, .avi, .mov, .wmv, .flv, .webm, .mkv`
- **Target**: `Videos`
- **Description**: Video files in various formats

### 🎵 Audio

- **Extensions**: `.mp3, .wav, .flac, .aac, .ogg, .m4a`
- **Target**: `Audio`
- **Description**: Audio files and music

### 📦 Archives

- **Extensions**: `.zip, .rar, .7z, .tar, .gz, .bz2`
- **Target**: `Archives`
- **Description**: Compressed files and archives

### 💻 Code Files

- **Extensions**: `.py, .js, .html, .css, .java, .cpp, .c, .h, .php, .rb, .go`
- **Target**: `Code`
- **Description**: Source code files and scripts

### 📊 Spreadsheets

- **Extensions**: `.xls, .xlsx, .csv, .ods`
- **Target**: `Spreadsheets`
- **Description**: Excel files and data tables

### 🎯 Presentations

- **Extensions**: `.ppt, .pptx, .odp`
- **Target**: `Presentations`
- **Description**: PowerPoint and presentation files

### 🎨 3D Models

- **Extensions**: `.obj, .fbx, .dae, .blend, .3ds, .max`
- **Target**: `3D Models`
- **Description**: 3D model files and scenes

### 🔤 Fonts

- **Extensions**: `.ttf, .otf, .woff, .woff2`
- **Target**: `Fonts`
- **Description**: Font files and typefaces

## 🔧 Creating Custom Rules

### Method 1: Rule Helper (Recommended)

1. Open **Custom Rules** manager
2. Click **"Rule Helper"**
3. Select a template or create custom
4. Modify the details as needed
5. Click **"Use Template"** or **"Create Custom Rule"**

### Method 2: Manual Creation

1. Open **Custom Rules** manager
2. Click **"Add New Rule"**
3. Fill in the rule details:
   - **Rule Name**: Descriptive name
   - **File Extensions**: Comma-separated list
   - **Target Folder**: Destination folder
   - **Enabled**: Check to activate
4. Review the preview
5. Click **"Save Rule"**

## 📝 Rule Examples

### Example 1: Photography Files

```
Rule Name: Photography
Extensions: .raw, .cr2, .nef, .arw, .dng
Target Folder: Photography
Enabled: Yes
```

### Example 2: Development Files

```
Rule Name: Development
Extensions: .py, .js, .ts, .jsx, .tsx, .vue, .svelte
Target Folder: Development
Enabled: Yes
```

### Example 3: Design Files

```
Rule Name: Design
Extensions: .psd, .ai, .sketch, .fig, .xd
Target Folder: Design
Enabled: Yes
```

### Example 4: Temporary Files

```
Rule Name: Temp Files
Extensions: .tmp, .temp, .bak, .old
Target Folder: Trash
Enabled: Yes
```

## 🔄 Managing Rules

### Editing Rules

1. Select a rule from the list
2. Click **"Edit Rule"**
3. Modify the details
4. Click **"Update Rule"**

### Deleting Rules

1. Select a rule from the list
2. Click **"Delete Rule"**
3. Confirm deletion

### Enabling/Disabling Rules

1. Select a rule from the list
2. Click **"Edit Rule"**
3. Toggle the **"Enable this rule"** checkbox
4. Click **"Update Rule"**

## 📤 Import/Export Rules

### Exporting Rules

1. Open **Custom Rules** manager
2. Click **"Export Rules"**
3. Choose save location
4. Rules are saved as JSON file

### Importing Rules

1. Open **Custom Rules** manager
2. Click **"Import Rules"**
3. Select JSON file
4. Rules are imported and added to existing rules

### Rule File Format

```json
[
  {
    "name": "Images",
    "file_extensions": [".jpg", ".png", ".gif"],
    "target_folder": "Images",
    "enabled": true
  },
  {
    "name": "Documents",
    "file_extensions": [".pdf", ".doc", ".txt"],
    "target_folder": "Documents",
    "enabled": true
  }
]
```

## 🎯 Best Practices

### Rule Naming

- Use descriptive names
- Avoid special characters
- Keep names concise but clear
- Use consistent naming convention

### File Extensions

- Always use lowercase
- Include the dot (.) prefix
- Group related extensions together
- Test with actual files

### Target Folders

- Use simple, clear names
- Avoid special characters
- Consider folder hierarchy
- Use consistent naming

### Organization Strategy

- Group by file type (Images, Documents)
- Group by project (Project A, Project B)
- Group by date (2024, 2023)
- Group by source (Downloads, Camera)

## 🔍 Troubleshooting

### Common Issues

#### Rule Not Working

- **Check**: Rule is enabled
- **Check**: File extensions are correct
- **Check**: Target folder is accessible
- **Check**: File permissions

#### Duplicate Rules

- **Solution**: Use different rule names
- **Solution**: Merge similar rules
- **Solution**: Disable conflicting rules

#### Files Not Moving

- **Check**: File is not in use
- **Check**: Sufficient disk space
- **Check**: File permissions
- **Check**: Antivirus interference

### Debug Tips

- Test rules with a small set of files first
- Use the preview feature to verify rules
- Check the log for error messages
- Verify file extensions are correct

## 🚀 Advanced Features

### Rule Priority

- Rules are processed in order
- First matching rule wins
- Reorder rules by editing and saving

### Multiple Extensions

- Use comma-separated lists
- Mix different file types
- Group by purpose, not just extension

### Nested Folders

- Use forward slashes for subfolders
- Example: `Images/Photos`, `Documents/Work`
- Folders are created automatically

### Wildcard Extensions

- Use `.*` for all files
- Use `.*` for specific patterns
- Be careful with broad rules

## 📊 Rule Statistics

### Viewing Rule Usage

- Check the log for rule applications
- Monitor file organization results
- Adjust rules based on usage

### Performance Tips

- Limit the number of active rules
- Use specific extensions when possible
- Avoid overly broad rules
- Regular rule maintenance

## 🔒 Security Considerations

### File Safety

- Rules only move files, never delete
- Always backup important files
- Test rules in a safe environment
- Review rules before applying

### Permission Requirements

- Read access to source files
- Write access to target folders
- Create folder permissions
- File system access

## 📚 Additional Resources

### File Type References

- [MIME Types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
- [File Extensions](https://fileinfo.com/)
- [Common File Types](https://en.wikipedia.org/wiki/List_of_file_formats)

### Organization Strategies

- [File Organization Methods](https://www.lifehack.org/articles/productivity/10-file-organization-tips.html)
- [Digital Decluttering](https://www.nytimes.com/wirecutter/reviews/digital-decluttering/)
- [Folder Structure Best Practices](https://www.folderstructure.com/)

## 🤝 Contributing

### Sharing Rules

- Export your rule sets
- Share with team members
- Contribute to community templates
- Submit rule suggestions

### Feedback

- Report rule issues
- Suggest new templates
- Share organization strategies
- Contribute improvements

## 📄 License

The custom rules feature is part of TidyDesk and is licensed under the MIT License.

---

**Happy Organizing! 🎉**

For more help, visit the [TidyDesk GitHub repository](https://github.com/code-zax/tiddesk) or check the main documentation.
