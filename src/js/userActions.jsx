/**
 * Serialise an array of plain objects to a JSON array string.
 *
 * ExtendScript targets ES3 and has no native JSON.stringify, so this
 * function provides a minimal hand-rolled replacement sufficient for objects
 * whose values are plain strings.
 *
 * @param {Object[]} items - Array of objects with string values to serialise.
 * @returns {string} A JSON array string, e.g. '[{"key":"value"},…]'.
 */
function serialize(items) {
    var parts = [];
    var i, key, obj, props;

    for (i = 0; i < items.length; i++) {
        obj = items[i];
        props = [];

        for (key in obj) {
            if (obj.hasOwnProperty(key)) {
                props.push('"' + key + '":"' + obj[key] + '"');
            }
        }

        parts.push("{" + props.join(",") + "}");
    }

    return "[" + parts.join(",") + "]";
}

/**
 * Read all Actions and Action Sets from Illustrator's preferences and return
 * them as an array of action descriptor objects.
 *
 * Illustrator stores Action Sets under the preference path
 * "plugin/Action/SavedSets/set-<n>/" (1-based, up to 100 sets).  Each set
 * contains an "actionCount" integer and individual actions keyed as
 * "action-<j>/name" (1-based).
 *
 * The returned objects contain everything user_actions.py needs to build an
 * Alfred result item and construct the JavaScript call passed back to
 * Illustrator via osascript.
 *
 * @returns {Object[]} Array of action descriptor objects, each with:
 *   - {string} id   - Unique identifier in the form "action_<set>_<name>".
 *   - {string} set  - The Action Set name as shown in the Actions panel.
 *   - {string} name - The Action name as shown in the Actions panel.
 */
function loadActions() {
    var currentPath;
    var set;
    var actionCount;
    var name;
    var id;
    var obj;
    var pref = app.preferences;
    // Base preference path for saved Action Sets (1-based index).
    var basePath = "plugin/Action/SavedSets/set-";
    var actions = [];

    for (var i = 1; i <= 100; i++) {
        currentPath = basePath + i + "/";
        // get action set name; an empty string signals no more sets exist.
        set = pref.getStringPreference(currentPath + "name");
        if (!set) break;
        // get the number of actions within this set
        actionCount = Number(pref.getIntegerPreference(currentPath + "actionCount"));
        for (var j = 1; j <= actionCount; j++) {
            name = pref.getStringPreference(currentPath + "action-" + j + "/name");
            // Build a stable, lowercase uid from the set and action names.
            id = "action_" + set + "_" + name.toLowerCase();
            obj = {
                id: id,
                set: set,
                name: name,
            };
            actions.push(obj);
        }
    }

    return actions;
}

// Collect all actions, then return their JSON representation.
// The Alfred "Run Script" action captures this return value and stores it in
// the USER_ACTIONS environment variable for use by user_actions.py.
serialize(loadActions());
