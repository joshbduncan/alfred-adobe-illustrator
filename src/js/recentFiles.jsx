/**
 * Reads Illustrator's recent-file preferences and returns a comma-separated
 * string of absolute file system paths for files that still exist on disk.
 *
 * The result is passed back to the Alfred workflow via `do javascript`, which
 * captures the return value of the last evaluated expression and stores it in
 * the RECENT_FILES environment variable for use by recent_files.py.
 *
 * Illustrator stores recent files under the preference key
 * "plugin/MixedFileList/file<n>/path" (0-based), with the total count at
 * "RecentFileNumber".
 *
 * @returns {string} Comma-separated list of native file-system paths.
 */
function loadRecentFiles() {
    var recentFiles = [];
    var fileCount = app.preferences.getIntegerPreference("RecentFileNumber");
    for (var i = 0; i < fileCount; i++) {
        // Build the preference key for the i-th recent file path.
        var prefKey = "plugin/MixedFileList/file" + i + "/path";
        var cur = new File(app.preferences.getStringPreference(prefKey));
        // Skip files that no longer exist on disk.
        if (!cur.exists) continue;
        // fsName returns the native OS path (e.g. /Users/… on macOS).
        recentFiles.push(cur.fsName);
    }
    // Explicitly join so the return type is a string, not an Array.
    return recentFiles.join(",");
}

// Return value is captured by the Alfred "Run Script" action and stored in
// the RECENT_FILES environment variable as a comma-separated string.
loadRecentFiles();
