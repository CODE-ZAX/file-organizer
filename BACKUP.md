# TidyDesk - Backup Management Guide

This guide explains how to use TidyDesk's backup management system to protect your files and manage storage.

## 🎯 Overview

TidyDesk includes a comprehensive backup management system that allows you to:

- Create backups of files and directories
- Restore previous versions
- Manage backup storage
- Clean up old backups to save space

## 🚀 Quick Start

### Accessing Backup Manager

1. Open TidyDesk
2. Click **"Backups"** in the main window
3. The Backup Manager window will open

### Creating Your First Backup

1. Click **"Create Backup"**
2. Select the directory you want to backup
3. Enter a name for your backup
4. Click **"OK"** to create the backup

## 💾 Backup Features

### Create Backup

- **Purpose**: Create a compressed backup of files or directories
- **Format**: ZIP archive with metadata
- **Location**: `~/Documents/TidyDesk/backups/`
- **Naming**: Automatic timestamp or custom name

### Restore Backup

- **Purpose**: Restore files from a backup
- **Target**: Choose where to restore files
- **Verification**: Automatic file count verification
- **Safety**: Original files are preserved

### Delete Backup

- **Purpose**: Remove unwanted backups
- **Confirmation**: Yes/No dialog for safety
- **Cleanup**: Removes both backup and metadata files

### Cleanup Old Backups

- **Purpose**: Automatically remove old backups
- **Keep Count**: Choose how many recent backups to keep
- **Storage**: Frees up disk space
- **Smart**: Keeps most recent backups

## 📊 Storage Management

### View Storage Usage

The Backup Manager shows:

- **Total Backups**: Number of backup files
- **Total Size**: Storage used in MB/GB
- **File Count**: Number of files in each backup
- **Creation Date**: When backup was created

### Storage Location

- **macOS/Linux**: `~/Documents/TidyDesk/backups/`
- **Windows**: `%USERPROFILE%\Documents\TidyDesk\backups\`
- **Custom**: Can be changed in code

## 🔧 Backup Manager Interface

### Main Window

- **Backup List**: Shows all available backups
- **Action Buttons**: Create, Restore, Delete, Cleanup
- **Storage Info**: Current storage usage
- **Refresh**: Update the backup list

### Backup List Columns

- **Name**: Backup identifier
- **Created**: Creation date and time
- **Source**: Original file/directory name
- **Size**: Backup file size in MB
- **Files**: Number of files in backup

## 📋 Backup Operations

### Creating Backups

#### From GUI

1. Click **"Create Backup"**
2. Select source directory
3. Enter backup name
4. Click **"OK"**

#### From Code

```python
from file_organizer.core.backup_manager import BackupManager

backup_manager = BackupManager()
backup_path = backup_manager.create_backup("/path/to/source", "my_backup")
```

### Restoring Backups

#### From GUI

1. Select backup from list
2. Click **"Restore Backup"**
3. Choose restore location
4. Click **"OK"**

#### From Code

```python
restored_path = backup_manager.restore_backup("/path/to/backup.zip", "/restore/location")
```

### Managing Backups

#### List All Backups

```python
backups = backup_manager.list_backups()
for backup in backups:
    print(f"Name: {backup['backup_name']}")
    print(f"Size: {backup['size_mb']} MB")
    print(f"Files: {backup['file_count']}")
```

#### Delete Backup

```python
success = backup_manager.delete_backup("backup_name")
```

#### Cleanup Old Backups

```python
deleted_count = backup_manager.cleanup_old_backups(keep_count=10)
```

## 🛡️ Backup Safety Features

### Data Integrity

- **ZIP Format**: Standard, reliable compression
- **Metadata**: Backup information stored separately
- **Verification**: File count and size tracking
- **Error Handling**: Graceful failure management

### Storage Safety

- **No Overwrite**: Backups never overwrite existing files
- **Confirmation**: Delete operations require confirmation
- **Metadata**: Backup information preserved
- **Recovery**: Deleted backups can be recovered from trash

### File Safety

- **Original Preservation**: Source files are never modified
- **Restore Safety**: Restore creates new files
- **Path Safety**: Restore location is user-selected
- **Permission Safety**: Respects file permissions

## 📈 Best Practices

### Backup Strategy

- **Regular Backups**: Create backups before major changes
- **Incremental**: Keep multiple versions of important files
- **Cleanup**: Regularly clean up old backups
- **Testing**: Test restore functionality periodically

### Storage Management

- **Monitor Usage**: Check storage usage regularly
- **Cleanup**: Remove old backups when storage is full
- **Organization**: Use descriptive backup names
- **Location**: Keep backups in accessible location

### File Organization

- **Before Backup**: Organize files before backing up
- **After Restore**: Verify restored files
- **Naming**: Use consistent naming conventions
- **Documentation**: Keep notes about important backups

## 🔍 Troubleshooting

### Common Issues

#### Backup Creation Fails

- **Check Permissions**: Ensure write access to backup directory
- **Check Space**: Verify sufficient disk space
- **Check Path**: Ensure source path exists
- **Check Name**: Use valid backup name

#### Restore Fails

- **Check Backup**: Verify backup file exists and is valid
- **Check Target**: Ensure restore location is writable
- **Check Space**: Verify sufficient disk space
- **Check Permissions**: Ensure proper file permissions

#### Storage Issues

- **Cleanup**: Use cleanup function to remove old backups
- **Location**: Move backups to different location
- **Compression**: Backups are already compressed
- **Monitoring**: Check storage usage regularly

### Error Messages

#### "Permission Denied"

- **Solution**: Check file/folder permissions
- **Fix**: Run as administrator or change permissions

#### "Insufficient Space"

- **Solution**: Free up disk space
- **Fix**: Delete old backups or move to different drive

#### "Backup Not Found"

- **Solution**: Check backup name and location
- **Fix**: Refresh backup list or check file system

## 🚀 Advanced Features

### Custom Backup Locations

```python
backup_manager = BackupManager("/custom/backup/path")
```

### Backup Metadata

Each backup includes:

- **Creation Date**: When backup was created
- **Source Path**: Original file/directory path
- **File Count**: Number of files backed up
- **Total Size**: Size of original files
- **Backup Type**: File or directory

### Storage Monitoring

```python
storage_info = backup_manager.get_backup_size()
print(f"Total size: {storage_info['total_size_gb']:.2f} GB")
print(f"Backup count: {storage_info['backup_count']}")
```

## 📚 Integration with TidyDesk

### Automatic Backups

- **Before Organization**: Optional backup before file organization
- **Settings**: Configure in TidyDesk settings
- **Integration**: Seamless integration with main app

### File Organization

- **Safe Organization**: Backups protect against data loss
- **Restore Capability**: Easy restoration if needed
- **Version Control**: Keep multiple versions of organized files

## 🔒 Security Considerations

### Data Protection

- **Local Storage**: Backups stored locally by default
- **No Cloud**: No automatic cloud upload
- **Privacy**: Files remain on your device
- **Control**: Full control over backup location

### Access Control

- **User Only**: Only current user can access backups
- **File Permissions**: Respects system file permissions
- **No Sharing**: Backups are not shared by default
- **Secure**: No network transmission

## 📄 Backup File Format

### ZIP Archive

- **Format**: Standard ZIP compression
- **Compatibility**: Works with any ZIP tool
- **Compression**: Efficient storage usage
- **Integrity**: Built-in error detection

### Metadata File

- **Format**: JSON file
- **Name**: `{backup_name}_metadata.json`
- **Content**: Backup information and statistics
- **Purpose**: Backup management and verification

## 🎯 Use Cases

### File Organization

- **Before**: Backup files before organizing
- **After**: Restore if organization goes wrong
- **Safety**: Protect against accidental changes

### Project Management

- **Versions**: Keep multiple project versions
- **Milestones**: Backup at important milestones
- **Recovery**: Restore previous project states

### System Maintenance

- **Cleanup**: Regular backup cleanup
- **Storage**: Monitor and manage storage usage
- **Organization**: Keep backups organized

## 🤝 Contributing

### Reporting Issues

- **Bug Reports**: Report backup-related issues
- **Feature Requests**: Suggest new backup features
- **Improvements**: Contribute to backup system

### Development

- **Code**: Backup manager is open source
- **Testing**: Test backup functionality
- **Documentation**: Improve backup documentation

## 📄 License

The backup management system is part of TidyDesk and is licensed under the MIT License.

---

**Happy Backing Up! 💾**

For more help, visit the [TidyDesk GitHub repository](https://github.com/code-zax/tiddesk) or check the main documentation.
